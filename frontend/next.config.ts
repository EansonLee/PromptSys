import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  // experimental: {
  //   optimizePackageImports: ['@/components', '@/hooks', '@/utils'],
  // },
};

export default nextConfig;
