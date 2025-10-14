"""
演習テーブルにcourseカラムを追加するマイグレーション
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
    """courseカラムを追加"""
    db_connection = get_db_connection()

    try:
        with db_connection.get_db_connection() as conn:
            with conn.cursor() as cursor:
                # courseカラムが存在するか確認
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'exercises'
                    AND COLUMN_NAME = 'course'
                """)
                result = cursor.fetchone()

                if result['count'] == 0:
                    logger.info("courseカラムを追加します...")

                    # courseカラムを追加
                    cursor.execute("""
                        ALTER TABLE exercises
                        ADD COLUMN course VARCHAR(50) NULL COMMENT 'コースID (例: php, python)' AFTER language,
                        ADD INDEX idx_course (course)
                    """)

                    conn.commit()
                    logger.info("✓ courseカラムの追加が完了しました")
                else:
                    logger.info("courseカラムは既に存在します")

    except Exception as e:
        logger.error(f"マイグレーションエラー: {str(e)}")
        raise


if __name__ == "__main__":
    migrate()
    logger.info("マイグレーション完了")
