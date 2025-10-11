import { Amplify } from "aws-amplify";

// Amplify設定
const amplifyConfig = {
  Auth: {
    Cognito: {
      // 環境変数から設定を読み込み
      userPoolId: process.env.NEXT_PUBLIC_USER_POOL_ID || "",
      userPoolClientId: process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID || "",
      loginWith: {
        email: true,
        username: false,
      },
      signUpVerificationMethod: "code", // メール認証
      userAttributes: {
        email: {
          required: true,
        },
        preferred_username: {
          required: false,
        },
      },
      allowGuestAccess: false,
      passwordFormat: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireNumbers: true,
        requireSpecialCharacters: false,
      },
    },
  },
};

// Amplifyを設定
Amplify.configure(amplifyConfig);

export default amplifyConfig;
