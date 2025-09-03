
from fastapi import FastAPI, HTTPException
from model import RecommendationModel

app = FastAPI(
    title="Recommendation API",
    description="A simple API to get item recommendations for a user.",
    version="0.1.0",
)

# グローバルにモデルをロード
model = RecommendationModel(data_path='ratings.csv')
model.fit()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recommendation API"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int):
    """
    ユーザーIDに基づいておすすめのアイテムリストを返します。
    """
    try:
        recommendations = model.recommend(user_id, n_recommendations=5)
        if not recommendations:
            # ユーザーは存在するが、おすすめがない場合も考慮
            raise HTTPException(status_code=404, detail=f"No recommendations found for user {user_id}. They may have rated all items or are a new user.")
        return {"user_id": user_id, "recommendations": recommendations}
    except KeyError:
        # モデルのユーザーリストに存在しない場合
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    except Exception as e:
        # その他の予期せぬエラー
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_users():
    """
    評価データに存在するユニークなユーザーIDのリストを返します。
    """
    user_ids = model.user_item_matrix.index.tolist()
    return {"user_ids": user_ids}
