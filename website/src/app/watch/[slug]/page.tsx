import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ArrowLeft, Clock, ExternalLink, MapPin } from 'lucide-react';
import { VIDEOS, videoBySlug } from '@/lib/videos';
import { discoveryBySlug } from '@/lib/discoveries';
import { categoryById } from '@/lib/categories';
import YouTube from '@/components/YouTube';
import { VideoCard } from '@/components/Cards';
import { SOCIALS } from '@/lib/site';

export function generateStaticParams() {
  return VIDEOS.map((v) => ({ slug: v.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const v = videoBySlug((await params).slug);
  if (!v) return {};
  return { title: v.title, description: `Watch “${v.title}” from Map Curious.`, alternates: { canonical: `/watch/${v.slug}` }, openGraph: { images: [v.image] } };
}

export default async function VideoPage({ params }: { params: Promise<{ slug: string }> }) {
  const v = videoBySlug((await params).slug);
  if (!v) notFound();
  const d = v.discovery ? discoveryBySlug(v.discovery) : undefined;
  const more = VIDEOS.filter((x) => x.slug !== v.slug && x.category === v.category).slice(0, 4);
  const yt = SOCIALS.find((s) => s.name === 'YouTube')!;

  return (
    <div className="wrap py-8">
      <Link href="/watch" className="inline-flex items-center gap-1 text-sm text-mist hover:text-lime"><ArrowLeft className="h-4 w-4" aria-hidden />All videos</Link>
      <div className="mt-6 grid gap-10 lg:grid-cols-[1fr_380px]">
        <div>
          {v.youtubeId ? <YouTube id={v.youtubeId} title={v.title} vertical={v.kind === 'short'} /> : (
            <div className="relative aspect-video overflow-hidden rounded-lg border border-line">
              <Image src={v.image} alt="" fill priority sizes="70vw" className="object-cover opacity-60" />
              <div className="absolute inset-0 grid place-items-center p-6 text-center">
                {v.status === 'coming-soon' ? (
                  <div><p className="flex items-center justify-center gap-1 font-display font-extrabold text-fire"><Clock className="h-4 w-4" aria-hidden />COMING SOON</p>
                    <a href={yt.href} target="_blank" rel="noopener noreferrer" className="btn-primary mt-4">Subscribe on YouTube</a></div>
                ) : (
                  <div className="flex flex-wrap justify-center gap-3">
                    {v.links?.map((l) => <a key={l.href} href={l.href} target="_blank" rel="noopener noreferrer" className="btn-primary">{l.label}<ExternalLink className="h-4 w-4" aria-hidden /></a>)}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        <div>
          <p className="chip">{categoryById(v.category).name} · {v.kind === 'long' ? 'Long-form' : 'Short'}</p>
          <h1 className="h-display mt-3 text-3xl">{v.title}</h1>
          {v.youtubeId && (
            <a href={`https://www.youtube.com/watch?v=${v.youtubeId}`} target="_blank" rel="noopener noreferrer" className="mt-4 inline-flex items-center gap-1 text-sm text-lime hover:underline">
              Open on YouTube<ExternalLink className="h-3.5 w-3.5" aria-hidden />
            </a>
          )}
          {d && (
            <Link href={`/discoveries/${d.slug}`} className="card mt-6 block p-4 hover:border-lime">
              <p className="eyebrow">Read the story</p>
              <p className="mt-1 font-display font-extrabold">{d.name}</p>
              <p className="mt-1 flex items-center gap-1 text-xs text-mist"><MapPin className="h-3.5 w-3.5" aria-hidden />{d.place}</p>
            </Link>
          )}
        </div>
      </div>
      {more.length > 0 && (
        <section className="mt-14">
          <h2 className="h-display mb-4 text-2xl">More like this</h2>
          <div className="grid grid-cols-2 gap-x-4 gap-y-6 md:grid-cols-4">{more.map((x) => <VideoCard key={x.slug} v={x} />)}</div>
        </section>
      )}
    </div>
  );
}
