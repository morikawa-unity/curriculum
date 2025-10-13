"""
アプリケーション設定管理
環境変数とデフォルト値の管理
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

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
    database_host: str = "programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com"
    database_port: int = 3306
    database_name: str = "programming_learning_app"
    database_user: str = "admin"
    database_password: str = "ProgrammingApp2024!"
    
    # AWS 設定
    aws_region: str = "ap-northeast-1"
    cognito_user_pool_id: Optional[str] = "ap-northeast-1_5SdJ4Iu5J"
    cognito_client_id: Optional[str] = "558bv8s595shb9bbk5i3nf78ee"
    
    # セキュリティ設定
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS 設定
    allowed_origins: str = "http://localhost:3000,https://localhost:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        """CORS許可オリジンをリストとして取得"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # 余分な環境変数を無視

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