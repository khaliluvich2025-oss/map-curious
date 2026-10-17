'use client';
import { useMemo, useState } from 'react';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { Search } from 'lucide-react';
import { DiscoveryCard } from '@/components/Cards';
import { DISCOVERIES } from '@/lib/discoveries';
import { CATEGORIES, type CategoryId } from '@/lib/categories';

export default function DiscoveryLibrary() {
  const params = useSearchParams();
  const router = useRouter();
  const path = usePathname();
  const [q, setQ] = useState(params.get('q') ?? '');
  const cat = (params.get('category') as CategoryId | null) ?? 'all';

  const setCat = (c: string) => {
    const p = new URLSearchParams(params.toString());
    if (c === 'all') p.delete('category'); else p.set('category', c);
    router.replace(`${path}${p.size ? `?${p}` : ''}`, { scroll: false });
  };
  const list = useMemo(() => {
    const s = q.trim().toLowerCase();
    return DISCOVERIES.filter((d) => (cat === 'all' || d.category === cat) &&
      (!s || [d.name, d.place, d.country, d.summary, d.intro].join(' ').toLowerCase().includes(s)));
  }, [q, cat]);

  return (
    <>
      <div className="mt-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div role="group" aria-label="Filter by category" className="flex flex-wrap gap-2">
          {[{ id: 'all', name: 'All' }, ...CATEGORIES].map((c) => (
            <button key={c.id} onClick={() => setCat(c.id)} aria-pressed={cat === c.id}
              className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${cat === c.id ? 'border-lime bg-lime text-navy' : 'border-line text-mist hover:border-lime hover:text-lime'}`}>
              {c.name}
            </button>
          ))}
        </div>
        <label className="relative md:w-72">
          <span className="sr-only">Search discoveries</span>
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-mist" aria-hidden />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search discoveries..."
            className="w-full rounded-md border border-line bg-navy2 py-2.5 pl-9 pr-3 text-sm focus:border-lime focus:outline-none" />
        </label>
      </div>
      <p className="mt-4 text-xs text-mist" aria-live="polite">{list.length} result{list.length === 1 ? '' : 's'}</p>
      {list.length ? (
        <div className="mt-4 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{list.map((d) => <DiscoveryCard key={d.slug} d={d} />)}</div>
      ) : (
        <div className="mt-6 rounded-lg border border-dashed border-line p-10 text-center text-mist">
          Nothing matches “{q}” yet. <button onClick={() => { setQ(''); setCat('all'); }} className="text-lime underline">Clear filters</button> or suggest it as our next story.
        </div>
      )}
    </>
  );
}
