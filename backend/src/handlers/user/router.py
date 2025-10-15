"""
ユーザー関連のAPIルーター
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
import logging


from .US0101001 import router as us0101001_router
from .PR0101001 import router as pr0101001_router

logger = logging.getLogger(__name__)

# ルーター作成
router = APIRouter(prefix="/users", tags=["ユーザー"])

# API別ルーターを追加
router.include_router(us0101001_router)
router.include_router(pr0101001_router)



