from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from detector import find_anomalies # Import our refactored function

app = FastAPI(
    title="Fitpass Check-in Anomaly Detector API",
    description="An AI service to detect suspicious check-in patterns.",
    version="1.0.0"
)

# Define the data models for incoming requests
class CheckIn(BaseModel):
    user_id: int
    timestamp: datetime
    latitude: float
    longitude: float

class CheckInBatch(BaseModel):
    checkins: List[CheckIn]

# Define the data model for the response
class Anomaly(BaseModel):
    user_id: int
    previous_checkin_time: datetime
    anomalous_checkin_time: datetime
    distance_km: float

class AnomalyResponse(BaseModel):
    anomalies: List[Anomaly]

@app.post("/detect", response_model=AnomalyResponse)
def detect_anomalies(batch: CheckInBatch):
    """
    Takes a batch of check-in data and returns a list of detected anomalies.
    """
    # Convert Pydantic models to a list of dictionaries
    checkin_data = [checkin.dict() for checkin in batch.checkins]
    anomalies_found = find_anomalies(checkin_data)
    return {"anomalies": anomalies_found}