"use client";

import { useRequireAuth } from "@/hooks/useAuth";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * 認証が必要なページを保護するコンポーネント
 */
export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useRequireAuth();

  // ローディング中は読み込み画面を表示
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">認証状態を確認中...</p>
        </div>
      </div>
    );
  }

  // 認証済みの場合のみ子コンポーネントを表示
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // 未認証の場合は何も表示しない（useRequireAuthでリダイレクト処理される）
  return null;
};
