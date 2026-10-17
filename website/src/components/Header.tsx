'use client';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Menu, Search, X, MapPin } from 'lucide-react';
import Logo from './Logo';
import { NAV } from '@/lib/site';

export default function Header() {
  const path = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState('');
  useEffect(() => setOpen(false), [path]);

  const active = (href: string) => (href === '/' ? path === '/' : path.startsWith(href));
  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push(q.trim() ? `/discoveries?q=${encodeURIComponent(q.trim())}` : '/discoveries');
  };

  return (
    <header className="sticky top-0 z-50 border-b border-line/70 bg-navy/85 backdrop-blur-md">
      <div className="wrap flex h-16 items-center gap-6">
        <Logo />
        <nav aria-label="Main" className="hidden flex-1 lg:block">
          <ul className="flex items-center gap-6">
            {NAV.map((n) => (
              <li key={n.href}>
                <Link href={n.href} aria-current={active(n.href) ? 'page' : undefined}
                  className={`relative py-5 text-sm font-medium transition hover:text-lime ${active(n.href) ? 'text-lime' : 'text-white/90'}`}>
                  {n.label}
                  {active(n.href) && <span className="absolute inset-x-0 bottom-3 h-0.5 rounded bg-lime" />}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <form onSubmit={submit} role="search" className="ml-auto hidden items-center md:flex">
          <label className="relative">
            <span className="sr-only">Search places and mysteries</span>
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-mist" aria-hidden />
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search places, mysteries..."
              className="w-56 rounded-md border border-line bg-navy2 py-2 pl-9 pr-3 text-sm text-white placeholder:text-mist/70 focus:border-lime focus:outline-none xl:w-64" />
          </label>
        </form>
        <Link href="/suggest" className="btn-primary hidden !px-4 !py-2 md:inline-flex">
          Suggest a Place <MapPin className="h-4 w-4" aria-hidden />
        </Link>
        <button onClick={() => setOpen((o) => !o)} className="ml-auto rounded p-2 text-white lg:hidden md:ml-0" aria-expanded={open} aria-controls="mobile-nav" aria-label="Menu">
          {open ? <X /> : <Menu />}
        </button>
      </div>
      {open && (
        <div id="mobile-nav" className="border-t border-line bg-navy lg:hidden">
          <div className="wrap space-y-1 py-4">
            <form onSubmit={submit} role="search" className="mb-3 md:hidden">
              <label className="relative block">
                <span className="sr-only">Search places and mysteries</span>
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-mist" aria-hidden />
                <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search places, mysteries..."
                  className="w-full rounded-md border border-line bg-navy2 py-2.5 pl-9 pr-3 text-sm focus:border-lime focus:outline-none" />
              </label>
            </form>
            {NAV.map((n) => (
              <Link key={n.href} href={n.href} className={`block rounded px-3 py-2.5 font-display font-bold ${active(n.href) ? 'bg-lime/10 text-lime' : 'text-white'}`}>
                {n.label}
              </Link>
            ))}
            <Link href="/suggest" className="btn-primary mt-3 w-full">Suggest a Place</Link>
          </div>
        </div>
      )}
    </header>
  );
}
