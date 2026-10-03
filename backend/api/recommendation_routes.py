from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from ml.smart_recommender import recommend_recipes

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)

class RecommendationRequest(BaseModel):
    ingredients: List[str]
    cuisine: str = "All"
    diet: str = "All"
    nutrition: str = "All"
    top_n: int = 5

@router.post("")
def get_recommendations(request: RecommendationRequest):
    try:
        results = recommend_recipes(
            user_ingredients=request.ingredients,
            top_n=request.top_n,
            cuisine=request.cuisine,
            diet=request.diet,
            nutrition=request.nutrition
        )

        return {
            "success": True,
            "count": len(results),
            "recommendations": results.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )