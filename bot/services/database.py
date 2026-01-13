"""Сервис для работы с базой данных"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import logging

from config import settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Сервис для работы с PostgreSQL"""
    
    def __init__(self):
        self.config = settings.db
    
    def get_connection(self):
        """Получить соединение с БД"""
        return psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password
        )
    
    @contextmanager
    def get_cursor(self, commit: bool = False):
        """Контекстный менеджер для работы с курсором"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    # Методы для работы с пользователями
    def get_or_create_user(self, chat_id: int, name: str) -> Dict[str, Any]:
        """Получить или создать пользователя"""
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE chat_id = %s",
                (chat_id,)
            )
            user = cursor.fetchone()
            
            if not user:
                cursor.execute(
                    "INSERT INTO users (chat_id, name) VALUES (%s, %s) RETURNING *",
                    (chat_id, name)
                )
                user = cursor.fetchone()
            
            return dict(user) if user else {}
    
    def get_user_by_chat_id(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Получить пользователя по chat_id"""
        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE chat_id = %s",
                (chat_id,)
            )
            user = cursor.fetchone()
            return dict(user) if user else None
    
    # Методы для работы с темами
    def get_oge_topics(self) -> List[Dict[str, Any]]:
        """Получить все темы ОГЭ"""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM oge_topics ORDER BY topic_number")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_ege_topics(self) -> List[Dict[str, Any]]:
        """Получить все темы ЕГЭ"""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM ege_topics ORDER BY topic_number")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_topic_by_number(self, topic_number: int, exam_type: str) -> Optional[Dict[str, Any]]:
        """Получить тему по номеру"""
        table = "oge_topics" if exam_type == "OGE" else "ege_topics"
        with self.get_cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {table} WHERE topic_number = %s",
                (topic_number,)
            )
            topic = cursor.fetchone()
            return dict(topic) if topic else None
    
    # Методы для работы с прогрессом
    def get_user_progress(self, user_id: int, exam_type: str) -> Dict[str, Any]:
        """Получить прогресс пользователя"""
        progress_table = "user_oge_progress" if exam_type == "OGE" else "user_ege_progress"
        topics_table = "oge_topics" if exam_type == "OGE" else "ege_topics"
        
        with self.get_cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    COUNT(*) FILTER (WHERE up.is_completed = TRUE) as completed_count,
                    COUNT(*) as total_count
                FROM {topics_table} t
                LEFT JOIN {progress_table} up ON t.topic_id = up.topic_id AND up.user_id = %s
            """, (user_id,))
            result = cursor.fetchone()
            return dict(result) if result else {"completed_count": 0, "total_count": 0}
    
    def get_user_topic_progress(self, user_id: int, topic_id: int, exam_type: str) -> Optional[Dict[str, Any]]:
        """Получить прогресс пользователя по конкретной теме"""
        progress_table = "user_oge_progress" if exam_type == "OGE" else "user_ege_progress"
        
        with self.get_cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM {progress_table}
                WHERE user_id = %s AND topic_id = %s
            """, (user_id, topic_id))
            progress = cursor.fetchone()
            return dict(progress) if progress else None
    
    def create_or_update_progress(self, user_id: int, topic_id: int, exam_type: str, 
                                  correct_count: int = 0, is_completed: bool = False):
        """Создать или обновить прогресс пользователя"""
        progress_table = "user_oge_progress" if exam_type == "OGE" else "user_ege_progress"
        
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(f"""
                INSERT INTO {progress_table} (user_id, topic_id, correct_answers_count, is_completed, total_attempts)
                VALUES (%s, %s, %s, %s, 1)
                ON CONFLICT (user_id, topic_id)
                DO UPDATE SET
                    correct_answers_count = {progress_table}.correct_answers_count + %s,
                    total_attempts = {progress_table}.total_attempts + 1,
                    is_completed = CASE WHEN %s THEN TRUE ELSE {progress_table}.is_completed END,
                    last_attempt_at = CURRENT_TIMESTAMP,
                    completed_at = CASE WHEN %s THEN CURRENT_TIMESTAMP ELSE {progress_table}.completed_at END
            """, (user_id, topic_id, correct_count, is_completed, correct_count, is_completed, is_completed))
    
    def save_task_attempt(self, user_id: int, task_id: int, task_type: str, 
                          user_answer: str, is_correct: bool):
        """Сохранить попытку решения задания"""
        with self.get_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO task_attempts (user_id, task_id, task_type, user_answer, is_correct)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, task_id, task_type, user_answer, is_correct))


# Глобальный экземпляр сервиса
db_service = DatabaseService()


