import { z } from "zod";

// ログインフォームのスキーマ
export const loginSchema = z.object({
  email: z.string().min(1, "メールアドレスを入力してください").email("有効なメールアドレスを入力してください"),
  password: z.string().min(1, "パスワードを入力してください").min(8, "パスワードは8文字以上で入力してください"),
});

// 新規登録フォームのスキーマ
export const registerSchema = z
  .object({
    email: z.string().min(1, "メールアドレスを入力してください").email("有効なメールアドレスを入力してください"),
    password: z
      .string()
      .min(8, "パスワードは8文字以上で入力してください")
      .regex(/[a-z]/, "パスワードには小文字を含めてください")
      .regex(/[A-Z]/, "パスワードには大文字を含めてください")
      .regex(/[0-9]/, "パスワードには数字を含めてください"),
    confirmPassword: z.string().min(1, "パスワード確認を入力してください"),
    preferredUsername: z
      .string()
      .min(1, "ユーザー名を入力してください")
      .max(50, "ユーザー名は50文字以内で入力してください")
      .regex(/^[a-zA-Z0-9_-]+$/, "ユーザー名は英数字、アンダースコア、ハイフンのみ使用できます"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "パスワードが一致しません",
    path: ["confirmPassword"],
  });

// メール確認フォームのスキーマ
export const confirmEmailSchema = z.object({
  email: z.string().min(1, "メールアドレスを入力してください").email("有効なメールアドレスを入力してください"),
  confirmationCode: z
    .string()
    .min(1, "確認コードを入力してください")
    .length(6, "確認コードは6桁で入力してください")
    .regex(/^[0-9]+$/, "確認コードは数字のみ入力してください"),
});

// パスワードリセット要求のスキーマ
export const forgotPasswordSchema = z.object({
  email: z.string().min(1, "メールアドレスを入力してください").email("有効なメールアドレスを入力してください"),
});

// パスワードリセットのスキーマ
export const resetPasswordSchema = z
  .object({
    email: z.string().min(1, "メールアドレスを入力してください").email("有効なメールアドレスを入力してください"),
    confirmationCode: z
      .string()
      .min(1, "確認コードを入力してください")
      .length(6, "確認コードは6桁で入力してください")
      .regex(/^[0-9]+$/, "確認コードは数字のみ入力してください"),
    newPassword: z
      .string()
      .min(8, "パスワードは8文字以上で入力してください")
      .regex(/[a-z]/, "パスワードには小文字を含めてください")
      .regex(/[A-Z]/, "パスワードには大文字を含めてください")
      .regex(/[0-9]/, "パスワードには数字を含めてください"),
    confirmNewPassword: z.string().min(1, "パスワード確認を入力してください"),
  })
  .refine((data) => data.newPassword === data.confirmNewPassword, {
    message: "パスワードが一致しません",
    path: ["confirmNewPassword"],
  });

// 型定義をエクスポート
export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type ConfirmEmailFormData = z.infer<typeof confirmEmailSchema>;
export type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;

// ユーザー情報のスキーマ
export const userSchema = z.object({
  userId: z.string(),
  email: z.string().email(),
  preferredUsername: z.string().optional(),
  emailVerified: z.boolean(),
  createdAt: z.string(),
  updatedAt: z.string(),
});

export type User = z.infer<typeof userSchema>;
