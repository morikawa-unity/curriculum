# 一時的なスクリプト・ユーティリティ

このフォルダには、開発・テスト・デバッグ用の一時的なスクリプトが含まれています。

## ファイル一覧

### データベース関連

- **check_existing_users.py** - 既存ユーザーの確認
- **insert_sample_data.py** - ローカル環境用サンプルデータ挿入
- **insert_sample_data_rds.py** - RDS 環境用サンプルデータ挿入

### インフラ関連

- **create_rds_infrastructure.py** - RDS インフラ作成スクリプト

### テスト関連

- **test_auth.py** - 認証機能のテスト
- **test_rds_connection.py** - RDS 接続テスト
- **test_rds_passwords.py** - RDS パスワード関連テスト
- **test_profile_api.py** - プロフィール API 機能のテスト

### マイグレーション・チェック関連

- **check_and_migrate_achievements.py** - user_achievements テーブルの存在確認とマイグレーション実行

## 使用方法

各スクリプトは独立して実行できます：

```bash
cd backend/scripts
python check_existing_users.py
```

## 注意事項

- これらのスクリプトは一時的な用途のものです
- 本番環境での使用は推奨されません
- 実行前に内容を確認してください
- 必要に応じてバックアップを取得してください

## 整理について

不要になったスクリプトは定期的に削除してください。
重要なスクリプトは適切なフォルダ（setup/, migrations/）に移動することを検討してください。
