"use client";

import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import Link from "next/link";
import { BookOpenIcon, ClockIcon } from "@heroicons/react/24/outline";

export default function PHPCoursePage() {
  return (
    <ProtectedRoute>
      <PHPCourseContent />
    </ProtectedRoute>
  );
}

function PHPCourseContent() {
  const lessons = [
    {
      id: 1,
      title: "PHPの基礎 - 環境構築と基本構文",
      description: "PHPの開発環境を構築し、基本的な構文を学びます",
      duration: "30分",
      completed: false,
    },
    {
      id: 2,
      title: "変数とデータ型",
      description: "PHPの変数の宣言方法と様々なデータ型について学びます",
      duration: "25分",
      completed: false,
    },
    {
      id: 3,
      title: "演算子と制御構文",
      description: "算術演算子、比較演算子、if文、switch文などを学びます",
      duration: "35分",
      completed: false,
    },
    {
      id: 4,
      title: "配列の基礎",
      description: "配列の作成、操作、配列関数の使い方を学びます",
      duration: "40分",
      completed: false,
    },
    {
      id: 5,
      title: "ループ処理",
      description: "for、while、foreach文を使った繰り返し処理を学びます",
      duration: "30分",
      completed: false,
    },
    {
      id: 6,
      title: "関数の定義と使用",
      description: "関数の定義方法、引数、戻り値について学びます",
      duration: "35分",
      completed: false,
    },
    {
      id: 7,
      title: "フォーム処理とスーパーグローバル変数",
      description: "$_GET、$_POSTを使ったフォームデータの処理を学びます",
      duration: "45分",
      completed: false,
    },
    {
      id: 8,
      title: "データベース連携 - MySQL入門",
      description: "MySQLデータベースとの接続、CRUD操作の基礎を学びます",
      duration: "50分",
      completed: false,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">
        {/* ヘッダー */}
        <div className="mb-8">
          <Link
            href="/materials"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4 transition-colors"
          >
            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            教材一覧に戻る
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">PHPコース</h1>
          <p className="text-gray-600">PHPの基礎から実践的な開発まで、順を追って学習します</p>
        </div>

        {/* コース情報カード */}
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-md p-6 mb-8 text-white">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-white/20 rounded-lg">
              <BookOpenIcon className="w-8 h-8" />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2">コース概要</h2>
              <p className="mb-4 text-white/90">
                このコースでは、PHPの基礎から実践的なWebアプリケーション開発まで学習します。
                全8レッスンを通じて、PHPプログラミングの基本スキルを習得できます。
              </p>
              <div className="flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <BookOpenIcon className="w-5 h-5" />
                  <span>{lessons.length}レッスン</span>
                </div>
                <div className="flex items-center gap-2">
                  <ClockIcon className="w-5 h-5" />
                  <span>合計 約5時間</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* レッスン一覧 */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">レッスン一覧</h2>
          {lessons.map((lesson, index) => (
            <div
              key={lesson.id}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-200"
            >
              <div className="p-6">
                <div className="flex items-start gap-4">
                  {/* レッスン番号 */}
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {lesson.id}
                  </div>

                  {/* レッスン情報 */}
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{lesson.title}</h3>
                    <p className="text-gray-600 mb-3">{lesson.description}</p>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <div className="flex items-center gap-1">
                        <ClockIcon className="w-4 h-4" />
                        <span>{lesson.duration}</span>
                      </div>
                      {lesson.completed && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          ✓ 完了
                        </span>
                      )}
                    </div>
                  </div>

                  {/* アクションボタン */}
                  <div className="flex-shrink-0">
                    <button
                      className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                      onClick={() => {
                        // TODO: レッスン詳細ページへの遷移
                        alert(`レッスン${lesson.id}は現在準備中です`);
                      }}
                    >
                      {lesson.completed ? "復習する" : "開始する"}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* 進捗状況 */}
        <div className="mt-8 bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4">学習進捗</h3>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-blue-500 to-purple-600 h-full rounded-full transition-all"
                  style={{ width: "0%" }}
                ></div>
              </div>
            </div>
            <span className="text-sm font-medium text-gray-600">0 / {lessons.length} 完了</span>
          </div>
        </div>
      </div>
    </div>
  );
}
