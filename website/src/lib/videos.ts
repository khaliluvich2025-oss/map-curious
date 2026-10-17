import type { CategoryId } from './categories';

export interface Video {
  slug: string;
  title: string;
  youtubeId?: string;          // verified public YouTube ID (from the channel's published posts)
  kind: 'short' | 'long';
  discovery?: string;          // related discovery slug
  category: CategoryId;
  image: string;
  status?: 'live' | 'coming-soon';
  links?: { label: string; href: string }[];
}

/**
 * Only videos whose YouTube IDs were returned by the channel's published posts are listed as live.
 * Upcoming uploads are clearly marked "coming soon" and are not embedded.
 */
export const VIDEOS: Video[] = [
  { slug: 'six-places-that-sound-made-up', title: '6 Places on the Map That Sound Made Up (But Are Real)', kind: 'long',
    category: 'geography-mysteries', image: '/img/six-places.jpg', status: 'coming-soon' },
  { slug: 'okavango-river-never-reaches-the-ocean', title: 'Why the Okavango River Never Reaches the Ocean', youtubeId: 'R9PmmkmlAuA',
    kind: 'short', discovery: 'okavango-delta-botswana', category: 'natural-wonders', image: '/img/okavango-delta.jpg' },
  { slug: 'suez-canal-no-locks', title: 'Why the Suez Canal Doesn’t Need Locks', youtubeId: 'GVjW_VXKr4w', kind: 'short',
    discovery: 'suez-canal-egypt', category: 'hidden-history', image: '/img/suez-canal.jpg' },
  { slug: 'manicouagan-water-ring', title: 'Canada’s Giant Water Ring Has Two Very Different Origins', youtubeId: '1EvziGdm6aA', kind: 'short',
    discovery: 'manicouagan-quebec', category: 'geography-mysteries', image: '/img/manicouagan.jpg' },
  { slug: 'river-moved-us-mexico-border', title: 'The River That Moved the U.S.–Mexico Border', youtubeId: 'oz4z_rrQBV4', kind: 'short',
    discovery: 'chamizal-us-mexico-border', category: 'strange-borders', image: '/img/chamizal-rio-grande.jpg' },
  { slug: 'alcatraz-hard-to-escape', title: 'Why Alcatraz Was So Hard to Escape', youtubeId: 'nwBcsOdl460', kind: 'short',
    discovery: 'alcatraz-island', category: 'crime-mysteries', image: '/img/alcatraz.jpg' },
  { slug: 'moving-plate-built-hawaii', title: 'The Moving Plate That Built Hawaii', youtubeId: 'CTkeJSdDSkg', kind: 'short',
    discovery: 'hawaii-hotspot', category: 'natural-wonders', image: '/img/hawaii-hotspot.jpg' },
  { slug: 'point-roberts-drive-through-canada', title: 'Why This Washington Town Requires Driving Through Canada', youtubeId: 'BZsgCufvE3E', kind: 'short',
    discovery: 'point-roberts-washington', category: 'strange-borders', image: '/img/point-roberts.jpg' },
  { slug: 'michigan-two-peninsulas', title: 'Why Michigan Has Two Peninsulas', youtubeId: 'EEBqoT9nicA', kind: 'short',
    discovery: 'michigan-upper-peninsula', category: 'strange-borders', image: '/img/michigan-peninsulas.jpg' },
  { slug: 'catatumbo-lightning', title: 'Why Lightning Keeps Returning to This Venezuelan Lake', youtubeId: 'qddSfHtMwNM', kind: 'short',
    discovery: 'catatumbo-lightning-venezuela', category: 'natural-wonders', image: '/img/catatumbo-lightning.jpg' },
  { slug: 'centralia-burning-since-1962', title: 'This American Town Has Been Burning Since 1962', youtubeId: 'C5WOd1Y-alg', kind: 'short',
    discovery: 'centralia-pennsylvania', category: 'abandoned-places', image: '/img/centralia-map.jpg' },
  { slug: 'iceland-pulled-apart', title: 'Iceland Is Being Pulled Apart', youtubeId: '0CNC8v1Cuq8', kind: 'short',
    discovery: 'thingvellir-iceland-rift', category: 'geography-mysteries', image: '/img/iceland-rift.jpg' },
  { slug: 'france-shares-border-with-brazil', title: 'How Does France Share a Border With Brazil?', youtubeId: '5KPIAKhsJrE', kind: 'short',
    discovery: 'france-brazil-border', category: 'strange-borders', image: '/img/france-brazil-border.jpg' },
  { slug: 'angel-island-poems', title: 'Why Immigrants Carved Poems Into Angel Island’s Walls', youtubeId: 'xPJ6sOIAK4E', kind: 'short',
    discovery: 'angel-island-california', category: 'hidden-history', image: '/img/angel-island.jpg' },
  { slug: 'why-is-the-gambia-so-narrow', title: 'Why Is The Gambia So Narrow?', youtubeId: 'zRKxerDgcZk', kind: 'short',
    discovery: 'the-gambia', category: 'strange-borders', image: '/img/the-gambia.jpg' },
  { slug: 'largest-waterfall-underwater', title: 'The World’s Largest Waterfall Is Hidden Underwater', youtubeId: 'zkk3CP_5H_c', kind: 'short',
    discovery: 'denmark-strait-cataract', category: 'geography-mysteries', image: '/img/denmark-strait.jpg' },
  { slug: 'fortress-in-the-ocean', title: 'The Mysterious Fortress in the Middle of the Ocean', youtubeId: 'mCfZMSpFBQY', kind: 'short',
    discovery: 'fort-jefferson-florida', category: 'hidden-history', image: '/img/fort-jefferson-map.jpg' },
  { slug: 'mount-st-helens-1300-feet', title: 'How Mount St. Helens Lost 1,300 Feet in One Morning', youtubeId: '4m-d5HX7dkg', kind: 'short',
    discovery: 'mount-st-helens-washington', category: 'natural-wonders', image: '/img/mount-st-helens.jpg' },
  { slug: 'niagara-falls-moving', title: 'Niagara Falls Is Moving Upstream', youtubeId: 'IoFPy5C4uvE', kind: 'short',
    discovery: 'niagara-falls', category: 'natural-wonders', image: '/img/niagara-falls.jpg' },
  { slug: 'crater-lake-collapsed-volcano', title: 'America’s Deepest Lake Is Inside a Collapsed Volcano', youtubeId: 'AnIcB19_kR8', kind: 'short',
    discovery: 'crater-lake-oregon', category: 'natural-wonders', image: '/img/crater-lake.jpg' },
  { slug: 'erie-canal-ditch', title: 'The Ditch That Built New York: The Erie Canal', youtubeId: 'cAYpzbQZb-o', kind: 'short',
    discovery: 'erie-canal-new-york', category: 'hidden-history', image: '/img/erie-canal.jpg' },
  { slug: 'highway-crosses-the-ocean', title: 'The Highway That Crosses the Ocean', youtubeId: 'rIRYUx-PhZA', kind: 'short',
    discovery: 'overseas-highway-florida', category: 'hidden-history', image: '/img/overseas-highway.jpg' },
  { slug: 'river-flows-both-ways', title: 'The River That Flows Both Ways', youtubeId: '2COjq4Co76E', kind: 'short',
    discovery: 'hudson-river-new-york', category: 'geography-mysteries', image: '/img/hudson-short.jpg' },
  { slug: 'db-cooper-hijacking', title: 'D.B. Cooper: The Hijacker Who Vanished', kind: 'short',
    discovery: 'db-cooper-mystery', category: 'crime-mysteries', image: '/img/db-cooper.jpg',
    links: [{ label: 'Watch on TikTok', href: 'https://www.tiktok.com/@mapcurious26/video/7696556098714651926' },
            { label: 'Watch on Facebook', href: 'https://facebook.com/reel/1653225319921945/' }] },
];

export const liveVideos = VIDEOS.filter((v) => v.youtubeId);
export const videoBySlug = (slug: string) => VIDEOS.find((v) => v.slug === slug);
export const videoForDiscovery = (slug: string) => VIDEOS.find((v) => v.discovery === slug && (v.youtubeId || v.links));
