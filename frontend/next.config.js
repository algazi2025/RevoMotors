/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
      },
    ],
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  },
  redirects: async () => {
    return [
      {
        source: '/dealer',
        destination: '/dealer/dashboard',
        permanent: false,
      },
      {
        source: '/seller',
        destination: '/seller/landing',
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;