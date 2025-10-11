"use client";

/* eslint-disable react/no-unescaped-entities */
import Link from "next/link";

interface ExerciseClientProps {
  id: string;
}

export function ExerciseClient({ id }: ExerciseClientProps) {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <Link href="/exercises" className="text-blue-600 hover:underline">
            ← 演習一覧に戻る
          </Link>
        </div>

        <h1 className="text-3xl font-bold mb-4">演習 {id}: Hello World</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">問題説明</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p>コンソールに "Hello, World!&quot; を出力するプログラムを作成してください。</p>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">コードエディター</h2>
            <textarea
              className="w-full h-64 p-4 border rounded-lg font-mono text-sm"
              defaultValue="// ここにコードを書いてください"
              placeholder="ここにコードを入力してください..."
            />

            <div className="flex gap-4 mt-4">
              <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">実行</button>
              <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">提出</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
