from pathlib import Path
import joblib
import pandas as pd
import lightgbm as lgb


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

rank_model = lgb.Booster(model_file=str(MODELS_DIR / "hybrid_rank_model.bin"))
als_model = joblib.load(MODELS_DIR / "als_model.pkl")

user2idx = joblib.load(MODELS_DIR / "user2idx.pkl")
idx2item = joblib.load(MODELS_DIR / "idx2item.pkl")
popular_products = joblib.load(MODELS_DIR / "popular_products.pkl")

product_popularity_map = joblib.load(MODELS_DIR / "product_popularity_map.pkl")
product_prev_popularity_map = joblib.load(MODELS_DIR / "product_prev_popularity_map.pkl")

rank_feature_cols = joblib.load(MODELS_DIR / "rank_feature_cols.pkl")
rank_cat_features = joblib.load(MODELS_DIR / "rank_cat_features.pkl")


def recommend(user_id: int, user_features: dict, top_k: int = 5) -> list[str]:
    candidates = []

    if user_id in user2idx:
        user_idx = user2idx[user_id]
        item_ids, scores = als_model.recommend(user_idx, None, N=20)

        for item_idx, score in zip(item_ids, scores):
            item_idx = int(item_idx)
            if item_idx in idx2item:
                product = idx2item[item_idx]
                candidates.append((product, float(score)))

    existing_products = set()

    for product in popular_products:
        if len(candidates) >= 20:
            break
        if product not in [p for p, _ in candidates] and product not in existing_products:
            candidates.append((product, 0.0))

    rows = []
    for product, als_score in candidates:
        row = dict(user_features)
        row["candidate_product"] = product
        row["als_score"] = als_score
        row["candidate_source_als"] = int(als_score != 0.0)
        row["candidate_source_pop"] = int(als_score == 0.0)
        row["product_popularity"] = product_popularity_map.get(product, 0.0)
        row["product_prev_popularity"] = product_prev_popularity_map.get(product, 0.0)
        row["prev_owned_candidate"] = 0
        rows.append(row)

    pred_df = pd.DataFrame(rows)

    for col in rank_feature_cols:
        if col not in pred_df.columns:
            pred_df[col] = 0

    for col in rank_cat_features:
        pred_df[col] = pred_df[col].fillna("UNKNOWN").astype(str).astype("category")

    pred_df["score"] = rank_model.predict(pred_df[rank_feature_cols])
    pred_df = pred_df.sort_values("score", ascending=False)

    return pred_df["candidate_product"].head(top_k).tolist()
