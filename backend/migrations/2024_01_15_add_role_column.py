#!/usr/bin/env python3
"""
usersテーブルにroleカラムを追加するマイグレーションスクリプト
1: 管理者, 2: 一般ユーザー
"""

import pymysql
import logging
from typing import Optional

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ローカル開発環境用設定
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'programming_learning_app',
    'charset': 'utf8mb4'
}

# RDS環境用設定
RDS_CONFIG = {
    'host': 'programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'ProgrammingApp2024!',
    'database': 'programming_learning_app',
    'charset': 'utf8mb4',
    'connect_timeout': 60,
    'read_timeout': 60,
    'write_timeout': 60
}

# roleカラム追加SQL
ADD_ROLE_COLUMN_SQL = """
ALTER TABLE users 
ADD COLUMN role TINYINT NOT NULL DEFAULT 2 COMMENT 'ユーザーロール: 1=管理者, 2=一般ユーザー' 
AFTER username;
"""

# roleカラムにインデックス追加
ADD_ROLE_INDEX_SQL = """
ALTER TABLE users ADD INDEX idx_role (role);
"""

def get_connection(use_rds: bool = False) -> Optional[pymysql.Connection]:
    """データベース接続を取得"""
    try:
        config = RDS_CONFIG if use_rds else LOCAL_DB_CONFIG
        connection = pymysql.connect(**config)
        logger.info(f"データベース接続成功: {config['host']}:{config['port']}")
        return connection
    except Exception as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        return None

def check_role_column_exists(connection: pymysql.Connection) -> bool:
    """roleカラムが既に存在するかチェック"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            for column in columns:
                if column[0] == 'role':
                    return True
            return False
    except Exception as e:
        logger.error(f"カラム確認エラー: {str(e)}")
        return False

def add_role_column(connection: pymysql.Connection) -> bool:
    """roleカラムを追加"""
    try:
        with connection.cursor() as cursor:
            # roleカラムが既に存在するかチェック
            if check_role_column_exists(connection):
                logger.info("roleカラムは既に存在します")
                return True
            
            # roleカラムを追加
            cursor.execute(ADD_ROLE_COLUMN_SQL)
            logger.info("roleカラムを追加しました")
            
            # インデックスを追加
            cursor.execute(ADD_ROLE_INDEX_SQL)
            logger.info("roleカラムにインデックスを追加しました")
            
            connection.commit()
            return True
    except Exception as e:
        logger.error(f"roleカラム追加エラー: {str(e)}")
        connection.rollback()
        return False

def show_table_structure(connection: pymysql.Connection):
    """テーブル構造を表示"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            
            logger.info("usersテーブル構造:")
            for column in columns:
                logger.info(f"  {column[0]} - {column[1]} - {column[2]} - {column[3]} - {column[4]} - {column[5]}")
    except Exception as e:
        logger.error(f"テーブル構造確認エラー: {str(e)}")

def main():
    """メイン処理"""
    print("=" * 60)
    print("usersテーブル roleカラム追加マイグレーション")
    print("=" * 60)
    
    # 環境選択
    env = input("\n環境を選択してください (1: ローカル, 2: RDS): ").strip()
    use_rds = env == "2"
    
    env_name = "RDS" if use_rds else "ローカル"
    print(f"\n{env_name}環境でマイグレーションを実行します...")
    
    # データベース接続
    connection = get_connection(use_rds)
    if not connection:
        print("✗ データベース接続失敗")
        return
    
    try:
        # 1. 現在のテーブル構造確認
        print("\n1. 現在のテーブル構造確認...")
        show_table_structure(connection)
        
        # 2. roleカラム追加
        print("\n2. roleカラム追加中...")
        if add_role_column(connection):
            print("✓ roleカラム追加完了")
        else:
            print("✗ roleカラム追加失敗")
            return
        
        # 3. 更新後のテーブル構造確認
        print("\n3. 更新後のテーブル構造確認...")
        show_table_structure(connection)
        
        print("\n" + "=" * 60)
        print("roleカラム追加マイグレーションが完了しました！")
        print("ロール定義:")
        print("  1: 管理者")
        print("  2: 一般ユーザー (デフォルト)")
        print("=" * 60)
        
    finally:
        connection.close()

if __name__ == "__main__":
    main()