'use client';

import { useEffect } from 'react';
import { Amplify } from 'aws-amplify';
import { amplifyConfig } from '@/lib/amplify';

export function AmplifyConfigurer() {
  useEffect(() => {
    const userPoolId = process.env.NEXT_PUBLIC_USER_POOL_ID;
    const userPoolClientId = process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID;

    console.log('🔧 Amplify設定を初期化中...', {
      userPoolId,
      userPoolClientId,
      hasUserPoolId: !!userPoolId,
      hasUserPoolClientId: !!userPoolClientId,
    });

    if (userPoolId && userPoolClientId) {
      Amplify.configure(amplifyConfig, { ssr: true });
      console.log('✅ Amplify設定完了');
    } else {
      console.error('❌ AWS Cognito環境変数が設定されていません');
      console.log('環境変数:', {
        NEXT_PUBLIC_USER_POOL_ID: process.env.NEXT_PUBLIC_USER_POOL_ID,
        NEXT_PUBLIC_USER_POOL_CLIENT_ID: process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID,
        NEXT_PUBLIC_AWS_REGION: process.env.NEXT_PUBLIC_AWS_REGION,
      });
    }
  }, []);

  return null;
}
