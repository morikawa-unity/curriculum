import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // output: 'export', // APIを使用するため静的エクスポートは無効化
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
