from aiogram import F, Router, types
from aiogram.filters import Command

router = Router()

@router.message(F.text == 'Помощь')
@router.message(Command('help'))
async def info(message: types.Message):
    help_text = '''
Этот бот может помочь тебе подготовиться к ОГЭ и ЕГЭ по русскому языку. 

Выбери интересующий вариант экзамена, чтобы начать.
Затем выбери номер задания. Когда решишь верно десять заданий, бот предложит пройти тест.

Ты можешь следить за своей статистикой. Выбери в главном меню пункт "Мой профиль".

'''
    await message.answer(text=help_text)


    