"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth, useGuestOnly } from "@/hooks/useAuth";
import { resetPasswordSchema, ResetPasswordFormData } from "@/schemas/auth";
import { useSearchParams } from "next/navigation";

export default function ResetPassword() {
  const { resetPassword, isLoading, error, clearError } = useAuth();
  const { isLoading: authLoading } = useGuestOnly();
  const searchParams = useSearchParams();

  // URL パラメータからメールアドレスを取得
  const emailFromUrl = searchParams?.get("email") || "";

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      email: emailFromUrl,
    },
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    clearError();
    try {
      await resetPassword(data);
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">新しいパスワード設定</h1>
            <p className="text-gray-600">メールに送信された確認コードと新しいパスワードを入力してください</p>
          </div>

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
                readOnly={!!emailFromUrl}
              />
              {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
            </div>

            <div>
              <label htmlFor="confirmationCode" className="block text-sm font-medium text-gray-700 mb-2">
                確認コード
              </label>
              <input
                type="text"
                id="confirmationCode"
                {...register("confirmationCode")}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center text-lg tracking-widest ${
                  errors.confirmationCode ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="123456"
                maxLength={6}
              />
              {errors.confirmationCode && <p className="mt-1 text-sm text-red-600">{errors.confirmationCode.message}</p>}
              <p className="mt-1 text-xs text-gray-500">メールに記載された6桁の数字を入力してください</p>
            </div>

            <div>
              <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-2">
                新しいパスワード
              </label>
              <input
                type="password"
                id="newPassword"
                {...register("newPassword")}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.newPassword ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="新しいパスワードを入力"
              />
              {errors.newPassword && <p className="mt-1 text-sm text-red-600">{errors.newPassword.message}</p>}
              <p className="mt-1 text-xs text-gray-500">8文字以上、大文字・小文字・数字を含む</p>
            </div>

            <div>
              <label htmlFor="confirmNewPassword" className="block text-sm font-medium text-gray-700 mb-2">
                新しいパスワード確認
              </label>
              <input
                type="password"
                id="confirmNewPassword"
                {...register("confirmNewPassword")}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.confirmNewPassword ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="新しいパスワードを再入力"
              />
              {errors.confirmNewPassword && <p className="mt-1 text-sm text-red-600">{errors.confirmNewPassword.message}</p>}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  更新中...
                </div>
              ) : (
                "パスワードを更新"
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              <Link href="/login" className="text-blue-600 hover:underline">
                ログインページに戻る
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
