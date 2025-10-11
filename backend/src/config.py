"""
アプリケーション設定管理
環境変数とデフォルト値の管理
"""

import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    アプリケーション設定クラス
    環境変数から設定を読み込み、デフォルト値を提供
    """
    
    # アプリケーション設定
    app_name: str = "プログラミング学習アプリ API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # データベース設定
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "programming_learning_app"
    database_user: str = "root"
    database_password: str = ""
    
    # AWS 設定
    aws_region: str = "ap-northeast-1"
    cognito_user_pool_id: Optional[str] = None
    cognito_client_id: Optional[str] = None
    
    # セキュリティ設定
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS 設定
    allowed_origins: list = ["http://localhost:3000", "https://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# グローバル設定インスタンス
settings = Settings()

def get_database_url() -> str:
    """
    データベース接続 URL を生成
    """
    return f"mysql+pymysql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

def get_settings() -> Settings:
    """
    設定インスタンスを取得
    """
    return settings