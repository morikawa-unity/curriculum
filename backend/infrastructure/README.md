# インフラストラクチャ設定

このディレクトリには、プログラミング学習アプリの AWS インフラストラクチャを管理する CloudFormation テンプレートが含まれています。

## ファイル構成

```
infrastructure/
├── main.yaml          # メインCloudFormationスタック
├── cognito.yaml       # Cognito ユーザープール設定
├── deploy.sh          # デプロイメントスクリプト
└── README.md          # このファイル
```

## 前提条件

1. AWS CLI がインストールされ、適切に設定されていること
2. 必要な AWS 権限を持つ IAM ユーザー/ロールでの認証
3. 東京リージョン（ap-northeast-1）へのアクセス権限

### 必要な AWS 権限

- CloudFormation: フルアクセス
- Cognito: フルアクセス
- S3: バケット作成・削除・オブジェクト操作
- IAM: ロール作成・管理（将来の Lambda 用）

## デプロイメント手順

### 開発環境へのデプロイ

```bash
cd backend/infrastructure
./deploy.sh dev
```

### 本番環境へのデプロイ

```bash
cd backend/infrastructure
./deploy.sh prod
```

## デプロイメント後の確認

デプロイメントが完了すると、以下のファイルが自動生成されます：

1. `frontend/.env.local` - フロントエンド用環境変数
2. `backend/.env` - バックエンド用環境変数

### 生成される環境変数

#### フロントエンド (.env.local)

```
NEXT_PUBLIC_AWS_REGION=ap-northeast-1
NEXT_PUBLIC_USER_POOL_ID=ap-northeast-1_xxxxxxxxx
NEXT_PUBLIC_USER_POOL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_USER_POOL_DOMAIN=https://programming-learning-app-dev-auth.auth.ap-northeast-1.amazoncognito.com
NEXT_PUBLIC_ENVIRONMENT=dev
```

#### バックエンド (.env)

```
AWS_REGION=ap-northeast-1
USER_POOL_ID=ap-northeast-1_xxxxxxxxx
USER_POOL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
USER_POOL_DOMAIN=https://programming-learning-app-dev-auth.auth.ap-northeast-1.amazoncognito.com
ENVIRONMENT=dev
```

## Cognito 設定詳細

### ユーザープール設定

- **認証方法**: メールアドレス + パスワード
- **パスワードポリシー**:
  - 最小 8 文字
  - 大文字・小文字・数字を含む
  - 記号は不要
- **MFA**: 無効（シンプルな学習アプリのため）
- **自動検証**: メールアドレス
- **アカウント復旧**: メール経由

### ユーザープールクライアント設定

- **認証フロー**: SRP 認証、リフレッシュトークン、パスワード認証
- **トークン有効期限**:
  - アクセストークン: 60 分
  - ID トークン: 60 分
  - リフレッシュトークン: 30 日
- **OAuth 設定**: 有効（将来のソーシャルログイン対応）

## 環境別設定

### 開発環境 (dev)

- スタック名: `programming-learning-app-dev`
- ドメイン: `programming-learning-app-dev-auth`
- コールバック URL:
  - `https://dev-programming-learning.amplifyapp.com/auth/callback`
  - `http://localhost:3000/auth/callback`

### 本番環境 (prod)

- スタック名: `programming-learning-app-prod`
- ドメイン: `programming-learning-app-prod-auth`
- コールバック URL:
  - `https://programming-learning.example.com/auth/callback`
  - `http://localhost:3000/auth/callback`

## トラブルシューティング

### よくある問題

1. **権限エラー**

   - AWS CLI の認証情報を確認
   - 必要な IAM 権限があることを確認

2. **スタック作成失敗**

   - CloudFormation コンソールでエラー詳細を確認
   - リソース名の重複がないか確認

3. **ドメイン名の競合**
   - Cognito ドメイン名は全世界で一意である必要があります
   - エラーが発生した場合は、cognito.yaml のドメイン名を変更してください

### スタックの削除

```bash
# 開発環境の削除
aws cloudformation delete-stack --stack-name programming-learning-app-dev --region ap-northeast-1

# 本番環境の削除
aws cloudformation delete-stack --stack-name programming-learning-app-prod --region ap-northeast-1
```

## 次のステップ

1. フロントエンドでの AWS Amplify Auth 設定
2. バックエンドでの Cognito トークン検証実装
3. RDS データベースの設定（将来のタスク）
4. Lambda 関数の設定（将来のタスク）
