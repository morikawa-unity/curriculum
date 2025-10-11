"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        {/* ヘッダー */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">プログラミング学習アプリ</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">ようこそ、ユーザーさん</span>
            <Link href="/login" className="text-blue-600 hover:underline">
              ログアウト
            </Link>
          </div>
        </div>

        {/* メインコンテンツ */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">学習を開始</h2>
            <p className="text-gray-600 mb-4">プログラミングの基礎から応用まで、段階的に学習を進めましょう。</p>
            <Link href="/exercises" className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
              演習を始める
            </Link>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">学習進捗</h2>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">完了した演習</span>
                <span className="text-sm font-medium">0/6</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: "0%" }}></div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">最近の活動</h2>
            <p className="text-gray-600 text-sm">
              まだ演習を開始していません。
              <br />
              最初の演習から始めてみましょう！
            </p>
          </div>
        </div>

        {/* 学習コンテンツ */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-6">学習コンテンツ</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-4 border rounded-lg">
              <div className="text-3xl mb-2">📚</div>
              <h3 className="text-lg font-semibold mb-2">基礎から学習</h3>
              <p className="text-gray-600 text-sm">プログラミングの基礎から段階的に学習できます</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <div className="text-3xl mb-2">💻</div>
              <h3 className="text-lg font-semibold mb-2">実践的な演習</h3>
              <p className="text-gray-600 text-sm">実際のコードを書いて理解を深めます</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="text-lg font-semibold mb-2">進捗管理</h3>
              <p className="text-gray-600 text-sm">学習の進捗を可視化して継続をサポート</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
