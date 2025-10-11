"use client";

import { useAuth } from "@/hooks/useAuth";

interface LogoutButtonProps {
  className?: string;
  children?: React.ReactNode;
}

/**
 * ログアウトボタンコンポーネント
 */
export const LogoutButton: React.FC<LogoutButtonProps> = ({
  className = "bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors",
  children = "ログアウト",
}) => {
  const { logout, isLoading } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("ログアウトエラー:", error);
    }
  };

  return (
    <button onClick={handleLogout} disabled={isLoading} className={`${className} disabled:opacity-50 disabled:cursor-not-allowed`}>
      {isLoading ? (
        <div className="flex items-center">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          ログアウト中...
        </div>
      ) : (
        children
      )}
    </button>
  );
};
