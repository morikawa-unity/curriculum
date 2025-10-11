"""
エラーハンドラー定義
FastAPI アプリケーション用のグローバルエラーハンドラー
"""

import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from src.utils.exceptions import AppException
from src.models.common import ErrorResponse, ValidationErrorResponse, ErrorDetail

logger = logging.getLogger(__name__)

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    アプリケーション例外ハンドラー
    """
    logger.error(f"アプリケーションエラー: {exc.message} - {exc.details}")
    
    error_response = ErrorResponse(
        error=ErrorDetail(
            code=exc.code,
            message=exc.message
        )
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    HTTP 例外ハンドラー
    """
    logger.error(f"HTTP エラー: {exc.status_code} - {exc.detail}")
    
    error_response = ErrorResponse(
        error=ErrorDetail(
            code="HTTP_ERROR",
            message=str(exc.detail)
        )
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    バリデーション例外ハンドラー
    """
    logger.error(f"バリデーションエラー: {exc.errors()}")
    
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"]) if error.get("loc") else None
        errors.append(ErrorDetail(
            field=field,
            code="VALIDATION_ERROR",
            message=error["msg"]
        ))
    
    validation_response = ValidationErrorResponse(errors=errors)
    
    return JSONResponse(
        status_code=422,
        content=validation_response.dict()
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    一般例外ハンドラー
    """
    logger.error(f"予期しないエラー: {str(exc)}", exc_info=True)
    
    error_response = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="内部サーバーエラーが発生しました"
        )
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )

def register_error_handlers(app):
    """
    エラーハンドラーを FastAPI アプリケーションに登録
    """
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)