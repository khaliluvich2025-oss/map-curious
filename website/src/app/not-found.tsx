import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="wrap grid min-h-[60vh] place-items-center py-20 text-center">
      <div>
        <p className="eyebrow">404 · Off the map</p>
        <h1 className="h-display mt-3 text-5xl">This place doesn’t exist</h1>
        <p className="mt-3 text-mist">Unlike the rest of our stories. Try the map instead.</p>
        <div className="mt-6 flex justify-center gap-3"><Link href="/explore" className="btn-primary">Explore the map</Link><Link href="/" className="btn-ghost">Home</Link></div>
      </div>
    </div>
  );
}
