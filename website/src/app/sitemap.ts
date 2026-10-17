import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/site';
import { DISCOVERIES } from '@/lib/discoveries';
import { VIDEOS } from '@/lib/videos';

export default function sitemap(): MetadataRoute.Sitemap {
  const pages = ['', '/explore', '/discoveries', '/watch', '/games', '/games/where-on-earth', '/games/map-detective', '/about', '/suggest', '/privacy'];
  return [
    ...pages.map((p) => ({ url: `${SITE.url}${p}`, changeFrequency: 'weekly' as const, priority: p === '' ? 1 : 0.7 })),
    ...DISCOVERIES.map((d) => ({ url: `${SITE.url}/discoveries/${d.slug}`, changeFrequency: 'monthly' as const, priority: 0.8 })),
    ...VIDEOS.map((v) => ({ url: `${SITE.url}/watch/${v.slug}`, changeFrequency: 'monthly' as const, priority: 0.6 })),
  ];
}
