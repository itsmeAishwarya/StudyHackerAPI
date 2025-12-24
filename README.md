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
pip install -r requirements.txt
uvicorn main:app --reload
