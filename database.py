from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:////home/harlem/Bureau/2025/Backend Development/todoList-api/todo.db"


engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dépendance pour les routes
def get_db():
  db = sessionLocal()
  try:
    yield db
    
  finally:
    db.close()