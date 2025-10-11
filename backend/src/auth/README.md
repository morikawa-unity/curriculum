# 認証モジュール

このモジュールは、AWS Cognito を使用した JWT 認証機能を提供します。

## 概要

- **認証方式**: AWS Cognito JWT トークン
- **トークンタイプ**: ID トークン、アクセストークン
- **検証方式**: JWKS を使用した RSA 署名検証

## ファイル構成

```
auth/
├── __init__.py          # モジュール初期化
├── cognito.py           # Cognito認証サービス
├── dependencies.py      # FastAPI依存関数
├── router.py           # APIルーター
└── README.md           # このファイル
```

## 主要コンポーネント

### CognitoAuthService

AWS Cognito との連携を行うメインサービスクラス。

**主要機能:**

- JWT トークンの検証
- JWKS の取得とキャッシュ
- ユーザー情報の抽出

**メソッド:**

- `verify_token(token: str)`: 汎用トークン検証
- `verify_access_token(token: str)`: アクセストークン検証
- `verify_id_token(token: str)`: ID トークン検証

### 依存関数

FastAPI で使用する認証依存関数。

**利用可能な依存関数:**

- `get_current_user`: 認証必須
- `get_current_user_optional`: 認証オプション
- `get_current_user_access_token`: アクセストークン必須
- `get_current_user_id_token`: ID トークン必須
- `require_verified_email`: メール確認済みユーザー必須

### API エンドポイント

認証関連の API エンドポイントを提供。

**エンドポイント一覧:**

- `GET /auth/me`: 現在のユーザー情報
- `GET /auth/status`: 認証状態確認
- `POST /auth/validate-token`: トークン検証
- `GET /auth/profile`: プロフィール（メール確認必須）
- `GET /auth/access-token-info`: アクセストークン情報
- `GET /auth/id-token-info`: ID トークン情報
- `GET /auth/health`: ヘルスチェック

## 使用方法

### 基本的な認証

```python
from fastapi import Depends
from src.auth import get_current_user, CognitoUser

@app.get("/protected")
async def protected_endpoint(current_user: CognitoUser = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "email": current_user.email}
```

### オプション認証

```python
from fastapi import Depends
from typing import Optional
from src.auth import get_current_user_optional, CognitoUser

@app.get("/optional-auth")
async def optional_auth_endpoint(current_user: Optional[CognitoUser] = Depends(get_current_user_optional)):
    if current_user:
        return {"authenticated": True, "user_id": current_user.user_id}
    else:
        return {"authenticated": False}
```

### メール確認必須

```python
from fastapi import Depends
from src.auth import require_verified_email, CognitoUser

@app.get("/verified-only")
async def verified_only_endpoint(current_user: CognitoUser = Depends(require_verified_email)):
    return {"message": "メール確認済みユーザーのみアクセス可能"}
```

## 環境変数

以下の環境変数が必要です：

```bash
# AWS設定
AWS_REGION=ap-northeast-1
USER_POOL_ID=ap-northeast-1_xxxxxxxxx
USER_POOL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

## エラーハンドリング

認証エラーは適切な HTTP ステータスコードとメッセージで返されます：

- `401 Unauthorized`: 認証失敗、トークン無効
- `403 Forbidden`: 権限不足（メール未確認など）
- `503 Service Unavailable`: JWKS の取得失敗

## セキュリティ考慮事項

1. **JWKS キャッシュ**: 1 時間の TTL でキャッシュし、パフォーマンスを向上
2. **トークン検証**: 署名、有効期限、発行者を厳密に検証
3. **エラー情報**: セキュリティ上重要な情報は漏洩しないよう配慮

## テスト

認証機能のテストは以下のコマンドで実行できます：

```bash
# 基本テスト
python backend/test_auth.py

# FastAPIサーバーを起動してからAPIテスト
cd backend
uvicorn src.main:app --reload
```

## トラブルシューティング

### よくある問題

1. **JWKS の取得失敗**

   - ネットワーク接続を確認
   - USER_POOL_ID が正しいか確認

2. **トークン検証失敗**

   - トークンの形式を確認（Bearer プレフィックスなし）
   - トークンの有効期限を確認
   - USER_POOL_CLIENT_ID が正しいか確認

3. **環境変数未設定**
   - .env ファイルが正しく読み込まれているか確認
   - 必要な環境変数がすべて設定されているか確認

### デバッグ

ログレベルを調整してデバッグ情報を確認：

```python
import logging
logging.getLogger("src.auth").setLevel(logging.DEBUG)
```
