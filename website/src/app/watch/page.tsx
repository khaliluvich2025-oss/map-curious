import type { Metadata } from 'next';
import Link from 'next/link';
import Image from 'next/image';
import { Clock, Play } from 'lucide-react';
import { VideoCard } from '@/components/Cards';
import SocialIcon from '@/components/SocialIcon';
import { VIDEOS } from '@/lib/videos';
import { CATEGORIES } from '@/lib/categories';
import { SOCIALS } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Watch',
  description: 'Map Curious videos: animated maps of mysterious places, strange borders and hidden history. Shorts and long-form documentaries.',
  alternates: { canonical: '/watch' },
};

export default function WatchPage() {
  const long = VIDEOS.filter((v) => v.kind === 'long');
  const featured = VIDEOS.find((v) => v.slug === 'okavango-river-never-reaches-the-ocean')!;
  return (
    <div className="wrap py-10">
      <p className="eyebrow">Watch</p>
      <h1 className="h-display mt-2 text-4xl sm:text-5xl">The video library</h1>

      <Link href={`/watch/${featured.slug}`} className="group relative mt-8 block overflow-hidden rounded-xl border border-line">
        <div className="relative aspect-[21/9] min-h-[260px]">
          <Image src={featured.image} alt="" fill priority sizes="100vw" className="object-cover transition duration-700 group-hover:scale-105" />
          <div className="absolute inset-0 bg-gradient-to-r from-navy via-navy/60 to-transparent" />
        </div>
        <div className="absolute inset-y-0 left-0 flex max-w-lg flex-col justify-center p-6 sm:p-10">
          <p className="eyebrow">Featured</p>
          <h2 className="h-display mt-2 text-3xl sm:text-4xl">{featured.title}</h2>
          <span className="btn-primary mt-5 self-start"><Play className="h-4 w-4 fill-navy" aria-hidden />Watch now</span>
        </div>
      </Link>

      <section className="mt-12">
        <h2 className="h-display mb-4 text-2xl">Long-form documentaries</h2>
        <div className="grid gap-5 sm:grid-cols-2">
          {long.map((v) => (
            <div key={v.slug} className="card flex flex-col overflow-hidden sm:flex-row">
              <div className="relative aspect-video sm:w-1/2"><Image src={v.image} alt="" fill sizes="50vw" className="object-cover" /></div>
              <div className="flex flex-1 flex-col justify-center p-5">
                {v.status === 'coming-soon' && <p className="mb-2 flex items-center gap-1 text-xs font-bold text-fire"><Clock className="h-3.5 w-3.5" aria-hidden />COMING SOON TO YOUTUBE</p>}
                <h3 className="font-display text-lg font-extrabold">{v.title}</h3>
                <p className="mt-2 text-sm text-mist">A river that flows both ways, a fortress at the end of the road, a burning town, a vanished hijacker, an underwater waterfall and an island born in 1963.</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {CATEGORIES.map((c) => {
        const vs = VIDEOS.filter((v) => v.kind === 'short' && v.category === c.id);
        if (!vs.length) return null;
        return (
          <section key={c.id} className="mt-12">
            <h2 className="h-display mb-4 text-2xl">{c.name}</h2>
            <div className="grid grid-cols-2 gap-x-4 gap-y-6 md:grid-cols-4">{vs.map((v) => <VideoCard key={v.slug} v={v} />)}</div>
          </section>
        );
      })}

      <section className="mt-14 rounded-xl border border-line bg-navy2 p-6">
        <h2 className="h-display text-xl">Watch us everywhere</h2>
        <div className="mt-4 flex flex-wrap gap-3">
          {SOCIALS.map((s) => (
            <a key={s.name} href={s.href} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 rounded-md border border-line px-4 py-2.5 text-sm hover:border-lime hover:text-lime">
              <SocialIcon name={s.name} />{s.name} · {s.handle}
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
