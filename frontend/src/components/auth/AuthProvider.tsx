"use client";

import { useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";

interface AuthProviderProps {
  children: React.ReactNode;
}

/**
 * 認証プロバイダーコンポーネント
 * アプリケーション全体で認証状態を管理
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { checkAuthState } = useAuth();

  useEffect(() => {
    // アプリケーション起動時に認証状態をチェック
    checkAuthState();
  }, [checkAuthState]);

  return <>{children}</>;
};
