from fastapi import FastAPI
from pydantic import BaseModel, Field
from router import route_by_language # Import our refactored function

app = FastAPI(
    title="Fitpass Language Router API",
    description="An AI service to detect language and suggest support routing.",
    version="1.0.0"
)

# Define data models
class SupportRequest(BaseModel):
    text: str = Field(..., example="I need help with my booking")

class RoutingResponse(BaseModel):
    language: str
    route_to: str

@app.post("/route", response_model=RoutingResponse)
def get_routing_suggestion(request: SupportRequest):
    """
    Takes a text input and returns the detected language and a routing key.
    """
    result = route_by_language(request.text)
    return result