"""
不要なテーブルを削除するマイグレーション
exercises, progress, user_achievements テーブルを削除
日付: 2025-01-15
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    """不要なテーブルを削除"""
    db_connection = get_db_connection()

    tables_to_drop = ['user_achievements', 'progress', 'exercises']

    try:
        with db_connection.get_db_connection() as conn:
            with conn.cursor() as cursor:
                for table in tables_to_drop:
                    # テーブルが存在するか確認
                    cursor.execute("""
                        SELECT COUNT(*) as count
                        FROM information_schema.TABLES
                        WHERE TABLE_SCHEMA = DATABASE()
                        AND TABLE_NAME = %s
                    """, (table,))
                    result = cursor.fetchone()

                    if result['count'] > 0:
                        logger.info(f"テーブル '{table}' を削除します...")
                        cursor.execute(f"DROP TABLE IF EXISTS {table}")
                        logger.info(f"✓ テーブル '{table}' を削除しました")
                    else:
                        logger.info(f"テーブル '{table}' は存在しません（スキップ）")

                conn.commit()
                logger.info("すべての不要なテーブルの削除が完了しました")

    except Exception as e:
        logger.error(f"マイグレーションエラー: {str(e)}")
        raise


if __name__ == "__main__":
    migrate()
    logger.info("マイグレーション完了")
