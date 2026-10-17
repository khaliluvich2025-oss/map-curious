import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ArrowLeft, ExternalLink, MapPin, AlertTriangle } from 'lucide-react';
import { DISCOVERIES, discoveryBySlug, relatedDiscoveries } from '@/lib/discoveries';
import { categoryById } from '@/lib/categories';
import { videoForDiscovery } from '@/lib/videos';
import { formatCoord } from '@/lib/geo';
import { DiscoveryCard } from '@/components/Cards';
import YouTube from '@/components/YouTube';
import MiniMap from './MiniMap';
import { SITE } from '@/lib/site';

export function generateStaticParams() {
  return DISCOVERIES.map((d) => ({ slug: d.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const d = discoveryBySlug((await params).slug);
  if (!d) return {};
  return {
    title: `${d.name} · ${d.place}`,
    description: d.summary + ' ' + d.intro.slice(0, 120),
    alternates: { canonical: `/discoveries/${d.slug}` },
    openGraph: { title: d.name, description: d.summary, images: [d.image], type: 'article' },
  };
}

export default async function DiscoveryPage({ params }: { params: Promise<{ slug: string }> }) {
  const d = discoveryBySlug((await params).slug);
  if (!d) notFound();
  const video = videoForDiscovery(d.slug);
  const ld = {
    '@context': 'https://schema.org', '@type': 'Article', headline: d.name, description: d.summary,
    image: `${SITE.url}${d.image}`, publisher: { '@type': 'Organization', name: 'Map Curious' },
    about: { '@type': 'Place', name: d.place, geo: { '@type': 'GeoCoordinates', latitude: d.lat, longitude: d.lng } },
  };

  return (
    <article>
      <header className="relative h-[52vh] min-h-[360px] overflow-hidden border-b border-line">
        <Image src={d.image} alt={`${d.place}`} fill priority sizes="100vw" className="object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/50 to-navy/10" />
        <div className="wrap relative flex h-full flex-col justify-end pb-10">
          <Link href="/discoveries" className="mb-auto mt-6 inline-flex items-center gap-1 self-start rounded bg-navy/70 px-2.5 py-1.5 text-sm text-mist hover:text-lime"><ArrowLeft className="h-4 w-4" aria-hidden />All discoveries</Link>
          <Link href={`/discoveries?category=${d.category}`} className="chip self-start !bg-navy/80 hover:text-lime">{categoryById(d.category).name}</Link>
          <h1 className="h-display mt-3 max-w-4xl text-4xl sm:text-6xl">{d.name}</h1>
          <p className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 text-mist">
            <span className="flex items-center gap-1 text-lime"><MapPin className="h-4 w-4" aria-hidden />{d.place}</span>
            <span>{d.country}</span>
            <span className="text-sm">{formatCoord(d.lat, d.lng)}</span>
          </p>
        </div>
      </header>

      <div className="wrap grid gap-10 py-10 lg:grid-cols-[1.5fr_1fr]">
        <div>
          <p className="text-xl leading-relaxed text-white">{d.intro}</p>
          {d.unresolved && (
            <p className="mt-6 flex gap-2 rounded-md border border-fire/50 bg-fire/10 p-3 text-sm text-fire">
              <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />Open case: what happened has never been confirmed. We present the evidence, not a solution.
            </p>
          )}
          <div className="mt-6 space-y-5 text-lg leading-relaxed text-mist">{d.story.map((p, i) => <p key={i}>{p}</p>)}</div>
          {video && (
            <section className="mt-10">
              <h2 className="h-display mb-4 text-2xl">Watch the story</h2>
              {video.youtubeId ? <YouTube id={video.youtubeId} title={video.title} vertical={video.kind === 'short'} /> : (
                <div className="flex flex-wrap gap-3">
                  {video.links?.map((l) => <a key={l.href} href={l.href} target="_blank" rel="noopener noreferrer" className="btn-ghost">{l.label}<ExternalLink className="h-4 w-4" aria-hidden /></a>)}
                </div>
              )}
            </section>
          )}
        </div>
        <aside className="space-y-6">
          <div className="card overflow-hidden">
            <div className="h-64"><MiniMap lat={d.lat} lng={d.lng} label={d.place} /></div>
            {d.coordNote && <p className="border-t border-line p-3 text-xs italic text-mist">{d.coordNote}</p>}
          </div>
          <div className="card p-5">
            <h2 className="eyebrow mb-3">Quick facts</h2>
            <ul className="space-y-2 text-sm">{d.facts.map((f) => <li key={f} className="flex gap-2"><span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-lime" />{f}</li>)}</ul>
          </div>
          <div className="card p-5">
            <h2 className="eyebrow mb-3">Sources</h2>
            <ul className="space-y-2 text-sm">
              {d.sources.map((s) => <li key={s.url}><a href={s.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-mist hover:text-lime">{s.label}<ExternalLink className="h-3.5 w-3.5" aria-hidden /></a></li>)}
            </ul>
          </div>
        </aside>
      </div>

      <section className="wrap">
        <h2 className="h-display mb-5 text-2xl">Explore next</h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{relatedDiscoveries(d).map((r) => <DiscoveryCard key={r.slug} d={r} />)}</div>
      </section>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }} />
    </article>
  );
}
