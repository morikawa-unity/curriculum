"""
演習モデル定義
Pydantic モデルとデータベーススキーマ
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class DifficultyLevel(str, Enum):
    """
    演習の難易度レベル
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ProgrammingLanguage(str, Enum):
    """
    サポートするプログラミング言語
    """
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"

class TestCase(BaseModel):
    """
    テストケース定義
    """
    input: str = Field(..., description="入力データ")
    expected_output: str = Field(..., description="期待される出力")
    description: Optional[str] = Field(None, description="テストケースの説明")

class ExerciseBase(BaseModel):
    """
    演習の基本情報
    """
    title: str = Field(..., min_length=1, max_length=255, description="演習タイトル")
    description: str = Field(..., min_length=1, description="演習説明")
    difficulty: DifficultyLevel = Field(..., description="難易度")
    language: ProgrammingLanguage = Field(..., description="プログラミング言語")
    initial_code: Optional[str] = Field(None, description="初期コード")
    solution_code: Optional[str] = Field(None, description="解答コード")

class ExerciseCreate(ExerciseBase):
    """
    演習作成用モデル
    """
    test_cases: List[TestCase] = Field(default_factory=list, description="テストケース")

class ExerciseUpdate(BaseModel):
    """
    演習更新用モデル
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="演習タイトル")
    description: Optional[str] = Field(None, min_length=1, description="演習説明")
    difficulty: Optional[DifficultyLevel] = Field(None, description="難易度")
    language: Optional[ProgrammingLanguage] = Field(None, description="プログラミング言語")
    initial_code: Optional[str] = Field(None, description="初期コード")
    solution_code: Optional[str] = Field(None, description="解答コード")
    test_cases: Optional[List[TestCase]] = Field(None, description="テストケース")

class ExerciseResponse(ExerciseBase):
    """
    演習情報レスポンス用モデル
    """
    id: int = Field(..., description="演習ID")
    test_cases: List[TestCase] = Field(default_factory=list, description="テストケース")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    class Config:
        from_attributes = True

class ExerciseListItem(BaseModel):
    """
    演習一覧表示用モデル（簡略版）
    """
    id: int = Field(..., description="演習ID")
    title: str = Field(..., description="演習タイトル")
    difficulty: DifficultyLevel = Field(..., description="難易度")
    language: ProgrammingLanguage = Field(..., description="プログラミング言語")
    created_at: datetime = Field(..., description="作成日時")
    
    class Config:
        from_attributes = True

class CodeSubmission(BaseModel):
    """
    コード提出用モデル
    """
    exercise_id: int = Field(..., description="演習ID")
    code: str = Field(..., min_length=1, description="提出コード")
    
class CodeExecutionResult(BaseModel):
    """
    コード実行結果モデル
    """
    success: bool = Field(..., description="実行成功フラグ")
    output: str = Field(..., description="実行結果出力")
    error_message: Optional[str] = Field(None, description="エラーメッセージ")
    test_results: List[Dict[str, Any]] = Field(default_factory=list, description="テスト結果")
    score: int = Field(0, description="スコア")
    execution_time: float = Field(0.0, description="実行時間（秒）")