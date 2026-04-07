from fastapi import FastAPI
from api.schemas import RecommendRequest, RecommendResponse
from api.inference import recommend


app = FastAPI(title="Bank Product Recommender API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def get_recommendations(request: RecommendRequest):
    recommendations = recommend(
        user_id=request.user_id,
        user_features=request.features,
        top_k=request.top_k,
    )
    return RecommendResponse(
        user_id=request.user_id,
        recommendations=recommendations,
    )
