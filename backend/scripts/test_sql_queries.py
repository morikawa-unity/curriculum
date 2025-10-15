#!/usr/bin/env python3
"""
生のSQLクエリ実行テストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.operations import get_db_operations
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_queries():
    """
    基本的なSQLクエリをテストする
    """
    print("=== 生のSQLクエリ実行テスト ===")
    
    try:
        db_ops = get_db_operations()
        
        # 1. データベース接続テスト
        print("\n1. データベース接続テスト")
        connection_test = db_ops.db_connection.test_connection()
        print(f"接続状態: {'成功' if connection_test else '失敗'}")
        
        if not connection_test:
            print("データベース接続に失敗しました。")
            return False
        
        # 2. テーブル一覧取得
        print("\n2. テーブル一覧取得")
        tables_query = "SHOW TABLES"
        tables = db_ops.execute_query(tables_query)
        print(f"テーブル数: {len(tables)}")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"  - {table_name}")
        
        # 3. usersテーブルの存在確認と構造確認
        print("\n3. usersテーブルの構造確認")
        if db_ops.check_table_exists('users'):
            print("✓ usersテーブルが存在します")
            
            # テーブル構造を取得
            describe_query = "DESCRIBE users"
            columns = db_ops.execute_query(describe_query)
            print("カラム構造:")
            for col in columns:
                print(f"  {col['Field']}: {col['Type']} ({col['Null']}) {col['Key']}")
            
            # レコード数を確認
            count_query = "SELECT COUNT(*) as count FROM users"
            count_result = db_ops.execute_query(count_query)
            user_count = count_result[0]['count'] if count_result else 0
            print(f"ユーザー数: {user_count}件")
            
            # サンプルユーザーを取得
            if user_count > 0:
                sample_query = "SELECT id, email, username, created_at FROM users LIMIT 3"
                sample_users = db_ops.execute_query(sample_query)
                print("サンプルユーザー:")
                for user in sample_users:
                    print(f"  {user['id']}: {user['email']} ({user['username']})")
        else:
            print("✗ usersテーブルが存在しません")
        
        # 4. user_achievementsテーブルの確認
        print("\n4. user_achievementsテーブルの確認")
        if db_ops.check_table_exists('user_achievements'):
            print("✓ user_achievementsテーブルが存在します")
            
            # レコード数を確認
            count_query = "SELECT COUNT(*) as count FROM user_achievements"
            count_result = db_ops.execute_query(count_query)
            achievement_count = count_result[0]['count'] if count_result else 0
            print(f"実績数: {achievement_count}件")
            
            # サンプル実績を取得
            if achievement_count > 0:
                sample_query = """
                    SELECT user_id, achievement_name, achievement_description, earned_date 
                    FROM user_achievements 
                    LIMIT 3
                """
                sample_achievements = db_ops.execute_query(sample_query)
                print("サンプル実績:")
                for achievement in sample_achievements:
                    print(f"  {achievement['user_id']}: {achievement['achievement_name']}")
        else:
            print("✗ user_achievementsテーブルが存在しません")
        
        # 5. exercise_progressテーブルの確認
        print("\n5. exercise_progressテーブルの確認")
        if db_ops.check_table_exists('exercise_progress'):
            print("✓ exercise_progressテーブルが存在します")
            
            # レコード数を確認
            count_query = "SELECT COUNT(*) as count FROM exercise_progress"
            count_result = db_ops.execute_query(count_query)
            progress_count = count_result[0]['count'] if count_result else 0
            print(f"進捗レコード数: {progress_count}件")
        else:
            print("✗ exercise_progressテーブルが存在しません（ダミーデータを使用）")
        
        # 6. プロフィールAPI用のクエリテスト
        print("\n6. プロフィールAPI用クエリテスト")
        if user_count > 0:
            # 最初のユーザーでテスト
            first_user_query = "SELECT id FROM users LIMIT 1"
            first_user = db_ops.execute_query(first_user_query)
            if first_user:
                user_id = first_user[0]['id']
                print(f"テストユーザーID: {user_id}")
                
                # ユーザー情報取得テスト
                user_info_query = "SELECT * FROM users WHERE id = %s"
                user_info = db_ops.execute_query(user_info_query, (user_id,))
                if user_info:
                    print("✓ ユーザー情報取得成功")
                    user_data = user_info[0]
                    print(f"  ユーザー名: {user_data['username']}")
                    print(f"  メール: {user_data['email']}")
                else:
                    print("✗ ユーザー情報取得失敗")
                
                # 実績情報取得テスト
                achievements_query = """
                    SELECT achievement_name, achievement_description, earned_date
                    FROM user_achievements 
                    WHERE user_id = %s
                    ORDER BY earned_date DESC
                """
                achievements = db_ops.execute_query(achievements_query, (user_id,))
                print(f"✓ 実績情報取得成功: {len(achievements)}件")
                
        print("\n=== テスト完了 ===")
        return True
        
    except Exception as e:
        print(f"✗ テスト中にエラーが発生しました: {e}")
        logger.error(f"SQLクエリテストエラー: {str(e)}")
        return False

if __name__ == '__main__':
    test_basic_queries()