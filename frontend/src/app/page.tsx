"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function Home() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // 認証状態に応じてリダイレクト
    if (!isLoading) {
      if (isAuthenticated) {
        // 認証済みの場合はホームにリダイレクト
        router.push("/home");
      } else {
        // 未認証の場合はログインページにリダイレクト
        router.push("/login");
      }
    }
  }, [isAuthenticated, isLoading, router]);

  // ローディング中は読み込み画面を表示
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">認証状態を確認中...</p>
        </div>
      </div>
    );
  }

  // リダイレクト処理中は何も表示しない
  return null;
}
