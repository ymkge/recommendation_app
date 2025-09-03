
import streamlit as st
import requests
import pandas as pd
import os

# APIのURLを環境変数から取得、なければローカルのURLをデフォルトに
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="推薦システム", layout="centered")

st.title("🎬 アイテム推薦アプリ")
st.markdown("ユーザーIDを選択すると、そのユーザーへのおすすめアイテムが5件表示されます。")

# --- ユーザー選択 ---
st.header("👤 ユーザーを選択")

# APIからユーザーリストを取得
try:
    response = requests.get(f"{API_URL}/users")
    response.raise_for_status() # エラーがあれば例外を発生
    users_data = response.json()
    user_ids = users_data.get("user_ids", [])
except requests.exceptions.RequestException as e:
    st.error(f"APIへの接続に失敗しました: {e}")
    st.info("バックエンドサーバーが起動していることを確認してください: `uvicorn main:app --reload`")
    user_ids = [] # エラー時は空のリスト

if not user_ids:
    st.warning("表示できるユーザーがいません。")
else:
    selected_user_id = st.selectbox(
        label="ユーザーIDを選択してください",
        options=user_ids,
        index=0
    )

    # --- 推薦結果の表示 ---
    if st.button("✨ おすすめを検索", type="primary"):
        if selected_user_id:
            st.header(f"🎁 ユーザー`{selected_user_id}`さんへのおすすめ")
            with st.spinner("おすすめを計算中..."):
                try:
                    response = requests.get(f"{API_URL}/recommend/{selected_user_id}")
                    response.raise_for_status()
                    
                    data = response.json()
                    recommendations = data.get("recommendations", [])
                    
                    if recommendations:
                        # 結果を表形式で表示
                        df = pd.DataFrame({
                            'おすすめアイテムID': recommendations,
                            '評価予測順位': range(1, len(recommendations) + 1)
                        })
                        st.dataframe(df.set_index('評価予測順位'), use_container_width=True)
                    else:
                        st.info("このユーザーへのおすすめアイテムは見つかりませんでした。")
                
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        st.error(f"ユーザー`{selected_user_id}`のおすすめは見つかりませんでした。すべてのアイテムを評価済みか、データが不足している可能性があります。")
                    else:
                        st.error(f"エラーが発生しました: {e.response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"APIへのリクエスト中にエラーが発生しました: {e}")

# --- フッター ---
st.markdown("---")
st.markdown("Developed with ❤️ by Gemini")
