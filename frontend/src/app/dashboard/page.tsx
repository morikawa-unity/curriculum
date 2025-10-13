"use client";

import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { LogoutButton } from "@/components/auth/LogoutButton";
import { useAuth } from "@/hooks/useAuth";

export default function Dashboard() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}

function DashboardContent() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">プログラミング学習アプリ</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">こんにちは、{user?.preferredUsername || user?.email}さん</span>
              <LogoutButton />
            </div>
          </div>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-8">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">ダッシュボード</h2>
              <p className="text-gray-600 mb-8">プログラミング学習アプリへようこそ！</p>

              {/* ユーザー情報カード */}
              <div className="bg-white rounded-lg shadow p-6 max-w-md mx-auto">
                <h3 className="text-lg font-medium text-gray-900 mb-4">ユーザー情報</h3>
                <div className="space-y-2 text-left">
                  <div className="flex justify-between">
                    <span className="text-gray-600">ユーザーID:</span>
                    <span className="text-gray-900 font-mono text-sm">{user?.userId}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">メールアドレス:</span>
                    <span className="text-gray-900">{user?.email}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">ユーザー名:</span>
                    <span className="text-gray-900">{user?.preferredUsername || "未設定"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">メール確認:</span>
                    <span className={`${user?.emailVerified ? "text-green-600" : "text-red-600"}`}>{user?.emailVerified ? "確認済み" : "未確認"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">登録日:</span>
                    <span className="text-gray-900">{user?.createdAt ? new Date(user.createdAt).toLocaleDateString("ja-JP") : "不明"}</span>
                  </div>
                </div>
              </div>

              {/* 今後の機能プレビュー */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <h4 className="text-lg font-medium text-gray-900 mb-2">学習コース</h4>
                  <p className="text-gray-600 text-sm">プログラミングの基礎から応用まで学べるコースを提供予定</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <h4 className="text-lg font-medium text-gray-900 mb-2">進捗管理</h4>
                  <p className="text-gray-600 text-sm">学習の進捗を可視化し、モチベーションを維持</p>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <h4 className="text-lg font-medium text-gray-900 mb-2">コード実行</h4>
                  <p className="text-gray-600 text-sm">ブラウザ上でコードを実行し、即座に結果を確認</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
