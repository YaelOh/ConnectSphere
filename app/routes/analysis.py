from fastapi import APIRouter
from app.utils.recommendation import analyze_interests, get_recommendations

router = APIRouter()

@router.post("/recommendations")
def get_recommendations_for_user(user_data: dict):
    """
    Analyze user's recent podcasts and provide recommendations.
    """
    interests = analyze_interests(user_data)
    recommendations = get_recommendations(interests)
    return {"interests": interests, "recommendations": recommendations}