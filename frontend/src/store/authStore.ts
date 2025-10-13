import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";
import { User } from "@/schemas/auth";

// 認証状態の型定義
interface AuthState {
  // 状態
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // アクション
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  logout: () => void;
  reset: () => void;
}

// 初期状態
const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: true, // 初期ロード時はtrue
  error: null,
};

// Zustand認証ストア
export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // ユーザー情報を設定
        setUser: (user: User | null) => {
          set(
            {
              user,
              isAuthenticated: !!user,
              error: null,
            },
            false,
            "auth/setUser"
          );
        },

        // ローディング状態を設定
        setLoading: (loading: boolean) => {
          set({ isLoading: loading }, false, "auth/setLoading");
        },

        // エラーを設定
        setError: (error: string | null) => {
          set({ error, isLoading: false }, false, "auth/setError");
        },

        // エラーをクリア
        clearError: () => {
          set({ error: null }, false, "auth/clearError");
        },

        // ログアウト
        logout: () => {
          set(
            {
              user: null,
              isAuthenticated: false,
              isLoading: false,
              error: null,
            },
            false,
            "auth/logout"
          );
        },

        // 状態をリセット
        reset: () => {
          set(initialState, false, "auth/reset");
        },
      }),
      {
        name: "auth-storage", // localStorage のキー名
        partialize: (state) => ({
          // 永続化する状態を選択（isLoadingとerrorは除外）
          user: state.user,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    ),
    {
      name: "auth-store", // DevTools での表示名
    }
  )
);

// セレクター関数（パフォーマンス最適化用）
export const useAuth = () =>
  useAuthStore((state) => ({
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    error: state.error,
  }));

export const useAuthActions = () =>
  useAuthStore((state) => ({
    setUser: state.setUser,
    setLoading: state.setLoading,
    setError: state.setError,
    clearError: state.clearError,
    logout: state.logout,
    reset: state.reset,
  }));
