"""
データベース操作ヘルパー関数
CRUD 操作とデータベース管理機能
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from src.database.connection import get_db_connection
from src.database.schema import CREATE_TABLES, INIT_DATABASE

logger = logging.getLogger(__name__)

class DatabaseOperations:
    """
    データベース操作クラス
    基本的な CRUD 操作とスキーマ管理を提供
    """
    
    def __init__(self):
        self.db_connection = get_db_connection()
    
    def initialize_database(self) -> bool:
        """
        データベースとテーブルを初期化
        """
        try:
            with self.db_connection.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # データベース作成（存在しない場合）
                    cursor.execute(INIT_DATABASE)
                    logger.info("データベースの初期化が完了しました")
                    
                    # テーブル作成
                    for create_sql in CREATE_TABLES:
                        cursor.execute(create_sql)
                        logger.info("テーブルが作成されました")
                    
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"データベース初期化エラー: {str(e)}")
            return False
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        SELECT クエリを実行して結果を返す
        """
        try:
            with self.db_connection.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                    results = cursor.fetchall()
                    logger.info(f"クエリ実行成功: {len(results)} 件の結果")
                    return results
        except Exception as e:
            logger.error(f"クエリ実行エラー: {str(e)}")
            raise
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """
        INSERT/UPDATE/DELETE クエリを実行して影響を受けた行数を返す
        """
        try:
            with self.db_connection.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    affected_rows = cursor.execute(query, params or ())
                    conn.commit()
                    logger.info(f"更新クエリ実行成功: {affected_rows} 行が影響を受けました")
                    return affected_rows
        except Exception as e:
            logger.error(f"更新クエリ実行エラー: {str(e)}")
            raise
    
    def insert_record(self, table: str, data: Dict[str, Any]) -> int:
        """
        レコードを挿入して新しい ID を返す
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with self.db_connection.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(data.values()))
                    new_id = cursor.lastrowid
                    conn.commit()
                    logger.info(f"レコード挿入成功: テーブル {table}, ID {new_id}")
                    return new_id
        except Exception as e:
            logger.error(f"レコード挿入エラー: {str(e)}")
            raise
    
    def update_record(self, table: str, data: Dict[str, Any], where_clause: str, where_params: Tuple) -> int:
        """
        レコードを更新して影響を受けた行数を返す
        """
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            params = tuple(data.values()) + where_params
            
            return self.execute_update(query, params)
        except Exception as e:
            logger.error(f"レコード更新エラー: {str(e)}")
            raise
    
    def delete_record(self, table: str, where_clause: str, where_params: Tuple) -> int:
        """
        レコードを削除して影響を受けた行数を返す
        """
        try:
            query = f"DELETE FROM {table} WHERE {where_clause}"
            return self.execute_update(query, where_params)
        except Exception as e:
            logger.error(f"レコード削除エラー: {str(e)}")
            raise
    
    def get_record_by_id(self, table: str, record_id: Any, id_column: str = 'id') -> Optional[Dict[str, Any]]:
        """
        ID でレコードを取得
        """
        try:
            query = f"SELECT * FROM {table} WHERE {id_column} = %s"
            results = self.execute_query(query, (record_id,))
            return results[0] if results else None
        except Exception as e:
            logger.error(f"レコード取得エラー: {str(e)}")
            raise
    
    def check_table_exists(self, table_name: str) -> bool:
        """
        テーブルの存在確認
        """
        try:
            query = """
            SELECT COUNT(*) as count 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() AND table_name = %s
            """
            results = self.execute_query(query, (table_name,))
            return results[0]['count'] > 0 if results else False
        except Exception as e:
            logger.error(f"テーブル存在確認エラー: {str(e)}")
            return False

# グローバルデータベース操作インスタンス
db_operations = DatabaseOperations()

def get_db_operations() -> DatabaseOperations:
    """
    データベース操作インスタンスを取得
    """
    return db_operations