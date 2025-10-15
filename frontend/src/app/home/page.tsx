"use client";

import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { useAuth } from "@/hooks/useAuth";

export default function Home() {
  return (
    <ProtectedRoute>
      <HomeContent />
    </ProtectedRoute>
  );
}

function HomeContent() {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* ヘッダー */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🏠 ホーム</h1>
          <p className="text-gray-600">プログラミング学習アプリへようこそ</p>
        </div>

        {/* ウェルカムカード */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8 border border-gray-200">
          <div className="flex items-start gap-6">
            {/* アバター */}
            <div className="flex-shrink-0">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                <span className="text-4xl text-white font-bold">
                  {user.preferredUsername?.charAt(0).toUpperCase()}
                </span>
              </div>
            </div>

            {/* ウェルカムメッセージ */}
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                ようこそ、{user.preferredUsername}さん！
              </h2>
              <p className="text-gray-600 mb-4">
                今日も学習を始めましょう。下のメニューからコースを選択できます。
              </p>
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>{user.email}</span>
              </div>
            </div>
          </div>
        </div>

        {/* クイックアクセス */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <a
            href="/materials"
            className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:border-blue-400 hover:shadow-lg transition-all group"
          >
            <div className="flex items-center gap-4 mb-3">
              <div className="p-3 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                <span className="text-2xl">📚</span>
              </div>
              <h3 className="text-lg font-bold text-gray-900">学習教材</h3>
            </div>
            <p className="text-sm text-gray-600">コースを選択して学習を開始</p>
          </a>

          <a
            href="/exercises"
            className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:border-purple-400 hover:shadow-lg transition-all group"
          >
            <div className="flex items-center gap-4 mb-3">
              <div className="p-3 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
                <span className="text-2xl">📝</span>
              </div>
              <h3 className="text-lg font-bold text-gray-900">演習問題</h3>
            </div>
            <p className="text-sm text-gray-600">実践的な演習で力をつける</p>
          </a>

          <a
            href="/dashboard"
            className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:border-indigo-400 hover:shadow-lg transition-all group"
          >
            <div className="flex items-center gap-4 mb-3">
              <div className="p-3 bg-indigo-100 rounded-lg group-hover:bg-indigo-200 transition-colors">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-lg font-bold text-gray-900">ダッシュボード</h3>
            </div>
            <p className="text-sm text-gray-600">学習進捗を確認する</p>
          </a>
        </div>
      </div>
    </div>
  );
}
