"""Минимальная админка для управления файлами теории и заданий."""
from __future__ import annotations
from pathlib import Path
from typing import Optional, Tuple

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import settings
from bot.models.states import AdminState

router = Router()


DATA_ROOT = Path("bot/data")


def _is_admin(user_id: int) -> bool:
    return user_id in settings.bot.admin_ids


def _parse_theory_meta(text: str) -> Optional[Tuple[str, int]]:
    parts = text.strip().upper().split()
    if len(parts) != 2:
        return None
    exam_type, task_str = parts
    if exam_type not in {"OGE", "EGE"}:
        return None
    if not task_str.isdigit():
        return None
    return exam_type, int(task_str)


def _parse_task_meta(text: str) -> Optional[Tuple[str, int, int]]:
    parts = text.strip().upper().split()
    if len(parts) != 3:
        return None
    exam_type, task_str, task_id_str = parts
    if exam_type not in {"OGE", "EGE"}:
        return None
    if not task_str.isdigit() or not task_id_str.isdigit():
        return None
    return exam_type, int(task_str), int(task_id_str)


async def _deny_not_admin(message: types.Message):
    await message.answer("⛔ Доступ только для администраторов.")


@router.message(Command("admin"))
async def admin_menu_handler(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    await state.clear()
    await message.answer(
        "Админка:\n"
        "- /admin_theory — загрузить/обновить PDF теории\n"
        "- /admin_task — создать/обновить текст задания\n\n"
        "Пример:\n"
        "/admin_theory OGE 4\n"
        "/admin_task OGE 4 1"
    )


@router.message(Command("admin_theory"))
async def admin_theory_command(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    args = message.text.replace("/admin_theory", "").strip()
    if not args:
        await state.set_state(AdminState.waiting_for_theory_meta)
        await message.answer("Введите тип и номер задания, например: OGE 4")
        return

    meta = _parse_theory_meta(args)
    if not meta:
        await message.answer("Неверный формат. Пример: /admin_theory OGE 4")
        return

    exam_type, task_number = meta
    target_path = DATA_ROOT / exam_type / f"task{task_number}" / f"task_{task_number}_theory.pdf"
    await state.update_data(target_path=str(target_path))
    await state.set_state(AdminState.waiting_for_theory_file)
    await message.answer("Отправьте PDF файл теории для сохранения.")


@router.message(AdminState.waiting_for_theory_meta)
async def admin_theory_meta_handler(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    meta = _parse_theory_meta(message.text)
    if not meta:
        await message.answer("Неверный формат. Пример: OGE 4")
        return

    exam_type, task_number = meta
    target_path = DATA_ROOT / exam_type / f"task{task_number}" / f"task_{task_number}_theory.pdf"
    await state.update_data(target_path=str(target_path))
    await state.set_state(AdminState.waiting_for_theory_file)
    await message.answer("Отправьте PDF файл теории для сохранения.")


@router.message(AdminState.waiting_for_theory_file, F.document)
async def admin_theory_file_handler(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    data = await state.get_data()
    target_path = data.get("target_path")
    if not target_path:
        await message.answer("Нет пути назначения. Начните заново: /admin_theory")
        await state.clear()
        return

    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    with open(target, "wb") as f:
        f.write(file_bytes.read())

    await state.clear()
    await message.answer(f"✅ Теория сохранена: {target}")


@router.message(AdminState.waiting_for_theory_file)
async def admin_theory_file_fallback(message: types.Message):
    await message.answer("Пожалуйста, отправьте PDF документ.")


@router.message(Command("admin_task"))
async def admin_task_command(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    args = message.text.replace("/admin_task", "").strip()
    if not args:
        await state.set_state(AdminState.waiting_for_task_meta)
        await message.answer("Введите тип, номер задания и id, например: OGE 4 1")
        return

    meta = _parse_task_meta(args)
    if not meta:
        await message.answer("Неверный формат. Пример: /admin_task OGE 4 1")
        return

    exam_type, task_number, task_id = meta
    target_path = DATA_ROOT / exam_type / f"task{task_number}" / f"{task_id}.txt"
    await state.update_data(target_path=str(target_path))
    await state.set_state(AdminState.waiting_for_task_content)
    await message.answer("Отправьте текст задания сообщением или .txt файлом.")


@router.message(AdminState.waiting_for_task_meta)
async def admin_task_meta_handler(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    meta = _parse_task_meta(message.text)
    if not meta:
        await message.answer("Неверный формат. Пример: OGE 4 1")
        return

    exam_type, task_number, task_id = meta
    target_path = DATA_ROOT / exam_type / f"task{task_number}" / f"{task_id}.txt"
    await state.update_data(target_path=str(target_path))
    await state.set_state(AdminState.waiting_for_task_content)
    await message.answer("Отправьте текст задания сообщением или .txt файлом.")


@router.message(AdminState.waiting_for_task_content, F.document)
async def admin_task_file_handler(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    data = await state.get_data()
    target_path = data.get("target_path")
    if not target_path:
        await message.answer("Нет пути назначения. Начните заново: /admin_task")
        await state.clear()
        return

    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    with open(target, "wb") as f:
        f.write(file_bytes.read())

    await state.clear()
    await message.answer(f"✅ Задание сохранено: {target}")


@router.message(AdminState.waiting_for_task_content)
async def admin_task_text_handler(message: types.Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        await _deny_not_admin(message)
        return

    data = await state.get_data()
    target_path = data.get("target_path")
    if not target_path:
        await message.answer("Нет пути назначения. Начните заново: /admin_task")
        await state.clear()
        return

    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "w", encoding="utf-8") as f:
        f.write(message.text.strip())

    await state.clear()
    await message.answer(f"✅ Задание сохранено: {target}")
