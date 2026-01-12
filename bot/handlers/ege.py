"""Обработчики для ЕГЭ"""
from aiogram import Router, types, F

from bot.keyboards.ege import generate_ege_menu_kb

router = Router()


@router.callback_query(F.data == 'ege_menu')
@router.message(lambda message: message.text == 'Подготовка к ЕГЭ')
async def ege_menu_handler(update: types.Message | types.CallbackQuery):
    """Обработчик меню ЕГЭ"""
    if isinstance(update, types.Message):
        await update.answer(
            'Выберите задание:',
            reply_markup=generate_ege_menu_kb()
        )
    else:
        await update.message.edit_text(
            'Выберите задание:',
            reply_markup=generate_ege_menu_kb()
        )


@router.callback_query(F.data.startswith('ege_task:'))
async def ege_task_info_handler(callback: types.CallbackQuery):
    """Обработчик выбора задания ЕГЭ"""
    await callback.message.answer(
        "⚠️ Функционал ЕГЭ находится в разработке. Скоро будет доступен!"
    )

