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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザー情報テーブル';
"""

# 演習テーブルの CREATE 文
CREATE_EXERCISES_TABLE = """
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '演習ID',
    title VARCHAR(255) NOT NULL COMMENT '演習タイトル',
    description TEXT NOT NULL COMMENT '演習説明',
    difficulty ENUM('beginner', 'intermediate', 'advanced') NOT NULL COMMENT '難易度',
    language VARCHAR(50) NOT NULL COMMENT 'プログラミング言語',
    initial_code TEXT COMMENT '初期コード',
    solution_code TEXT COMMENT '解答コード',
    test_cases JSON COMMENT 'テストケース',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    INDEX idx_difficulty (difficulty),
    INDEX idx_language (language),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='演習問題テーブル';
"""

# 進捗テーブルの CREATE 文
CREATE_PROGRESS_TABLE = """
CREATE TABLE IF NOT EXISTS progress (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '進捗ID',
    user_id VARCHAR(36) NOT NULL COMMENT 'ユーザーID',
    exercise_id INT NOT NULL COMMENT '演習ID',
    status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started' COMMENT 'ステータス',
    submitted_code TEXT COMMENT '提出コード',
    score INT DEFAULT 0 COMMENT 'スコア',
    attempts INT DEFAULT 0 COMMENT '試行回数',
    completed_at TIMESTAMP NULL COMMENT '完了日時',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_exercise (user_id, exercise_id),
    INDEX idx_user_id (user_id),
    INDEX idx_exercise_id (exercise_id),
    INDEX idx_status (status),
    INDEX idx_completed_at (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学習進捗テーブル';
"""

# 全テーブル作成用の SQL 文リスト
CREATE_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_EXERCISES_TABLE,
    CREATE_PROGRESS_TABLE
]

# データベース初期化用の SQL 文
INIT_DATABASE = f"""
CREATE DATABASE IF NOT EXISTS programming_learning_app 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;
"""