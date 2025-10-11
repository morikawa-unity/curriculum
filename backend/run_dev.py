#!/usr/bin/env python3
"""
開発サーバー起動スクリプト
ローカル開発環境での FastAPI サーバー起動
"""

import uvicorn
import logging
from src.main import app

if __name__ == "__main__":
    # ログレベル設定
    logging.basicConfig(level=logging.INFO)
    
    print("プログラミング学習アプリ API 開発サーバーを起動します...")
    print("API ドキュメント: http://localhost:8000/docs")
    print("ヘルスチェック: http://localhost:8000/health")
    print("=" * 50)
    
    # 開発サーバー起動
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # ファイル変更時の自動リロード
        log_level="info"
    )