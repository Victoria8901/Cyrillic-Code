from aiogram import F, Router, types
from aiogram.filters import Command, BaseFilter
from keyboards.menu import main_menu_kb
from handlers.db_handler import load_db

import random

router = Router()
conn_db = load_db()
cursor = conn_db.cursor()

TEST_TASKS = []
TEST_FLAG = False
IND = 0
TEST_SCORE = 0
TASK_NUM = 0


@router.callback_query(F.data.startswith('oge_test'))
async def generate_test(callback: types.CallbackQuery):
    global TEST_FLAG, IND, TEST_TASKS, TASK_NUM
    TEST_FLAG = True
    TASK_NUM = callback.data.split(':')[-1]
    path = f'data/OGE/task{TASK_NUM}/'
    
    for i in range(10):
        file = open(path + f'{random.randint(1,20)}.txt', encoding='UTF-8')
        text, ans = file.read().split('Ответ:')
        ans = ans.strip(' .!?-+\n')
        TEST_TASKS.append({'text': text, 'answer': ans})

    await callback.message.answer(TEST_TASKS[IND]['text'])
    IND += 1


@router.message(lambda message: TEST_FLAG)
async def test_step(message: types.Message):
    global TEST_SCORE, TEST_TASKS, IND, TASK_NUM, TEST_FLAG
    user_ans = message.text
    if user_ans.lower() == TEST_TASKS[IND - 1]['answer'].lower():
        TEST_SCORE += 1
    
    if IND < len(TEST_TASKS):
        await message.answer(TEST_TASKS[IND]['text'])
        IND += 1
    else:
        TEST_FLAG = False
        if TEST_SCORE >= 0.8 * len(TEST_TASKS):
            chat_id = message.from_user.id
            cursor.execute(f"SELECT * FROM USERS WHERE chat_id = '{chat_id}' AND oge{TASK_NUM}=FALSE")
            res = cursor.fetchall()
            if len(res) != 0:
                cursor.execute(f"UPDATE users SET count_oge = count_oge + 1 WHERE chat_id = '{chat_id}'")
                cursor.execute(f"UPDATE users SET oge{TASK_NUM} = TRUE WHERE chat_id = '{chat_id}'")

            conn_db.commit()
            text = 'Вы успешно прошли тему: ваша статистика обновлена!'
        else:
            text = 'Вы не смогли набрать нужное количество правильных ответов. Пройдите эту тему снова!'

        await message.answer(f'Тест окончен, вы решили верно {TEST_SCORE} заданий из {len(TEST_TASKS)}.\n{text}', reply_markup=main_menu_kb())
        TEST_SCORE = 0
        TEST_TASKS = []
        IND = 0

    
