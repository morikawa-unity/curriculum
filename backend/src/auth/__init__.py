"""
認証モジュール
"""

from .cognito import CognitoUser, CognitoAuthService, cognito_auth
from .dependencies import (
    get_current_user,
    get_current_user_optional,
    get_current_user_access_token,
    get_current_user_id_token,
    require_verified_email
)
from .router import router as auth_router

__all__ = [
    'CognitoUser',
    'CognitoAuthService',
    'cognito_auth',
    'get_current_user',
    'get_current_user_optional',
    'get_current_user_access_token',
    'get_current_user_id_token',
    'require_verified_email',
    'auth_router'
]