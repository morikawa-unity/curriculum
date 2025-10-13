#!/usr/bin/env python3
"""
認証機能のテストスクリプト
"""

import os
import sys
import asyncio
import httpx
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# テスト用の設定
BASE_URL = "http://localhost:8000"
TEST_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."  # 実際のテストトークンに置き換え


async def test_auth_endpoints():
    """認証エンドポイントをテスト"""
    
    async with httpx.AsyncClient() as client:
        print("🔍 認証エンドポイントのテストを開始...")
        
        # 1. ヘルスチェック
        print("\n1. ヘルスチェック")
        try:
            response = await client.get(f"{BASE_URL}/auth/health")
            print(f"   ステータス: {response.status_code}")
            print(f"   レスポンス: {response.json()}")
        except Exception as e:
            print(f"   エラー: {e}")
        
        # 2. 認証状態確認（トークンなし）
        print("\n2. 認証状態確認（トークンなし）")
        try:
            response = await client.get(f"{BASE_URL}/auth/status")
            print(f"   ステータス: {response.status_code}")
            print(f"   レスポンス: {response.json()}")
        except Exception as e:
            print(f"   エラー: {e}")
        
        # 3. トークン検証（トークンなし）
        print("\n3. トークン検証（トークンなし）")
        try:
            response = await client.post(f"{BASE_URL}/auth/validate-token")
            print(f"   ステータス: {response.status_code}")
            print(f"   レスポンス: {response.json()}")
        except Exception as e:
            print(f"   エラー: {e}")
        
        # 4. ユーザー情報取得（認証必須、トークンなし）
        print("\n4. ユーザー情報取得（認証必須、トークンなし）")
        try:
            response = await client.get(f"{BASE_URL}/auth/me")
            print(f"   ステータス: {response.status_code}")
            print(f"   レスポンス: {response.json()}")
        except Exception as e:
            print(f"   エラー: {e}")
        
        # 5. 無効なトークンでのテスト
        print("\n5. 無効なトークンでのテスト")
        headers = {"Authorization": "Bearer invalid_token"}
        try:
            response = await client.get(f"{BASE_URL}/auth/me", headers=headers)
            print(f"   ステータス: {response.status_code}")
            print(f"   レスポンス: {response.json()}")
        except Exception as e:
            print(f"   エラー: {e}")
        
        print("\n✅ テスト完了")


def test_cognito_service():
    """Cognitoサービスの基本テスト"""
    print("🔍 Cognitoサービスのテストを開始...")
    
    try:
        from src.auth.cognito import CognitoAuthService
        
        # サービスの初期化テスト
        print("\n1. サービス初期化テスト")
        service = CognitoAuthService()
        print(f"   リージョン: {service.region}")
        print(f"   ユーザープールID: {service.user_pool_id}")
        print(f"   クライアントID: {service.user_pool_client_id}")
        print(f"   JWKS URL: {service.jwks_url}")
        
        # JWKSの取得テスト
        print("\n2. JWKS取得テスト")
        try:
            jwks = service._get_jwks()
            print(f"   JWKS取得成功: {len(jwks.get('keys', []))} 個のキー")
        except Exception as e:
            print(f"   JWKS取得エラー: {e}")
        
        print("\n✅ Cognitoサービステスト完了")
        
    except Exception as e:
        print(f"❌ Cognitoサービステストエラー: {e}")


def main():
    """メイン関数"""
    print("🚀 認証機能テストスイート")
    print("=" * 50)
    
    # 環境変数の確認
    print("\n📋 環境変数の確認")
    required_vars = ['AWS_REGION', 'USER_POOL_ID', 'USER_POOL_CLIENT_ID']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value[:20]}...")
        else:
            print(f"   ❌ {var}: 未設定")
    
    # Cognitoサービステスト
    test_cognito_service()
    
    # APIエンドポイントテスト
    print("\n" + "=" * 50)
    try:
        asyncio.run(test_auth_endpoints())
    except KeyboardInterrupt:
        print("\n⚠️  テストが中断されました")
    except Exception as e:
        print(f"❌ テストエラー: {e}")


if __name__ == "__main__":
    main()