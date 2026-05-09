from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    metrics = relationship("Metric", back_populates="owner")

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # pulse, weight, height, pressure, sleep, glucose, stress
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="metrics")