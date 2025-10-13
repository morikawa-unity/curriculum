# AWS Amplify デプロイメント設定

## 概要

プログラミング学習アプリの AWS Amplify を使用した開発環境デプロイの設定情報です。

## AWS アカウント情報

- **アカウント ID**: 238136372347
- **ユーザー**: morikawa_admin
- **リージョン**: ap-northeast-1 (東京)
- **AWS Profile**: morikawa_admin

## Amplify アプリケーション情報

- **アプリ名**: programming-learning-app
- **アプリ ID**: d1ctw4uq3hjb47
- **デフォルトドメイン**: d1ctw4uq3hjb47.amplifyapp.com
- **GitHub リポジトリ**: https://github.com/morikawa-unity/curriculum
- **接続ブランチ**: develop

## URL 情報

- **Amplify コンソール**: https://ap-northeast-1.console.aws.amazon.com/amplify/apps/d1ctw4uq3hjb47/overview
- **開発環境 URL**: https://develop.d1ctw4uq3hjb47.amplifyapp.com
- **Amplify アプリ一覧**: https://ap-northeast-1.console.aws.amazon.com/amplify/apps

## GitHub 設定

### リポジトリ情報

- **リポジトリ**: morikawa-unity/curriculum
- **ブランチ**: develop
- **接続方法**: SSH

### GitHub アクセストークン

- **トークン**: [セキュリティ上の理由により非表示]
- **権限**:
  - repo (Full control of private repositories)
  - admin:repo_hook (Full control of repository hooks)
- **有効期限**: 90 日間

## 環境変数設定

### Amplify 環境変数

```
NEXT_PUBLIC_AWS_REGION=ap-northeast-1
NEXT_PUBLIC_USER_POOL_ID=ap-northeast-1_5SdJ4Iu5J
NEXT_PUBLIC_USER_POOL_CLIENT_ID=558bv8s595shb9bbk5i3nf78ee
NEXT_PUBLIC_ENVIRONMENT=dev
```

## ビルド設定 (amplify.yml)

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - cd frontend
        - npm run build
  artifacts:
    baseDirectory: frontend/.next
    files:
      - "**/*"
  cache:
    paths:
      - frontend/node_modules/**/*
      - frontend/.next/cache/**/*
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. ビルドエラー「Missing script: build」

**エラー**: `npm error Missing script: "build"`
**解決方法**:

- `amplify.yml`で frontend ディレクトリに明示的に移動
- `cd frontend`コマンドを追加

#### 2. モノレポエラー

**エラー**: `Build spec does not contain any app roots`
**解決方法**: `amplify.yml`でディレクトリを明示的に指定

#### 3. 同時実行エラー

**エラー**: `already have pending or running jobs`
**解決方法**: 現在のジョブが完了するまで待機

### デプロイ状況確認コマンド

```bash
# ジョブ状況確認
export AWS_PROFILE=morikawa_admin
aws amplify get-job \
    --app-id d1ctw4uq3hjb47 \
    --branch-name develop \
    --job-id [JOB_ID] \
    --region ap-northeast-1

# アプリ一覧確認
aws amplify list-apps --region ap-northeast-1

# ブランチ一覧確認
aws amplify list-branches \
    --app-id d1ctw4uq3hjb47 \
    --region ap-northeast-1
```

## 次のステップ

1. **現在のデプロイ完了を待つ**
2. **ビルドログを確認してエラーを修正**
3. **本番環境（main ブランチ）の設定**
4. **カスタムドメインの設定**
5. **CI/CD パイプラインの最適化**

---

**作成日**: 2025 年 10 月 13 日  
**最終更新**: 2025 年 10 月 13 日  
**作成者**: Programming Learning App Team
