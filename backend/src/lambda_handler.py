"""
AWS Lambda ハンドラー
FastAPI アプリケーションを Lambda 関数として実行するためのエントリーポイント
"""

from mangum import Mangum
from src.main import app

# Lambda ハンドラー
handler = Mangum(app, lifespan="off")