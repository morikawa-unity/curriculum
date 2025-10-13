# プログラミング学習アプリ - Backend

このディレクトリには、プログラミング学習アプリのバックエンド API が含まれています。

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成して以下の設定を追加：

```env
# AWS設定
AWS_REGION=ap-northeast-1
COGNITO_USER_POOL_ID=ap-northeast-1_5SdJ4Iu5J
COGNITO_CLIENT_ID=558bv8s595shb9bbk5i3nf78ee
COGNITO_CLIENT_SECRET=1227lp5ksk4chn6q55lm2l067dq5ch9lurj0inm04b8s5hom8r6h

# データベース設定（AWS RDS）
DATABASE_HOST=programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com
DATABASE_PORT=3306
DATABASE_NAME=programming_learning_app
DATABASE_USER=admin
DATABASE_PASSWORD=ProgrammingApp2024!

# セキュリティ設定
SECRET_KEY=your-secret-key-change-in-production
```

### 3. データベースセットアップ

```bash
# RDSデータベースの初期化
python setup_rds_database.py

# サンプルデータの投入（RDS用）
python insert_sample_data_rds.py
```

### 4. アプリケーション起動

```bash
# 開発サーバーの起動
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 AWS 環境設定情報

### Cognito 設定

- **ユーザープール ID**: `ap-northeast-1_5SdJ4Iu5J`
- **クライアント ID**: `558bv8s595shb9bbk5i3nf78ee`
- **クライアントシークレット**: `1227lp5ksk4chn6q55lm2l067dq5ch9lurj0inm04b8s5hom8r6h`

### テストユーザー

- **ユーザー ID**: `37240af8-9041-701f-8eca-954b33eefe76`
- **メール**: `testuser@example.com`
- **パスワード**: `TestUser2024!`

### RDS 設定

- **エンドポイント**: `programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com`
- **ポート**: `3306`
- **ユーザー名**: `admin`
- **パスワード**: `ProgrammingApp2024!`
- **データベース名**: `programming_learning_app`
- **インスタンスクラス**: `db.t3.micro`
- **エンジンバージョン**: `MySQL 5.7.44`

## 🏗️ プロジェクト構成

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリケーションのエントリーポイント
│   ├── config.py            # 設定管理
│   ├── auth/                # 認証関連
│   │   ├── __init__.py
│   │   ├── cognito.py       # Cognito認証
│   │   └── middleware.py    # 認証ミドルウェア
│   ├── database/            # データベース関連
│   │   ├── __init__.py
│   │   ├── connection.py    # データベース接続
│   │   ├── operations.py    # データベース操作
│   │   ├── schema.py        # スキーマ定義
│   │   └── init_db.py       # データベース初期化
│   ├── models/              # データモデル
│   │   ├── __init__.py
│   │   ├── user.py          # ユーザーモデル
│   │   ├── exercise.py      # 演習モデル
│   │   └── progress.py      # 進捗モデル
│   ├── services/            # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── user_service.py  # ユーザーサービス
│   │   ├── exercise_service.py # 演習サービス
│   │   └── progress_service.py # 進捗サービス
│   └── api/                 # APIエンドポイント
│       ├── __init__.py
│       ├── auth.py          # 認証API
│       ├── users.py         # ユーザーAPI
│       ├── exercises.py     # 演習API
│       └── progress.py      # 進捗API
├── tests/                   # テストファイル
├── requirements.txt         # Python依存関係
├── setup_database.py        # ローカルDB初期化スクリプト
├── setup_rds_database.py    # RDS初期化スクリプト
├── insert_sample_data.py    # サンプルデータ投入スクリプト
├── DATABASE_SETUP.md        # データベースセットアップガイド
└── README.md               # このファイル
```

## 🔧 開発用コマンド

### データベース関連

```bash
# ローカルMySQLでの開発
python setup_database.py

# RDS環境での開発（データベースとテーブル作成）
python setup_rds_database.py

# サンプルデータの投入（ローカル用）
python insert_sample_data.py

# サンプルデータの投入（RDS用）
python insert_sample_data_rds.py
```

### テスト実行

```bash
# 全テストの実行
pytest

# カバレッジ付きテスト実行
pytest --cov=src

# 特定のテストファイルの実行
pytest tests/test_auth.py
```

### コード品質チェック

```bash
# コードフォーマット
black src/

# リンター実行
flake8 src/

# 型チェック
mypy src/
```

## 🌐 API エンドポイント

### 認証

- `POST /auth/login` - ユーザーログイン
- `POST /auth/refresh` - トークンリフレッシュ
- `POST /auth/logout` - ログアウト

### ユーザー

- `GET /users/me` - 現在のユーザー情報取得
- `PUT /users/me` - ユーザー情報更新

### 演習

- `GET /exercises` - 演習一覧取得
- `GET /exercises/{exercise_id}` - 特定の演習取得
- `POST /exercises/{exercise_id}/submit` - 演習の解答提出

### 進捗

- `GET /progress` - 学習進捗取得
- `GET /progress/{exercise_id}` - 特定演習の進捗取得

## 🔐 認証について

このアプリケーションは AWS Cognito を使用した認証システムを採用しています。

### 認証フロー

1. ユーザーがメールアドレスとパスワードでログイン
2. Cognito が JWT トークンを発行
3. API リクエスト時に Authorization ヘッダーでトークンを送信
4. バックエンドでトークンを検証

### テストユーザーでのログイン

```bash
# Cognitoテストユーザー
メール: testuser@example.com
パスワード: TestUser2024!
```

## 🗄️ データベース構成

### テーブル構造

#### users テーブル

- `id`: Cognito User ID (VARCHAR(36), PRIMARY KEY)
- `email`: メールアドレス (VARCHAR(255), UNIQUE)
- `username`: ユーザー名 (VARCHAR(50), UNIQUE)
- `created_at`: 作成日時 (TIMESTAMP)
- `updated_at`: 更新日時 (TIMESTAMP)

#### exercises テーブル

- `id`: 演習 ID (INT, AUTO_INCREMENT, PRIMARY KEY)
- `title`: 演習タイトル (VARCHAR(255))
- `description`: 演習説明 (TEXT)
- `difficulty`: 難易度 (ENUM: 'beginner', 'intermediate', 'advanced')
- `language`: プログラミング言語 (VARCHAR(50))
- `initial_code`: 初期コード (TEXT)
- `solution_code`: 解答コード (TEXT)
- `test_cases`: テストケース (JSON)
- `created_at`: 作成日時 (TIMESTAMP)
- `updated_at`: 更新日時 (TIMESTAMP)

#### progress テーブル

- `id`: 進捗 ID (INT, AUTO_INCREMENT, PRIMARY KEY)
- `user_id`: ユーザー ID (VARCHAR(36), FOREIGN KEY)
- `exercise_id`: 演習 ID (INT, FOREIGN KEY)
- `status`: ステータス (ENUM: 'not_started', 'in_progress', 'completed')
- `submitted_code`: 提出コード (TEXT)
- `score`: スコア (INT)
- `attempts`: 試行回数 (INT)
- `completed_at`: 完了日時 (TIMESTAMP)
- `created_at`: 作成日時 (TIMESTAMP)
- `updated_at`: 更新日時 (TIMESTAMP)

## 🚨 トラブルシューティング

### データベース接続エラー

1. RDS インスタンスが起動していることを確認
   ```bash
   aws rds describe-db-instances --db-instance-identifier programming-learning-app-db-v2 --region ap-northeast-1 --query 'DBInstances[0].DBInstanceStatus'
   ```
2. セキュリティグループでポート 3306 が開放されていることを確認
   ```bash
   aws ec2 describe-security-groups --group-ids sg-0941cbd3d9f8e741e --region ap-northeast-1 --query 'SecurityGroups[0].IpPermissions'
   ```
3. 接続情報（ホスト、ユーザー名、パスワード）が正しいことを確認
   - `.env` ファイルと `src/config.py` の設定を確認
4. パスワードをリセットする場合：
   ```bash
   aws rds modify-db-instance --db-instance-identifier programming-learning-app-db-v2 --master-user-password "ProgrammingApp2024!" --apply-immediately --region ap-northeast-1
   ```

### Cognito 認証エラー

1. ユーザープール ID とクライアント ID が正しいことを確認
2. AWS リージョンが正しく設定されていることを確認
3. ユーザーのステータスが`CONFIRMED`であることを確認

### 依存関係エラー

```bash
# 仮想環境を再作成
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 開発ガイドライン

### コーディング規約

- PEP 8 に準拠
- 型ヒントの使用を推奨
- docstring の記述を推奨

### コミット規約

- feat: 新機能
- fix: バグ修正
- docs: ドキュメント更新
- style: コードスタイル修正
- refactor: リファクタリング
- test: テスト追加・修正

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. [DATABASE_SETUP.md](./DATABASE_SETUP.md) - データベースセットアップの詳細
2. ログファイルの確認
3. AWS CloudWatch でのエラーログ確認

---

**開発者**: Programming Learning App Team
**最終更新**: 2025 年 10 月 13 日
