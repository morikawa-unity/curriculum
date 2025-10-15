"""
ユーザー基本情報取得API
API ID: US0101001 - 現在のログインユーザー情報取得
"""

from fastapi import APIRouter, Depends, HTTPException, status
import logging

from src.auth.dependencies import get_current_user
from src.auth.cognito import CognitoUser
from src.models.user import UserResponse
from src.database.connection import get_db_connection

logger = logging.getLogger(__name__)

# ルーター作成
router = APIRouter(tags=["ユーザー"])


@router.get("/me", response_model=UserResponse)
async def US0101001(
    current_user: CognitoUser = Depends(get_current_user)
):
    """
    API ID: US0101001
    現在のログインユーザー情報取得API

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
        # データベース接続を取得
        db_connection = get_db_connection()

        # US0101001専用クエリ: ユーザー基本情報を取得
        user_query = """
            SELECT id, email, username, role, created_at, updated_at
            FROM users 
            WHERE id = %s
        """
        
        with db_connection.get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(user_query, (current_user.user_id,))
                user_result = cursor.fetchall()
        
        if not user_result:
            logger.warning(f"US0101001: ユーザーが見つかりません: {current_user.user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ユーザー情報が見つかりません"
            )

        user_data = user_result[0]
        logger.info(f"US0101001: ユーザー情報を取得しました: {current_user.user_id}")

        # UserResponseモデルに変換して返す
        return UserResponse(
            id=user_data["id"],
            email=user_data["email"],
            username=user_data["username"],
            role=user_data["role"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"]
        )

    except HTTPException:
        # HTTPExceptionはそのまま再スロー
        raise
    except Exception as e:
        logger.error(f"US0101001: ユーザー情報取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ユーザー情報の取得中にエラーが発生しました"
        )