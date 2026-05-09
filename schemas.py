from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class MetricCreate(BaseModel):
    type: str  # pulse, weight, height, pressure, sleep, glucose, stress
    value: float

class MetricOut(BaseModel):
    id: int
    user_id: int
    type: str
    value: float
    timestamp: datetime
    class Config:
        from_attributes = True
        
class ReportMetric(BaseModel):
    type: str
    avg_value: Optional[float] = None
    entries_count: int = 0
    comment: str = ""

class ReportResponse(BaseModel):
    user_id: int
    days: int
    metrics: List[ReportMetric]