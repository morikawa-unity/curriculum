"use client";

import { BookOpenIcon, PlayIcon } from "@heroicons/react/24/outline";

const materials = [
  {
    id: 1,
    title: "JavaScript基礎",
    description: "JavaScriptの基本的な文法と概念を学習します",
    duration: "2時間",
    level: "初級",
    topics: ["変数", "関数", "配列", "オブジェクト"],
  },
  {
    id: 2,
    title: "React入門",
    description: "Reactの基本的な使い方とコンポーネントの作成方法",
    duration: "3時間",
    level: "中級",
    topics: ["コンポーネント", "Props", "State", "Hooks"],
  },
  {
    id: 3,
    title: "TypeScript基礎",
    description: "TypeScriptの型システムと基本的な使い方",
    duration: "2.5時間",
    level: "中級",
    topics: ["型注釈", "インターフェース", "ジェネリクス", "型推論"],
  },
  {
    id: 4,
    title: "Next.js入門",
    description: "Next.jsを使ったWebアプリケーション開発",
    duration: "4時間",
    level: "上級",
    topics: ["ルーティング", "SSR", "API Routes", "デプロイ"],
  },
];

const getLevelColor = (level: string) => {
  switch (level) {
    case "初級":
      return "bg-green-100 text-green-800";
    case "中級":
      return "bg-yellow-100 text-yellow-800";
    case "上級":
      return "bg-red-100 text-red-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

export default function MaterialsPage() {
  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">教材</h1>
        <p className="text-gray-600">プログラミングの基礎から応用まで、段階的に学習できる教材を提供しています。</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {materials.map((material) => (
          <div key={material.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <BookOpenIcon className="h-8 w-8 text-blue-600" />
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(material.level)}`}>{material.level}</span>
              </div>

              <h3 className="text-xl font-semibold text-gray-900 mb-2">{material.title}</h3>

              <p className="text-gray-600 mb-4">{material.description}</p>

              <div className="mb-4">
                <p className="text-sm text-gray-500 mb-2">学習時間: {material.duration}</p>
                <div className="flex flex-wrap gap-1">
                  {material.topics.map((topic, index) => (
                    <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                      {topic}
                    </span>
                  ))}
                </div>
              </div>

              <button className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors duration-200">
                <PlayIcon className="h-4 w-4 mr-2" />
                学習を開始
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
