#!/usr/bin/env python3
"""
データベースセットアップスクリプト
ローカル開発環境でのデータベース初期化用
"""

import pymysql
import logging
from typing import Optional

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# データベース設定
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # ローカル環境のMySQLパスワード（必要に応じて変更）
    'charset': 'utf8mb4'
}

DATABASE_NAME = 'programming_learning_app'

# テーブル作成SQL
CREATE_DATABASE_SQL = f"""
CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;
"""

CREATE_USERS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {DATABASE_NAME}.users (
    id VARCHAR(36) PRIMARY KEY COMMENT 'Cognito User ID',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT 'メールアドレス',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT 'ユーザー名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザー情報テーブル';
"""

CREATE_EXERCISES_TABLE = f"""
CREATE TABLE IF NOT EXISTS {DATABASE_NAME}.exercises (
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

CREATE_PROGRESS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {DATABASE_NAME}.progress (
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
    FOREIGN KEY (user_id) REFERENCES {DATABASE_NAME}.users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES {DATABASE_NAME}.exercises(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_exercise (user_id, exercise_id),
    INDEX idx_user_id (user_id),
    INDEX idx_exercise_id (exercise_id),
    INDEX idx_status (status),
    INDEX idx_completed_at (completed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学習進捗テーブル';
"""

def get_connection(include_db: bool = False) -> Optional[pymysql.Connection]:
    """
    データベース接続を取得
    """
    try:
        config = DB_CONFIG.copy()
        if include_db:
            config['database'] = DATABASE_NAME
        
        connection = pymysql.connect(**config)
        logger.info(f"データベース接続成功: {config['host']}:{config['port']}")
        return connection
    except Exception as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        return None

def create_database():
    """
    データベースを作成
    """
    connection = get_connection(include_db=False)
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_DATABASE_SQL)
            connection.commit()
            logger.info(f"データベース '{DATABASE_NAME}' を作成しました")
        return True
    except Exception as e:
        logger.error(f"データベース作成エラー: {str(e)}")
        return False
    finally:
        connection.close()

def create_tables():
    """
    テーブルを作成
    """
    connection = get_connection(include_db=True)
    if not connection:
        return False
    
    tables = [
        ("users", CREATE_USERS_TABLE),
        ("exercises", CREATE_EXERCISES_TABLE),
        ("progress", CREATE_PROGRESS_TABLE)
    ]
    
    try:
        with connection.cursor() as cursor:
            for table_name, create_sql in tables:
                cursor.execute(create_sql)
                logger.info(f"テーブル '{table_name}' を作成しました")
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"テーブル作成エラー: {str(e)}")
        return False
    finally:
        connection.close()

def check_tables():
    """
    テーブルの存在確認
    """
    connection = get_connection(include_db=True)
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            logger.info("既存のテーブル:")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                logger.info(f"  - {table_name}: {count} レコード")
        return True
    except Exception as e:
        logger.error(f"テーブル確認エラー: {str(e)}")
        return False
    finally:
        connection.close()

def main():
    """
    メイン処理
    """
    print("=" * 50)
    print("プログラミング学習アプリ - データベースセットアップ")
    print("=" * 50)
    
    # 1. データベース作成
    print("\n1. データベース作成中...")
    if create_database():
        print("✓ データベース作成完了")
    else:
        print("✗ データベース作成失敗")
        return
    
    # 2. テーブル作成
    print("\n2. テーブル作成中...")
    if create_tables():
        print("✓ テーブル作成完了")
    else:
        print("✗ テーブル作成失敗")
        return
    
    # 3. テーブル確認
    print("\n3. テーブル確認中...")
    if check_tables():
        print("✓ テーブル確認完了")
    else:
        print("✗ テーブル確認失敗")
        return
    
    print("\n" + "=" * 50)
    print("データベースセットアップが完了しました！")
    print("=" * 50)

if __name__ == "__main__":
    main()