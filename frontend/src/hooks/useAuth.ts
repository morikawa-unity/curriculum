import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth as useAuthState, useAuthActions } from "@/store/authStore";
import { AuthService, AuthServiceError } from "@/lib/auth";
import { LoginFormData } from "@/schemas/auth";

// 認証フックの戻り値の型定義
interface UseAuthReturn {
  // 状態
  user: ReturnType<typeof useAuthState>["user"];
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // アクション
  login: (data: LoginFormData) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  checkAuthState: () => Promise<void>;
}

/**
 * 認証フック
 */
export const useAuth = (): UseAuthReturn => {
  const { user, isAuthenticated, isLoading, error } = useAuthState();
  const { setUser, setLoading, setError, clearError, logout: logoutStore } = useAuthActions();
  const router = useRouter();

  /**
   * 認証状態をチェック
   */
  const checkAuthState = async (): Promise<void> => {
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
      console.warn("認証状態の確認中にエラーが発生しました:", error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * ログイン
   */
  const login = async (data: LoginFormData): Promise<void> => {
    try {
      setLoading(true);
      clearError();

      await AuthService.login(data.email, data.password);

      // ログイン成功後、ユーザー情報を取得
      const user = await AuthService.getCurrentUser();
      setUser(user);

      // ホームにリダイレクト
      router.push("/home");
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // 新規登録、メール確認、パスワードリセット機能は一旦無効化

  /**
   * ログアウト
   */
  const logout = async (): Promise<void> => {
    try {
      setLoading(true);

      await AuthService.logout();
      logoutStore();

      // ログインページにリダイレクト
      router.push("/login");
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    // 状態
    user,
    isAuthenticated,
    isLoading,
    error,

    // アクション
    login,
    logout,
    clearError,
    checkAuthState,
  };
};

/**
 * 認証が必要なページで使用するフック
 */
export const useRequireAuth = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // ローディング完了後、未認証の場合はログインページにリダイレクト
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  return { isAuthenticated, isLoading };
};

/**
 * 認証済みユーザーがアクセスできないページで使用するフック
 */
export const useGuestOnly = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // ローディング完了後、認証済みの場合はホームにリダイレクト
    if (!isLoading && isAuthenticated) {
      router.push("/home");
    }
  }, [isAuthenticated, isLoading, router]);

  return { isAuthenticated, isLoading };
};
