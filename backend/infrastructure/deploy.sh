#!/bin/bash

# プログラミング学習アプリ - CloudFormation デプロイメントスクリプト

set -e

# 設定
APP_NAME="programming-learning-app"
REGION="ap-northeast-1"  # 東京リージョン

# 引数チェック
if [ $# -ne 1 ]; then
    echo "使用方法: $0 <environment>"
    echo "environment: dev または prod"
    exit 1
fi

ENVIRONMENT=$1

# 環境チェック
if [ "$ENVIRONMENT" != "dev" ] && [ "$ENVIRONMENT" != "prod" ]; then
    echo "エラー: 環境は 'dev' または 'prod' を指定してください"
    exit 1
fi

# スタック名
STACK_NAME="${APP_NAME}-${ENVIRONMENT}"

echo "=== プログラミング学習アプリ インフラデプロイメント ==="
echo "環境: $ENVIRONMENT"
echo "スタック名: $STACK_NAME"
echo "リージョン: $REGION"
echo ""

# S3バケット名（CloudFormationテンプレート用）
BUCKET_NAME="${APP_NAME}-${ENVIRONMENT}-cf-templates-$(date +%s)"

echo "CloudFormationテンプレート用S3バケットを作成中..."
aws s3 mb s3://$BUCKET_NAME --region $REGION

# テンプレートをS3にアップロード
echo "CloudFormationテンプレートをS3にアップロード中..."
aws s3 cp cognito.yaml s3://$BUCKET_NAME/cognito.yaml
aws s3 cp main.yaml s3://$BUCKET_NAME/main.yaml

# CloudFormationスタックのデプロイ
echo "CloudFormationスタックをデプロイ中..."

# スタックが存在するかチェック
if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION >/dev/null 2>&1; then
    echo "既存スタックを更新中..."
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-url https://s3.$REGION.amazonaws.com/$BUCKET_NAME/main.yaml \
        --parameters ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
                    ParameterKey=AppName,ParameterValue=$APP_NAME \
        --capabilities CAPABILITY_IAM \
        --region $REGION
    
    echo "スタック更新完了を待機中..."
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --region $REGION
else
    echo "新規スタックを作成中..."
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-url https://s3.$REGION.amazonaws.com/$BUCKET_NAME/main.yaml \
        --parameters ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
                    ParameterKey=AppName,ParameterValue=$APP_NAME \
        --capabilities CAPABILITY_IAM \
        --region $REGION
    
    echo "スタック作成完了を待機中..."
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $REGION
fi

# スタック出力を表示
echo ""
echo "=== デプロイメント完了 ==="
echo "スタック出力:"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

# 環境変数ファイルを生成
echo ""
echo "環境変数ファイルを生成中..."

# Cognito設定を取得
USER_POOL_ID=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' \
    --output text)

USER_POOL_CLIENT_ID=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`UserPoolClientId`].OutputValue' \
    --output text)

USER_POOL_DOMAIN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`UserPoolDomain`].OutputValue' \
    --output text)

# フロントエンド用環境変数ファイル
cat > ../../frontend/.env.local << EOF
# AWS Cognito 設定 - $ENVIRONMENT 環境
NEXT_PUBLIC_AWS_REGION=$REGION
NEXT_PUBLIC_USER_POOL_ID=$USER_POOL_ID
NEXT_PUBLIC_USER_POOL_CLIENT_ID=$USER_POOL_CLIENT_ID
NEXT_PUBLIC_USER_POOL_DOMAIN=$USER_POOL_DOMAIN
NEXT_PUBLIC_ENVIRONMENT=$ENVIRONMENT
EOF

# バックエンド用環境変数ファイル
cat > ../.env << EOF
# AWS Cognito 設定 - $ENVIRONMENT 環境
AWS_REGION=$REGION
USER_POOL_ID=$USER_POOL_ID
USER_POOL_CLIENT_ID=$USER_POOL_CLIENT_ID
USER_POOL_DOMAIN=$USER_POOL_DOMAIN
ENVIRONMENT=$ENVIRONMENT
EOF

echo "環境変数ファイルが生成されました:"
echo "  - フロントエンド: frontend/.env.local"
echo "  - バックエンド: backend/.env"

# 一時的なS3バケットを削除
echo ""
echo "一時的なS3バケットを削除中..."
aws s3 rb s3://$BUCKET_NAME --force

echo ""
echo "=== デプロイメント完了 ==="
echo "Cognito ユーザープールが正常にデプロイされました。"
echo "User Pool ID: $USER_POOL_ID"
echo "User Pool Client ID: $USER_POOL_CLIENT_ID"