# RDS 自動停止・開始スケジューラー

## 概要

プログラミング学習アプリの RDS インスタンスを自動的に停止・開始してコストを削減するシステムです。

## スケジュール

- **毎日 1:00 JST**: RDS 停止
- **月曜・火曜 19:00 JST**: RDS 開始
- **水曜〜日曜 10:00 JST**: RDS 開始

## コスト削減効果

- **水曜〜日曜**: 37.5%稼働（15 時間/40 時間）
- **月曜・火曜**: 25%稼働（6 時間/24 時間）
- **週全体**: 約 32%稼働 → **約 68%のコスト削減**

## デプロイ方法

### 1. RDS スケジューラー単体でデプロイ

```bash
cd backend/infrastructure
./deploy-rds-scheduler.sh dev
```

### 2. メインスタックに含めてデプロイ

```bash
cd backend/infrastructure
./deploy.sh dev
```

## 手動制御

### RDS 停止

```bash
aws lambda invoke \
  --function-name programming-learning-app-rds-scheduler-dev \
  --payload '{"action":"stop"}' \
  response.json && cat response.json
```

### RDS 開始

```bash
aws lambda invoke \
  --function-name programming-learning-app-rds-scheduler-dev \
  --payload '{"action":"start"}' \
  response.json && cat response.json
```

## 構成要素

### Lambda 関数

- **名前**: `programming-learning-app-rds-scheduler-dev`
- **ランタイム**: Python 3.10
- **機能**: RDS インスタンスの停止・開始制御

### EventBridge ルール

1. **停止スケジュール**: `cron(0 16 * * ? *)` (毎日 16:00 UTC = 1:00 JST)
2. **開始スケジュール（月火）**: `cron(0 10 ? * MON,TUE *)` (月火 10:00 UTC = 19:00 JST)
3. **開始スケジュール（水日）**: `cron(0 1 ? * WED,THU,FRI,SAT,SUN *)` (水日 01:00 UTC = 10:00 JST)

### IAM ロール

- **RDSSchedulerRole**: Lambda 実行用（RDS 制御権限付き）
- **EventBridgeRole**: EventBridge 実行用（Lambda 呼び出し権限付き）

## 監視とログ

### CloudWatch ログ

Lambda 関数の実行ログは以下で確認できます：

```
/aws/lambda/programming-learning-app-rds-scheduler-dev
```

### 実行状況の確認

```bash
# 最新の実行ログを確認
aws logs describe-log-streams \
  --log-group-name /aws/lambda/programming-learning-app-rds-scheduler-dev \
  --order-by LastEventTime \
  --descending \
  --max-items 1

# ログの内容を確認
aws logs get-log-events \
  --log-group-name /aws/lambda/programming-learning-app-rds-scheduler-dev \
  --log-stream-name [LOG_STREAM_NAME]
```

## トラブルシューティング

### よくある問題

1. **RDS が停止しない**

   - RDS インスタンスが`available`状態でない可能性
   - Lambda 関数のログを確認

2. **RDS が開始しない**

   - RDS インスタンスが`stopped`状態でない可能性
   - Lambda 関数のログを確認

3. **スケジュールが動作しない**
   - EventBridge ルールが有効になっているか確認
   - Lambda 関数の実行権限を確認

### デバッグコマンド

```bash
# RDSインスタンスの現在の状態を確認
aws rds describe-db-instances \
  --db-instance-identifier programming-learning-app-db-v2 \
  --query 'DBInstances[0].DBInstanceStatus'

# EventBridgeルールの状態を確認
aws events list-rules \
  --name-prefix programming-learning-app-rds
```

## 注意事項

1. **RDS 停止の制限**

   - RDS は 7 日間連続で停止すると自動的に開始されます
   - このスケジューラーは毎日停止・開始するため問題ありません

2. **タイムゾーン**

   - EventBridge は UTC 時間で動作します
   - JST = UTC + 9 時間で計算されています

3. **コスト**
   - Lambda 実行コストは月数円程度です
   - RDS 削減コストと比較すると無視できる範囲です

## カスタマイズ

スケジュールを変更したい場合は、`rds-scheduler.yaml`の以下の部分を編集してください：

```yaml
# 停止時刻の変更（現在：毎日1:00 JST）
ScheduleExpression: "cron(0 16 * * ? *)"

# 開始時刻の変更（現在：月火19:00 JST、水日10:00 JST）
ScheduleExpression: "cron(0 10 ? * MON,TUE *)"
ScheduleExpression: "cron(0 1 ? * WED,THU,FRI,SAT,SUN *)"
```
