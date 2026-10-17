import type { Metadata } from 'next';
import { Suspense } from 'react';
import DiscoveryLibrary from './DiscoveryLibrary';

export const metadata: Metadata = {
  title: 'Discoveries',
  description: 'A searchable library of fact-checked geography stories: mysteries, borders, abandoned places, hidden history and natural wonders.',
  alternates: { canonical: '/discoveries' },
};

export default function DiscoveriesPage() {
  return (
    <div className="wrap py-10">
      <p className="eyebrow">The library</p>
      <h1 className="h-display mt-2 text-4xl sm:text-5xl">Discoveries</h1>
      <p className="mt-3 max-w-2xl text-mist">Every place we have mapped, with the story behind it and the sources we used.</p>
      <Suspense fallback={<div className="mt-8 h-96 animate-pulse rounded-lg bg-navy2" />}>
        <DiscoveryLibrary />
      </Suspense>
    </div>
  );
}
