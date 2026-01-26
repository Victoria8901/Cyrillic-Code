"""FSM состояния для бота.

Файл был восстановлен, так как использовался в обработчиках.
"""

from aiogram.fsm.state import State, StatesGroup


class SolvingState(StatesGroup):
    """Состояния для режима решения одиночных заданий ОГЭ."""

    waiting_for_answer = State()
    topic_number = State()


class TestingState(StatesGroup):
    """Состояния для режима прохождения теста по теме."""

    answering = State()
    topic_number = State()
    current_question = State()
    score = State()


class AdminState(StatesGroup):
    """Состояния для админки (редактор файлов)."""

    waiting_for_theory_meta = State()
    waiting_for_theory_file = State()
    waiting_for_task_meta = State()
    waiting_for_task_content = State()


