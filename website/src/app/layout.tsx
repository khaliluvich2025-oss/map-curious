import type { Metadata, Viewport } from 'next';
import localFont from 'next/font/local';
import { Inter } from 'next/font/google';
import './globals.css';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { SITE, SOCIALS } from '@/lib/site';

const manrope = localFont({ src: '../fonts/Manrope.ttf', variable: '--font-manrope', weight: '200 800', display: 'swap' });
const inter = Inter({ subsets: ['latin'], variable: '--font-inter', display: 'swap' });

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: { default: 'Map Curious · The World Is Stranger Than You Think', template: '%s · Map Curious' },
  description: SITE.tagline + ' Explore mysterious places, strange borders and hidden history on an interactive map.',
  openGraph: { type: 'website', siteName: 'Map Curious', images: ['/og.jpg'] },
  twitter: { card: 'summary_large_image' },
  icons: { icon: '/icon.svg' },
};

export const viewport: Viewport = { themeColor: '#081521' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const org = {
    '@context': 'https://schema.org', '@type': 'Organization', name: 'Map Curious', url: SITE.url,
    sameAs: SOCIALS.map((s) => s.href),
  };
  return (
    <html lang="en" className={`${manrope.variable} ${inter.variable}`}>
      <body className="min-h-screen">
        <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-[100] focus:rounded focus:bg-lime focus:px-3 focus:py-2 focus:text-navy">
          Skip to content
        </a>
        <Header />
        <main id="main">{children}</main>
        <Footer />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(org) }} />
      </body>
    </html>
  );
}
