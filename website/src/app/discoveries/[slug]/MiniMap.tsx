'use client';
import dynamic from 'next/dynamic';

const LeafletMap = dynamic(() => import('@/components/LeafletMap'), { ssr: false, loading: () => <div className="h-full w-full animate-pulse bg-navy2" /> });

export default function MiniMap({ lat, lng, label }: { lat: number; lng: number; label: string }) {
  return <LeafletMap label={`Map showing ${label}`} points={[{ id: 'here', lat, lng, label }]} activeId="here" center={[lat, lng]} zoom={6} />;
}
