import Link from "next/link";

// コース情報の型定義
interface Course {
  id: string;
  title: string;
  description: string;
  icon: string;
  level: string;
  lessons: number;
  color: string;
}

// コース一覧データ
const courses: Course[] = [
  {
    id: "php",
    title: "PHPコース",
    description: "Web開発の基礎となるPHPを学びます。変数、配列、関数などの基本から、フォーム処理まで段階的に習得できます。",
    icon: "🐘",
    level: "初級〜中級",
    lessons: 8,
    color: "from-purple-500 to-indigo-600",
  },
];

export default function MaterialsPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* ヘッダー */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📚 学習教材
          </h1>
          <p className="text-gray-600">コースを選択して学習を始めましょう</p>
        </div>

        {/* コース選択画面 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Link
              key={course.id}
              href={`/materials/${course.id}`}
              className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg border border-gray-200 hover:border-gray-300 block"
            >
              {/* コースアイコン */}
              <div className={`inline-block p-4 bg-gradient-to-br ${course.color} rounded-2xl shadow-lg mb-4`}>
                <span className="text-4xl">{course.icon}</span>
              </div>

              {/* コース情報 */}
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{course.title}</h2>
              <p className="text-gray-600 mb-4 text-sm leading-relaxed">{course.description}</p>

              {/* メタ情報 */}
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                  <span>{course.level}</span>
                </div>
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                    />
                  </svg>
                  <span>{course.lessons}レッスン</span>
                </div>
              </div>

              {/* 開始ボタンテキスト */}
              <div className="mt-6 w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg text-center">
                コースを開始
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
