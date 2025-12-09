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



@router.callback_query(F.data.startswith('EGE_task') )
async def EGE_task_info(callback: types.CallbackQuery):
    await callback.message.answer(text="В процессе разработки")
