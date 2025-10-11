# プログラミング学習アプリ バックエンド API

FastAPI を使用したプログラミング学習アプリのバックエンド API です。

## 技術スタック

- **FastAPI**: 高性能な Python Web フレームワーク
- **Pydantic**: データバリデーションと設定管理
- **PyMySQL**: MySQL データベースクライアント
- **AWS Lambda**: サーバーレス実行環境
- **AWS RDS**: マネージドデータベース

## プロジェクト構造

```
backend/
├── src/
│   ├── main.py              # FastAPI アプリケーションエントリーポイント
│   ├── config.py            # アプリケーション設定
│   ├── lambda_handler.py    # AWS Lambda ハンドラー
│   ├── database/            # データベース関連
│   │   ├── connection.py    # データベース接続管理
│   │   ├── operations.py    # データベース操作
│   │   ├── schema.py        # データベーススキーマ
│   │   └── init_db.py       # データベース初期化
│   ├── handlers/            # API ハンドラー
│   │   ├── auth/            # 認証関連 API
│   │   ├── exercise/        # 演習関連 API
│   │   └── progress/        # 進捗関連 API
│   ├── models/              # Pydantic モデル
│   │   ├── user.py          # ユーザーモデル
│   │   ├── exercise.py      # 演習モデル
│   │   ├── progress.py      # 進捗モデル
│   │   └── common.py        # 共通モデル
│   ├── services/            # ビジネスロジック
│   └── utils/               # ユーティリティ
│       ├── exceptions.py    # カスタム例外
│       └── error_handlers.py # エラーハンドラー
├── infrastructure/          # CloudFormation テンプレート
├── requirements.txt         # Python 依存関係
├── run_dev.py              # 開発サーバー起動スクリプト
└── .env.example            # 環境変数テンプレート
```

## セットアップ

### 1. 依存関係のインストール

```bash
cd backend
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
cp .env.example .env
# .env ファイルを編集してデータベース接続情報を設定
```

### 3. データベースの初期化

```bash
python -m src.database.init_db
```

### 4. 開発サーバーの起動

```bash
python run_dev.py
```

## API エンドポイント

### 基本情報

- **ベース URL**: `http://localhost:8000/api/v1`
- **API ドキュメント**: `http://localhost:8000/docs`
- **ヘルスチェック**: `http://localhost:8000/health`

### 認証 API (`/api/v1/auth`)

- `POST /register` - ユーザー登録
- `GET /profile/{user_id}` - ユーザープロフィール取得
- `PUT /profile/{user_id}` - ユーザープロフィール更新
- `POST /verify-token` - トークン検証

### 演習 API (`/api/v1/exercises`)

- `GET /` - 演習一覧取得
- `GET /{exercise_id}` - 演習詳細取得
- `POST /` - 演習作成
- `PUT /{exercise_id}` - 演習更新
- `DELETE /{exercise_id}` - 演習削除
- `POST /submit` - コード提出・実行

### 進捗 API (`/api/v1/progress`)

- `GET /user/{user_id}` - ユーザー進捗一覧取得
- `GET /user/{user_id}/stats` - ユーザー進捗統計取得
- `GET /user/{user_id}/summary` - ユーザー進捗サマリー取得
- `GET /{user_id}/{exercise_id}` - 個別進捗取得
- `POST /` - 進捗記録
- `PUT /{user_id}/{exercise_id}` - 進捗更新
- `DELETE /{user_id}/{exercise_id}` - 進捗削除

## 開発

### ローカル開発

```bash
# 開発サーバー起動（自動リロード有効）
python run_dev.py

# データベース初期化
python -m src.database.init_db
```

### AWS Lambda デプロイ

Lambda 関数として動作させる場合は `src/lambda_handler.py` を使用します。

## 環境変数

| 変数名                 | 説明                      | デフォルト値               |
| ---------------------- | ------------------------- | -------------------------- |
| `DATABASE_HOST`        | データベースホスト        | `localhost`                |
| `DATABASE_PORT`        | データベースポート        | `3306`                     |
| `DATABASE_NAME`        | データベース名            | `programming_learning_app` |
| `DATABASE_USER`        | データベースユーザー      | `root`                     |
| `DATABASE_PASSWORD`    | データベースパスワード    | ``                         |
| `AWS_REGION`           | AWS リージョン            | `ap-northeast-1`           |
| `COGNITO_USER_POOL_ID` | Cognito ユーザープール ID | -                          |
| `COGNITO_CLIENT_ID`    | Cognito クライアント ID   | -                          |

## ログ

アプリケーションは標準的な Python logging を使用しています。ログレベルは環境変数 `LOG_LEVEL` で設定できます。

## エラーハンドリング

統一的なエラーレスポンス形式を使用しています：

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ"
  }
}
```
