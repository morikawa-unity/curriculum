import { useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuthActions } from "@/store/authStore";
import { AuthService } from "@/lib/auth";

// 自動ログアウトまでの時間（ミリ秒）
// テスト用: 10秒でログアウトする場合は下記をコメントアウト解除
// const AUTO_LOGOUT_TIME = 10 * 1000; // 10秒
const AUTO_LOGOUT_TIME = 75 * 60 * 1000; // 75分

/**
 * 自動ログアウトフック
 * 一定時間操作がない場合に自動的にログアウトする
 */
export const useAutoLogout = (isAuthenticated: boolean) => {
  const router = useRouter();
  const { logout: logoutStore } = useAuthActions();
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleLogout = useCallback(async () => {
    try {
      await AuthService.logout();
      logoutStore();
      router.push("/login?timeout=true");
    } catch (error) {
      console.error("自動ログアウトエラー:", error);
    }
  }, [logoutStore, router]);

  const resetTimer = useCallback(() => {
    // 既存のタイマーをクリア
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // 認証済みの場合のみタイマーを設定
    if (isAuthenticated) {
      // 自動ログアウトタイマー
      timeoutRef.current = setTimeout(() => {
        handleLogout();
      }, AUTO_LOGOUT_TIME);
    }
  }, [isAuthenticated, handleLogout]);

  useEffect(() => {
    if (!isAuthenticated) {
      return;
    }

    // 初期タイマー設定
    resetTimer();

    // マウス移動を監視してユーザーアクティビティを検知
    const handleMouseMove = () => {
      resetTimer();
    };

    // イベントリスナーを追加
    document.addEventListener("mousemove", handleMouseMove);

    // クリーンアップ
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      document.removeEventListener("mousemove", handleMouseMove);
    };
  }, [isAuthenticated, resetTimer]);
};
