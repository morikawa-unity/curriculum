export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          {/* 左側：著作権 */}
          <div className="text-sm text-gray-600">
            <p>© 2024 プログラミング学習アプリ. All rights reserved.</p>
          </div>

          {/* 右側：リンク */}
          <div className="flex space-x-6 text-sm text-gray-600">
            <a href="#" className="hover:text-blue-600 transition-colors">
              利用規約
            </a>
            <a href="#" className="hover:text-blue-600 transition-colors">
              プライバシーポリシー
            </a>
            <a href="#" className="hover:text-blue-600 transition-colors">
              お問い合わせ
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
