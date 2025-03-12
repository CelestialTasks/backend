from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# URL to connect to the database (using SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Creating a synchronous engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create sessionmaker for synchronous work
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Database initialization function (creation of tables)
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency for getting database session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: remove it when we switch to Potgre
if __name__ == "__main__":
    init_db()
