"""
ユーザーモデル定義
Pydantic モデルとデータベーススキーマ
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """
    ユーザーの基本情報
    """
    email: EmailStr = Field(..., description="メールアドレス")
    username: str = Field(..., min_length=3, max_length=50, description="ユーザー名")

class UserCreate(UserBase):
    """
    ユーザー作成用モデル
    """
    id: str = Field(..., description="Cognito User ID")

class UserUpdate(BaseModel):
    """
    ユーザー更新用モデル
    """
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="ユーザー名")

class UserResponse(UserBase):
    """
    ユーザー情報レスポンス用モデル
    """
    id: str = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    class Config:
        from_attributes = True

class UserProfile(UserResponse):
    """
    ユーザープロフィール用モデル（統計情報含む）
    """
    total_exercises: int = Field(0, description="総演習数")
    completed_exercises: int = Field(0, description="完了演習数")
    total_score: int = Field(0, description="総スコア")
    completion_rate: float = Field(0.0, description="完了率")
    
    class Config:
        from_attributes = True