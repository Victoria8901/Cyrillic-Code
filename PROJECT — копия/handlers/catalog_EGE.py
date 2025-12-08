from aiogram import F, Router, types
from aiogram.filters import Command
import random

from keyboards.EGE import generate_EGE_menu_kb

FLAG = False
ANSWER = ''

router = Router()

@router.callback_query(F.data == 'EGE')
@router.message(F.text == 'Подготовка к ЕГЭ')
async def EGE_study(update: types.Message | types.CallbackQuery):
    if isinstance(update, types.Message):
        await update.answer(
            'Выберите задание:',
            reply_markup=generate_EGE_menu_kb()
        )
    else:
        await update.message.edit_text(
            'Выберите задание:',
            reply_markup=generate_EGE_menu_kb()
        )



@router.callback_query(F.data.startswith('EGE_task'))
async def EGE_task_info(callback: types.CallbackQuery):
    task_num = callback.data.split(':')[-1]

    path = f'data/EGE/{task_num} task/'
    theory_path = path + f'task_{task_num}_theory.pdf'

    await callback.message.answer_document(types.FSInputFile(theory_path))

    await callback.message.answer(
        'Хотите решить задание?',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text='Да', callback_data=f'YES:{task_num}'),
                 types.InlineKeyboardButton(text='Нет', callback_data='EGE'),
                ]
            ]
        )
    )


@router.callback_query(F.data.startswith('YES'))
async def give_task(callback: types.CallbackQuery):
    global FLAG, ANSWER
    FLAG = True
    task_num = callback.data.split(':')[-1]
    path = f'data/EGE/{task_num} task/tasks/'
    file = open(path + f'{random}.txt', encoding='UTF-8')
    text, ANSWER = file.read().split('Ответ:')

    await callback.message.answer(text)

