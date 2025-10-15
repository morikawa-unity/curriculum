#!/usr/bin/env python3
"""
プロフィールAPIのテストスクリプト
"""

import requests
import json

def test_profile_endpoints():
    """
    プロフィールAPIエンドポイントをテストする
    """
    base_url = "http://localhost:8000/api/v1/users/profile"
    
    endpoints = [
        ("PR0101001", "ユーザープロフィール情報取得")
    ]
    
    print("プロフィールAPIエンドポイントのテスト")
    print("=" * 50)
    
    for endpoint_id, description in endpoints:
        url = f"{base_url}/{endpoint_id}"
        print(f"\n{description} ({endpoint_id})")
        print(f"URL: {url}")
        
        try:
            # 認証なしでリクエスト（エラーレスポンスを確認）
            response = requests.get(url, timeout=5)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 401:
                print("✓ 認証が必要なエンドポイントとして正しく動作")
            elif response.status_code == 422:
                print("✓ 認証トークンが必要として正しく動作")
            else:
                print(f"Response: {response.text[:200]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ リクエストエラー: {e}")
    
    # ヘルスチェック
    print(f"\n{'='*50}")
    print("ヘルスチェック")
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health Check Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"Status: {health_data.get('status')}")
            print(f"Database: {health_data.get('database_status')}")
        else:
            print(f"Health Check Response: {health_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ ヘルスチェックエラー: {e}")

if __name__ == '__main__':
    test_profile_endpoints()