import {
  signIn,
  signUp,
  signOut,
  confirmSignUp,
  resendSignUpCode,
  resetPassword,
  confirmResetPassword,
  getCurrentUser,
  fetchAuthSession,
  AuthError,
} from "aws-amplify/auth";
import { User } from "@/schemas/auth";

// 認証エラーの型定義
export interface AuthServiceError {
  code: string;
  message: string;
}

// 認証キャッシュの型定義
interface AuthCache {
  isAuthenticated: boolean;
  timestamp: number;
  user: User | null;
}

// 認証サービスクラス
export class AuthService {
  // 認証状態のキャッシュ（5秒間有効）
  private static authCache: AuthCache | null = null;
  private static readonly CACHE_DURATION = 5000; // 5秒
  /**
   * ログイン
   */
  static async login(email: string, password: string): Promise<void> {
    // 環境変数が未設定の場合はエラーを投げる
    if (!process.env.NEXT_PUBLIC_USER_POOL_ID || !process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID) {
      throw {
        code: "CONFIG_ERROR",
        message: "AWS Cognito環境変数が設定されていません。管理者にお問い合わせください。",
      };
    }

    try {
      await signIn({
        username: email,
        password,
        options: {
          authFlowType: "USER_PASSWORD_AUTH",
        },
      });

      // ログイン成功時にキャッシュをクリアして最新情報を取得
      this.clearAuthCache();
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * 新規登録
   */
  static async register(email: string, password: string, preferredUsername: string): Promise<void> {
    try {
      await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            email,
            preferred_username: preferredUsername,
          },
        },
      });
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * メール確認
   */
  static async confirmEmail(email: string, confirmationCode: string): Promise<void> {
    try {
      await confirmSignUp({
        username: email,
        confirmationCode,
      });
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * 確認コード再送信
   */
  static async resendConfirmationCode(email: string): Promise<void> {
    try {
      await resendSignUpCode({
        username: email,
      });
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * パスワードリセット要求
   */
  static async forgotPassword(email: string): Promise<void> {
    try {
      await resetPassword({
        username: email,
      });
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * パスワードリセット確認
   */
  static async confirmResetPassword(email: string, confirmationCode: string, newPassword: string): Promise<void> {
    try {
      await confirmResetPassword({
        username: email,
        confirmationCode,
        newPassword,
      });
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * ログアウト
   */
  static async logout(): Promise<void> {
    try {
      await signOut();
      // ログアウト時にキャッシュをクリア
      this.clearAuthCache();
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * 現在のユーザー情報を取得（キャッシュ付き）
   */
  static async getCurrentUser(): Promise<User | null> {
    // キャッシュが有効でユーザー情報がある場合はキャッシュを返す
    if (this.authCache && Date.now() - this.authCache.timestamp < this.CACHE_DURATION && this.authCache.user) {
      return this.authCache.user;
    }
    try {
      // 環境変数が未設定の場合は認証機能を無効化
      if (!process.env.NEXT_PUBLIC_USER_POOL_ID || !process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID) {
        console.warn("AWS Cognito環境変数が未設定のため、認証機能は無効化されています");
        return null;
      }

      const authUser = await getCurrentUser();
      const session = await fetchAuthSession();

      if (!authUser || !session.tokens) {
        return null;
      }

      // JWTトークンからユーザー情報を取得
      const idToken = session.tokens.idToken;
      if (!idToken) {
        return null;
      }

      const payload = idToken.payload;
      const cognitoUserId = authUser.userId; // Cognitoのsub

      // バックエンドAPIからユーザー情報を取得
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(`${apiUrl}/api/v1/users/me`, {
          headers: {
            Authorization: `Bearer ${idToken.toString()}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const dbUser = await response.json();
          // DBから取得した情報を使用
          const userInfo: User = {
            userId: cognitoUserId,
            email: dbUser.email || (payload.email as string),
            preferredUsername: dbUser.username || (payload.preferred_username as string) || (payload.name as string),
            emailVerified: payload.email_verified as boolean,
            createdAt: dbUser.created_at || new Date(payload.iat! * 1000).toISOString(),
            updatedAt: dbUser.updated_at || new Date().toISOString(),
          };

          // キャッシュを更新
          this.updateAuthCache(true, userInfo);

          return userInfo;
        }
      } catch (apiError) {
        console.warn("DBからユーザー情報を取得できませんでした。Cognitoの情報を使用します:", apiError);
      }

      // API呼び出しが失敗した場合はCognitoの情報のみ使用
      const fallbackUser: User = {
        userId: cognitoUserId,
        email: payload.email as string,
        preferredUsername: (payload.preferred_username as string) || (payload.name as string),
        emailVerified: payload.email_verified as boolean,
        createdAt: new Date(payload.iat! * 1000).toISOString(),
        updatedAt: new Date().toISOString(),
      };

      // キャッシュを更新
      this.updateAuthCache(true, fallbackUser);

      return fallbackUser;
    } catch {
      // ユーザーが認証されていない場合はnullを返す
      this.updateAuthCache(false, null);
      return null;
    }
  }

  /**
   * 認証状態をチェック（キャッシュ付き）
   */
  static async checkAuthState(): Promise<boolean> {
    try {
      // キャッシュが有効な場合はキャッシュを返す
      if (this.authCache && Date.now() - this.authCache.timestamp < this.CACHE_DURATION) {
        return this.authCache.isAuthenticated;
      }

      // 環境変数が未設定の場合は認証機能を無効化
      if (!process.env.NEXT_PUBLIC_USER_POOL_ID || !process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID) {
        this.updateAuthCache(false, null);
        return false;
      }

      const session = await fetchAuthSession();
      const isAuthenticated = !!session.tokens?.accessToken;

      // キャッシュを更新
      this.updateAuthCache(isAuthenticated, null);

      return isAuthenticated;
    } catch {
      this.updateAuthCache(false, null);
      return false;
    }
  }

  /**
   * アクセストークンを取得
   */
  static async getAccessToken(): Promise<string | null> {
    try {
      const session = await fetchAuthSession();
      return session.tokens?.accessToken?.toString() || null;
    } catch {
      return null;
    }
  }

  /**
   * IDトークンを取得
   */
  static async getIdToken(): Promise<string | null> {
    try {
      const session = await fetchAuthSession();
      return session.tokens?.idToken?.toString() || null;
    } catch {
      return null;
    }
  }

  /**
   * 認証エラーを処理
   */
  private static handleAuthError(error: unknown): AuthServiceError {
    if (error instanceof AuthError) {
      return {
        code: error.name,
        message: this.getErrorMessage(error.name),
      };
    }

    if (error instanceof Error) {
      return {
        code: "UNKNOWN_ERROR",
        message: error.message,
      };
    }

    return {
      code: "UNKNOWN_ERROR",
      message: "予期しないエラーが発生しました",
    };
  }

  /**
   * 認証キャッシュを更新
   */
  private static updateAuthCache(isAuthenticated: boolean, user: User | null): void {
    this.authCache = {
      isAuthenticated,
      user,
      timestamp: Date.now(),
    };
  }

  /**
   * 認証キャッシュをクリア
   */
  private static clearAuthCache(): void {
    this.authCache = null;
  }

  /**
   * エラーメッセージを日本語に変換
   */
  private static getErrorMessage(errorCode: string): string {
    const errorMessages: Record<string, string> = {
      // ログイン関連
      NotAuthorizedException: "メールアドレスまたはパスワードが正しくありません",
      UserNotConfirmedException: "メールアドレスの確認が完了していません",
      UserNotFoundException: "ユーザーが見つかりません",

      // 新規登録関連
      UsernameExistsException: "このメールアドレスは既に使用されています",
      LimitExceededException: "試行回数の上限に達しました。しばらく時間をおいてから再試行してください",

      // 共通エラー
      InvalidParameterException: "入力パラメータが無効です",
      InvalidPasswordException: "パスワードが要件を満たしていません",
      CodeMismatchException: "確認コードが正しくありません",
      ExpiredCodeException: "確認コードの有効期限が切れています",

      // ネットワーク関連
      NetworkError: "ネットワークエラーが発生しました。接続を確認してください",

      // その他
      UNKNOWN_ERROR: "予期しないエラーが発生しました",
    };

    return errorMessages[errorCode] || errorMessages["UNKNOWN_ERROR"];
  }
}
