
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD

class RecommendationModel:
    def __init__(self, data_path):
        """
        モデルの初期化
        
        Args:
            data_path (str): 評価データCSVのパス
        """
        self.data_path = data_path
        self.svd = TruncatedSVD(n_components=2, random_state=42)
        self.user_item_matrix = None
        self.predicted_ratings = None
        self.item_ids = None

    def _load_data(self):
        """
        データを読み込み、ユーザー×アイテムの評価行列を作成する
        """
        ratings_df = pd.read_csv(self.data_path)
        self.user_item_matrix = ratings_df.pivot_table(
            index='user_id', 
            columns='item_id', 
            values='rating'
        ).fillna(0)
        self.item_ids = self.user_item_matrix.columns

    def fit(self):
        """
        モデルを学習させる (SVDによる行列分解)
        """
        self._load_data()
        # SVDを実行して次元削減
        matrix_reduced = self.svd.fit_transform(self.user_item_matrix)
        # 削減された次元から元の次元に復元し、評価値を予測
        self.predicted_ratings = np.dot(matrix_reduced, self.svd.components_)
        # 予測評価値をDataFrameに変換
        self.predicted_ratings = pd.DataFrame(
            self.predicted_ratings,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.columns
        )

    def recommend(self, user_id, n_recommendations=5):
        """
        指定されたユーザーへのおすすめアイテムを返す
        
        Args:
            user_id (int): ユーザーID
            n_recommendations (int): おすすめするアイテム数
            
        Returns:
            list: おすすめアイテムIDのリスト
        """
        if user_id not in self.user_item_matrix.index:
            return []

        # ユーザーの予測評価値を取得
        user_ratings = self.predicted_ratings.loc[user_id]
        
        # ユーザーが既に評価したアイテムを取得
        rated_items = self.user_item_matrix.loc[user_id]
        rated_items = rated_items[rated_items > 0].index
        
        # 未評価のアイテムの中から、予測評価値が高い順にソート
        recommendations = user_ratings.drop(rated_items).sort_values(ascending=False)
        
        return recommendations.head(n_recommendations).index.tolist()

# テスト用
if __name__ == '__main__':
    model = RecommendationModel('ratings.csv')
    model.fit()
    
    # ユーザー1へのおすすめ
    user_id = 1
    recommendations = model.recommend(user_id)
    print(f"Recommendations for user {user_id}: {recommendations}")

    # ユーザー3へのおすすめ
    user_id = 3
    recommendations = model.recommend(user_id)
    print(f"Recommendations for user {user_id}: {recommendations}")
