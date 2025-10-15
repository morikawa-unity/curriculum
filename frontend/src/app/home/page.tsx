"use client";

import Link from "next/link";
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
      <div className="max-w-5xl mx-auto">
        {/* ウェルカムカード */}
        <div className="bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl shadow-2xl p-8 mb-8 border border-blue-300 relative overflow-hidden">
          {/* 背景装飾 */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 right-0 w-64 h-64 bg-white rounded-full -translate-y-1/2 translate-x-1/2"></div>
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white rounded-full translate-y-1/2 -translate-x-1/2"></div>
          </div>

          <div className="flex items-start gap-6 relative z-10">
            {/* アバター */}
            <div className="flex-shrink-0">
              <div className="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center shadow-xl border-4 border-white/30">
                <span className="text-4xl text-white font-bold">{user.preferredUsername?.charAt(0).toUpperCase()}</span>
              </div>
            </div>

            {/* ウェルカムメッセージ */}
            <div className="flex-1">
              <h2 className="text-3xl font-bold text-white mb-2 drop-shadow-lg">ようこそ、{user.preferredUsername}さん！</h2>
              <p className="text-white/90 mb-4 text-lg">今日も学習を始めましょう。下のメニューからコースを選択できます。</p>
              <div className="flex items-center gap-2 text-sm text-white/80 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2 w-fit">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                  />
                </svg>
                <span className="font-medium">{user.email}</span>
              </div>
            </div>
          </div>
        </div>

        {/* クイックアクセス */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/materials"
            className="bg-white rounded-xl shadow-lg p-6 border-2 border-blue-100 hover:border-blue-400 hover:shadow-xl transition-all group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl group-hover:scale-110 transition-transform shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900">学習教材</h3>
              </div>
              <p className="text-sm text-gray-600 leading-relaxed">コースを選択して学習を開始</p>
              <div className="mt-4 flex items-center text-blue-600 font-semibold text-sm group-hover:translate-x-2 transition-transform">
                <span>始める</span>
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>

          <Link
            href="/exercises"
            className="bg-white rounded-xl shadow-lg p-6 border-2 border-cyan-100 hover:border-cyan-400 hover:shadow-xl transition-all group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-gradient-to-br from-cyan-500 to-teal-600 rounded-xl group-hover:scale-110 transition-transform shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900">演習問題</h3>
              </div>
              <p className="text-sm text-gray-600 leading-relaxed">実践的な演習で力をつける</p>
              <div className="mt-4 flex items-center text-cyan-600 font-semibold text-sm group-hover:translate-x-2 transition-transform">
                <span>挑戦する</span>
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>

          <Link
            href="/dashboard"
            className="bg-white rounded-xl shadow-lg p-6 border-2 border-teal-100 hover:border-teal-400 hover:shadow-xl transition-all group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-teal-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-xl group-hover:scale-110 transition-transform shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-bold text-gray-900">ダッシュボード</h3>
              </div>
              <p className="text-sm text-gray-600 leading-relaxed">学習進捗を確認する</p>
              <div className="mt-4 flex items-center text-teal-600 font-semibold text-sm group-hover:translate-x-2 transition-transform">
                <span>確認する</span>
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
