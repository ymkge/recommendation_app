
# 推薦システムアプリ

ユーザー×アイテムの評価データに基づき、協調フィルタリング（SVD）を用いておすすめのアイテムを提示するシンプルなWebアプリケーションです。

- **バックエンド**: FastAPI
- **フロントエンド**: Streamlit
- **推薦モデル**: scikit-learn, pandas, numpy

## 🚀 プロジェクト構成

```
/recommendation_app
├── ratings.csv         # サンプル評価データ
├── requirements.txt    # Pythonライブラリ
├── model.py            # 推薦モデルのロジック
├── main.py             # FastAPIバックエンド
├── app.py              # Streamlitフロントエンド
└── README.md           # このファイル
```

## 🛠️ ローカルでの実行方法

### 1. リポジトリのクローン

```bash
git clone <your-repository-url>
cd recommendation_app
```

### 2. 仮想環境の作成と有効化（推奨）

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate    # Windows
```

### 3. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. バックエンドサーバーの起動

新しいターミナルを開き、以下のコマンドを実行します。

```bash
uvicorn main:app --reload
```

サーバーが `http://127.0.0.1:8000` で起動します。
APIドキュメントは `http://127.0.0.1:8000/docs` で確認できます。

### 5. フロントエンドの起動

別の新しいターミナルを開き、以下のコマンドを実行します。

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が自動的に開かれ、アプリケーションを操作できます。

---

## ☁️ デプロイ手順

このアプリケーションは、バックエンド（FastAPI）を**Render**に、フロントエンド（Streamlit）を**Vercel**にデプロイすることを想定しています。

### 準備

- 上記で作成したすべてのファイルをGitHubリポジトリにプッシュします。
- [Render](https://render.com/) と [Vercel](https://vercel.com/) のアカウントを作成しておきます。

### 1. バックエンド (FastAPI) を Render にデプロイ

1.  Renderのダッシュボードで `New +` > `Web Service` を選択します。
2.  作成したGitHubリポジトリを接続します。
3.  以下の設定を入力します:
    -   **Name**: `recommendation-api` （または好きな名前）
    -   **Root Directory**: `recommendation_app` （リポジトリのルートにファイルがある場合は空白）
    -   **Environment**: `Python 3`
    -   **Region**: （好きなリージョンを選択）
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4.  `Create Web Service` をクリックしてデプロイを開始します。
5.  デプロイが完了すると、`xxx.onrender.com` のようなURLが発行されます。このURLをコピーしておきます。

### 2. フロントエンド (Streamlit) を Vercel にデプロイ

1.  Vercelのダッシュボードで `Add New...` > `Project` を選択します。
2.  作成したGitHubリポジトリをインポートします。
3.  **Framework Preset** が `Streamlit` として自動的に検出されることを確認します。
4.  `Environment Variables` のセクションを開き、新しい環境変数を追加します:
    -   **Name**: `API_URL`
    -   **Value**: `手順1でコピーしたRenderのURL` (例: `https://recommendation-api.onrender.com`)
5.  `Deploy` をクリックします。

デプロイが完了すると、フロントエンド用のURLが発行され、公開されたアプリケーションにアクセスできます。
