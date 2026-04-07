from pydantic import BaseModel
from typing import Dict, List, Any


class RecommendRequest(BaseModel):
    user_id: int
    features: Dict[str, Any]
    top_k: int = 5


class RecommendResponse(BaseModel):
    user_id: int
    recommendations: List[str]
    