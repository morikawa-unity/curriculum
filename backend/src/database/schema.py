"""
データベーススキーマ定義
テーブル作成用の SQL 文とスキーマ管理
"""

# ユーザーテーブルの CREATE 文
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY COMMENT 'Cognito User ID',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT 'メールアドレス',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT 'ユーザー名',
    role INT DEFAULT 0 COMMENT 'ユーザーロール (0: 一般, 1: 管理者)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザー情報テーブル';
"""

# 全テーブル作成用の SQL 文リスト
CREATE_TABLES = [
    CREATE_USERS_TABLE
]

# データベース初期化用の SQL 文
INIT_DATABASE = f"""
CREATE DATABASE IF NOT EXISTS programming_learning_app 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;
"""