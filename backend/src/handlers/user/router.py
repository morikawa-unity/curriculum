"""
ユーザー関連のAPIルーター
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
import logging

from src.auth.dependencies import get_current_user
from src.auth.cognito import CognitoUser
from src.models.user import UserResponse
from src.database.operations import get_db_operations

logger = logging.getLogger(__name__)

# ルーター作成
router = APIRouter(prefix="/users", tags=["ユーザー"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CognitoUser = Depends(get_current_user)
):
    """
    現在のログインユーザーの情報をデータベースから取得

    認証が必要なエンドポイント
    JWTトークンからユーザーIDを取得し、データベースからユーザー情報を返す

    Args:
        current_user: 認証済みのCognitoユーザー情報

    Returns:
        UserResponse: データベースから取得したユーザー情報

    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    try:
        # データベース操作インスタンスを取得
        db_ops = get_db_operations()

        # Cognito User IDを使用してデータベースからユーザー情報を取得
        user_data = db_ops.get_record_by_id(
            table="users",
            record_id=current_user.user_id,
            id_column="id"
        )

        if not user_data:
            logger.warning(f"ユーザーが見つかりません: {current_user.user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ユーザー情報が見つかりません"
            )

        logger.info(f"ユーザー情報を取得しました: {current_user.user_id}")

        # UserResponseモデルに変換して返す
        return UserResponse(
            id=user_data["id"],
            email=user_data["email"],
            username=user_data["username"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"]
        )

    except HTTPException:
        # HTTPExceptionはそのまま再スロー
        raise
    except Exception as e:
        logger.error(f"ユーザー情報取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ユーザー情報の取得中にエラーが発生しました"
        )
