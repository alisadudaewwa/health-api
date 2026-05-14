from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, get_db, Base
from models import User, Metric
from schemas import (
    UserCreate, UserOut, MetricCreate, MetricOut,
    ReportMetric, ReportResponse
)
from datetime import datetime, timedelta
from typing import List
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Health Metrics API v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или ["*"] для тестов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/metrics", response_model=MetricOut)
def create_metric(user_id: int, metric: MetricCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_metric = Metric(user_id=user_id, type=metric.type, value=metric.value)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@app.get("/metrics/{user_id}", response_model=List[MetricOut])
def get_metrics(user_id: int, db: Session = Depends(get_db)):
    return db.query(Metric).filter(Metric.user_id == user_id).all()

@app.get("/metrics/{user_id}/report", response_model=ReportResponse)
def get_report(user_id: int, days: int = Query(default=7, ge=1, le=30), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    metrics = db.query(Metric).filter(
        Metric.user_id == user_id,
        Metric.timestamp >= start_date,
        Metric.timestamp <= end_date
    ).all()

    grouped = {}
    for m in metrics:
        if m.type not in grouped:
            grouped[m.type] = []
        grouped[m.type].append(m.value)

    result_metrics = []
    for m_type, values in grouped.items():
        avg = round(sum(values) / len(values), 2)
        comment = ""

        if m_type == "pulse":
            comment = "Норма" if 60 <= avg <= 100 else "Внимание: отклонение от нормы"
        elif m_type == "stress":
            comment = "Низкий уровень" if avg <= 3 else ("Средний" if avg <= 7 else "Высокий уровень стресса")
        elif m_type == "sleep":
            hrs = int(avg // 60)
            mins = int(avg % 60)
            comment = f"Средний сон: {hrs}ч {mins}м"
        elif m_type == "height":
            comment = f"Постоянный показатель: {avg} см"
        else:
            comment = "Данные записаны"

        result_metrics.append(ReportMetric(type=m_type, avg_value=avg, entries_count=len(values), comment=comment))

    return ReportResponse(user_id=user_id, days=days, metrics=result_metrics)
