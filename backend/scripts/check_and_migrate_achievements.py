#!/usr/bin/env python3
"""
user_achievementsテーブルの存在確認とマイグレーション実行スクリプト
"""

import pymysql
import os
from dotenv import load_dotenv

def main():
    # 環境変数を読み込み
    load_dotenv()
    
    # データベース接続情報を取得
    db_config = {
        'host': os.getenv('DATABASE_HOST'),
        'port': int(os.getenv('DATABASE_PORT', 3306)),
        'database': os.getenv('DATABASE_NAME'),
        'user': os.getenv('DATABASE_USER'),
        'password': os.getenv('DATABASE_PASSWORD'),
        'charset': 'utf8mb4'
    }
    
    print("AWS RDS MySQLデータベースに接続中...")
    print(f"Host: {db_config['host']}")
    print(f"Database: {db_config['database']}")
    
    try:
        # データベースに接続
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # user_achievementsテーブルの存在確認
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_name = 'user_achievements'
        """, (db_config['database'],))
        
        table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            print('✓ user_achievementsテーブルは既に存在します')
            
            # テーブル構造を確認
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = 'user_achievements'
                ORDER BY ordinal_position
            """, (db_config['database'],))
            
            columns = cursor.fetchall()
            print('\nテーブル構造:')
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f'  {col[0]}: {col[1]} {nullable}{default}')
                
            # レコード数を確認
            cursor.execute('SELECT COUNT(*) FROM user_achievements')
            count = cursor.fetchone()[0]
            print(f'\n現在のレコード数: {count}件')
            
            if count > 0:
                # サンプルデータを表示
                cursor.execute("""
                    SELECT user_id, achievement_name, achievement_description, earned_date 
                    FROM user_achievements 
                    LIMIT 5
                """)
                sample_data = cursor.fetchall()
                print('\nサンプルデータ:')
                for row in sample_data:
                    print(f'  {row[0]}: {row[1]} - {row[2]} ({row[3]})')
            
        else:
            print('✗ user_achievementsテーブルが存在しません。マイグレーションを実行します...')
            
            # マイグレーションファイルを読み込み
            migration_file = '../migrations/004_create_user_achievements.sql'
            
            if not os.path.exists(migration_file):
                print(f'エラー: マイグレーションファイル {migration_file} が見つかりません')
                return
            
            with open(migration_file, 'r', encoding='utf-8') as f:
                migration_sql = f.read()
            
            # SQLを実行（複数のステートメントを分割して実行）
            statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        print(f'✓ 実行完了: {statement[:50]}...')
                    except Exception as e:
                        print(f'✗ エラー: {statement[:50]}... - {e}')
            
            # 変更をコミット
            connection.commit()
            print('\n✓ マイグレーションが完了しました')
            
            # 作成されたテーブルを確認
            cursor.execute('SELECT COUNT(*) FROM user_achievements')
            count = cursor.fetchone()[0]
            print(f'作成後のレコード数: {count}件')
        
        cursor.close()
        connection.close()
        print('\nデータベース接続を閉じました')
        
    except Exception as e:
        print(f'エラー: {e}')
        return False
    
    return True

if __name__ == '__main__':
    main()