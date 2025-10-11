"""
データベース接続管理
MySQL データベースへの接続とコネクションプールの管理
"""

import pymysql
import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager
from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class DatabaseConnection:
    """
    データベース接続クラス
    MySQL への接続を管理し、コネクションプールを提供
    """
    
    def __init__(self):
        self.connection_params = {
            'host': settings.database_host,
            'port': settings.database_port,
            'user': settings.database_user,
            'password': settings.database_password,
            'database': settings.database_name,
            'charset': 'utf8mb4',
            'autocommit': False,
            'cursorclass': pymysql.cursors.DictCursor
        }
    
    def get_connection(self) -> pymysql.Connection:
        """
        新しいデータベース接続を取得
        """
        try:
            connection = pymysql.connect(**self.connection_params)
            logger.info("データベース接続が確立されました")
            return connection
        except Exception as e:
            logger.error(f"データベース接続エラー: {str(e)}")
            raise
    
    @contextmanager
    def get_db_connection(self):
        """
        コンテキストマネージャーとしてデータベース接続を提供
        自動的に接続のクローズを行う
        """
        connection = None
        try:
            connection = self.get_connection()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"データベース操作エラー: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
                logger.info("データベース接続をクローズしました")
    
    def test_connection(self) -> bool:
        """
        データベース接続をテスト
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logger.error(f"データベース接続テスト失敗: {str(e)}")
            return False

# グローバルデータベース接続インスタンス
db_connection = DatabaseConnection()

def get_db_connection():
    """
    データベース接続インスタンスを取得
    """
    return db_connection