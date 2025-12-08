from aiogram import F, Router, types
from aiogram.filters import Command, BaseFilter

from keyboards.OGE import generate_OGE_menu_kb

import random

FLAG = False
ANSWER = ''
TOTAL_TASKS = 0
CURRENT_TASK = 0
router = Router()


@router.callback_query(F.data == 'OGE')
@router.message(F.text == 'Подготовка к ОГЭ')
async def OGE_study(update: types.Message | types.CallbackQuery):
    global FLAG
    FLAG = False
    if isinstance(update, types.Message):
        await update.answer(
            'Выберите задание:',
            reply_markup=generate_OGE_menu_kb()
        )
    else:
        await update.message.edit_text(
            'Выберите задание:',
            reply_markup=generate_OGE_menu_kb()
        )



@router.callback_query(F.data.startswith('OGE_task'))
async def OGE_task_info(callback: types.CallbackQuery):
    global TOTAL_TASKS, CURRENT_TASK
    TOTAL_TASKS = 0
    CURRENT_TASK = callback.data.split(':')[-1]

    path = f'data/OGE/task{CURRENT_TASK}/'
    theory_path = path + f'task_{CURRENT_TASK}_theory.pdf'

    await callback.message.answer_document(types.FSInputFile(theory_path))

    await callback.message.answer(
        'Хотите решить задание?',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text='Да', callback_data=f'YES:{CURRENT_TASK}'),
                 types.InlineKeyboardButton(text='Нет', callback_data='OGE'),
                ]
            ]
        )
    )


@router.callback_query(F.data.startswith('YES'))
async def give_task(callback: types.CallbackQuery):
    global FLAG, ANSWER
    FLAG = True
    task_num = callback.data.split(':')[-1]
    path = f'data/OGE/task{task_num}/'
    file = open(path + f'{random.randint(1,20)}.txt', encoding='UTF-8')
    text, ANSWER = file.read().split('Ответ:')
    ANSWER = ANSWER.strip(' .!?-+\n')

    await callback.message.answer(text)


@router.message(lambda message: FLAG)
async def check_answer(message: types.Message):
    global TOTAL_TASKS, CURRENT_TASK, FLAG
    user_answer = message.text
    print(f'cor.: {ANSWER}')
    print(f'user: {user_answer}')
    if user_answer.lower() == ANSWER.lower():
        TOTAL_TASKS += 1
        if TOTAL_TASKS < 10:
            await message.answer('Молодец, продолжим?', reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text='Да', callback_data=f'YES:{CURRENT_TASK}'),
                 types.InlineKeyboardButton(text='Нет', callback_data='OGE'),
                ]
            ]
            )
        )
        else:
            FLAG = False
            await message.answer('Ты отлично справляешься! Время пройти тест по этой теме!', 
                                 reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text='Начать тест', callback_data=f'oge_test:{CURRENT_TASK}'),]
            ]
            )

        )
    else:
        await message.answer('Неверно', reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text='Еще раз', callback_data=f'YES:{CURRENT_TASK}'),
                 types.InlineKeyboardButton(text='Завершить', callback_data='OGE'),
                ]
            ]
            )
        )
        FLAG = False



