"""
AWS Cognito認証サービス
"""

import os
import json
import jwt
import requests
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import HTTPException, status
from pydantic import BaseModel


class CognitoUser(BaseModel):
    """Cognitoユーザー情報"""
    user_id: str
    email: str
    preferred_username: Optional[str] = None
    email_verified: bool = False
    token_use: str
    iss: str
    aud: str
    exp: int
    iat: int


class CognitoAuthService:
    """AWS Cognito認証サービス"""
    
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'ap-northeast-1')
        self.user_pool_id = os.getenv('USER_POOL_ID')
        self.user_pool_client_id = os.getenv('USER_POOL_CLIENT_ID')
        
        if not self.user_pool_id:
            raise ValueError("USER_POOL_ID environment variable is required")
        if not self.user_pool_client_id:
            raise ValueError("USER_POOL_CLIENT_ID environment variable is required")
        
        # JWKSエンドポイントURL
        self.jwks_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        
        # JWKSキャッシュ
        self._jwks_cache: Optional[Dict[str, Any]] = None
        self._jwks_cache_time: Optional[datetime] = None
        self._jwks_cache_ttl = 3600  # 1時間
    
    def _get_jwks(self) -> Dict[str, Any]:
        """JWKSを取得（キャッシュ付き）"""
        now = datetime.now(timezone.utc)
        
        # キャッシュが有効な場合は使用
        if (self._jwks_cache and 
            self._jwks_cache_time and 
            (now - self._jwks_cache_time).total_seconds() < self._jwks_cache_ttl):
            return self._jwks_cache
        
        try:
            response = requests.get(self.jwks_url, timeout=10)
            response.raise_for_status()
            
            self._jwks_cache = response.json()
            self._jwks_cache_time = now
            
            return self._jwks_cache
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"JWKSの取得に失敗しました: {str(e)}"
            )
    
    def _get_public_key(self, token_header: Dict[str, Any]) -> str:
        """JWTトークンのヘッダーから公開鍵を取得"""
        kid = token_header.get('kid')
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="トークンヘッダーにkidが含まれていません"
            )
        
        jwks = self._get_jwks()
        
        # 対応するキーを検索
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                # RSA公開鍵を構築
                return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="対応する公開鍵が見つかりません"
        )
    
    def verify_token(self, token: str) -> CognitoUser:
        """
        JWTトークンを検証してユーザー情報を返す
        
        Args:
            token: JWTトークン（Bearer プレフィックスなし）
            
        Returns:
            CognitoUser: 検証済みユーザー情報
            
        Raises:
            HTTPException: トークンが無効な場合
        """
        try:
            # トークンヘッダーをデコード（検証なし）
            unverified_header = jwt.get_unverified_header(token)
            
            # 公開鍵を取得
            public_key = self._get_public_key(unverified_header)
            
            # トークンを検証・デコード
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=self.user_pool_client_id,
                issuer=f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}"
            )
            
            # 必須フィールドの確認
            required_fields = ['sub', 'email', 'token_use', 'iss', 'aud', 'exp', 'iat']
            for field in required_fields:
                if field not in payload:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"トークンに必須フィールド '{field}' が含まれていません"
                    )
            
            # トークンタイプの確認（IDトークンまたはアクセストークン）
            token_use = payload.get('token_use')
            if token_use not in ['id', 'access']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="無効なトークンタイプです"
                )
            
            # ユーザー情報を構築
            return CognitoUser(
                user_id=payload['sub'],
                email=payload.get('email', ''),
                preferred_username=payload.get('preferred_username'),
                email_verified=payload.get('email_verified', False),
                token_use=token_use,
                iss=payload['iss'],
                aud=payload['aud'],
                exp=payload['exp'],
                iat=payload['iat']
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="トークンの有効期限が切れています"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"無効なトークンです: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"トークン検証中にエラーが発生しました: {str(e)}"
            )
    
    def verify_access_token(self, token: str) -> CognitoUser:
        """
        アクセストークンを検証
        
        Args:
            token: アクセストークン
            
        Returns:
            CognitoUser: 検証済みユーザー情報
        """
        user = self.verify_token(token)
        
        if user.token_use != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="アクセストークンが必要です"
            )
        
        return user
    
    def verify_id_token(self, token: str) -> CognitoUser:
        """
        IDトークンを検証
        
        Args:
            token: IDトークン
            
        Returns:
            CognitoUser: 検証済みユーザー情報
        """
        user = self.verify_token(token)
        
        if user.token_use != 'id':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="IDトークンが必要です"
            )
        
        return user


# シングルトンインスタンス
cognito_auth = CognitoAuthService()