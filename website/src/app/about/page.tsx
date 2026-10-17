import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { CheckCircle2 } from 'lucide-react';
import { CATEGORIES } from '@/lib/categories';
import { SITE, SOCIALS } from '@/lib/site';
import SocialIcon from '@/components/SocialIcon';

export const metadata: Metadata = {
  title: 'About',
  description: SITE.mission + ' Learn how Map Curious researches, maps and tells its stories.',
  alternates: { canonical: '/about' },
};

const PRINCIPLES = [
  ['Real places only', 'Every story is tied to a real location on the map, at a verified coordinate.'],
  ['Primary sources first', 'We check facts against agencies and institutions such as NOAA, USGS, the National Park Service, the FBI and UNESCO.'],
  ['Mysteries stay mysteries', 'When a case is unsolved, we present the evidence and say so. We never invent a solution.'],
  ['Show, don’t just tell', 'Animated maps, routes and cross-sections explain how a place works, not just where it is.'],
];

export default function AboutPage() {
  return (
    <div>
      <section className="relative overflow-hidden border-b border-line">
        <Image src="/img/world.jpg" alt="" fill priority sizes="100vw" className="object-cover opacity-30" />
        <div className="absolute inset-0 bg-gradient-to-b from-navy/40 to-navy" />
        <div className="wrap relative py-20">
          <p className="eyebrow">About Map Curious</p>
          <h1 className="h-display mt-3 max-w-3xl text-4xl sm:text-6xl">We explore the places, borders and stories that make our world <span className="text-lime">extraordinary.</span></h1>
        </div>
      </section>
      <div className="wrap grid gap-12 py-14 lg:grid-cols-2">
        <section>
          <h2 className="h-display text-2xl">What we cover</h2>
          <ul className="mt-5 grid gap-3 sm:grid-cols-2">
            {CATEGORIES.map((c) => (
              <li key={c.id}><Link href={`/discoveries?category=${c.id}`} className="card block p-4 hover:border-lime"><p className="font-display font-extrabold">{c.name}</p><p className="text-sm text-mist">{c.blurb}</p></Link></li>
            ))}
          </ul>
        </section>
        <section>
          <h2 className="h-display text-2xl">How we explore</h2>
          <ul className="mt-5 space-y-4">
            {PRINCIPLES.map(([t, d]) => (
              <li key={t} className="flex gap-3"><CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-lime" aria-hidden /><div><p className="font-semibold">{t}</p><p className="text-sm text-mist">{d}</p></div></li>
            ))}
          </ul>
          <p className="mt-6 text-sm text-mist">Our narration is produced with an AI voice (ElevenLabs), and we label it on every platform that asks.</p>
        </section>
      </div>
      <section className="wrap">
        <div className="flex flex-col items-start justify-between gap-6 rounded-xl border border-line bg-navy2 p-8 md:flex-row md:items-center">
          <div>
            <h2 className="h-display text-2xl">Have a place we should map?</h2>
            <p className="mt-1 text-mist">Strange borders, ghost towns, local legends: send it in.</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link href="/suggest" className="btn-primary">Suggest a place</Link>
            {SOCIALS.map((s) => <a key={s.name} href={s.href} target="_blank" rel="noopener noreferrer" aria-label={s.name} className="grid h-12 w-12 place-items-center rounded-md border border-line hover:border-lime hover:text-lime"><SocialIcon name={s.name} /></a>)}
          </div>
        </div>
      </section>
    </div>
  );
}
