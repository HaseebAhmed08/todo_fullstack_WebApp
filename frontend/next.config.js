/** @type {import('next').NextConfig} */
const nextConfig = {
  // App Router is enabled by default in Next.js 14+
  // No need to specify experimental.appDir anymore
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    BETTER_AUTH_URL: process.env.BETTER_AUTH_URL,
    BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET,
  },
  images: {
    domains: ['localhost', 'your-api-domain.com'], // Add your API domains here
  },
};

module.exports = nextConfig;