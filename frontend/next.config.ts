import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export', // CSRアプリのため静的エクスポート
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
