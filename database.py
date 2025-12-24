from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime#create_engine-DB connection,
from sqlalchemy.ext.declarative import declarative_base#Base class for ORM models
from sqlalchemy.orm import sessionmaker#creates db
from datetime import datetime
#Each class represents a table, and SQLAlchemy maps Python objects to database records.
#This file handles database configuration and ORM models using SQLAlchemy.
# -----------------------------
# DATABASE SETUP
# -----------------------------

DATABASE_URL = "sqlite:///./studyhacker.db"
#“SQLite is lightweight and suitable for local development and academic projects.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False})
#by default sqlite restricts to same thread

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#creates independent DB for each request.changes r not automatically saved,we must call
Base = declarative_base()

# -----------------------------
# STUDY SESSION MODEL
# -----------------------------

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    duration = Column(Integer)
    date = Column(DateTime, default=datetime.now)

# -----------------------------
# TASK MODEL
# -----------------------------

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

# -----------------------------
# NOTES MODEL
# -----------------------------

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    date = Column(DateTime, default=datetime.now)

# -----------------------------
# CREATE TABLES
# -----------------------------
from models import FocusSession
Base.metadata.create_all(bind=engine)
#This file handles database configuration and ORM models using SQLAlchemy.
#Each class represents a table, and SQLAlchemy maps Python objects to database records.
'''def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''