#!/usr/bin/env python3
"""
サンプルデータ投入スクリプト
初心者向けプログラミング演習のサンプルデータを作成
"""

import pymysql
import json
import logging
from typing import List, Dict, Any

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# データベース設定
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'programming_learning_app',
    'charset': 'utf8mb4'
}

# サンプル演習データ
SAMPLE_EXERCISES = [
    {
        'title': 'Hello World を出力する',
        'description': '''プログラミングの基本中の基本！
「Hello, World!」という文字列を出力するプログラムを作成してください。

**学習目標:**
- 基本的な出力方法を理解する
- プログラムの実行方法を学ぶ

**ヒント:**
- Pythonでは `print()` 関数を使用します
- 文字列は引用符（"）で囲みます''',
        'difficulty': 'beginner',
        'language': 'python',
        'initial_code': '# Hello, World! を出力してください\n',
        'solution_code': 'print("Hello, World!")',
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
        'description': '''変数を使って値を保存し、計算を行いましょう。

**課題:**
1. 変数 `name` に自分の名前を代入
2. 変数 `age` に年齢を代入
3. 「私の名前は○○で、年齢は○○歳です」という形式で出力

**学習目標:**
- 変数の宣言と代入を理解する
- 文字列の結合方法を学ぶ''',
        'difficulty': 'beginner',
        'language': 'python',
        'initial_code': '''# 変数を使って自己紹介をしてください
name = ""  # ここに名前を入力
age = 0    # ここに年齢を入力

# 自己紹介を出力してください
''',
        'solution_code': '''name = "太郎"
age = 20
print(f"私の名前は{name}で、年齢は{age}歳です")''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '私の名前は太郎で、年齢は20歳です',
                'description': '正しい形式で自己紹介が出力される'
            }
        ]
    },
    {
        'title': '簡単な計算プログラム',
        'description': '''基本的な四則演算を行うプログラムを作成しましょう。

**課題:**
2つの数値を足し算、引き算、掛け算、割り算して結果を出力してください。

**学習目標:**
- 算術演算子の使い方を理解する
- 数値の計算方法を学ぶ

**使用する数値:**
- 数値1: 10
- 数値2: 3''',
        'difficulty': 'beginner',
        'language': 'python',
        'initial_code': '''# 2つの数値で四則演算を行ってください
num1 = 10
num2 = 3

# 足し算の結果を出力
# 引き算の結果を出力
# 掛け算の結果を出力
# 割り算の結果を出力
''',
        'solution_code': '''num1 = 10
num2 = 3

print(f"足し算: {num1} + {num2} = {num1 + num2}")
print(f"引き算: {num1} - {num2} = {num1 - num2}")
print(f"掛け算: {num1} × {num2} = {num1 * num2}")
print(f"割り算: {num1} ÷ {num2} = {num1 / num2}")''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''足し算: 10 + 3 = 13
引き算: 10 - 3 = 7
掛け算: 10 × 3 = 30
割り算: 10 ÷ 3 = 3.3333333333333335''',
                'description': '四則演算の結果が正しく出力される'
            }
        ]
    },
    {
        'title': '条件分岐の基本',
        'description': '''if文を使って条件に応じて異なる処理を行いましょう。

**課題:**
年齢を入力として受け取り、以下の条件で分岐してください：
- 20歳未満: "未成年です"
- 20歳以上65歳未満: "成人です"
- 65歳以上: "高齢者です"

**学習目標:**
- if文の基本的な使い方を理解する
- 条件式の書き方を学ぶ''',
        'difficulty': 'beginner',
        'language': 'python',
        'initial_code': '''# 年齢に応じて分類するプログラムを作成してください
age = 25  # この値を変更してテストしてください

# if文を使って年齢を分類してください
''',
        'solution_code': '''age = 25

if age < 20:
    print("未成年です")
elif age < 65:
    print("成人です")
else:
    print("高齢者です")''',
        'test_cases': [
            {
                'input': 'age = 15',
                'expected_output': '未成年です',
                'description': '20歳未満の場合'
            },
            {
                'input': 'age = 25',
                'expected_output': '成人です',
                'description': '20歳以上65歳未満の場合'
            },
            {
                'input': 'age = 70',
                'expected_output': '高齢者です',
                'description': '65歳以上の場合'
            }
        ]
    },
    {
        'title': 'リストの基本操作',
        'description': '''リスト（配列）を使ってデータを管理しましょう。

**課題:**
果物のリストを作成し、以下の操作を行ってください：
1. リストの全要素を出力
2. リストの長さを出力
3. 新しい果物を追加
4. 特定の果物があるかチェック

**学習目標:**
- リストの作成と操作方法を理解する
- リストの基本メソッドを学ぶ''',
        'difficulty': 'beginner',
        'language': 'python',
        'initial_code': '''# 果物のリストを操作するプログラムを作成してください
fruits = ["りんご", "バナナ", "オレンジ"]

# 1. リストの全要素を出力

# 2. リストの長さを出力

# 3. "ぶどう"を追加

# 4. "バナナ"があるかチェック
''',
        'solution_code': '''fruits = ["りんご", "バナナ", "オレンジ"]

# 1. リストの全要素を出力
print("果物リスト:", fruits)

# 2. リストの長さを出力
print("果物の数:", len(fruits))

# 3. "ぶどう"を追加
fruits.append("ぶどう")
print("追加後:", fruits)

# 4. "バナナ"があるかチェック
if "バナナ" in fruits:
    print("バナナがあります")
else:
    print("バナナがありません")''',
        'test_cases': [
            {
                'input': '',
                'expected_output': '''果物リスト: ['りんご', 'バナナ', 'オレンジ']
果物の数: 3
追加後: ['りんご', 'バナナ', 'オレンジ', 'ぶどう']
バナナがあります''',
                'description': 'リストの基本操作が正しく実行される'
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
- range関数の使い方を学ぶ
- 条件を組み合わせた処理を学ぶ''',
        'difficulty': 'beginner',
        'language': 'python',
        'initial_code': '''# for文を使った繰り返し処理を作成してください

# 1. 1から10までの数値を順番に出力

# 2. 1から10までの数値の合計を計算

# 3. 偶数のみを出力
''',
        'solution_code': '''# 1. 1から10までの数値を順番に出力
print("1から10までの数値:")
for i in range(1, 11):
    print(i)

# 2. 1から10までの数値の合計を計算
total = 0
for i in range(1, 11):
    total += i
print(f"合計: {total}")

# 3. 偶数のみを出力
print("偶数のみ:")
for i in range(1, 11):
    if i % 2 == 0:
        print(i)''',
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
- 引数と戻り値の概念を学ぶ
- 関数の呼び出し方を学ぶ''',
        'difficulty': 'intermediate',
        'language': 'python',
        'initial_code': '''# 関数を定義して使用してください

# 1. 2つの数値を足し算する関数
def add_numbers(a, b):
    # ここに処理を書いてください
    pass

# 2. 名前を受け取って挨拶する関数
def greet(name):
    # ここに処理を書いてください
    pass

# 3. 偶数か奇数かを判定する関数
def check_even_odd(number):
    # ここに処理を書いてください
    pass

# 関数を呼び出してテストしてください
''',
        'solution_code': '''# 1. 2つの数値を足し算する関数
def add_numbers(a, b):
    return a + b

# 2. 名前を受け取って挨拶する関数
def greet(name):
    return f"こんにちは、{name}さん！"

# 3. 偶数か奇数かを判定する関数
def check_even_odd(number):
    if number % 2 == 0:
        return "偶数"
    else:
        return "奇数"

# 関数を呼び出してテスト
print(add_numbers(5, 3))
print(greet("太郎"))
print(check_even_odd(4))
print(check_even_odd(7))''',
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
        'title': '辞書（Dictionary）の基本操作',
        'description': '''辞書を使ってキーと値のペアでデータを管理しましょう。

**課題:**
学生の情報を辞書で管理し、以下の操作を行ってください：
1. 学生情報の辞書を作成
2. 新しい情報を追加
3. 特定の情報を取得
4. 全ての情報を表示

**学習目標:**
- 辞書の作成と操作方法を理解する
- キーと値の概念を学ぶ
- 辞書の基本メソッドを学ぶ''',
        'difficulty': 'intermediate',
        'language': 'python',
        'initial_code': '''# 学生情報を辞書で管理するプログラムを作成してください

# 1. 学生情報の辞書を作成
student = {
    "name": "田中太郎",
    "age": 20,
    "grade": "大学2年"
}

# 2. 新しい情報（専攻）を追加

# 3. 名前を取得して表示

# 4. 全ての情報を表示
''',
        'solution_code': '''# 1. 学生情報の辞書を作成
student = {
    "name": "田中太郎",
    "age": 20,
    "grade": "大学2年"
}

# 2. 新しい情報（専攻）を追加
student["major"] = "情報工学"
print("専攻を追加しました")

# 3. 名前を取得して表示
print(f"学生名: {student['name']}")

# 4. 全ての情報を表示
print("学生情報:")
for key, value in student.items():
    print(f"  {key}: {value}")''',
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
                'description': '辞書の基本操作が正しく実行される'
            }
        ]
    }
]

def get_connection():
    """データベース接続を取得"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        logger.info("データベース接続成功")
        return connection
    except Exception as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        return None

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

def check_existing_data():
    """既存データの確認"""
    connection = get_connection()
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM exercises")
            count = cursor.fetchone()[0]
            logger.info(f"既存の演習数: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, title, difficulty FROM exercises")
                exercises = cursor.fetchall()
                logger.info("既存の演習:")
                for exercise in exercises:
                    logger.info(f"  ID: {exercise[0]}, タイトル: {exercise[1]}, 難易度: {exercise[2]}")
            
            return True
    except Exception as e:
        logger.error(f"データ確認エラー: {str(e)}")
        return False
    finally:
        connection.close()

def main():
    """メイン処理"""
    print("=" * 60)
    print("プログラミング学習アプリ - サンプルデータ投入")
    print("=" * 60)
    
    # 既存データの確認
    print("\n1. 既存データの確認...")
    check_existing_data()
    
    # サンプルデータの投入
    print(f"\n2. サンプル演習データの投入... ({len(SAMPLE_EXERCISES)}件)")
    success_count = 0
    
    for i, exercise in enumerate(SAMPLE_EXERCISES, 1):
        print(f"  {i}. {exercise['title']} を投入中...")
        if insert_exercise(exercise):
            success_count += 1
            print(f"     ✓ 成功")
        else:
            print(f"     ✗ 失敗")
    
    # 結果の確認
    print(f"\n3. 投入結果: {success_count}/{len(SAMPLE_EXERCISES)} 件成功")
    
    # 最終確認
    print("\n4. 最終確認...")
    check_existing_data()
    
    print("\n" + "=" * 60)
    print("サンプルデータ投入が完了しました！")
    print("=" * 60)

if __name__ == "__main__":
    main()