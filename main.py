from fastapi import FastAPI, Depends, HTTPException
#fast api - creating api server,depends- dependency injection, HTTP exceptions
# SQLAlchemy imports-python library for DB handling
from sqlalchemy.orm import Session#Object Relational Mapper (ORM)
from datetime import datetime, timedelta
from sqlalchemy import func#allows the operations like sum, avg in queries

# Import DB session and ORM models
from database import SessionLocal, StudySession, Task, Note
from models import FocusSession # Timer-related model (non-ML)

app = FastAPI(title="StudyHacker API")#swagger UI

# ============================
# CORS MIDDLEWARE SETUP--Cross-Origin Resource Sharing,
# ============================
# Browsers do NOT allow one website to freely talk to another website’s backend unless the backend explicitly allows it.

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can restrict to localhost for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============================
# DATABASE DEPENDENCY
# ============================
# This function provides a database session to each request
# and ensures it is closed after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# BASIC HEALTH CHECK
# ============================
@app.get("/")#route decorator
def home():#When a GET request comes to'/'(endpoint), run the function below
    return {"message": "StudyHacker API is running successfully"}

# ======================================================
# PART 1 — STUDY SESSION MODULE
# ======================================================

# Add a study session
@app.post("/add-session")
def add_session(subject: str, duration: int, db: Session = Depends(get_db)):
    """
    Stores subject-wise study duration.
    This is raw data collection (NO analytics).
    """ #new orm object
    session = StudySession(
        subject=subject,
        duration=duration,
        date=datetime.utcnow()
    )
    db.add(session)#adds to session
    db.commit()#add permentaly to DB
    db.refresh(session)#get the latest state from DB(id)
    return {"message": "Study session added", "session": session}

# Retrieve all study sessions
@app.get("/get-sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(StudySession).all()

# Summary analytics (rule-based, not ML)
@app.get("/get-summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Aggregates total study time and subject-wise distribution.
    Simple statistics-based analytics.
    """
    sessions = db.query(StudySession).all()#fetches 

    total_minutes = sum(s.duration for s in sessions)
    subject_wise = {}#d

    for s in sessions:
        subject_wise[s.subject] = subject_wise.get(s.subject, 0) + s.duration

    return {
        "total_sessions": len(sessions),
        "total_minutes": total_minutes,
        "minutes_per_subject": subject_wise
    }

# ======================================================
# PART 2 — TASK MANAGEMENT MODULE
# ======================================================

# Add a task
@app.post("/add-task")
def add_task(title: str, db: Session = Depends(get_db)):
    task = Task(title=title, completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"message": "Task added", "task": task}

# Get all tasks
@app.get("/get-tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# Mark task as completed(put-update)
@app.put("/complete-task/{task_id}")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()
    return {"message": "Task completed", "task": task}

# Delete a task
@app.delete("/delete-task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

# ======================================================
# PART 3 — NOTES MODULE
# ======================================================

@app.post("/add-note")
def add_note(title: str, content: str, db: Session = Depends(get_db)):
    note = Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"message": "Note added", "note": note}

@app.get("/get-notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

# ======================================================
# PART 4 — FOCUS TIMER MODULE
# ======================================================

@app.post("/start-timer")
def start_timer(db: Session = Depends(get_db)):
    """
    Starts a focus session by storing start time.
    Duration is calculated only when the timer is stopped.
    """
    timer = FocusSession(start_time=datetime.utcnow())
    db.add(timer)
    db.commit()
    db.refresh(timer)
    return {"message": "Timer started", "session_id": timer.id}

@app.post("/stop-timer/{session_id}")
def stop_timer(session_id: int, db: Session = Depends(get_db)):
    timer = db.query(FocusSession).filter(FocusSession.id == session_id).first()
    if not timer:
        raise HTTPException(status_code=404, detail="Timer session not found")
    
    timer.end_time = datetime.utcnow()
    timer.duration = int((timer.end_time - timer.start_time).total_seconds() / 60)
    db.commit()
    return {
        "message": "Timer stopped",
        "duration_minutes": timer.duration
    }

# ======================================================
# PART 5 — ANALYTICS / REPORTS (USED BY DASHBOARD)
# ======================================================
@app.get("/stats/weekly")
def weekly_stats(db: Session = Depends(get_db)):
    week_ago = datetime.utcnow() - timedelta(days=7)#dynamic, gets date 7 days ago

    study_minutes = (
        db.query(func.sum(StudySession.duration))
        .filter(StudySession.date >= week_ago)
        .scalar()#one single value
    ) or 0

    focus_minutes = (
        db.query(func.sum(FocusSession.duration))
        .filter(FocusSession.start_time >= week_ago)
        .scalar()
    ) or 0

    return {
        "study_minutes": study_minutes,
        "focus_minutes": focus_minutes,
        "total_minutes": study_minutes + focus_minutes
    }

@app.get("/stats/monthly")
def monthly_stats(db: Session = Depends(get_db)):
    start_month = datetime.utcnow().replace(day=1)

    study_minutes = (
        db.query(func.sum(StudySession.duration))
        .filter(StudySession.date >= start_month)
        .scalar()
    ) or 0

    focus_minutes = (
        db.query(func.sum(FocusSession.duration))
        .filter(FocusSession.start_time >= start_month)
        .scalar()
    ) or 0

    return {
        "study_minutes": study_minutes,
        "focus_minutes": focus_minutes,
        "total_minutes": study_minutes + focus_minutes
    }

@app.get("/stats/tasks-progress")
def tasks_progress(db: Session = Depends(get_db)):
    """
    Simple task completion statistics.
    """
    total = db.query(Task).count()
    completed = db.query(Task).filter(Task.completed == True).count()

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": total - completed
    }
#===========================
#modelpart
#==========================
'''from ml_model import train_model, predict
import pandas as pd

# Dummy training data endpoint (you can extend this later)
@app.post("/train-model")
def train():
    # Example training data
    data = [
        {"study_hours": 2, "tasks_completed": 1, "focus_minutes": 30, "notes_added":1, "productivity": "Low"},
        {"study_hours": 5, "tasks_completed": 3, "focus_minutes": 90, "notes_added":2, "productivity": "High"},
        {"study_hours": 3, "tasks_completed": 2, "focus_minutes": 60, "notes_added":1, "productivity": "Medium"},
    ]
    df = pd.DataFrame(data)
    return train_model(df)

# Predict productivity
@app.post("/predict-productivity")
def predict_productivity(study_hours: int, tasks_completed: int, focus_minutes: int, notes_added: int):
    input_dict = {
        "study_hours": study_hours,
        "tasks_completed": tasks_completed,
        "focus_minutes": focus_minutes,
        "notes_added": notes_added
    }
    return predict(input_dict)

# Recommended study plan (dummy logic)
@app.get("/recommended-study-plan")
def recommended_plan():
    return {
        "subject": "Python",
        "duration_minutes": 60,
        "tip": "Focus on algorithms today"
    }
'''
