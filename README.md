# プログラミング学習アプリ

AWS 上でサーバーレスアーキテクチャを採用したフルスタック Web アプリケーションです。

## 技術スタック

### フロントエンド

- React + TypeScript
- TanStack Query (サーバー状態管理)
- Zustand (クライアント状態管理)
- Zod (スキーマ検証)

### バックエンド

- FastAPI + Python
- AWS Lambda
- AWS RDS (MySQL)

### インフラ

- AWS Amplify (ホスティング・CI/CD)
- AWS Cognito (認証)
- CloudFormation (Infrastructure as Code)

## プロジェクト構成

```
├── frontend/          # フロントエンドアプリケーション
│   └── src/
│       ├── components/    # UIコンポーネント
│       ├── pages/         # ページコンポーネント
│       ├── hooks/         # カスタムフック
│       ├── store/         # 状態管理
│       ├── api/           # API呼び出し
│       ├── schemas/       # Zodスキーマ
│       └── utils/         # ユーティリティ
├── backend/           # バックエンドアプリケーション
│   ├── src/
│   │   ├── handlers/      # Lambda関数ハンドラー
│   │   ├── models/        # データモデル
│   │   ├── database/      # データベース操作
│   │   ├── services/      # ビジネスロジック
│   │   └── utils/         # ユーティリティ
│   └── infrastructure/    # CloudFormationテンプレート
└── .kiro/             # Kiro設定・仕様書
    └── specs/
        └── programming-learning-app/
```

## 開発環境セットアップ

### 前提条件

- Node.js (v18 以上)
- Python (v3.9 以上)
- MySQL (ローカル開発用)
- AWS CLI (デプロイ用)

### ブランチ戦略

このプロジェクトは Git Flow を採用しています：

- **main**: 本番環境用ブランチ（本番デプロイ）
  - 直接プッシュ禁止
  - develop ブランチからのプルリクエストのみ許可
  - 本番環境への自動デプロイが実行される
- **develop**: 開発環境用ブランチ（開発環境デプロイ）
  - デフォルトブランチ
  - feature ブランチからのマージを受け入れる
  - 開発環境への自動デプロイが実行される
- **feature/\***: 機能開発用ブランチ（ローカル開発）
  - develop ブランチから分岐
  - 機能開発完了後は develop にマージ

### ブランチ保護ルール

GitHub リポジトリで以下の保護ルールを設定してください：

#### main ブランチ

- ✅ Restrict pushes that create files (直接プッシュを禁止)
- ✅ Require pull request reviews before merging (プルリクエストレビュー必須)
- ✅ Require status checks to pass before merging (ステータスチェック必須)
- ✅ Require branches to be up to date before merging (最新状態必須)
- ✅ Include administrators (管理者も含める)

#### develop ブランチ

- ✅ Require pull request reviews before merging (プルリクエストレビュー必須)
- ✅ Require status checks to pass before merging (ステータスチェック必須)

### 開発ワークフロー

#### 1. 新機能開発の開始

```bash
# 最新の develop ブランチを取得
git checkout develop
git pull origin develop

# 新しい feature ブランチを作成
git checkout -b feature/機能名

# 例: 認証機能の開発
git checkout -b feature/auth-implementation
```

#### 2. 開発中のコミット

```bash
# 変更をステージング
git add .

# 日本語でコミットメッセージを記述
git commit -m "feat: ユーザー認証機能を実装"

# リモートにプッシュ
git push origin feature/機能名
```

#### 3. 開発完了後のマージ（develop へ）

```bash
# develop ブランチに切り替え
git checkout develop

# 最新の変更を取得
git pull origin develop

# feature ブランチをマージ
git merge feature/機能名

# develop にプッシュ（開発環境に自動デプロイ）
git push origin develop

# 不要になった feature ブランチを削除
git branch -d feature/機能名
git push origin --delete feature/機能名
```

#### 4. 本番リリース（main へ）

```bash
# main ブランチに切り替え
git checkout main

# 最新の変更を取得
git pull origin main

# develop ブランチをマージ
git merge develop

# main にプッシュ（本番環境に自動デプロイ）
git push origin main
```

#### 5. プルリクエストを使用したワークフロー（推奨）

```bash
# feature ブランチで開発完了後
git push origin feature/機能名

# GitHub でプルリクエストを作成
# develop ← feature/機能名
# レビュー後にマージ

# 本番リリース時も同様
# main ← develop のプルリクエストを作成
```

### コミットメッセージ規約

以下の形式でコミットメッセージを記述してください：

```
<type>: <description>

例:
feat: ユーザー認証機能を実装
fix: ログイン時のバリデーションエラーを修正
docs: README にデプロイ手順を追加
style: コードフォーマットを統一
refactor: 認証サービスのコードを整理
test: ユーザー登録のテストケースを追加
```

### 緊急時の対応

#### ホットフィックス

```bash
# main ブランチから hotfix ブランチを作成
git checkout main
git checkout -b hotfix/緊急修正内容

# 修正作業
git add .
git commit -m "hotfix: 緊急修正内容"

# main と develop の両方にマージ
git checkout main
git merge hotfix/緊急修正内容
git push origin main

git checkout develop
git merge hotfix/緊急修正内容
git push origin develop

# hotfix ブランチを削除
git branch -d hotfix/緊急修正内容
```

### セットアップ手順

#### 1. リポジトリのクローン

```bash
git clone https://github.com/morikawa-unity/curriculum.git
cd curriculum
git checkout develop  # 開発ブランチに切り替え
```

#### 2. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係のインストール
pip install -r requirements.txt
```

**環境変数の設定**

`backend/.env` ファイルを作成：

```env
# データベース設定（AWS RDS）
DATABASE_HOST=programming-learning-app-db-v2.c7wewuq6yxt2.ap-northeast-1.rds.amazonaws.com
DATABASE_PORT=3306
DATABASE_NAME=programming_learning_app
DATABASE_USER=admin
DATABASE_PASSWORD=ProgrammingApp2024!

# AWS設定
AWS_REGION=ap-northeast-1
COGNITO_USER_POOL_ID=ap-northeast-1_5SdJ4Iu5J
COGNITO_CLIENT_ID=558bv8s595shb9bbk5i3nf78ee
USER_POOL_ID=ap-northeast-1_5SdJ4Iu5J
USER_POOL_CLIENT_ID=558bv8s595shb9bbk5i3nf78ee

# セキュリティ設定
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS設定
ALLOWED_ORIGINS=http://localhost:3000,https://localhost:3000
```

**データベースのセットアップ（初回のみ）**

```bash
# RDSデータベースの初期化
python setup_rds_database.py

# サンプルデータの投入
python insert_sample_data_rds.py
```

#### 3. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install
```

**環境変数の設定**

`frontend/.env.local` ファイルを作成：

```env
# AWS Cognito 設定
NEXT_PUBLIC_AWS_REGION=ap-northeast-1
NEXT_PUBLIC_USER_POOL_ID=ap-northeast-1_5SdJ4Iu5J
NEXT_PUBLIC_USER_POOL_CLIENT_ID=558bv8s595shb9bbk5i3nf78ee
NEXT_PUBLIC_ENVIRONMENT=dev

# バックエンドAPI URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ローカル起動方法

アプリケーションを起動するには、**バックエンドとフロントエンドの両方を起動する必要があります**。

### 1. バックエンドの起動

ターミナル1で：

```bash
cd backend
source venv/bin/activate  # 仮想環境を有効化
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

起動確認：
```bash
curl http://localhost:8000/health
# => {"status":"healthy",...} が返ってくればOK
```

### 2. フロントエンドの起動

ターミナル2で（別のターミナルウィンドウを開く）：

```bash
cd frontend
npm run dev
```

起動すると、ブラウザで http://localhost:3000 にアクセスできます。

### 3. ログイン

- **メールアドレス**: `testuser@example.com`
- **パスワード**: `TestUser2024!`

## トラブルシューティング

### バックエンドが起動しない

- `.env` ファイルが正しく設定されているか確認
- RDSインスタンスが起動しているか確認：
  ```bash
  aws rds describe-db-instances --db-instance-identifier programming-learning-app-db-v2 --region ap-northeast-1
  ```

### フロントエンドで「AWS Cognito環境変数が設定されていません」と表示される

- `frontend/.env.local` ファイルが作成されているか確認
- ファイルを作成/編集した後は、`npm run dev` を再起動

### データベース接続エラー

- セキュリティグループでポート3306が開放されているか確認
- `backend/README.md` のトラブルシューティングセクションを参照

## デプロイメント

AWS Amplify の統合 CI/CD パイプラインを使用してブランチ別の自動デプロイを行います。

### 環境とブランチの対応

- **開発環境**: `develop` ブランチ → 開発用 AWS リソース
- **本番環境**: `main` ブランチ → 本番用 AWS リソース

### デプロイフロー

1. `develop` ブランチにプッシュ → 開発環境に自動デプロイ
2. `main` ブランチにプッシュ → 本番環境に自動デプロイ
3. Amplify が自動的にビルド・デプロイを実行
4. CloudFormation でインフラリソースを管理

## 開発者向けブランチ運用ガイド

### 日常的な開発作業

#### 作業開始時

```bash
# 1. develop ブランチの最新状態を確認
git checkout develop
git pull origin develop

# 2. 新しい feature ブランチを作成
git checkout -b feature/[JIRA番号]-[機能名]
# 例: git checkout -b feature/CURR-123-user-profile
```

#### 作業中

```bash
# 定期的にコミット
git add .
git commit -m "feat: プロフィール画面のレイアウトを実装"

# リモートにバックアップ
git push origin feature/[ブランチ名]

# 長期間の作業では develop の変更を取り込み
git checkout develop
git pull origin develop
git checkout feature/[ブランチ名]
git merge develop
```

#### 作業完了時

```bash
# 1. 最終的なテストとコミット
npm test  # または pytest
git add .
git commit -m "feat: ユーザープロフィール機能を完成"

# 2. develop の最新変更を取り込み
git checkout develop
git pull origin develop
git checkout feature/[ブランチ名]
git merge develop

# 3. プルリクエストを作成
git push origin feature/[ブランチ名]
# GitHub でプルリクエスト作成: develop ← feature/[ブランチ名]
```

### 注意事項

- **main ブランチには直接プッシュしない**
- **develop ブランチへの直接プッシュは避け、プルリクエストを使用する**
- **feature ブランチは小さく、短期間で完了させる**
- **コミットメッセージは日本語で分かりやすく記述する**
- **プルリクエストには適切な説明とレビュアーを設定する**

### トラブルシューティング

#### コンフリクトが発生した場合

```bash
# develop の最新変更を取り込み時にコンフリクト
git checkout develop
git pull origin develop
git checkout feature/[ブランチ名]
git merge develop

# コンフリクトファイルを手動で解決
# エディタでコンフリクトマーカーを削除し、適切にマージ

git add .
git commit -m "merge: develop の変更をマージ"
```

#### 間違ったブランチにコミットした場合

```bash
# 最新のコミットを別のブランチに移動
git checkout 正しいブランチ
git cherry-pick 間違ったブランチ

# 間違ったブランチから削除
git checkout 間違ったブランチ
git reset --hard HEAD~1
```

## 仕様書

詳細な仕様書は `.kiro/specs/programming-learning-app/` ディレクトリに格納されています：

- `requirements.md` - 要件定義書
- `design.md` - 設計書
- `tasks.md` - 実装計画
