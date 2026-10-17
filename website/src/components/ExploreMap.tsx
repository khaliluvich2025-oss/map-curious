'use client';
import dynamic from 'next/dynamic';
import Image from 'next/image';
import Link from 'next/link';
import { useMemo, useState } from 'react';
import { ArrowRight, MapPin, Search, X } from 'lucide-react';
import type { Discovery } from '@/lib/discoveries';
import { CATEGORIES, categoryById, type CategoryId } from '@/lib/categories';
import { formatCoord } from '@/lib/geo';

const LeafletMap = dynamic(() => import('./LeafletMap'), {
  ssr: false,
  loading: () => <div className="relative h-full w-full overflow-hidden bg-navy2"><div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/5 to-transparent" /></div>,
});

export default function ExploreMap({ items, compact = false }: { items: Discovery[]; compact?: boolean }) {
  const [cat, setCat] = useState<CategoryId | 'all'>('all');
  const [q, setQ] = useState('');
  const [active, setActive] = useState<string | null>(compact ? 'surtsey-iceland' : null);

  const shown = useMemo(() => {
    const s = q.trim().toLowerCase();
    return items.filter((d) => (cat === 'all' || d.category === cat) &&
      (!s || [d.name, d.place, d.country, d.summary].join(' ').toLowerCase().includes(s)));
  }, [items, cat, q]);
  const points = useMemo(() => shown.map((d) => ({ id: d.slug, lat: d.lat, lng: d.lng, label: `${d.place}: ${d.name}` })), [shown]);
  const sel = items.find((d) => d.slug === active) ?? null;

  const preview = sel && (
    <div className="card overflow-hidden shadow-2xl shadow-black/40">
      <div className="relative aspect-video">
        <Image src={sel.image} alt="" fill sizes="380px" className="object-cover" />
        {!compact && (
          <button onClick={() => setActive(null)} aria-label="Close preview" className="absolute right-2 top-2 rounded bg-navy/80 p-1.5 hover:text-lime"><X className="h-4 w-4" /></button>
        )}
      </div>
      <div className="p-4">
        <p className="text-xs font-semibold text-lime">{categoryById(sel.category).name}</p>
        <h3 className="mt-1 font-display text-lg font-extrabold leading-tight">{sel.name}</h3>
        <p className="mt-1 flex items-center gap-1 text-xs text-mist"><MapPin className="h-3.5 w-3.5" aria-hidden />{sel.place} · {formatCoord(sel.lat, sel.lng)}</p>
        <p className="mt-2 text-sm text-mist">{sel.summary}</p>
        {sel.coordNote && <p className="mt-2 text-xs italic text-mist/80">{sel.coordNote}</p>}
        <Link href={`/discoveries/${sel.slug}`} className="btn-primary mt-4 w-full !py-2.5">Read the story <ArrowRight className="h-4 w-4" aria-hidden /></Link>
      </div>
    </div>
  );

  if (compact)
    return (
      <div className="relative h-[460px] overflow-hidden rounded-xl border border-line sm:h-[520px]">
        <LeafletMap label="Interactive map of Map Curious discoveries" points={points} activeId={active} onSelect={setActive} center={[30, -30]} zoom={2} />
        <div className="pointer-events-none absolute inset-x-3 bottom-3 z-[500] sm:inset-x-auto sm:right-4 sm:top-4 sm:bottom-auto sm:w-80">
          <div className="pointer-events-auto">{preview}</div>
        </div>
      </div>
    );

  return (
    <div className="grid gap-4 lg:grid-cols-[320px_1fr]">
      <aside className="order-2 flex flex-col gap-4 lg:order-1">
        <label className="relative block">
          <span className="sr-only">Search locations</span>
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-mist" aria-hidden />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search a place, country, story..."
            className="w-full rounded-md border border-line bg-navy2 py-2.5 pl-9 pr-3 text-sm focus:border-lime focus:outline-none" />
        </label>
        <div role="group" aria-label="Filter by category" className="flex flex-wrap gap-2">
          {[{ id: 'all', name: 'All' }, ...CATEGORIES].map((c) => (
            <button key={c.id} onClick={() => setCat(c.id as CategoryId | 'all')} aria-pressed={cat === c.id}
              className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${cat === c.id ? 'border-lime bg-lime text-navy' : 'border-line text-mist hover:border-lime hover:text-lime'}`}>
              {c.name}
            </button>
          ))}
        </div>
        <p className="text-xs text-mist" aria-live="polite">{shown.length} location{shown.length === 1 ? '' : 's'}</p>
        <ul className="max-h-[420px] space-y-1 overflow-y-auto pr-1 lg:max-h-[520px]">
          {shown.map((d) => (
            <li key={d.slug}>
              <button onClick={() => setActive(d.slug)} aria-current={active === d.slug}
                className={`flex w-full items-center gap-3 rounded-md border px-2 py-2 text-left transition ${active === d.slug ? 'border-lime bg-lime/10' : 'border-transparent hover:border-line hover:bg-navy2'}`}>
                <span className="relative h-10 w-14 shrink-0 overflow-hidden rounded"><Image src={d.image} alt="" fill sizes="56px" className="object-cover" /></span>
                <span>
                  <span className="block text-sm font-semibold leading-tight">{d.name}</span>
                  <span className="block text-xs text-mist">{d.place}</span>
                </span>
              </button>
            </li>
          ))}
          {shown.length === 0 && <li className="rounded-md border border-dashed border-line p-4 text-sm text-mist">No places match. Try another search or category.</li>}
        </ul>
      </aside>
      <div className="relative order-1 h-[62vh] min-h-[420px] overflow-hidden rounded-xl border border-line lg:order-2 lg:h-[680px]">
        <LeafletMap label="Interactive map of Map Curious discoveries" points={points} activeId={active} onSelect={setActive} cluster center={[28, -20]} zoom={2} />
        {sel && <div className="absolute inset-x-3 bottom-3 z-[500] sm:inset-x-auto sm:right-4 sm:top-4 sm:bottom-auto sm:w-80">{preview}</div>}
      </div>
    </div>
  );
}
