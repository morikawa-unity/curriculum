#!/usr/bin/env python3
"""
PHPコース設定スクリプト
既存の演習を削除してPHPコースを設定
"""

import pymysql
import json
import logging
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# データベース設定（環境変数から取得）
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST'),
    'port': int(os.getenv('DATABASE_PORT', 3306)),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'database': os.getenv('DATABASE_NAME'),
    'charset': 'utf8mb4'
}

# PHPコースの演習データ
PHP_EXERCISES = [
    {
        'title': 'PHPの基本 - Hello World',
        'description': '''PHPの基本中の基本！
「Hello, World!」という文字列を出力するプログラムを作成してください。

**学習目標:**
- PHPの基本的な出力方法を理解する
- PHPタグの使い方を学ぶ

**ヒント:**
- PHPでは `echo` または `print` を使用します
- PHPコードは `<?php` と `?>` で囲みます''',
        'difficulty': 'beginner',
        'language': 'php',
        'initial_code': '''<?php
// Hello, World! を出力してください

?>''',
        'solution_code': '''<?php
echo "Hello, World!";
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': 'Hello, World!',
                'description': 'Hello, World! が正しく出力される'
            }
        ]
    },
    {
        'title': '変数の基本操作',
        'description': '''PHPで変数を使って値を保存し、表示しましょう。

**課題:**
1. 変数 `$name` に名前を代入
2. 変数 `$age` に年齢を代入
3. 「私の名前は○○で、年齢は○○歳です」という形式で出力

**学習目標:**
- PHPの変数宣言（$記号）を理解する
- 文字列の結合方法を学ぶ''',
        'difficulty': 'beginner',
        'language': 'php',
        'initial_code': '''<?php
// 変数を使って自己紹介をしてください
$name = "";  // ここに名前を入力
$age = 0;    // ここに年齢を入力

// 自己紹介を出力してください

?>''',
        'solution_code': '''<?php
$name = "太郎";
$age = 20;
echo "私の名前は{$name}で、年齢は{$age}歳です";
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '私の名前は太郎で、年齢は20歳です',
                'description': '正しい形式で自己紹介が出力される'
            }
        ]
    },
    {
        'title': '配列の基本操作',
        'description': '''PHPの配列を使ってデータを管理しましょう。

**課題:**
果物の配列を作成し、以下の操作を行ってください：
1. 配列の全要素を表示
2. 配列の要素数を表示
3. 新しい果物を追加
4. 特定の果物があるかチェック

**学習目標:**
- 配列の作成と操作方法を理解する
- array関数の使い方を学ぶ''',
        'difficulty': 'beginner',
        'language': 'php',
        'initial_code': '''<?php
// 果物の配列を操作するプログラムを作成してください
$fruits = array("りんご", "バナナ", "オレンジ");

// 1. 配列の全要素を表示


// 2. 配列の要素数を表示


// 3. "ぶどう"を追加


// 4. "バナナ"があるかチェック


?>''',
        'solution_code': '''<?php
$fruits = array("りんご", "バナナ", "オレンジ");

// 1. 配列の全要素を表示
echo "果物リスト: " . implode(", ", $fruits) . "\n";

// 2. 配列の要素数を表示
echo "果物の数: " . count($fruits) . "\n";

// 3. "ぶどう"を追加
array_push($fruits, "ぶどう");
echo "追加後: " . implode(", ", $fruits) . "\n";

// 4. "バナナ"があるかチェック
if (in_array("バナナ", $fruits)) {
    echo "バナナがあります\n";
} else {
    echo "バナナがありません\n";
}
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''果物リスト: りんご, バナナ, オレンジ
果物の数: 3
追加後: りんご, バナナ, オレンジ, ぶどう
バナナがあります''',
                'description': '配列の基本操作が正しく実行される'
            }
        ]
    },
    {
        'title': '条件分岐 - if文',
        'description': '''if文を使って条件に応じて異なる処理を行いましょう。

**課題:**
年齢を変数に代入し、以下の条件で分岐してください：
- 20歳未満: "未成年です"
- 20歳以上65歳未満: "成人です"
- 65歳以上: "高齢者です"

**学習目標:**
- PHPのif文の基本的な使い方を理解する
- 条件式の書き方を学ぶ''',
        'difficulty': 'beginner',
        'language': 'php',
        'initial_code': '''<?php
// 年齢に応じて分類するプログラムを作成してください
$age = 25;  // この値を変更してテストしてください

// if文を使って年齢を分類してください


?>''',
        'solution_code': '''<?php
$age = 25;

if ($age < 20) {
    echo "未成年です";
} elseif ($age < 65) {
    echo "成人です";
} else {
    echo "高齢者です";
}
?>''',
        'test_cases': [
            {
                'input': '$age = 15',
                'expected_output': '未成年です',
                'description': '20歳未満の場合'
            },
            {
                'input': '$age = 25',
                'expected_output': '成人です',
                'description': '20歳以上65歳未満の場合'
            },
            {
                'input': '$age = 70',
                'expected_output': '高齢者です',
                'description': '65歳以上の場合'
            }
        ]
    },
    {
        'title': 'for文を使った繰り返し処理',
        'description': '''for文を使って繰り返し処理を行いましょう。

**課題:**
1から10までの数値を使って以下を実行してください：
1. 1から10までの数値を順番に出力
2. 1から10までの数値の合計を計算
3. 偶数のみを出力

**学習目標:**
- for文の基本的な使い方を理解する
- ループ処理を学ぶ''',
        'difficulty': 'beginner',
        'language': 'php',
        'initial_code': '''<?php
// for文を使った繰り返し処理を作成してください

// 1. 1から10までの数値を順番に出力


// 2. 1から10までの数値の合計を計算


// 3. 偶数のみを出力


?>''',
        'solution_code': '''<?php
// 1. 1から10までの数値を順番に出力
echo "1から10までの数値:\n";
for ($i = 1; $i <= 10; $i++) {
    echo $i . "\n";
}

// 2. 1から10までの数値の合計を計算
$total = 0;
for ($i = 1; $i <= 10; $i++) {
    $total += $i;
}
echo "合計: " . $total . "\n";

// 3. 偶数のみを出力
echo "偶数のみ:\n";
for ($i = 1; $i <= 10; $i++) {
    if ($i % 2 == 0) {
        echo $i . "\n";
    }
}
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''1から10までの数値:
1
2
3
4
5
6
7
8
9
10
合計: 55
偶数のみ:
2
4
6
8
10''',
                'description': 'for文を使った各種処理が正しく実行される'
            }
        ]
    },
    {
        'title': '関数の基本',
        'description': '''関数を定義して再利用可能なコードを作成しましょう。

**課題:**
以下の関数を作成してください：
1. 2つの数値を受け取って足し算する関数
2. 名前を受け取って挨拶する関数
3. 数値を受け取って偶数か奇数かを判定する関数

**学習目標:**
- 関数の定義方法を理解する
- 引数と戻り値の概念を学ぶ''',
        'difficulty': 'intermediate',
        'language': 'php',
        'initial_code': '''<?php
// 関数を定義して使用してください

// 1. 2つの数値を足し算する関数
function addNumbers($a, $b) {
    // ここに処理を書いてください
}

// 2. 名前を受け取って挨拶する関数
function greet($name) {
    // ここに処理を書いてください
}

// 3. 偶数か奇数かを判定する関数
function checkEvenOdd($number) {
    // ここに処理を書いてください
}

// 関数を呼び出してテストしてください


?>''',
        'solution_code': '''<?php
// 1. 2つの数値を足し算する関数
function addNumbers($a, $b) {
    return $a + $b;
}

// 2. 名前を受け取って挨拶する関数
function greet($name) {
    return "こんにちは、{$name}さん！";
}

// 3. 偶数か奇数かを判定する関数
function checkEvenOdd($number) {
    if ($number % 2 == 0) {
        return "偶数";
    } else {
        return "奇数";
    }
}

// 関数を呼び出してテスト
echo addNumbers(5, 3) . "\n";
echo greet("太郎") . "\n";
echo checkEvenOdd(4) . "\n";
echo checkEvenOdd(7) . "\n";
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''8
こんにちは、太郎さん！
偶数
奇数''',
                'description': '各関数が正しく動作する'
            }
        ]
    },
    {
        'title': '連想配列の基本操作',
        'description': '''連想配列（キーと値のペア）を使ってデータを管理しましょう。

**課題:**
学生の情報を連想配列で管理し、以下の操作を行ってください：
1. 学生情報の連想配列を作成
2. 新しい情報を追加
3. 特定の情報を取得
4. 全ての情報を表示

**学習目標:**
- 連想配列の作成と操作方法を理解する
- キーと値の概念を学ぶ''',
        'difficulty': 'intermediate',
        'language': 'php',
        'initial_code': '''<?php
// 学生情報を連想配列で管理するプログラムを作成してください

// 1. 学生情報の連想配列を作成
$student = array(
    "name" => "田中太郎",
    "age" => 20,
    "grade" => "大学2年"
);

// 2. 新しい情報（専攻）を追加


// 3. 名前を取得して表示


// 4. 全ての情報を表示


?>''',
        'solution_code': '''<?php
// 1. 学生情報の連想配列を作成
$student = array(
    "name" => "田中太郎",
    "age" => 20,
    "grade" => "大学2年"
);

// 2. 新しい情報（専攻）を追加
$student["major"] = "情報工学";
echo "専攻を追加しました\n";

// 3. 名前を取得して表示
echo "学生名: " . $student["name"] . "\n";

// 4. 全ての情報を表示
echo "学生情報:\n";
foreach ($student as $key => $value) {
    echo "  {$key}: {$value}\n";
}
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''専攻を追加しました
学生名: 田中太郎
学生情報:
  name: 田中太郎
  age: 20
  grade: 大学2年
  major: 情報工学''',
                'description': '連想配列の基本操作が正しく実行される'
            }
        ]
    },
    {
        'title': 'フォーム処理の基本',
        'description': '''PHPでフォームデータを処理する基本を学びましょう。

**課題:**
$_POSTスーパーグローバル変数を使ってフォームデータを処理してください：
1. 名前とメールアドレスを受け取る
2. バリデーション（空チェック）
3. 受け取ったデータを表示

**学習目標:**
- $_POSTの使い方を理解する
- 基本的なバリデーションを学ぶ''',
        'difficulty': 'intermediate',
        'language': 'php',
        'initial_code': '''<?php
// フォームデータ処理プログラムを作成してください
// テスト用データ
$_POST['name'] = '山田太郎';
$_POST['email'] = 'yamada@example.com';

// 1. データを受け取る


// 2. バリデーション（空チェック）


// 3. データを表示


?>''',
        'solution_code': '''<?php
// テスト用データ
$_POST['name'] = '山田太郎';
$_POST['email'] = 'yamada@example.com';

// 1. データを受け取る
$name = isset($_POST['name']) ? $_POST['name'] : '';
$email = isset($_POST['email']) ? $_POST['email'] : '';

// 2. バリデーション（空チェック）
if (empty($name) || empty($email)) {
    echo "エラー: 名前とメールアドレスを入力してください\n";
} else {
    // 3. データを表示
    echo "登録情報:\n";
    echo "名前: {$name}\n";
    echo "メール: {$email}\n";
    echo "登録が完了しました\n";
}
?>''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''登録情報:
名前: 山田太郎
メール: yamada@example.com
登録が完了しました''',
                'description': 'フォームデータが正しく処理される'
            }
        ]
    }
]


def get_connection():
    """RDSデータベース接続を取得"""
    try:
        if not all([DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['database']]):
            logger.error("データベース接続情報が不完全です。.envファイルを確認してください。")
            return None

        connection = pymysql.connect(**DB_CONFIG)
        logger.info("RDSデータベース接続成功")
        return connection
    except Exception as e:
        logger.error(f"RDSデータベース接続エラー: {str(e)}")
        return None


def delete_all_exercises():
    """全ての演習を削除"""
    connection = get_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            # まず既存の演習数を確認
            cursor.execute("SELECT COUNT(*) FROM exercises")
            count = cursor.fetchone()[0]
            logger.info(f"削除対象の演習数: {count}")

            if count > 0:
                # 全ての演習を削除
                cursor.execute("DELETE FROM exercises")
                connection.commit()
                logger.info(f"{count}件の演習を削除しました")
            else:
                logger.info("削除対象の演習がありません")

            return True

    except Exception as e:
        logger.error(f"演習削除エラー: {str(e)}")
        return False
    finally:
        connection.close()


def insert_exercise(exercise_data: Dict[str, Any]) -> bool:
    """演習データを挿入"""
    connection = get_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            # テストケースをJSON形式に変換
            test_cases_json = json.dumps(exercise_data['test_cases'], ensure_ascii=False)

            sql = """
            INSERT INTO exercises (title, description, difficulty, language, initial_code, solution_code, test_cases)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                exercise_data['title'],
                exercise_data['description'],
                exercise_data['difficulty'],
                exercise_data['language'],
                exercise_data['initial_code'],
                exercise_data['solution_code'],
                test_cases_json
            ))

            connection.commit()
            exercise_id = cursor.lastrowid
            logger.info(f"演習 '{exercise_data['title']}' を挿入しました (ID: {exercise_id})")
            return True

    except Exception as e:
        logger.error(f"演習データ挿入エラー: {str(e)}")
        return False
    finally:
        connection.close()


def check_exercises():
    """演習データの確認"""
    connection = get_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM exercises")
            count = cursor.fetchone()[0]
            logger.info(f"現在の演習数: {count}")

            if count > 0:
                cursor.execute("SELECT id, title, language, difficulty FROM exercises ORDER BY id")
                exercises = cursor.fetchall()
                logger.info("演習一覧:")
                for exercise in exercises:
                    logger.info(f"  ID: {exercise[0]}, タイトル: {exercise[1]}, 言語: {exercise[2]}, 難易度: {exercise[3]}")

            return True
    except Exception as e:
        logger.error(f"データ確認エラー: {str(e)}")
        return False
    finally:
        connection.close()


def main():
    """メイン処理"""
    print("=" * 60)
    print("PHPコース設定スクリプト")
    print("=" * 60)

    # 設定確認
    print("\n設定確認:")
    print(f"ホスト: {DB_CONFIG['host']}")
    print(f"ポート: {DB_CONFIG['port']}")
    print(f"データベース: {DB_CONFIG['database']}")
    print(f"ユーザー: {DB_CONFIG['user']}")

    # 既存データの確認
    print("\n1. 既存データの確認...")
    check_exercises()

    # 既存演習の削除
    print("\n2. 既存演習の削除...")
    if delete_all_exercises():
        print("   ✓ 削除完了")
    else:
        print("   ✗ 削除失敗")
        return

    # PHPコースの投入
    print(f"\n3. PHPコース演習データの投入... ({len(PHP_EXERCISES)}件)")
    success_count = 0

    for i, exercise in enumerate(PHP_EXERCISES, 1):
        print(f"  {i}. {exercise['title']} を投入中...")
        if insert_exercise(exercise):
            success_count += 1
            print(f"     ✓ 成功")
        else:
            print(f"     ✗ 失敗")

    # 結果の確認
    print(f"\n4. 投入結果: {success_count}/{len(PHP_EXERCISES)} 件成功")

    # 最終確認
    print("\n5. 最終確認...")
    check_exercises()

    print("\n" + "=" * 60)
    print("PHPコース設定が完了しました！")
    print("=" * 60)


if __name__ == "__main__":
    main()
