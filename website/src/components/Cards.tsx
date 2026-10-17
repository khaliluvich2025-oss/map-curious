import Image from 'next/image';
import Link from 'next/link';
import { MapPin, Play, Clock } from 'lucide-react';
import type { Discovery } from '@/lib/discoveries';
import type { Video } from '@/lib/videos';
import { categoryById, type Category } from '@/lib/categories';

export function DiscoveryCard({ d, priority = false }: { d: Discovery; priority?: boolean }) {
  return (
    <Link href={`/discoveries/${d.slug}`} className="group card block overflow-hidden transition hover:-translate-y-0.5 hover:border-lime/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-lime">
      <div className="relative aspect-video overflow-hidden">
        <Image src={d.image} alt={`${d.place}: ${d.summary}`} fill sizes="(min-width:1024px) 33vw, (min-width:640px) 50vw, 100vw"
          className="object-cover transition duration-500 group-hover:scale-105" priority={priority} />
        <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/10 to-transparent" />
        <span className="chip absolute left-3 top-3 !bg-navy/80">{categoryById(d.category).name}</span>
      </div>
      <div className="p-4">
        <h3 className="font-display text-lg font-extrabold leading-tight group-hover:text-lime">{d.name}</h3>
        <p className="mt-1 flex items-center gap-1 text-xs text-lime"><MapPin className="h-3.5 w-3.5" aria-hidden />{d.place}</p>
        <p className="mt-2 text-sm text-mist">{d.summary}</p>
      </div>
    </Link>
  );
}

export function CategoryCard({ c, count }: { c: Category; count: number }) {
  return (
    <Link href={`/discoveries?category=${c.id}`} className="group relative block aspect-[4/5] overflow-hidden rounded-lg border border-line focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-lime sm:aspect-[3/4]">
      <Image src={c.image} alt="" fill sizes="(min-width:1024px) 16vw, 50vw" className="object-cover transition duration-500 group-hover:scale-105" />
      <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/40 to-transparent" />
      <div className="absolute inset-x-0 bottom-0 p-3">
        <p className="font-display font-extrabold leading-tight group-hover:text-lime">{c.name}</p>
        <p className="text-xs text-mist">{c.blurb} · {count}</p>
      </div>
    </Link>
  );
}

export function VideoCard({ v }: { v: Video }) {
  const soon = v.status === 'coming-soon';
  return (
    <Link href={`/watch/${v.slug}`} className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-lime rounded-lg">
      <div className="relative aspect-video overflow-hidden rounded-lg border border-line">
        <Image src={v.image} alt="" fill sizes="(min-width:1024px) 25vw, 50vw" className="object-cover transition duration-500 group-hover:scale-105" />
        <div className="absolute inset-0 bg-navy/20 transition group-hover:bg-navy/0" />
        <span className="absolute bottom-2 right-2 rounded bg-navy/85 px-1.5 py-0.5 text-[11px] font-bold">
          {soon ? <span className="flex items-center gap-1 text-fire"><Clock className="h-3 w-3" aria-hidden />COMING SOON</span> : v.kind === 'long' ? 'LONG-FORM' : 'SHORT'}
        </span>
        <span className="absolute left-1/2 top-1/2 grid h-11 w-11 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-lime/90 text-navy opacity-0 transition group-hover:opacity-100">
          <Play className="h-5 w-5 fill-navy" aria-hidden />
        </span>
      </div>
      <h3 className="mt-2 font-display text-sm font-extrabold uppercase leading-snug group-hover:text-lime">{v.title}</h3>
    </Link>
  );
}

export function SectionHead({ eyebrow, title, sub, link }: { eyebrow?: string; title: string; sub?: string; link?: { href: string; label: string } }) {
  return (
    <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
      <div>
        {eyebrow && <p className="eyebrow mb-2">{eyebrow}</p>}
        <h2 className="h-display text-2xl sm:text-3xl">{title}</h2>
        {sub && <p className="mt-1 text-sm text-mist">{sub}</p>}
      </div>
      {link && <Link href={link.href} className="text-sm font-semibold text-lime hover:underline">{link.label} →</Link>}
    </div>
  );
}
