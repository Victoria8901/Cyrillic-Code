"""Обработчики для ОГЭ"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboards.oge import (
    generate_oge_menu_kb,
    get_task_actions_kb,
    get_continue_solving_kb,
    get_test_start_kb
)
from bot.keyboards.menu import main_menu_kb
from bot.models.states import SolvingState, TestingState
from bot.services.database import db_service
from bot.services.task_service import task_service
from bot.services.storage import storage_service

router = Router()


@router.callback_query(F.data == 'oge_menu')
@router.message(lambda message: message.text == 'Подготовка к ОГЭ')
async def oge_menu_handler(update: types.Message | types.CallbackQuery):
    """Обработчик меню ОГЭ"""
    if isinstance(update, types.Message):
        await update.answer(
            'Выберите задание:',
            reply_markup=generate_oge_menu_kb()
        )
    else:
        await update.message.edit_text(
            'Выберите задание:',
            reply_markup=generate_oge_menu_kb()
        )


@router.callback_query(F.data.startswith('oge_task:'))
async def oge_task_info_handler(callback: types.CallbackQuery):
    """Обработчик выбора задания ОГЭ"""
    task_number = int(callback.data.split(':')[1])
    
    # Получаем путь к файлу теории
    theory_path = task_service.get_theory_file_path("OGE", task_number)
    
    if theory_path:
        try:
            # Проверяем, это путь к файлу или путь в хранилище
            import os
            if os.path.exists(theory_path):
                # Локальный файл
                await callback.message.answer_document(
                    types.FSInputFile(theory_path)
                )
            elif storage_service.use_minio:
                # Файл в MinIO
                file_data = storage_service.get_file(theory_path)
                if file_data:
                    file_bytes = file_data.read()
                    await callback.message.answer_document(
                        types.BufferedInputFile(
                            file_bytes,
                            filename=f"task_{task_number}_theory.pdf"
                        )
                    )
        except Exception as e:
            await callback.message.answer(f"⚠️ Теория для этого задания пока не доступна. Начинаем решать задания!")
    
    await callback.message.answer(
        'Хотите решить задание?',
        reply_markup=get_task_actions_kb(task_number)
    )


@router.callback_query(F.data.startswith('solve_task:'))
async def start_solving_handler(callback: types.CallbackQuery, state: FSMContext):
    """Начать решение заданий"""
    task_number = int(callback.data.split(':')[1])
    
    # Получаем случайное задание
    tasks = task_service.get_random_tasks("OGE", task_number, 1)
    if not tasks:
        await callback.message.answer("Ошибка: задания не найдены")
        return
    
    task = tasks[0]
    
    # Сохраняем состояние
    await state.set_state(SolvingState.waiting_for_answer)
    await state.update_data(
        topic_number=task_number,
        correct_answer=task["answer"],
        correct_count=0
    )
    
    await callback.message.answer(task["text"])


@router.message(SolvingState.waiting_for_answer)
async def check_answer_handler(message: types.Message, state: FSMContext):
    """Проверка ответа пользователя"""
    data = await state.get_data()
    topic_number = data["topic_number"]
    correct_answer = data["correct_answer"]
    correct_count = data.get("correct_count", 0)
    
    user_answer = message.text
    
    if task_service.check_answer(user_answer, correct_answer):
        correct_count += 1
        await state.update_data(correct_count=correct_count)
        
        if correct_count < 10:
            # Получаем новое задание
            tasks = task_service.get_random_tasks("OGE", topic_number, 1)
            if tasks:
                task = tasks[0]
                await state.update_data(correct_answer=task["answer"])
                await message.answer(
                    '✅ Молодец, продолжим?',
                    reply_markup=get_continue_solving_kb(topic_number)
                )
                await message.answer(task["text"])
            else:
                await message.answer("Ошибка: задания не найдены")
                await state.clear()
        else:
            # 10 правильных ответов - предлагаем тест
            await state.clear()
            await message.answer(
                '🎉 Ты отлично справляешься! Время пройти тест по этой теме!',
                reply_markup=get_test_start_kb(topic_number)
            )
    else:
        await state.clear()
        await message.answer(
            '❌ Неверно. Попробуй еще раз!',
            reply_markup=get_continue_solving_kb(topic_number)
        )


@router.callback_query(F.data.startswith('oge_test:'))
async def start_test_handler(callback: types.CallbackQuery, state: FSMContext):
    """Начать тест"""
    import json
    task_number = int(callback.data.split(':')[1])
    
    # Получаем 10 случайных заданий
    tasks = task_service.get_random_tasks("OGE", task_number, 10)
    if not tasks:
        await callback.message.answer("Ошибка: задания для теста не найдены")
        return
    
    # Сохраняем состояние теста (сериализуем задачи в JSON)
    await state.set_state(TestingState.answering)
    await state.update_data(
        topic_number=task_number,
        tasks_json=json.dumps(tasks),  # Сериализуем в JSON
        current_index=0,
        score=0
    )
    
    # Отправляем первое задание
    await callback.message.answer(f"📝 Тест начался! Всего заданий: {len(tasks)}")
    await callback.message.answer(tasks[0]["text"])


@router.message(TestingState.answering)
async def test_answer_handler(message: types.Message, state: FSMContext):
    """Обработка ответа в тесте"""
    import json
    data = await state.get_data()
    tasks = json.loads(data["tasks_json"])  # Десериализуем из JSON
    current_index = data["current_index"]
    score = data["score"]
    topic_number = data["topic_number"]
    user_id = message.from_user.id
    
    # Проверяем ответ
    current_task = tasks[current_index]
    user_answer = message.text
    
    is_correct = task_service.check_answer(user_answer, current_task["answer"])
    if is_correct:
        score += 1
    
    current_index += 1
    
    if current_index < len(tasks):
        # Продолжаем тест
        await state.update_data(
            current_index=current_index,
            score=score,
            tasks_json=data["tasks_json"]  # Сохраняем JSON обратно
        )
        await message.answer(tasks[current_index]["text"])
    else:
        # Тест завершен
        await state.clear()
        
        # Получаем пользователя
        user = db_service.get_user_by_chat_id(user_id)
        if not user:
            await message.answer("Ошибка: пользователь не найден")
            return
        
        # Получаем тему
        topic = db_service.get_topic_by_number(topic_number, "OGE")
        if not topic:
            await message.answer("Ошибка: тема не найдена")
            return
        
        # Проверяем, прошел ли тест (>= 80%)
        passed = score >= len(tasks) * 0.8
        
        # Обновляем прогресс
        db_service.create_or_update_progress(
            user["user_id"],
            topic["topic_id"],
            "OGE",
            correct_count=score if passed else 0,
            is_completed=passed
        )
        
        # Формируем сообщение
        result_text = (
            f"📊 Тест окончен!\n\n"
            f"Правильных ответов: {score} из {len(tasks)}\n"
            f"Процент: {score * 100 // len(tasks)}%\n\n"
        )
        
        if passed:
            result_text += "✅ Вы успешно прошли тему! Ваша статистика обновлена!"
        else:
            result_text += "❌ Вы не набрали нужное количество правильных ответов (минимум 80%). Пройдите тему снова!"
        
        await message.answer(result_text, reply_markup=main_menu_kb())

