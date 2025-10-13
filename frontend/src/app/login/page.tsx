"use client";

// 動的レンダリングを強制
export const dynamic = "force-dynamic";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth, useGuestOnly } from "@/hooks/useAuth";
import { loginSchema, LoginFormData } from "@/schemas/auth";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

function LoginForm() {
  const { login, isLoading, error, clearError } = useAuth();
  const { isLoading: authLoading } = useGuestOnly();
  const searchParams = useSearchParams();

  // URL パラメータからメッセージを取得
  const confirmed = searchParams?.get("confirmed");
  const reset = searchParams?.get("reset");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    clearError();
    try {
      await login(data);
    } catch (error) {
      // エラーは useAuth フック内で処理される
    }
  };

  // 認証状態チェック中はローディング表示
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center p-8 bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8 bg-gray-50">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">ログイン</h1>
            <p className="text-gray-600">プログラミング学習アプリ</p>
          </div>

          {/* 成功メッセージ */}
          {confirmed && (
            <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md">
              メールアドレスの確認が完了しました。ログインしてください。
            </div>
          )}

          {reset && (
            <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md">
              パスワードがリセットされました。新しいパスワードでログインしてください。
            </div>
          )}

          {/* エラーメッセージ */}
          {error && <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">{error}</div>}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                メールアドレス
              </label>
              <input
                type="email"
                id="email"
                {...register("email")}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.email ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="your@example.com"
              />
              {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                パスワード
              </label>
              <input
                type="password"
                id="password"
                {...register("password")}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.password ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="パスワードを入力"
              />
              {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  ログイン中...
                </div>
              ) : (
                "ログイン"
              )}
            </button>
          </form>

          <div className="mt-6 text-center space-y-2">
            <p className="text-sm text-gray-600">
              アカウントをお持ちでない方は{" "}
              <Link href="/register" className="text-blue-600 hover:underline">
                新規登録
              </Link>
            </p>
            <p className="text-sm text-gray-600">
              <Link href="/auth/forgot-password" className="text-blue-600 hover:underline">
                パスワードを忘れた方はこちら
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Login() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center p-8 bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    }>
      <LoginForm />
    </Suspense>
  );
}
