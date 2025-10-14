"use client";

export default function ExercisesPage() {

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center">
        {/* アイコン */}
        <div className="mb-8">
          <div className="inline-block p-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full shadow-2xl">
            <span className="text-7xl">🚀</span>
          </div>
        </div>

        {/* タイトル */}
        <h1 className="text-5xl font-bold text-gray-900 mb-4">Coming Soon</h1>

        {/* 説明 */}
        <p className="text-xl text-gray-600 mb-8">
          演習機能は現在開発中です
        </p>

        {/* 詳細メッセージ */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <p className="text-gray-700 leading-relaxed">
            プログラミング演習機能を準備中です。<br />
            近日中に公開予定ですので、もうしばらくお待ちください。
          </p>
        </div>
      </div>
    </div>
  );
}
