# Study & Focus Tracker API

## Description
A FastAPI-based backend application to track study sessions and focus time, and provide weekly and monthly productivity analytics.

## Features
- Log study sessions
- Log focus sessions
- Weekly productivity statistics
- Monthly productivity statistics
- RESTful APIs with Swagger UI

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Project Structure
- `main.py` – Application entry point
- `database.py` – Database configuration
- `models.py` – ORM models
- `dashboard.py` – Analytics endpoints

## How to Run
```bash
### Prerequisites
- Python 3.9 or above
- Git installed

### Steps

1. Clone the repository:
```bash
git clone https://github.com/your-username/StudyHackerAPI.git
2.cd StudyHackerAPI
3.pip install -r requirements.txt
4.python -m uvicorn main:app --reload
#5.http://127.0.0.1:8000/docs- open
