"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";
import Header from "./Header";
import Footer from "./Footer";
import { Bars3Icon, XMarkIcon, ChevronDoubleLeftIcon, ChevronDoubleRightIcon } from "@heroicons/react/24/outline";
import { useAuth as useAuthState } from "@/store/authStore";
import { useAutoLogout } from "@/hooks/useAutoLogout";

interface AppLayoutProps {
  children: React.ReactNode;
}

export default function AppLayout({ children }: AppLayoutProps) {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [desktopSidebarCollapsed, setDesktopSidebarCollapsed] = useState(true); // 初期表示は閉じた状態
  const pathname = usePathname();
  const { isAuthenticated } = useAuthState();

  // 自動ログアウト機能
  useAutoLogout(isAuthenticated);

  // サイドバーを表示しないページのパス
  const hideLayoutPaths = ["/login", "/register", "/auth"];
  const shouldHideLayout = hideLayoutPaths.some((path) => pathname?.startsWith(path));

  // 認証ページではサイドバーなしのシンプルなレイアウト
  if (shouldHideLayout) {
    return <>{children}</>;
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-40 lg:hidden ${mobileSidebarOpen ? "" : "hidden"}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setMobileSidebarOpen(false)} />
        <div className="relative flex w-full max-w-xs flex-1 flex-col bg-gray-900">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex h-10 w-10 items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setMobileSidebarOpen(false)}
            >
              <XMarkIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </button>
          </div>
          <Sidebar isCollapsed={false} />
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:flex lg:flex-shrink-0 relative group">
        <Sidebar isCollapsed={desktopSidebarCollapsed} />

        {/* Desktop sidebar toggle button - より自然な配置 */}
        <button
          type="button"
          className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/2 z-50 h-8 w-8 flex items-center justify-center bg-white border-2 border-gray-300 rounded-full shadow-md hover:shadow-lg hover:border-blue-400 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all opacity-0 group-hover:opacity-100"
          onClick={() => setDesktopSidebarCollapsed(!desktopSidebarCollapsed)}
          title={desktopSidebarCollapsed ? "サイドバーを開く" : "サイドバーを閉じる"}
        >
          {desktopSidebarCollapsed ? (
            <ChevronDoubleRightIcon className="h-5 w-5 text-gray-600" aria-hidden="true" />
          ) : (
            <ChevronDoubleLeftIcon className="h-5 w-5 text-gray-600" aria-hidden="true" />
          )}
        </button>
      </div>

      {/* Main content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <Header />

        {/* Mobile menu button - only on mobile */}
        <div className="lg:hidden fixed top-4 left-4 z-50">
          <button
            type="button"
            className="h-10 w-10 inline-flex items-center justify-center rounded-md bg-white shadow-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            onClick={() => setMobileSidebarOpen(true)}
          >
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>

        {/* Page content + Footer */}
        <div className="flex-1 overflow-y-auto flex flex-col">
          <main className="flex-1">{children}</main>
          <Footer />
        </div>
      </div>
    </div>
  );
}
