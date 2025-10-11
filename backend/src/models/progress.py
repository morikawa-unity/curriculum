"""
進捗モデル定義
Pydantic モデルとデータベーススキーマ
"""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class ProgressStatus(str, Enum):
    """
    進捗ステータス
    """
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ProgressBase(BaseModel):
    """
    進捗の基本情報
    """
    user_id: str = Field(..., description="ユーザーID")
    exercise_id: int = Field(..., description="演習ID")
    status: ProgressStatus = Field(ProgressStatus.NOT_STARTED, description="ステータス")
    submitted_code: Optional[str] = Field(None, description="提出コード")
    score: int = Field(0, ge=0, le=100, description="スコア（0-100）")
    attempts: int = Field(0, ge=0, description="試行回数")

class ProgressCreate(ProgressBase):
    """
    進捗作成用モデル
    """
    pass

class ProgressUpdate(BaseModel):
    """
    進捗更新用モデル
    """
    status: Optional[ProgressStatus] = Field(None, description="ステータス")
    submitted_code: Optional[str] = Field(None, description="提出コード")
    score: Optional[int] = Field(None, ge=0, le=100, description="スコア（0-100）")
    attempts: Optional[int] = Field(None, ge=0, description="試行回数")

class ProgressResponse(ProgressBase):
    """
    進捗情報レスポンス用モデル
    """
    id: int = Field(..., description="進捗ID")
    completed_at: Optional[datetime] = Field(None, description="完了日時")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    class Config:
        from_attributes = True

class ProgressWithExercise(ProgressResponse):
    """
    演習情報を含む進捗モデル
    """
    exercise_title: str = Field(..., description="演習タイトル")
    exercise_difficulty: str = Field(..., description="演習難易度")
    exercise_language: str = Field(..., description="プログラミング言語")
    
    class Config:
        from_attributes = True

class ProgressStats(BaseModel):
    """
    進捗統計モデル
    """
    total_exercises: int = Field(0, description="総演習数")
    completed_exercises: int = Field(0, description="完了演習数")
    in_progress_exercises: int = Field(0, description="進行中演習数")
    not_started_exercises: int = Field(0, description="未開始演習数")
    total_score: int = Field(0, description="総スコア")
    average_score: float = Field(0.0, description="平均スコア")
    completion_rate: float = Field(0.0, description="完了率")
    total_attempts: int = Field(0, description="総試行回数")
    
class UserProgressSummary(BaseModel):
    """
    ユーザー進捗サマリー
    """
    user_id: str = Field(..., description="ユーザーID")
    stats: ProgressStats = Field(..., description="統計情報")
    recent_activities: list[ProgressWithExercise] = Field(default_factory=list, description="最近のアクティビティ")
    
    class Config:
        from_attributes = True