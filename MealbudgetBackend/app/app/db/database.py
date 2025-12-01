from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# SQLite connection string (το αρχείο θα δημιουργηθεί τοπικά αν δεν υπάρχει)
SQLALCHEMY_DATABASE_URL = "sqlite:///./mealbudget.db"

# Δημιουργία engine για SQLite 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Factory για συνεδρίες βάσης δεδομένων
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Βασική κλάση για τα ORM models
class Base(DeclarativeBase):
    pass


# Dependency για FastAPI: δίνει και κλείνει μια Session ανά request
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
