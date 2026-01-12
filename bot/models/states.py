"""FSM состояния для бота"""
from aiogram.fsm.state import State, StatesGroup


class SolvingState(StatesGroup):
    """Состояние решения заданий"""
    waiting_for_answer = State()
    topic_number = State()


class TestingState(StatesGroup):
    """Состояние прохождения теста"""
    answering = State()
    topic_number = State()
    current_question = State()
    score = State()

