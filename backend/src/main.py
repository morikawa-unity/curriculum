"""
FastAPI アプリケーションのメインエントリーポイント
プログラミング学習アプリのバックエンド API
"""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# 設定とルーターのインポート
from src.config import get_settings
from src.auth.router import router as auth_router
from src.handlers.exercise.router import exercise_router
from src.handlers.progress.router import progress_router
from src.handlers.user.router import router as user_router
from src.utils.error_handlers import register_error_handlers
from src.models.common import HealthCheckResponse
from src.database.connection import get_db_connection

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 設定取得
settings = get_settings()

# FastAPI アプリケーションの初期化
app = FastAPI(
    title="プログラミング学習アプリ API",
    description="プログラミング演習と進捗管理のための API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# エラーハンドラーの登録
register_error_handlers(app)

# API ルーターの登録
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(exercise_router, prefix="/api/v1")
app.include_router(progress_router, prefix="/api/v1")

# ヘルスチェックエンドポイント
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    アプリケーションの健全性をチェックするエンドポイント
    """
    # データベース接続テスト
    db_connection = get_db_connection()
    db_status = "connected" if db_connection.test_connection() else "disconnected"
    
    return HealthCheckResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        message="API は正常に動作しています" if db_status == "connected" else "データベース接続エラー",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        database_status=db_status
    )

# ルートエンドポイント
@app.get("/")
async def root():
    """
    API のルートエンドポイント
    """
    return {
        "message": "プログラミング学習アプリ API へようこそ",
        "version": "1.0.0",
        "docs": "/docs",
        "api_prefix": "/api/v1"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)