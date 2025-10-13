# データベースセットアップガイド

このドキュメントでは、プログラミング学習アプリのデータベースセットアップ方法について説明します。

## 前提条件

- MySQL 8.0 以上がインストールされていること
- Python 3.8 以上がインストールされていること
- 必要な Python パッケージがインストールされていること

## セットアップ手順

### 1. 仮想環境の作成と依存関係のインストール

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. データベースの初期化

```bash
# データベースとテーブルの作成
python setup_database.py
```

このスクリプトは以下の処理を行います：

- `programming_learning_app` データベースの作成
- `users`, `exercises`, `progress` テーブルの作成
- 適切なインデックスと制約の設定

### 3. サンプルデータの投入

```bash
# サンプル演習データの投入
python insert_sample_data.py
```

このスクリプトは以下のサンプル演習を投入します：

1. Hello World を出力する (beginner)
2. 変数の基本操作 (beginner)
3. 簡単な計算プログラム (beginner)
4. 条件分岐の基本 (beginner)
5. リストの基本操作 (beginner)
6. for 文を使った繰り返し処理 (beginner)
7. 関数の基本 (intermediate)
8. 辞書（Dictionary）の基本操作 (intermediate)

## データベース構成

### テーブル構造

#### users テーブル

- `id`: Cognito User ID (VARCHAR(36), PRIMARY KEY)
- `email`: メールアドレス (VARCHAR(255), UNIQUE)
- `username`: ユーザー名 (VARCHAR(50), UNIQUE)
- `created_at`: 作成日時 (TIMESTAMP)
- `updated_at`: 更新日時 (TIMESTAMP)

#### exercises テーブル

- `id`: 演習 ID (INT, AUTO_INCREMENT, PRIMARY KEY)
- `title`: 演習タイトル (VARCHAR(255))
- `description`: 演習説明 (TEXT)
- `difficulty`: 難易度 (ENUM: 'beginner', 'intermediate', 'advanced')
- `language`: プログラミング言語 (VARCHAR(50))
- `initial_code`: 初期コード (TEXT)
- `solution_code`: 解答コード (TEXT)
- `test_cases`: テストケース (JSON)
- `created_at`: 作成日時 (TIMESTAMP)
- `updated_at`: 更新日時 (TIMESTAMP)

#### progress テーブル

- `id`: 進捗 ID (INT, AUTO_INCREMENT, PRIMARY KEY)
- `user_id`: ユーザー ID (VARCHAR(36), FOREIGN KEY)
- `exercise_id`: 演習 ID (INT, FOREIGN KEY)
- `status`: ステータス (ENUM: 'not_started', 'in_progress', 'completed')
- `submitted_code`: 提出コード (TEXT)
- `score`: スコア (INT)
- `attempts`: 試行回数 (INT)
- `completed_at`: 完了日時 (TIMESTAMP)
- `created_at`: 作成日時 (TIMESTAMP)
- `updated_at`: 更新日時 (TIMESTAMP)

## 設定のカスタマイズ

データベース接続設定を変更する場合は、以下のファイルを編集してください：

### setup_database.py

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # MySQLのパスワードを設定
    'charset': 'utf8mb4'
}
```

### src/config.py

```python
class Settings(BaseSettings):
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "programming_learning_app"
    database_user: str = "root"
    database_password: str = ""
```

## トラブルシューティング

### MySQL 接続エラー

- MySQL サーバーが起動していることを確認
- 接続情報（ホスト、ポート、ユーザー、パスワード）が正しいことを確認
- ファイアウォールの設定を確認

### 権限エラー

- MySQL ユーザーにデータベース作成権限があることを確認
- 必要に応じて以下のコマンドで権限を付与：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### 文字化け

- データベースとテーブルの文字セットが `utf8mb4` に設定されていることを確認
- MySQL 設定ファイル（my.cnf）で文字セットが正しく設定されていることを確認

## 開発環境での使用

開発時は以下のコマンドでデータベースの状態を確認できます：

```bash
# テーブル一覧の確認
mysql -u root programming_learning_app -e "SHOW TABLES;"

# 演習データの確認
mysql -u root programming_learning_app -e "SELECT id, title, difficulty FROM exercises;"

# データベースの削除（リセット時）
mysql -u root -e "DROP DATABASE IF EXISTS programming_learning_app;"
```

## 本番環境での注意事項

本番環境では以下の点に注意してください：

1. **セキュリティ**: 強力なパスワードを設定
2. **バックアップ**: 定期的なデータベースバックアップの設定
3. **監視**: データベースのパフォーマンス監視
4. **SSL**: SSL 接続の有効化
5. **権限**: 最小権限の原則に従ったユーザー権限の設定
