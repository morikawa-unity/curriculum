"""
データベース初期化スクリプト
開発環境でのデータベースセットアップ用
"""

import logging
from src.database.operations import get_db_operations
from src.config import get_settings

logger = logging.getLogger(__name__)

def initialize_database():
    """
    データベースとテーブルを初期化
    """
    try:
        settings = get_settings()
        logger.info(f"データベース初期化を開始します: {settings.database_name}")
        
        db_ops = get_db_operations()
        success = db_ops.initialize_database()
        
        if success:
            logger.info("データベース初期化が完了しました")
            return True
        else:
            logger.error("データベース初期化に失敗しました")
            return False
            
    except Exception as e:
        logger.error(f"データベース初期化エラー: {str(e)}")
        return False

def check_database_status():
    """
    データベースの状態をチェック
    """
    try:
        db_ops = get_db_operations()
        
        # テーブルの存在確認
        tables = ["users", "exercises", "progress"]
        for table in tables:
            exists = db_ops.check_table_exists(table)
            logger.info(f"テーブル {table}: {'存在' if exists else '未作成'}")
        
        return True
    except Exception as e:
        logger.error(f"データベース状態チェックエラー: {str(e)}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("データベース初期化スクリプト")
    print("=" * 40)
    
    # データベース状態チェック
    print("1. データベース状態チェック")
    check_database_status()
    
    # データベース初期化
    print("\n2. データベース初期化")
    if initialize_database():
        print("✓ データベース初期化が完了しました")
    else:
        print("✗ データベース初期化に失敗しました")
    
    # 初期化後の状態チェック
    print("\n3. 初期化後の状態チェック")
    check_database_status()