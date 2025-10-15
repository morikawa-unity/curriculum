import { z } from "zod";

// ログインフォームのスキーマ
export const loginSchema = z.object({
  email: z.string().min(1, "メールアドレスを入力してください").email("有効なメールアドレスを入力してください"),
  password: z.string().min(1, "パスワードを入力してください").min(8, "パスワードは8文字以上で入力してください"),
});

// 新規登録、メール確認、パスワードリセット機能は一旦無効化

// 型定義をエクスポート
export type LoginFormData = z.infer<typeof loginSchema>;

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
