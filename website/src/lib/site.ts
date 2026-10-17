export const SITE = {
  name: 'Map Curious',
  url: process.env.NEXT_PUBLIC_SITE_URL ?? 'https://map-curious.vercel.app',
  tagline: 'Real places. Impossible stories. Hidden corners of our planet.',
  mission: 'We explore the places, borders, and stories that make our world extraordinary.',
};

/** Verified Map Curious channels (from the brand's connected accounts). */
export const SOCIALS = [
  { name: 'YouTube', handle: 'Map Curious', href: 'https://www.youtube.com/channel/UCpFAb47epl4v75L_YCiaB4Q' },
  { name: 'Instagram', handle: '@map_curious', href: 'https://www.instagram.com/map_curious/' },
  { name: 'TikTok', handle: '@mapcurious26', href: 'https://www.tiktok.com/@mapcurious26' },
  { name: 'Facebook', handle: 'Map Curious', href: 'https://www.facebook.com/1372660739268411' },
] as const;

export const NAV = [
  { href: '/', label: 'Home' },
  { href: '/explore', label: 'Explore Map' },
  { href: '/discoveries', label: 'Discoveries' },
  { href: '/watch', label: 'Watch' },
  { href: '/games', label: 'Games' },
  { href: '/about', label: 'About' },
];

export const IMAGERY_CREDIT =
  'Satellite imagery: Esri, Maxar, Earthstar Geographics and the GIS User Community. Map renders: Map Curious, using NASA Blue Marble imagery.';
