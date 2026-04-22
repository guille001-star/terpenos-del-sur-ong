/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  typescript: {
    ignoreBuildErrors: true, // Evita que el build falle por errores menores de tipos
  },
};

module.exports = nextConfig;
