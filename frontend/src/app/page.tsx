"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="text-center max-w-2xl">
        <h1 className="text-4xl font-bold mb-6">プログラミング学習アプリ</h1>
        <p className="text-lg text-gray-600 mb-8">効率的にプログラミングスキルを向上させるための学習アプリケーション</p>

        <Link href="/exercises" className="inline-block px-8 py-3 bg-blue-600 text-white text-lg rounded-lg hover:bg-blue-700 transition-colors">
          演習を始める
        </Link>
      </div>
    </div>
  );
}
