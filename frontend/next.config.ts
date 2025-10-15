import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export", // CSRアプリのため静的エクスポート
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  // ページプリフェッチを有効化してナビゲーションを高速化
  experimental: {
    optimizePackageImports: ["@/components", "@/hooks", "@/lib"],
  },
};

export default nextConfig;
