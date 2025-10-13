"""
FastAPI認証依存関数
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .cognito import cognito_auth, CognitoUser


# HTTPベアラートークンスキーム
security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> CognitoUser:
    """
    現在のユーザーを取得（認証必須）
    
    Args:
        credentials: HTTPベアラートークン
        
    Returns:
        CognitoUser: 認証済みユーザー情報
        
    Raises:
        HTTPException: 認証に失敗した場合
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証トークンが必要です",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return cognito_auth.verify_token(credentials.credentials)


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[CognitoUser]:
    """
    現在のユーザーを取得（認証オプション）
    
    Args:
        credentials: HTTPベアラートークン
        
    Returns:
        Optional[CognitoUser]: 認証済みユーザー情報（認証されていない場合はNone）
    """
    if not credentials:
        return None
    
    try:
        return cognito_auth.verify_token(credentials.credentials)
    except HTTPException:
        return None


def get_current_user_access_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> CognitoUser:
    """
    アクセストークンから現在のユーザーを取得
    
    Args:
        credentials: HTTPベアラートークン
        
    Returns:
        CognitoUser: 認証済みユーザー情報
        
    Raises:
        HTTPException: 認証に失敗した場合
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="アクセストークンが必要です",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return cognito_auth.verify_access_token(credentials.credentials)


def get_current_user_id_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> CognitoUser:
    """
    IDトークンから現在のユーザーを取得
    
    Args:
        credentials: HTTPベアラートークン
        
    Returns:
        CognitoUser: 認証済みユーザー情報
        
    Raises:
        HTTPException: 認証に失敗した場合
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="IDトークンが必要です",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return cognito_auth.verify_id_token(credentials.credentials)


def require_verified_email(
    current_user: CognitoUser = Depends(get_current_user)
) -> CognitoUser:
    """
    メール確認済みユーザーのみ許可
    
    Args:
        current_user: 現在のユーザー
        
    Returns:
        CognitoUser: メール確認済みユーザー情報
        
    Raises:
        HTTPException: メールが未確認の場合
    """
    if not current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="メールアドレスの確認が必要です"
        )
    
    return current_user