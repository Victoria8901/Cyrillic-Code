"""Сервис для работы с заданиями"""
import os
import random
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from bot.services.storage import storage_service

logger = logging.getLogger(__name__)


class TaskService:
    """Сервис для работы с заданиями"""
    
    def __init__(self):
        self.base_path = Path("bot/data")
    
    def load_task_from_file(self, exam_type: str, task_number: int, task_id: int) -> Optional[Dict[str, str]]:
        """Загрузить задание из файла"""
        file_path = f"{exam_type}/task{task_number}/{task_id}.txt"
        
        try:
            file_data = storage_service.get_file(file_path)
            if not file_data:
                # Попробуем локальный путь
                local_path = self.base_path / file_path
                if local_path.exists():
                    with open(local_path, "r", encoding="UTF-8") as f:
                        content = f.read()
                else:
                    logger.error(f"Task file not found: {file_path}")
                    return None
            else:
                content = file_data.read().decode("UTF-8")
            
            # Парсим задание
            if "Ответ:" in content:
                text, answer = content.split("Ответ:", 1)
                return {
                    "text": text.strip(),
                    "answer": answer.strip(" .!?-+\n")
                }
            else:
                logger.error(f"Invalid task format in file: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading task from {file_path}: {e}")
            return None
    
    def get_random_tasks(self, exam_type: str, task_number: int, count: int = 10) -> List[Dict[str, str]]:
        """Получить случайные задания"""
        tasks = []
        max_task_id = 20  # Предполагаем, что заданий не больше 20
        
        available_ids = list(range(1, max_task_id + 1))
        random.shuffle(available_ids)
        
        for task_id in available_ids[:count]:
            task = self.load_task_from_file(exam_type, task_number, task_id)
            if task:
                tasks.append(task)
                if len(tasks) >= count:
                    break
        
        return tasks
    
    def get_theory_file_path(self, exam_type: str, task_number: int) -> Optional[str]:
        """Получить путь к файлу теории"""
        file_path = f"{exam_type}/task{task_number}/task_{task_number}_theory.pdf"
        local_path = self.base_path / file_path
        if local_path.exists():
            return str(local_path)
        return None
    
    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Проверить ответ пользователя"""
        return user_answer.lower().strip() == correct_answer.lower().strip()


# Глобальный экземпляр сервиса
task_service = TaskService()
