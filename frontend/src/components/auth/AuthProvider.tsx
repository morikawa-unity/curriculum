"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";
import { AuthService } from "@/lib/auth";

interface AuthProviderProps {
  children: React.ReactNode;
}

/**
 * 認証プロバイダーコンポーネント
 * アプリケーション全体で認証状態を管理
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { setUser, setLoading, clearError } = useAuthStore();

  useEffect(() => {
    // アプリケーション起動時に認証状態をチェック
    const checkInitialAuthState = async () => {
      try {
        setLoading(true);
        clearError();

        // 認証状態をチェック
        const isAuthenticated = await AuthService.checkAuthState();

        if (isAuthenticated) {
          // 認証済みの場合、ユーザー情報を取得
          const currentUser = await AuthService.getCurrentUser();
          setUser(currentUser);
        } else {
          // 未認証の場合、ユーザー情報をクリア
          setUser(null);
        }
      } catch (error) {
        // エラーが発生した場合は未認証として扱う
        setUser(null);
        console.warn("初期認証状態の確認中にエラーが発生しました:", error);
      } finally {
        setLoading(false);
      }
    };

    checkInitialAuthState();
  }, [setUser, setLoading, clearError]);

  return <>{children}</>;
};
