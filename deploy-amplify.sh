#!/bin/bash

# プログラミング学習アプリ - Amplify デプロイメントスクリプト

set -e

# 設定
APP_NAME="programming-learning-app"
REGION="ap-northeast-1"
GITHUB_REPO="morikawa-unity/curriculum"  # GitHubリポジトリ名を適切に設定してください

echo "=== AWS Amplify アプリケーション作成 ==="
echo "アプリ名: $APP_NAME"
echo "リージョン: $REGION"
echo "GitHubリポジトリ: $GITHUB_REPO"
echo ""

# Amplifyアプリケーションを作成
echo "Amplifyアプリケーションを作成中..."
APP_ID=$(aws amplify create-app \
    --name $APP_NAME \
    --description "プログラミング学習用Webアプリケーション" \
    --repository "https://github.com/$GITHUB_REPO" \
    --platform WEB \
    --iam-service-role-arn "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/amplifyconsole-backend-role" \
    --region $REGION \
    --query 'app.appId' \
    --output text)

echo "Amplifyアプリケーション作成完了: $APP_ID"

# 開発環境ブランチを作成
echo "開発環境ブランチ（develop）を設定中..."
aws amplify create-branch \
    --app-id $APP_ID \
    --branch-name develop \
    --description "開発環境" \
    --enable-auto-build \
    --region $REGION

# 本番環境ブランチを作成
echo "本番環境ブランチ（main）を設定中..."
aws amplify create-branch \
    --app-id $APP_ID \
    --branch-name main \
    --description "本番環境" \
    --enable-auto-build \
    --region $REGION

# 環境変数を設定（開発環境）
echo "開発環境の環境変数を設定中..."
aws amplify put-backend-environment \
    --app-id $APP_ID \
    --environment-name develop \
    --region $REGION

# 環境変数を設定（本番環境）
echo "本番環境の環境変数を設定中..."
aws amplify put-backend-environment \
    --app-id $APP_ID \
    --environment-name production \
    --region $REGION

echo ""
echo "=== デプロイメント完了 ==="
echo "Amplify アプリID: $APP_ID"
echo "開発環境URL: https://develop.$APP_ID.amplifyapp.com"
echo "本番環境URL: https://main.$APP_ID.amplifyapp.com"
echo ""
echo "次のステップ:"
echo "1. AWS Amplifyコンソールでアプリケーションを確認"
echo "2. GitHubとの連携を設定"
echo "3. 環境変数を設定"
echo "4. developブランチにプッシュしてデプロイをテスト"