'use client';
import dynamic from 'next/dynamic';
import Image from 'next/image';
import Link from 'next/link';
import type { Discovery } from '@/lib/discoveries';

const Globe = dynamic(() => import('./Globe'), { ssr: false });

const SLOTS = ['left-0 top-[8%]', 'right-0 top-[2%]', 'right-[2%] top-[52%]', 'left-[4%] bottom-[6%]'];

export default function HeroGlobe({ items, markers }: { items: Discovery[]; markers: { lat: number; lng: number }[] }) {
  return (
    <div className="relative mx-auto aspect-square w-full max-w-[600px]">
      <div className="absolute inset-[8%] rounded-full bg-teal/40 blur-3xl" aria-hidden />
      <Globe markers={markers} className="relative" />
      {items.slice(0, 4).map((d, i) => (
        <Link key={d.slug} href={`/discoveries/${d.slug}`}
          className={`group absolute hidden w-36 overflow-hidden rounded-lg border border-white/60 bg-navy/90 shadow-xl transition hover:-translate-y-1 hover:border-lime sm:block md:w-40 ${SLOTS[i]}`}>
          <span className="relative block aspect-[16/10]"><Image src={d.image} alt="" fill sizes="160px" className="object-cover" /></span>
          <span className="block px-2 py-1.5">
            <span className="block text-xs font-bold leading-tight group-hover:text-lime">{d.place.split(',')[0]}</span>
            <span className="block text-[10px] text-mist">{d.country}</span>
          </span>
        </Link>
      ))}
    </div>
  );
}
