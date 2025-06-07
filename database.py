from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

# 1. Настройка пути к БД
# Лучше использовать абсолютный путь и кроссплатформенное создание директорий
db_dir = Path("Общая_папка")
db_dir.mkdir(exist_ok=True)  # Создаем папку, если её нет
db_path = db_dir / "employees.db"

# 2. Подключение к SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path.absolute()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Только для SQLite!
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=True  # Логирование SQL-запросов (удобно для разработки)
)

# 3. Настройка сессии
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Позволяет использовать объекты после коммита
)

# 4. Базовый класс для моделей
Base = declarative_base()

# 5. Функция для получения БД (используется в зависимостях FastAPI)
def get_db():
    """
    Генератор сессий БД для использования в Depends()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()