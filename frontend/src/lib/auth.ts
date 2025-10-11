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

// 認証サービスクラス
export class AuthService {
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
      });
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
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * 現在のユーザー情報を取得
   */
  static async getCurrentUser(): Promise<User | null> {
    try {
      // 環境変数が未設定の場合は認証機能を無効化
      if (!process.env.NEXT_PUBLIC_USER_POOL_ID || !process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID) {
        console.warn("AWS Cognito環境変数が未設定のため、認証機能は無効化されています");
        return null;
      }

      const user = await getCurrentUser();
      const session = await fetchAuthSession();

      if (!user || !session.tokens) {
        return null;
      }

      // JWTトークンからユーザー情報を取得
      const idToken = session.tokens.idToken;
      if (!idToken) {
        return null;
      }

      const payload = idToken.payload;

      return {
        userId: user.userId,
        email: payload.email as string,
        preferredUsername: payload.preferred_username as string,
        emailVerified: payload.email_verified as boolean,
        createdAt: new Date(payload.iat! * 1000).toISOString(),
        updatedAt: new Date().toISOString(),
      };
    } catch (error) {
      // ユーザーが認証されていない場合はnullを返す
      return null;
    }
  }

  /**
   * 認証状態をチェック
   */
  static async checkAuthState(): Promise<boolean> {
    try {
      // 環境変数が未設定の場合は認証機能を無効化
      if (!process.env.NEXT_PUBLIC_USER_POOL_ID || !process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID) {
        return false;
      }

      const session = await fetchAuthSession();
      return !!session.tokens?.accessToken;
    } catch (error) {
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
    } catch (error) {
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
    } catch (error) {
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
   * エラーメッセージを日本語に変換
   */
  private static getErrorMessage(errorCode: string): string {
    const errorMessages: Record<string, string> = {
      // ログイン関連
      NotAuthorizedException: "メールアドレスまたはパスワードが正しくありません",
      UserNotConfirmedException: "メールアドレスの確認が完了していません",
      UserNotFoundException: "ユーザーが見つかりません",
      InvalidParameterException: "入力パラメータが無効です",
      InvalidPasswordException: "パスワードが無効です",

      // 新規登録関連
      UsernameExistsException: "このメールアドレスは既に使用されています",
      InvalidParameterException: "入力パラメータが無効です",
      CodeMismatchException: "確認コードが正しくありません",
      ExpiredCodeException: "確認コードの有効期限が切れています",
      LimitExceededException: "試行回数の上限に達しました。しばらく時間をおいてから再試行してください",

      // パスワードリセット関連
      CodeMismatchException: "確認コードが正しくありません",
      ExpiredCodeException: "確認コードの有効期限が切れています",
      InvalidPasswordException: "パスワードが要件を満たしていません",

      // ネットワーク関連
      NetworkError: "ネットワークエラーが発生しました。接続を確認してください",

      // その他
      UNKNOWN_ERROR: "予期しないエラーが発生しました",
    };

    return errorMessages[errorCode] || errorMessages["UNKNOWN_ERROR"];
  }
}
