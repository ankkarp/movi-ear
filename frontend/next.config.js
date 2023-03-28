/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    SERVER: process.env.SERVER,
  },
  async redirects() {
    return [
      {
        source: "/",
        destination: "/upload",
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;
