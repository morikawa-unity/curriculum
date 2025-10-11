"""
共通モデル定義
API レスポンスとエラーハンドリング用の共通モデル
"""

from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    """
    標準 API レスポンスモデル
    """
    success: bool = Field(True, description="成功フラグ")
    message: str = Field("", description="メッセージ")
    data: Optional[Any] = Field(None, description="レスポンスデータ")

class ErrorDetail(BaseModel):
    """
    エラー詳細情報
    """
    field: Optional[str] = Field(None, description="エラーが発生したフィールド")
    code: str = Field(..., description="エラーコード")
    message: str = Field(..., description="エラーメッセージ")

class ErrorResponse(BaseModel):
    """
    エラーレスポンスモデル
    """
    success: bool = Field(False, description="成功フラグ")
    error: ErrorDetail = Field(..., description="エラー情報")

class ValidationErrorResponse(BaseModel):
    """
    バリデーションエラーレスポンスモデル
    """
    success: bool = Field(False, description="成功フラグ")
    message: str = Field("バリデーションエラーが発生しました", description="メッセージ")
    errors: List[ErrorDetail] = Field(..., description="エラー詳細リスト")

class PaginationParams(BaseModel):
    """
    ページネーションパラメータ
    """
    page: int = Field(1, ge=1, description="ページ番号")
    limit: int = Field(20, ge=1, le=100, description="1ページあたりの件数")
    
    @property
    def offset(self) -> int:
        """オフセット値を計算"""
        return (self.page - 1) * self.limit

class PaginatedResponse(BaseModel):
    """
    ページネーション付きレスポンス
    """
    items: List[Any] = Field(..., description="データリスト")
    total: int = Field(..., description="総件数")
    page: int = Field(..., description="現在のページ")
    limit: int = Field(..., description="1ページあたりの件数")
    total_pages: int = Field(..., description="総ページ数")
    has_next: bool = Field(..., description="次のページが存在するか")
    has_prev: bool = Field(..., description="前のページが存在するか")

class HealthCheckResponse(BaseModel):
    """
    ヘルスチェックレスポンス
    """
    status: str = Field("healthy", description="ステータス")
    message: str = Field("API は正常に動作しています", description="メッセージ")
    timestamp: str = Field(..., description="チェック時刻")
    version: str = Field("1.0.0", description="APIバージョン")
    database_status: str = Field("connected", description="データベース接続状態")