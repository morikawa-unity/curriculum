#!/usr/bin/env python3
"""
RDS接続テストスクリプト
異なる方法でRDS接続をテスト
"""

import pymysql
import MySQLdb
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RDS接続設定
RDS_CONFIG = {
    'host': 'programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'ProgrammingApp2024!',
    'charset': 'utf8mb4'
}

def test_pymysql_connection():
    """PyMySQLでの接続テスト"""
    try:
        logger.info("PyMySQLでの接続テスト開始...")
        connection = pymysql.connect(**RDS_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            logger.info(f"PyMySQL接続成功! MySQL Version: {version[0]}")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"PyMySQL接続エラー: {str(e)}")
        return False

def test_mysqlclient_connection():
    """MySQLclientでの接続テスト"""
    try:
        logger.info("MySQLclientでの接続テスト開始...")
        connection = MySQLdb.connect(**RDS_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        logger.info(f"MySQLclient接続成功! MySQL Version: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        logger.error(f"MySQLclient接続エラー: {str(e)}")
        return False

def test_pymysql_with_auth_plugin():
    """PyMySQLで認証プラグインを指定した接続テスト"""
    try:
        logger.info("PyMySQL（認証プラグイン指定）での接続テスト開始...")
        config = RDS_CONFIG.copy()
        config['auth_plugin_map'] = {
            'mysql_native_password': '',
            'caching_sha2_password': ''
        }
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            logger.info(f"PyMySQL（認証プラグイン指定）接続成功! MySQL Version: {version[0]}")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"PyMySQL（認証プラグイン指定）接続エラー: {str(e)}")
        return False

def main():
    """メイン処理"""
    print("=" * 60)
    print("RDS接続テスト")
    print("=" * 60)
    
    results = []
    
    # 1. PyMySQL接続テスト
    print("\n1. PyMySQL接続テスト")
    results.append(("PyMySQL", test_pymysql_connection()))
    
    # 2. MySQLclient接続テスト
    print("\n2. MySQLclient接続テスト")
    results.append(("MySQLclient", test_mysqlclient_connection()))
    
    # 3. PyMySQL（認証プラグイン指定）接続テスト
    print("\n3. PyMySQL（認証プラグイン指定）接続テスト")
    results.append(("PyMySQL（認証プラグイン指定）", test_pymysql_with_auth_plugin()))
    
    # 結果表示
    print("\n" + "=" * 60)
    print("接続テスト結果:")
    for method, success in results:
        status = "✓ 成功" if success else "✗ 失敗"
        print(f"  {method}: {status}")
    
    # 成功した方法があるかチェック
    successful_methods = [method for method, success in results if success]
    if successful_methods:
        print(f"\n推奨接続方法: {successful_methods[0]}")
    else:
        print("\nすべての接続方法が失敗しました。")
        print("以下を確認してください:")
        print("- RDSインスタンスが利用可能な状態か")
        print("- セキュリティグループの設定")
        print("- パスワードが正しいか")
    
    print("=" * 60)

if __name__ == "__main__":
    main()