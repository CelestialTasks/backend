from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Предполагается, что Base определён в models.py

# URL для подключения к базе данных (с использованием SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Создаем синхронный движок
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаем sessionmaker для синхронной работы
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция инициализации базы данных (создание таблиц)
def init_db():
    Base.metadata.create_all(bind=engine)

# Зависимость для получения сессии базы данных в FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Если этот файл запустить напрямую, создадим таблицы в базе
if __name__ == "__main__":
    init_db()
