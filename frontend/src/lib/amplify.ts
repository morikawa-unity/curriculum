import { Amplify } from "aws-amplify";

// 環境変数の確認
const userPoolId = process.env.NEXT_PUBLIC_USER_POOL_ID;
const userPoolClientId = process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID;

// 開発環境では環境変数が未設定でも動作するようにする
if (process.env.NODE_ENV === "production" && (!userPoolId || !userPoolClientId)) {
  console.error("AWS Cognito環境変数が設定されていません");
}

// Amplify設定
const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId: userPoolId || "dummy-pool-id",
      userPoolClientId: userPoolClientId || "dummy-client-id",
      loginWith: {
        email: true,
      },
      signUpVerificationMethod: "code" as const,
      userAttributes: {
        email: {
          required: true,
        },
      },
    },
  },
};

// Amplifyを設定（環境変数が設定されている場合のみ）
if (userPoolId && userPoolClientId) {
  Amplify.configure(amplifyConfig);
} else {
  console.warn("AWS Cognito環境変数が未設定のため、認証機能は無効化されています");
}

export default amplifyConfig;
