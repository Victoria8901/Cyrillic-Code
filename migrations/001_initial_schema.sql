-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы тем ОГЭ
CREATE TABLE IF NOT EXISTS oge_topics (
    topic_id SERIAL PRIMARY KEY,
    topic_number INTEGER NOT NULL UNIQUE,
    topic_name VARCHAR(255),
    description TEXT
);

-- Создание таблицы тем ЕГЭ
CREATE TABLE IF NOT EXISTS ege_topics (
    topic_id SERIAL PRIMARY KEY,
    topic_number INTEGER NOT NULL UNIQUE,
    topic_name VARCHAR(255),
    description TEXT
);

-- Создание таблицы прогресса пользователей по темам ОГЭ
CREATE TABLE IF NOT EXISTS user_oge_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    topic_id INTEGER NOT NULL REFERENCES oge_topics(topic_id) ON DELETE CASCADE,
    is_completed BOOLEAN DEFAULT FALSE,
    correct_answers_count INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE(user_id, topic_id)
);

-- Создание таблицы прогресса пользователей по темам ЕГЭ
CREATE TABLE IF NOT EXISTS user_ege_progress (
    progress_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    topic_id INTEGER NOT NULL REFERENCES ege_topics(topic_id) ON DELETE CASCADE,
    is_completed BOOLEAN DEFAULT FALSE,
    correct_answers_count INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE(user_id, topic_id)
);

-- Создание таблицы заданий ОГЭ
CREATE TABLE IF NOT EXISTS oge_tasks (
    task_id SERIAL PRIMARY KEY,
    topic_id INTEGER NOT NULL REFERENCES oge_topics(topic_id) ON DELETE CASCADE,
    task_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы заданий ЕГЭ
CREATE TABLE IF NOT EXISTS ege_tasks (
    task_id SERIAL PRIMARY KEY,
    topic_id INTEGER NOT NULL REFERENCES ege_topics(topic_id) ON DELETE CASCADE,
    task_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы истории решений
CREATE TABLE IF NOT EXISTS task_attempts (
    attempt_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    task_id INTEGER NOT NULL,
    task_type VARCHAR(10) NOT NULL CHECK (task_type IN ('OGE', 'EGE')),
    user_answer TEXT,
    is_correct BOOLEAN,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для оптимизации
CREATE INDEX IF NOT EXISTS idx_users_chat_id ON users(chat_id);
CREATE INDEX IF NOT EXISTS idx_user_oge_progress_user_id ON user_oge_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_oge_progress_topic_id ON user_oge_progress(topic_id);
CREATE INDEX IF NOT EXISTS idx_user_ege_progress_user_id ON user_ege_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_ege_progress_topic_id ON user_ege_progress(topic_id);
CREATE INDEX IF NOT EXISTS idx_oge_tasks_topic_id ON oge_tasks(topic_id);
CREATE INDEX IF NOT EXISTS idx_ege_tasks_topic_id ON ege_tasks(topic_id);
CREATE INDEX IF NOT EXISTS idx_task_attempts_user_id ON task_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_task_attempts_attempted_at ON task_attempts(attempted_at);

-- Вставка начальных данных для тем ОГЭ (задания 2-9)
INSERT INTO oge_topics (topic_number, topic_name) VALUES
(2, 'Задание 2 ОГЭ'),
(3, 'Задание 3 ОГЭ'),
(4, 'Задание 4 ОГЭ'),
(5, 'Задание 5 ОГЭ'),
(6, 'Задание 6 ОГЭ'),
(7, 'Задание 7 ОГЭ'),
(8, 'Задание 8 ОГЭ'),
(9, 'Задание 9 ОГЭ')
ON CONFLICT (topic_number) DO NOTHING;

-- Вставка начальных данных для тем ЕГЭ (задания 4-21)
INSERT INTO ege_topics (topic_number, topic_name) VALUES
(4, 'Задание 4 ЕГЭ'),
(5, 'Задание 5 ЕГЭ'),
(6, 'Задание 6 ЕГЭ'),
(7, 'Задание 7 ЕГЭ'),
(8, 'Задание 8 ЕГЭ'),
(9, 'Задание 9 ЕГЭ'),
(10, 'Задание 10 ЕГЭ'),
(11, 'Задание 11 ЕГЭ'),
(12, 'Задание 12 ЕГЭ'),
(13, 'Задание 13 ЕГЭ'),
(14, 'Задание 14 ЕГЭ'),
(15, 'Задание 15 ЕГЭ'),
(16, 'Задание 16 ЕГЭ'),
(17, 'Задание 17 ЕГЭ'),
(18, 'Задание 18 ЕГЭ'),
(19, 'Задание 19 ЕГЭ'),
(20, 'Задание 20 ЕГЭ'),
(21, 'Задание 21 ЕГЭ')
ON CONFLICT (topic_number) DO NOTHING;

