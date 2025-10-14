/**
 * プロフィール関連のAPIサービス
 * API ID: PR0101 - プロフィール機能
 */

import { fetchAuthenticatedApi } from "@/lib/api";

/**
 * PR0101001 APIのレスポンス型定義
 */
export interface PR0101001Response {
  id: string;
  email: string;
  username: string;
  role: number;
  created_at: string;
  updated_at: string;
}

/**
 * API ID: PR0101001
 * ユーザープロフィール情報取得API
 *
 * @returns Promise<PR0101001Response> ユーザープロフィール情報
 * @throws Error API呼び出しエラー
 */
export const PR0101001 = async (): Promise<PR0101001Response> => {
  try {
    const response = await fetchAuthenticatedApi("/users/profile/PR0101001");

    if (!response.ok) {
      throw new Error(`PR0101001 API エラー: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("PR0101001 API エラー:", error);
    throw error;
  }
};

// 後方互換性のためのエイリアス（必要に応じて削除可能）
export const getUserProfile = PR0101001;
export type UserProfile = PR0101001Response;
