"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth, useGuestOnly } from "@/hooks/useAuth";
import { confirmEmailSchema, ConfirmEmailFormData } from "@/schemas/auth";
import { useSearchParams } from "next/navigation";
import { useState } from "react";

export default function ConfirmEmail() {
  const { confirmEmail, resendConfirmationCode, isLoading, error, clearError } = useAuth();
  const { isLoading: authLoading } = useGuestOnly();
  const searchParams = useSearchParams();
  const [resendMessage, setResendMessage] = useState("");

  // URL パラメータからメールアドレスを取得
  const emailFromUrl = searchParams.get("email") || "";

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<ConfirmEmailFormData>({
    resolver: zodResolver(confirmEmailSchema),
    defaultValues: {
      email: emailFromUrl,
    },
  });

  const onSubmit = async (data: ConfirmEmailFormData) => {
    clearError();
    setResendMessage("");
    try {
      await confirmEmail(data);
    } catch (error) {
      // エラーは useAuth フック内で処理される
    }
  };

  const handleResendCode = async () => {
    if (!emailFromUrl) return;

    clearError();
    setResendMessage("");
    try {
      await resendConfirmationCode(emailFromUrl);
      setResendMessage("確認コードを再送信しました。メールをご確認ください。");
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">メール確認</h1>
            <p className="text-gray-600">登録したメールアドレスに送信された確認コードを入力してください</p>
          </div>

          {/* 成功メッセージ */}
          {resendMessage && <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md">{resendMessage}</div>}

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

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  確認中...
                </div>
              ) : (
                "メールアドレスを確認"
              )}
            </button>
          </form>

          <div className="mt-6 text-center space-y-2">
            <p className="text-sm text-gray-600">
              確認コードが届かない場合は{" "}
              <button
                type="button"
                onClick={handleResendCode}
                disabled={isLoading || !emailFromUrl}
                className="text-blue-600 hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
              >
                再送信
              </button>
            </p>
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
