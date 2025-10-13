#!/usr/bin/env python3
"""
RDSデータベース接続テストスクリプト
異なるパスワードで接続をテスト
"""

import pymysql
import sys

RDS_HOST = 'programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com'
RDS_PORT = 3306
RDS_USER = 'admin'

# テストするパスワード
PASSWORDS = [
    'ProgrammingApp2024!',
    'SimplePass123!'
]

def test_connection(password: str) -> bool:
    """指定されたパスワードで接続をテスト"""
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=password,
            connect_timeout=10
        )
        connection.close()
        return True
    except Exception as e:
        print(f"  エラー: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("RDS接続テスト")
    print("=" * 60)
    print(f"\nホスト: {RDS_HOST}")
    print(f"ユーザー: {RDS_USER}")
    print()

    for i, password in enumerate(PASSWORDS, 1):
        print(f"{i}. パスワード '{password}' をテスト中...")
        if test_connection(password):
            print(f"   ✓ 接続成功！正しいパスワード: {password}")
            return password
        else:
            print(f"   ✗ 接続失敗")

    print("\nすべてのパスワードで接続に失敗しました")
    return None

if __name__ == "__main__":
    correct_password = main()
    if correct_password:
        sys.exit(0)
    else:
        sys.exit(1)
