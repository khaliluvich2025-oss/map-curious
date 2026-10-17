import type { Metadata } from 'next';
import ExploreMap from '@/components/ExploreMap';
import { DISCOVERIES } from '@/lib/discoveries';

export const metadata: Metadata = {
  title: 'Explore Map',
  description: 'An interactive satellite map of mysterious places, strange borders, abandoned towns and natural wonders, with fact-checked stories.',
  alternates: { canonical: '/explore' },
};

export default function ExplorePage() {
  return (
    <div className="wrap py-10">
      <p className="eyebrow">Interactive map</p>
      <h1 className="h-display mt-2 text-4xl sm:text-5xl">Explore the world</h1>
      <p className="mt-3 max-w-2xl text-mist">Zoom, pan, filter and search. Select a pin or a place in the list to preview it, then open the full story.</p>
      <div className="mt-8"><ExploreMap items={DISCOVERIES} /></div>
    </div>
  );
}
