"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { UserCircleIcon, ArrowRightOnRectangleIcon } from "@heroicons/react/24/outline";
import { useAuth } from "@/hooks/useAuth";

export default function Header() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const { user, logout } = useAuth();
  const router = useRouter();
  const dropdownRef = useRef<HTMLDivElement>(null);

  // ドロップダウン外側クリックで閉じる
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/login");
    } catch (error) {
      console.error("ログアウトエラー:", error);
    }
  };

  const handleProfileClick = () => {
    setDropdownOpen(false);
    router.push("/profile");
  };

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* 左側：タイトル（デスクトップのみ表示） */}
          <div className="hidden lg:block">
            <h1 className="text-xl font-semibold text-gray-900">学習アプリ</h1>
          </div>

          {/* 中央：空白（モバイルでは非表示） */}
          <div className="flex-1" />

          {/* 右側：ユーザーアイコン */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-2 rounded-full p-1 hover:bg-gray-100 transition-colors"
            >
              {user?.preferredUsername ? (
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-lg text-white font-bold">
                    {user.preferredUsername.charAt(0).toUpperCase()}
                  </span>
                </div>
              ) : (
                <UserCircleIcon className="w-10 h-10 text-gray-400" />
              )}
            </button>

            {/* ドロップダウンメニュー */}
            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
                <div className="py-1">
                  {/* ユーザー情報 */}
                  {user && (
                    <div className="px-4 py-3 border-b border-gray-200">
                      <p className="text-sm font-medium text-gray-900">{user.preferredUsername}</p>
                      <p className="text-xs text-gray-500 truncate">{user.email}</p>
                    </div>
                  )}

                  {/* プロフィール */}
                  <button
                    onClick={handleProfileClick}
                    className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                  >
                    <UserCircleIcon className="w-5 h-5 text-gray-400" />
                    プロフィール
                  </button>

                  {/* ログアウト */}
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2 border-t border-gray-200"
                  >
                    <ArrowRightOnRectangleIcon className="w-5 h-5 text-red-600" />
                    ログアウト
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
