/**
 * API通信用のユーティリティ関数
 */

import { getCurrentUser } from "aws-amplify/auth";

// API基底URL（環境変数から取得）
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * 認証付きAPIリクエストを送信する
 */
export const fetchAuthenticatedApi = async (endpoint: string, options: RequestInit = {}): Promise<Response> => {
  try {
    // AuthServiceを使用してIDトークンを取得
    const { AuthService } = await import("./auth");
    const token = await AuthService.getIdToken();

    if (!token) {
      throw new Error("認証トークンが取得できませんでした");
    }

    // デフォルトヘッダーを設定
    const defaultHeaders = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    // リクエストオプションをマージ
    const requestOptions: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    // APIリクエストを送信
    const response = await fetch(`${API_BASE_URL}/api/v1${endpoint}`, requestOptions);

    return response;
  } catch (error) {
    console.error("API通信エラー:", error);
    throw error;
  }
};

/**
 * 認証なしAPIリクエストを送信する
 */
export const fetchPublicApi = async (endpoint: string, options: RequestInit = {}): Promise<Response> => {
  try {
    // デフォルトヘッダーを設定
    const defaultHeaders = {
      "Content-Type": "application/json",
    };

    // リクエストオプションをマージ
    const requestOptions: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    // APIリクエストを送信
    const response = await fetch(`${API_BASE_URL}${endpoint}`, requestOptions);

    return response;
  } catch (error) {
    console.error("API通信エラー:", error);
    throw error;
  }
};

/**
 * APIエラーハンドリング用のユーティリティ
 */
export const handleApiError = (error: unknown): string => {
  if (error && typeof error === "object") {
    // サーバーからのエラーレスポンス
    if ("response" in error && error.response && typeof error.response === "object") {
      const response = error.response as { data?: { detail?: string } };
      return response.data?.detail || "サーバーエラーが発生しました";
    }

    // ネットワークエラー
    if ("request" in error) {
      return "ネットワークエラーが発生しました";
    }

    // Error オブジェクトの場合
    if ("message" in error && typeof error.message === "string") {
      return error.message;
    }
  }

  // その他のエラー
  return "予期しないエラーが発生しました";
};
