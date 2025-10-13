#!/usr/bin/env python3
"""
既存ユーザーを確認するスクリプト
"""

import pymysql
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# RDS設定
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

def get_db_connection():
    """データベース接続を取得"""
    try:
        connection = pymysql.connect(**RDS_CONFIG)
        logger.info(f"データベース接続成功: {RDS_CONFIG['host']}:{RDS_CONFIG['port']}")
        return connection
    except Exception as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        return None

def check_existing_users():
    """既存ユーザーを確認"""
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        with connection.cursor() as cursor:
            # テーブル構造確認
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            
            print("=" * 60)
            print("usersテーブル構造:")
            print("=" * 60)
            for column in columns:
                print(f"  {column[0]} - {column[1]} - NULL:{column[2]} - KEY:{column[3]} - DEFAULT:{column[4]}")
            
            # 既存ユーザー確認
            cursor.execute("SELECT id, email, username, role, created_at FROM users")
            users = cursor.fetchall()
            
            print("\n" + "=" * 60)
            print("既存ユーザー:")
            print("=" * 60)
            if users:
                for user in users:
                    role_name = "管理者" if user[3] == 1 else "一般ユーザー"
                    print(f"ID: {user[0]}")
                    print(f"Email: {user[1]}")
                    print(f"Username: {user[2]}")
                    print(f"Role: {user[3]} ({role_name})")
                    print(f"Created: {user[4]}")
                    print("-" * 40)
            else:
                print("ユーザーが存在しません")
                
    except Exception as e:
        logger.error(f"ユーザー確認エラー: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    check_existing_users()