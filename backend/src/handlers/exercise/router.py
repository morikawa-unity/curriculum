"""
演習関連 API ルーター
演習の取得、作成、更新、削除、コード実行
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from src.models.exercise import (
    ExerciseCreate, ExerciseResponse, ExerciseUpdate, ExerciseListItem,
    CodeSubmission, CodeExecutionResult, DifficultyLevel, ProgrammingLanguage
)
from src.models.common import APIResponse, ErrorResponse, PaginationParams, PaginatedResponse

# 演習ルーター
exercise_router = APIRouter(
    prefix="/exercises",
    tags=["演習"],
    responses={
        404: {"model": ErrorResponse, "description": "リソースが見つかりません"},
        500: {"model": ErrorResponse, "description": "内部サーバーエラー"}
    }
)

@exercise_router.get("/", response_model=PaginatedResponse, summary="演習一覧取得")
async def get_exercises(
    page: int = Query(1, ge=1, description="ページ番号"),
    limit: int = Query(20, ge=1, le=100, description="1ページあたりの件数"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="難易度フィルター"),
    language: Optional[ProgrammingLanguage] = Query(None, description="言語フィルター")
):
    """
    演習一覧を取得します
    
    - **page**: ページ番号
    - **limit**: 1ページあたりの件数
    - **difficulty**: 難易度フィルター（オプション）
    - **language**: プログラミング言語フィルター（オプション）
    """
    try:
        # TODO: 実際の演習一覧取得ロジックを実装
        return PaginatedResponse(
            items=[],
            total=0,
            page=page,
            limit=limit,
            total_pages=0,
            has_next=False,
            has_prev=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"演習一覧取得エラー: {str(e)}")

@exercise_router.get("/{exercise_id}", response_model=ExerciseResponse, summary="演習詳細取得")
async def get_exercise(exercise_id: int):
    """
    指定された演習の詳細情報を取得します
    
    - **exercise_id**: 演習ID
    """
    try:
        # TODO: 実際の演習詳細取得ロジックを実装
        raise HTTPException(status_code=501, detail="実装予定の機能です")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"演習詳細取得エラー: {str(e)}")

@exercise_router.post("/", response_model=APIResponse, summary="演習作成")
async def create_exercise(exercise_data: ExerciseCreate):
    """
    新しい演習を作成します
    
    - **exercise_data**: 演習データ
    """
    try:
        # TODO: 実際の演習作成ロジックを実装
        return APIResponse(
            success=True,
            message="演習が作成されました",
            data={"exercise_id": 1}  # 仮のID
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"演習作成エラー: {str(e)}")

@exercise_router.put("/{exercise_id}", response_model=APIResponse, summary="演習更新")
async def update_exercise(exercise_id: int, exercise_data: ExerciseUpdate):
    """
    演習情報を更新します
    
    - **exercise_id**: 演習ID
    - **exercise_data**: 更新する演習データ
    """
    try:
        # TODO: 実際の演習更新ロジックを実装
        return APIResponse(
            success=True,
            message="演習が更新されました",
            data={"exercise_id": exercise_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"演習更新エラー: {str(e)}")

@exercise_router.delete("/{exercise_id}", response_model=APIResponse, summary="演習削除")
async def delete_exercise(exercise_id: int):
    """
    演習を削除します
    
    - **exercise_id**: 演習ID
    """
    try:
        # TODO: 実際の演習削除ロジックを実装
        return APIResponse(
            success=True,
            message="演習が削除されました",
            data={"exercise_id": exercise_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"演習削除エラー: {str(e)}")

@exercise_router.post("/submit", response_model=CodeExecutionResult, summary="コード提出・実行")
async def submit_code(submission: CodeSubmission):
    """
    コードを提出して実行します
    
    - **submission**: コード提出データ
    """
    try:
        # TODO: 実際のコード実行ロジックを実装
        return CodeExecutionResult(
            success=True,
            output="実行結果（実装予定）",
            test_results=[],
            score=0,
            execution_time=0.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"コード実行エラー: {str(e)}")