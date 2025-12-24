from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class FocusSession(Base):
    __tablename__ = "focus_sessions"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # in minutes


