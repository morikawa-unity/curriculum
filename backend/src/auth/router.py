"""
認証関連のAPIルーター
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from .dependencies import (
    get_current_user,
    get_current_user_optional,
    get_current_user_access_token,
    get_current_user_id_token,
    require_verified_email
)
from .cognito import CognitoUser


# レスポンスモデル
class UserResponse(BaseModel):
    """ユーザー情報レスポンス"""
    user_id: str
    email: str
    preferred_username: Optional[str] = None
    email_verified: bool
    token_use: str


class AuthStatusResponse(BaseModel):
    """認証状態レスポンス"""
    authenticated: bool
    user: Optional[UserResponse] = None


class TokenValidationResponse(BaseModel):
    """トークン検証レスポンス"""
    valid: bool
    user: Optional[UserResponse] = None
    error: Optional[str] = None


# ルーター作成
router = APIRouter(prefix="/auth", tags=["認証"])


def _user_to_response(user: CognitoUser) -> UserResponse:
    """CognitoUserをUserResponseに変換"""
    return UserResponse(
        user_id=user.user_id,
        email=user.email,
        preferred_username=user.preferred_username,
        email_verified=user.email_verified,
        token_use=user.token_use
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CognitoUser = Depends(get_current_user)):
    """
    現在のユーザー情報を取得
    
    認証が必要なエンドポイント
    """
    return _user_to_response(current_user)


@router.get("/status", response_model=AuthStatusResponse)
async def get_auth_status(current_user: Optional[CognitoUser] = Depends(get_current_user_optional)):
    """
    認証状態を確認
    
    認証はオプション
    """
    if current_user:
        return AuthStatusResponse(
            authenticated=True,
            user=_user_to_response(current_user)
        )
    else:
        return AuthStatusResponse(authenticated=False)


@router.post("/validate-token", response_model=TokenValidationResponse)
async def validate_token(current_user: Optional[CognitoUser] = Depends(get_current_user_optional)):
    """
    トークンの有効性を検証
    
    認証はオプション
    """
    if current_user:
        return TokenValidationResponse(
            valid=True,
            user=_user_to_response(current_user)
        )
    else:
        return TokenValidationResponse(
            valid=False,
            error="無効なトークンまたはトークンが提供されていません"
        )


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: CognitoUser = Depends(require_verified_email)):
    """
    ユーザープロフィールを取得
    
    メール確認済みユーザーのみアクセス可能
    """
    return _user_to_response(current_user)


@router.get("/access-token-info", response_model=UserResponse)
async def get_access_token_info(current_user: CognitoUser = Depends(get_current_user_access_token)):
    """
    アクセストークンの情報を取得
    
    アクセストークンが必要
    """
    return _user_to_response(current_user)


@router.get("/id-token-info", response_model=UserResponse)
async def get_id_token_info(current_user: CognitoUser = Depends(get_current_user_id_token)):
    """
    IDトークンの情報を取得
    
    IDトークンが必要
    """
    return _user_to_response(current_user)


# ヘルスチェック用エンドポイント
@router.get("/health")
async def health_check():
    """
    認証サービスのヘルスチェック
    """
    return {"status": "healthy", "service": "authentication"}