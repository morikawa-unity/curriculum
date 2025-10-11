"use client";

import Link from "next/link";

export default function Exercises() {
  const exercises = [
    { id: "1", title: "Hello World", difficulty: "初級" },
    { id: "2", title: "変数と演算", difficulty: "初級" },
    { id: "3", title: "条件分岐", difficulty: "中級" },
  ];

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <Link href="/" className="text-blue-600 hover:underline">
            ← ホームに戻る
          </Link>
        </div>

        <h1 className="text-3xl font-bold mb-8">演習一覧</h1>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="border rounded-lg p-6">
              <h3 className="text-xl font-semibold mb-2">{exercise.title}</h3>
              <p className="text-gray-600 mb-4">{exercise.difficulty}</p>
              <Link href={`/exercises/${exercise.id}`} className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                開始する
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
