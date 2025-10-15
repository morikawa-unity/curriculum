#!/bin/bash

# RDSスケジューラーデプロイスクリプト
# 使用方法: ./deploy-rds-scheduler.sh [dev|prod]

set -e

# 環境パラメータの設定
ENVIRONMENT=${1:-dev}
APP_NAME="programming-learning-app"
STACK_NAME="${APP_NAME}-rds-scheduler-${ENVIRONMENT}"
REGION="ap-northeast-1"

echo "🚀 RDSスケジューラーをデプロイしています..."
echo "環境: ${ENVIRONMENT}"
echo "スタック名: ${STACK_NAME}"
echo "リージョン: ${REGION}"

# CloudFormationスタックのデプロイ
aws cloudformation deploy \
  --template-file rds-scheduler.yaml \
  --stack-name ${STACK_NAME} \
  --parameter-overrides \
    Environment=${ENVIRONMENT} \
    AppName=${APP_NAME} \
  --capabilities CAPABILITY_NAMED_IAM \
  --region ${REGION} \

  --tags \
    Environment=${ENVIRONMENT} \
    Application=${APP_NAME} \
    Component=RDSScheduler

if [ $? -eq 0 ]; then
    echo "✅ RDSスケジューラーのデプロイが完了しました！"
    echo ""
    echo "📋 デプロイされたリソース:"
    echo "- Lambda関数: ${APP_NAME}-rds-scheduler-${ENVIRONMENT}"
    echo "- EventBridgeルール（停止）: 毎日 1:00 JST"
    echo "- EventBridgeルール（開始・月火）: 月火 19:00 JST"
    echo "- EventBridgeルール（開始・水日）: 水木金土日 10:00 JST"
    echo ""
    echo "💰 コスト削減効果:"
    echo "- 水曜〜日曜: 37.5%稼働（9時間/24時間）"
    echo "- 月曜・火曜: 25%稼働（6時間/24時間）"
    echo "- 週全体: 約32%稼働 → 約68%のコスト削減"
    echo ""
    echo "🔧 手動制御コマンド:"
    echo "# RDS停止"
    echo "aws lambda invoke --function-name ${APP_NAME}-rds-scheduler-${ENVIRONMENT} --payload '{\"action\":\"stop\"}' response.json"
    echo ""
    echo "# RDS開始"
    echo "aws lambda invoke --function-name ${APP_NAME}-rds-scheduler-${ENVIRONMENT} --payload '{\"action\":\"start\"}' response.json"
else
    echo "❌ デプロイに失敗しました"
    exit 1
fi