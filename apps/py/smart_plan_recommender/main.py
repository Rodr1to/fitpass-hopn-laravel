from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Any, Dict
from recommender import recommend_plan # Import our refactored function

# Initialize the FastAPI app
app = FastAPI(
    title="Fitpass Smart Plan Recommender API",
    description="A rule-based AI service to recommend membership plans.",
    version="1.0.0"
)

# Define the data model for the incoming request using Pydantic
# This provides automatic data validation
class UserProfile(BaseModel):
    age: int = Field(..., example=30)
    gender: str = Field(..., example="female")
    goal: str = Field(..., example="Relax")
    activities: List[str] = Field(..., example=["Yoga", "Spa"])

# Define the data model for the response
class RecommendationResponse(BaseModel):
    recommended_plan: str

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendation(profile: UserProfile):
    """
    Takes a user profile and returns a recommended membership plan.
    """
    # Convert the Pydantic model to a dictionary to pass to our function
    user_profile_dict = profile.dict()
    plan = recommend_plan(user_profile_dict)
    return {"recommended_plan": plan}