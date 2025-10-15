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
    color: "from-blue-500 to-cyan-600",
  },
];

export default function MaterialsPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* ヘッダー */}
        <div className="mb-8 ml-2">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
            学習教材
          </h1>
        </div>

        {/* コース選択画面 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Link
              key={course.id}
              href={`/materials/${course.id}`}
              className="bg-white rounded-2xl shadow-lg p-6 transition-all hover:shadow-2xl border-2 border-blue-100 hover:border-blue-400 block group relative overflow-hidden"
            >
              {/* ホバー時の背景 */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>

              <div className="relative z-10">
                {/* コースアイコン */}
                <div className={`inline-block p-5 bg-gradient-to-br ${course.color} rounded-2xl shadow-xl mb-4 group-hover:scale-110 transition-transform`}>
                  <span className="text-5xl">{course.icon}</span>
                </div>

                {/* コース情報 */}
                <h2 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">{course.title}</h2>
                <p className="text-gray-600 mb-5 text-sm leading-relaxed">{course.description}</p>

                {/* メタ情報 */}
                <div className="flex items-center gap-3 text-sm text-gray-600 mb-4 flex-wrap">
                  <div className="flex items-center gap-2 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-100">
                    <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span className="font-medium">{course.level}</span>
                  </div>
                  <div className="flex items-center gap-2 bg-cyan-50 px-3 py-1.5 rounded-lg border border-cyan-100">
                    <svg className="w-4 h-4 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                      />
                    </svg>
                    <span className="font-medium">{course.lessons}レッスン</span>
                  </div>
                </div>

                {/* プログレスバー */}
                <div className="mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-gray-600">進捗</span>
                    <span className="text-xs font-bold text-gray-700">0%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                    <div className={`bg-gradient-to-r ${course.color} h-full rounded-full transition-all`} style={{ width: "0%" }}></div>
                  </div>
                </div>

                {/* 開始ボタン */}
                <div className={`w-full bg-gradient-to-r ${course.color} text-white font-bold py-3 px-4 rounded-xl text-center group-hover:shadow-xl transition-all flex items-center justify-center gap-2`}>
                  <span>コースを開始</span>
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
