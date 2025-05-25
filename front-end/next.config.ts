/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    // domains: ['espiafacil.com.br'],
    // remotePatterns: [
    //   {
    //     protocol: 'https',
    //     hostname: '**.fbcdn.net', // Permite imagens hospedadas nos servidores do Facebook/Instagram
    //   },
    //   {
    //     protocol: 'https',
    //     hostname: '**.cdninstagram.com', // Se precisar carregar imagens deste também
    //   },
    // ],
  },
   trailingSlash: true,
  output:"export"
};

module.exports = nextConfig;
