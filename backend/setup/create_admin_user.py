#!/usr/bin/env python3
"""
管理者ユーザーをCognitoとusersテーブルに作成するスクリプト
"""

import boto3
import pymysql
import uuid
import logging
from typing import Optional, Dict, Any

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# AWS Cognito設定
COGNITO_USER_POOL_ID = 'ap-northeast-1_5SdJ4Iu5J'
COGNITO_CLIENT_ID = 'your-client-id'  # Client IDは管理者作成には不要
AWS_REGION = 'ap-northeast-1'

# データベース設定
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'programming_learning_app',
    'charset': 'utf8mb4'
}

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

# 管理者ユーザー情報
ADMIN_USER = {
    'email': 'admin@programming-learning.com',
    'username': 'admin',  # データベース用の短いユーザー名
    'temporary_password': 'AdminPass123!',
    'role': 1  # 管理者
}

def get_cognito_client():
    """Cognitoクライアントを取得"""
    try:
        return boto3.client('cognito-idp', region_name=AWS_REGION)
    except Exception as e:
        logger.error(f"Cognitoクライアント作成エラー: {str(e)}")
        return None

def get_db_connection(use_rds: bool = False) -> Optional[pymysql.Connection]:
    """データベース接続を取得"""
    try:
        config = RDS_CONFIG if use_rds else LOCAL_DB_CONFIG
        connection = pymysql.connect(**config)
        logger.info(f"データベース接続成功: {config['host']}:{config['port']}")
        return connection
    except Exception as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        return None

def create_cognito_user(cognito_client, user_pool_id: str) -> Optional[str]:
    """Cognitoユーザーを作成"""
    try:
        # メールアドレスでユーザーが既に存在するかチェック
        try:
            response = cognito_client.admin_get_user(
                UserPoolId=user_pool_id,
                Username=ADMIN_USER['email']  # メールアドレスで検索
            )
            logger.info(f"Cognitoユーザー '{ADMIN_USER['email']}' は既に存在します")
            # 既存ユーザーのsubを取得
            for attr in response['UserAttributes']:
                if attr['Name'] == 'sub':
                    return attr['Value']
        except cognito_client.exceptions.UserNotFoundException:
            pass
        
        # 新しいユーザーを作成（メールアドレスをユーザー名として使用）
        response = cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=ADMIN_USER['email'],  # メールアドレスをユーザー名として使用
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': ADMIN_USER['email']
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
                {
                    'Name': 'name',
                    'Value': '管理者'
                }
            ],
            TemporaryPassword=ADMIN_USER['temporary_password'],
            MessageAction='SUPPRESS'  # ウェルカムメールを送信しない
        )
        
        # ユーザーのsubを取得
        user_sub = None
        for attr in response['User']['Attributes']:
            if attr['Name'] == 'sub':
                user_sub = attr['Value']
                break
        
        if user_sub:
            logger.info(f"Cognitoユーザー '{ADMIN_USER['email']}' を作成しました (sub: {user_sub})")
            
            # パスワードを永続化（初回ログイン時の強制変更を回避）
            try:
                cognito_client.admin_set_user_password(
                    UserPoolId=user_pool_id,
                    Username=ADMIN_USER['email'],  # メールアドレスを使用
                    Password=ADMIN_USER['temporary_password'],
                    Permanent=True
                )
                logger.info("管理者パスワードを永続化しました")
            except Exception as e:
                logger.warning(f"パスワード永続化エラー: {str(e)}")
            
            return user_sub
        else:
            logger.error("ユーザーのsubを取得できませんでした")
            return None
            
    except Exception as e:
        logger.error(f"Cognitoユーザー作成エラー: {str(e)}")
        return None

def create_db_user(connection: pymysql.Connection, user_sub: str) -> bool:
    """データベースにユーザーを作成"""
    try:
        with connection.cursor() as cursor:
            # ユーザーが既に存在するかチェック
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", (user_sub,))
            if cursor.fetchone()[0] > 0:
                logger.info(f"データベースユーザー 'admin' は既に存在します")
                return True
            
            # 新しいユーザーを挿入（データベースのusernameは短い形式を使用）
            sql = "INSERT INTO users (id, email, username, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (
                user_sub,
                ADMIN_USER['email'],
                ADMIN_USER['username'],  # 'admin'
                ADMIN_USER['role']
            ))
            connection.commit()
            logger.info(f"データベースユーザー '{ADMIN_USER['username']}' を作成しました")
            return True
            
    except Exception as e:
        logger.error(f"データベースユーザー作成エラー: {str(e)}")
        connection.rollback()
        return False

def verify_user_creation(connection: pymysql.Connection, user_sub: str):
    """ユーザー作成の確認"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, email, username, role, created_at FROM users WHERE id = %s",
                (user_sub,)
            )
            user = cursor.fetchone()
            
            if user:
                logger.info("作成されたユーザー情報:")
                logger.info(f"  ID: {user[0]}")
                logger.info(f"  Email: {user[1]}")
                logger.info(f"  Username: {user[2]}")
                logger.info(f"  Role: {user[3]} ({'管理者' if user[3] == 1 else '一般ユーザー'})")
                logger.info(f"  Created: {user[4]}")
            else:
                logger.error("ユーザーが見つかりません")
                
    except Exception as e:
        logger.error(f"ユーザー確認エラー: {str(e)}")

def main():
    """メイン処理"""
    print("=" * 60)
    print("管理者ユーザー作成スクリプト")
    print("=" * 60)
    
    print(f"\n作成する管理者ユーザー:")
    print(f"  Email: {ADMIN_USER['email']}")
    print(f"  Cognito Username: {ADMIN_USER['email']} (メールアドレス)")
    print(f"  DB Username: {ADMIN_USER['username']}")
    print(f"  Role: {ADMIN_USER['role']} (管理者)")
    print(f"  Temporary Password: {ADMIN_USER['temporary_password']}")
    
    # 確認
    confirm = input("\n上記の管理者ユーザーを作成しますか？ (y/N): ").strip().lower()
    if confirm != 'y':
        print("キャンセルしました")
        return
    
    # 環境選択
    env = input("\nデータベース環境を選択してください (1: ローカル, 2: RDS): ").strip()
    use_rds = env == "2"
    env_name = "RDS" if use_rds else "ローカル"
    
    # User Pool ID入力
    user_pool_id = input(f"\nCognito User Pool IDを入力してください [{COGNITO_USER_POOL_ID}]: ").strip()
    if not user_pool_id:
        user_pool_id = COGNITO_USER_POOL_ID
    
    print(f"\n{env_name}環境で管理者ユーザーを作成します...")
    
    # 1. Cognitoユーザー作成
    print("\n1. Cognitoユーザー作成中...")
    cognito_client = get_cognito_client()
    if not cognito_client:
        print("✗ Cognitoクライアント作成失敗")
        return
    
    user_sub = create_cognito_user(cognito_client, user_pool_id)
    if not user_sub:
        print("✗ Cognitoユーザー作成失敗")
        return
    
    print("✓ Cognitoユーザー作成完了")
    
    # 2. データベースユーザー作成
    print("\n2. データベースユーザー作成中...")
    connection = get_db_connection(use_rds)
    if not connection:
        print("✗ データベース接続失敗")
        return
    
    try:
        if create_db_user(connection, user_sub):
            print("✓ データベースユーザー作成完了")
        else:
            print("✗ データベースユーザー作成失敗")
            return
        
        # 3. ユーザー作成確認
        print("\n3. ユーザー作成確認...")
        verify_user_creation(connection, user_sub)
        
        print("\n" + "=" * 60)
        print("管理者ユーザー作成が完了しました！")
        print("\nログイン情報:")
        print(f"  Email/Username: {ADMIN_USER['email']}")
        print(f"  Password: {ADMIN_USER['temporary_password']}")
        print(f"  Role: 管理者")
        print("=" * 60)
        
    finally:
        connection.close()

if __name__ == "__main__":
    main()