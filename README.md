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

### セットアップ手順

1. リポジトリのクローン

```bash
git clone <repository-url>
cd programming-learning-app
```

2. フロントエンドのセットアップ

```bash
cd frontend
npm install
npm start
```

3. バックエンドのセットアップ

```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## デプロイメント

AWS Amplify の統合 CI/CD パイプラインを使用して自動デプロイを行います。

1. GitHub リポジトリにプッシュ
2. Amplify が自動的にビルド・デプロイを実行
3. CloudFormation でインフラリソースを管理

## 仕様書

詳細な仕様書は `.kiro/specs/programming-learning-app/` ディレクトリに格納されています：

- `requirements.md` - 要件定義書
- `design.md` - 設計書
- `tasks.md` - 実装計画
