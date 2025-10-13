# セットアップスクリプト

このフォルダには、データベースの初期セットアップとユーザー作成に関するスクリプトが含まれています。

## ファイル一覧

### setup_database.py

ローカル開発環境用のデータベースセットアップスクリプト

**使用方法:**

```bash
cd backend/setup
python setup_database.py
```

**機能:**

- データベース作成
- テーブル作成（users, exercises, progress）
- テーブル確認

### setup_rds_database.py

AWS RDS 環境用のデータベースセットアップスクリプト

**使用方法:**

```bash
cd backend/setup
python setup_rds_database.py
```

**機能:**

- RDS データベース作成
- テーブル作成（users, exercises, progress）
- テストユーザー挿入
- テーブル確認

### create_admin_user.py

管理者ユーザーを Cognito とデータベースに作成するスクリプト

**使用方法:**

```bash
cd backend/setup
python create_admin_user.py
```

**機能:**

- Cognito ユーザー作成
- データベースに管理者ユーザー追加（role=1）
- ユーザー作成確認

**注意事項:**

- AWS 認証情報が設定されている必要があります
- Cognito User Pool ID を正しく設定してください

## 実行順序

新規環境の場合：

1. `setup_database.py` または `setup_rds_database.py`
2. `create_admin_user.py`

既存環境で role カラムを追加する場合：

1. `../migrations/add_role_column.py`
2. `create_admin_user.py`

## 管理者ログイン情報

`create_admin_user.py`実行後、以下の情報で管理者としてログインできます：

- **Email/Username**: `admin@programming-learning.com`
- **Password**: `AdminPass123!`
- **Role**: 管理者 (role=1)

> **セキュリティ注意事項**:
>
> - 本番環境では必ずパスワードを変更してください
> - 管理者アカウントの使用は必要最小限に留めてください
> - 定期的にパスワードを更新してください
