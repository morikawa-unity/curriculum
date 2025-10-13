# バックエンド構成

## フォルダ構成

```
backend/
├── setup/              # 初期セットアップスクリプト
│   ├── README.md
│   ├── setup_database.py          # ローカル環境セットアップ
│   ├── setup_rds_database.py      # RDS環境セットアップ
│   └── create_admin_user.py       # 管理者ユーザー作成
├── migrations/         # データベースマイグレーション
│   ├── README.md
│   └── 2024_01_15_add_role_column.py  # roleカラム追加
└── README.md          # このファイル
```

## 使用方法

### 新規環境構築

1. **ローカル環境の場合:**

   ```bash
   cd backend/setup
   python setup_database.py
   python create_admin_user.py
   ```

2. **RDS 環境の場合:**
   ```bash
   cd backend/setup
   python setup_rds_database.py
   python create_admin_user.py
   ```

### 既存環境のマイグレーション

```bash
cd backend/migrations
python 2024_01_15_add_role_column.py
```

その後、管理者ユーザーを作成：

```bash
cd backend/setup
python create_admin_user.py
```

## データベース構成

### users テーブル

- `id`: Cognito User ID (VARCHAR(36), PRIMARY KEY)
- `email`: メールアドレス (VARCHAR(255), UNIQUE)
- `username`: ユーザー名 (VARCHAR(50), UNIQUE)
- `role`: ユーザーロール (TINYINT, DEFAULT 2)
  - 1: 管理者
  - 2: 一般ユーザー
- `created_at`: 作成日時
- `updated_at`: 更新日時

### exercises テーブル

- 演習問題の管理

### progress テーブル

- ユーザーの学習進捗管理

## 管理者ログイン情報

管理者ユーザーが作成済みの場合、以下の情報でログインできます：

- **Email/Username**: `admin@programming-learning.com`
- **Password**: `AdminPass123!`
- **Role**: 管理者 (role=1)

> **注意**: 本番環境では必ずパスワードを変更してください。

## 環境設定

### 必要な設定

- MySQL/RDS 接続情報
- AWS 認証情報（Cognito 使用時）
- Cognito User Pool ID

### 依存関係

```bash
pip install pymysql boto3
```
