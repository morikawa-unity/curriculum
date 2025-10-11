"""
カスタム例外クラス定義
アプリケーション固有のエラーハンドリング
"""

from typing import Optional, Dict, Any

class AppException(Exception):
    """
    アプリケーション基底例外クラス
    """
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationException(AppException):
    """
    バリデーションエラー例外
    """
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details or {}
        )
        self.field = field

class AuthenticationException(AppException):
    """
    認証エラー例外
    """
    def __init__(self, message: str = "認証が必要です", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=401,
            details=details or {}
        )

class AuthorizationException(AppException):
    """
    認可エラー例外
    """
    def __init__(self, message: str = "アクセス権限がありません", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=403,
            details=details or {}
        )

class NotFoundException(AppException):
    """
    リソース未発見例外
    """
    def __init__(self, message: str = "リソースが見つかりません", resource_type: Optional[str] = None, resource_id: Optional[str] = None):
        details = {}
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id
            
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details
        )

class ConflictException(AppException):
    """
    リソース競合例外
    """
    def __init__(self, message: str = "リソースが競合しています", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details=details or {}
        )

class DatabaseException(AppException):
    """
    データベースエラー例外
    """
    def __init__(self, message: str = "データベースエラーが発生しました", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details=details or {}
        )

class ExternalServiceException(AppException):
    """
    外部サービスエラー例外
    """
    def __init__(self, message: str = "外部サービスエラーが発生しました", service_name: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        exception_details = details or {}
        if service_name:
            exception_details["service_name"] = service_name
            
        super().__init__(
            message=message,
            code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
            details=exception_details
        )