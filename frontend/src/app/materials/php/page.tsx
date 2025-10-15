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
        <div className="mb-2">
          <Link
            href="/materials"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4 transition-colors font-semibold group"
          >
            <svg className="w-5 h-5 mr-1 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            教材一覧に戻る
          </Link>
        </div>

        {/* コース情報カード */}
        <div className="bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl shadow-2xl p-8 mb-8 text-white border border-blue-300 relative overflow-hidden">
          {/* 背景装飾 */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full -translate-y-1/2 translate-x-1/2"></div>
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white rounded-full translate-y-1/2 -translate-x-1/2"></div>
          </div>

          <div className="flex items-start gap-6 relative z-10">
            <div className="p-4 bg-white/20 backdrop-blur-sm rounded-2xl shadow-lg border-2 border-white/30">
              <BookOpenIcon className="w-10 h-10" />
            </div>
            <div className="flex-1">
              <h2 className="text-3xl font-bold mb-3 drop-shadow-lg">コース概要</h2>
              <p className="mb-4 text-white/95 text-lg leading-relaxed">
                PHPの基礎から実践的な開発まで、順を追って学習します。
                このコースでは、PHPの基礎から実践的なWebアプリケーション開発まで学習します。
                全8レッスンを通じて、PHPプログラミングの基本スキルを習得できます。
              </p>
              <div className="flex items-center gap-8 text-sm">
                <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
                  <BookOpenIcon className="w-5 h-5" />
                  <span className="font-semibold">{lessons.length}レッスン</span>
                </div>
                <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
                  <ClockIcon className="w-5 h-5" />
                  <span className="font-semibold">合計 約5時間</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* 学習進捗 */}
        <div className="mb-8 bg-white rounded-xl shadow-lg p-6 border-2 border-blue-100 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-50"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">学習進捗</h3>
              <span className="text-sm font-bold text-gray-700 bg-blue-50 px-4 py-2 rounded-lg">0 / {lessons.length} 完了</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex-1">
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden shadow-inner">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-cyan-600 h-full rounded-full transition-all shadow-lg"
                    style={{ width: "0%" }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>


        {/* レッスン一覧 */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent mb-6">レッスン一覧</h2>
          {lessons.map((lesson, index) => (
            <div
              key={lesson.id}
              className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all border-2 border-blue-100 hover:border-blue-400 group relative overflow-hidden"
            >
              {/* ホバー時の背景 */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>

              <div className="p-6 relative z-10">
                <div className="flex items-start gap-6">
                  {/* レッスン番号 */}
                  <div className="flex-shrink-0 w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl shadow-lg group-hover:scale-110 transition-transform">
                    {lesson.id}
                  </div>

                  {/* レッスン情報 */}
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-700 transition-colors">{lesson.title}</h3>
                    <p className="text-gray-600 mb-4 leading-relaxed">{lesson.description}</p>
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-2 bg-cyan-50 px-3 py-1.5 rounded-lg">
                        <ClockIcon className="w-4 h-4 text-cyan-600" />
                        <span className="font-medium">{lesson.duration}</span>
                      </div>
                      {lesson.completed && (
                        <span className="inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold bg-green-100 text-green-800">
                          ✓ 完了
                        </span>
                      )}
                    </div>
                  </div>

                  {/* アクションボタン */}
                  <div className="flex-shrink-0">
                    <button
                      className="px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-cyan-700 transition-all shadow-lg transform hover:scale-105 active:scale-95 flex items-center gap-2"
                      onClick={() => {
                        // TODO: レッスン詳細ページへの遷移
                        alert(`レッスン${lesson.id}は現在準備中です`);
                      }}
                    >
                      <span>{lesson.completed ? "復習する" : "開始する"}</span>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
