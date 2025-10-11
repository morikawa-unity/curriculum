import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore, useAuth as useAuthState, useAuthActions } from "@/store/authStore";
import { AuthService, AuthServiceError } from "@/lib/auth";
import { LoginFormData, RegisterFormData, ConfirmEmailFormData, ForgotPasswordFormData, ResetPasswordFormData } from "@/schemas/auth";

// 認証フックの戻り値の型定義
interface UseAuthReturn {
  // 状態
  user: ReturnType<typeof useAuthState>["user"];
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // アクション
  login: (data: LoginFormData) => Promise<void>;
  register: (data: RegisterFormData) => Promise<void>;
  confirmEmail: (data: ConfirmEmailFormData) => Promise<void>;
  resendConfirmationCode: (email: string) => Promise<void>;
  forgotPassword: (data: ForgotPasswordFormData) => Promise<void>;
  resetPassword: (data: ResetPasswordFormData) => Promise<void>;
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
      const currentUser = await AuthService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      setError("認証状態の確認に失敗しました");
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

      // ダッシュボードにリダイレクト
      router.push("/dashboard");
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  /**
   * 新規登録
   */
  const register = async (data: RegisterFormData): Promise<void> => {
    try {
      setLoading(true);
      clearError();

      await AuthService.register(data.email, data.password, data.preferredUsername);

      // 登録成功後、確認ページにリダイレクト
      router.push(`/auth/confirm-email?email=${encodeURIComponent(data.email)}`);
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  /**
   * メール確認
   */
  const confirmEmail = async (data: ConfirmEmailFormData): Promise<void> => {
    try {
      setLoading(true);
      clearError();

      await AuthService.confirmEmail(data.email, data.confirmationCode);

      // 確認成功後、ログインページにリダイレクト
      router.push("/auth/login?confirmed=true");
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  /**
   * 確認コード再送信
   */
  const resendConfirmationCode = async (email: string): Promise<void> => {
    try {
      setLoading(true);
      clearError();

      await AuthService.resendConfirmationCode(email);
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  /**
   * パスワードリセット要求
   */
  const forgotPassword = async (data: ForgotPasswordFormData): Promise<void> => {
    try {
      setLoading(true);
      clearError();

      await AuthService.forgotPassword(data.email);

      // リセットコード入力ページにリダイレクト
      router.push(`/auth/reset-password?email=${encodeURIComponent(data.email)}`);
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  /**
   * パスワードリセット確認
   */
  const resetPassword = async (data: ResetPasswordFormData): Promise<void> => {
    try {
      setLoading(true);
      clearError();

      await AuthService.confirmResetPassword(data.email, data.confirmationCode, data.newPassword);

      // リセット成功後、ログインページにリダイレクト
      router.push("/auth/login?reset=true");
    } catch (error) {
      const authError = error as AuthServiceError;
      setError(authError.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  /**
   * ログアウト
   */
  const logout = async (): Promise<void> => {
    try {
      setLoading(true);

      await AuthService.logout();
      logoutStore();

      // ログインページにリダイレクト
      router.push("/auth/login");
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
    register,
    confirmEmail,
    resendConfirmationCode,
    forgotPassword,
    resetPassword,
    logout,
    clearError,
    checkAuthState,
  };
};

/**
 * 認証が必要なページで使用するフック
 */
export const useRequireAuth = () => {
  const { isAuthenticated, isLoading, checkAuthState } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // 初回ロード時に認証状態をチェック
    checkAuthState();
  }, []);

  useEffect(() => {
    // ローディング完了後、未認証の場合はログインページにリダイレクト
    if (!isLoading && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, isLoading, router]);

  return { isAuthenticated, isLoading };
};

/**
 * 認証済みユーザーがアクセスできないページで使用するフック
 */
export const useGuestOnly = () => {
  const { isAuthenticated, isLoading, checkAuthState } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // 初回ロード時に認証状態をチェック
    checkAuthState();
  }, []);

  useEffect(() => {
    // ローディング完了後、認証済みの場合はダッシュボードにリダイレクト
    if (!isLoading && isAuthenticated) {
      router.push("/dashboard");
    }
  }, [isAuthenticated, isLoading, router]);

  return { isAuthenticated, isLoading };
};
