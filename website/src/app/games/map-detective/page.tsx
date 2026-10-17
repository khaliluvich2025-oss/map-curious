import type { Metadata } from 'next';
import MapDetective from './MapDetective';

export const metadata: Metadata = {
  title: 'Map Detective · Case #001: The Vanishing Cartographer',
  description: 'A fictional map investigation. Examine the evidence, read compass bearings and tide tables, and work out where the cartographer went.',
  alternates: { canonical: '/games/map-detective' },
};

export default function Page() {
  return (
    <div className="wrap py-10">
      <p className="eyebrow">Game · Fictional case</p>
      <h1 className="h-display mt-2 text-4xl">Map Detective</h1>
      <MapDetective />
    </div>
  );
}
