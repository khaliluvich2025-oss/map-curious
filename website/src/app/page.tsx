import Image from 'next/image';
import Link from 'next/link';
import { Globe2, Play, Target, Search as SearchIcon, MapPin, Lock } from 'lucide-react';
import HeroGlobe from '@/components/HeroGlobe';
import ExploreMap from '@/components/ExploreMap';
import Reveal from '@/components/Reveal';
import SocialIcon from '@/components/SocialIcon';
import { CategoryCard, DiscoveryCard, SectionHead, VideoCard } from '@/components/Cards';
import { DISCOVERIES, featuredDiscoveries } from '@/lib/discoveries';
import { CATEGORIES } from '@/lib/categories';
import { VIDEOS } from '@/lib/videos';
import { SOCIALS } from '@/lib/site';

export default function Home() {
  const markers = DISCOVERIES.map((d) => ({ lat: d.lat, lng: d.lng }));
  const latest = VIDEOS.slice(0, 8);
  return (
    <>
      {/* HERO */}
      <section className="relative overflow-hidden border-b border-line">
        <div className="map-grid absolute inset-0 opacity-60" aria-hidden />
        <div className="wrap relative grid items-center gap-8 py-12 md:py-16 lg:grid-cols-[1.05fr_1fr] lg:py-20">
          <div>
            <p className="eyebrow mb-4">Explore the unbelievable.</p>
            <h1 className="h-display text-[2.7rem] sm:text-6xl lg:text-7xl">
              The world is <span className="block text-lime">stranger</span> than you think.
            </h1>
            <p className="mt-5 max-w-md text-lg text-mist">Real places. Impossible stories. Hidden corners of our planet.</p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/explore" className="btn-primary"><Globe2 className="h-4 w-4" aria-hidden />Explore the map</Link>
              <Link href="/watch" className="btn-ghost"><Play className="h-4 w-4" aria-hidden />Watch stories</Link>
            </div>
            <dl className="mt-10 grid max-w-md grid-cols-3 gap-4 border-t border-line pt-6">
              <div><dt className="text-xs text-mist">Discoveries</dt><dd className="font-display text-2xl font-extrabold">{DISCOVERIES.length}</dd></div>
              <div><dt className="text-xs text-mist">Videos</dt><dd className="font-display text-2xl font-extrabold">{VIDEOS.filter((v) => v.youtubeId || v.links).length}</dd></div>
              <div><dt className="text-xs text-mist">Categories</dt><dd className="font-display text-2xl font-extrabold">{CATEGORIES.length}</dd></div>
            </dl>
          </div>
          <HeroGlobe items={featuredDiscoveries} markers={markers} />
        </div>
      </section>

      {/* FEATURED */}
      <section className="wrap py-14">
        <Reveal><SectionHead eyebrow="Featured discoveries" title="Places that sound made up" sub="Every story fact-checked against primary sources." link={{ href: '/discoveries', label: 'All discoveries' }} /></Reveal>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {featuredDiscoveries.map((d, i) => <Reveal key={d.slug} delay={i * 0.05}><DiscoveryCard d={d} priority={i < 3} /></Reveal>)}
          <Reveal delay={0.25}>
            <Link href="/explore" className="group card relative flex aspect-video h-full flex-col justify-end overflow-hidden p-5 sm:aspect-auto">
              <Image src="/img/world.jpg" alt="" fill sizes="33vw" className="object-cover opacity-40 transition group-hover:opacity-60" />
              <span className="relative font-display text-xl font-extrabold">See all {DISCOVERIES.length} on the map →</span>
              <span className="relative text-sm text-mist">Borders, ghost towns, hidden history and more.</span>
            </Link>
          </Reveal>
        </div>
      </section>

      {/* CATEGORIES */}
      <section className="wrap pb-14">
        <Reveal><SectionHead title="Explore by category" sub="Different places. Stranger stories." link={{ href: '/discoveries', label: 'View all' }} /></Reveal>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {CATEGORIES.map((c) => <CategoryCard key={c.id} c={c} count={DISCOVERIES.filter((d) => d.category === c.id).length} />)}
        </div>
      </section>

      {/* VIDEOS */}
      <section className="wrap pb-14">
        <Reveal><SectionHead title="Latest videos" sub="New places. New mysteries." link={{ href: '/watch', label: 'All videos' }} /></Reveal>
        <div className="grid grid-cols-2 gap-x-4 gap-y-6 md:grid-cols-4">
          {latest.map((v) => <VideoCard key={v.slug} v={v} />)}
        </div>
      </section>

      {/* MAP PREVIEW */}
      <section className="border-y border-line bg-navy2">
        <div className="wrap grid items-center gap-8 py-14 lg:grid-cols-[0.8fr_1.6fr]">
          <div>
            <p className="eyebrow mb-3">Interactive map</p>
            <h2 className="h-display text-4xl sm:text-5xl">Explore <span className="block text-lime">the world</span></h2>
            <p className="mt-4 text-mist">Click a pin to open a place. Every marker sits at a verified coordinate, and where a story covers an area rather than a point, we say so.</p>
            <Link href="/explore" className="btn-primary mt-6"><Globe2 className="h-4 w-4" aria-hidden />Open interactive map</Link>
          </div>
          <ExploreMap items={DISCOVERIES} compact />
        </div>
      </section>

      {/* GAMES */}
      <section className="wrap py-14">
        <Reveal><SectionHead title="Interactive experiences" sub="More than videos. Explore, play and test your geography." /></Reveal>
        <div className="grid gap-4 md:grid-cols-3">
          {[
            { href: '/games/where-on-earth', img: '/img/world.jpg', icon: Target, title: 'Where on Earth?', text: 'Read the clue, drop a pin, see how close you got.', cta: 'Play now' },
            { href: '/games/map-detective', img: '/img/db-cooper.jpg', icon: SearchIcon, title: 'Map Detective', text: 'Study the evidence, follow the clues, solve a fictional case.', cta: 'Open case file' },
            { href: '/suggest', img: '/img/surtsey-lab.jpg', icon: MapPin, title: 'Suggest a place', text: 'Know a strange or mysterious place? Send it our way.', cta: 'Submit now' },
          ].map((g) => (
            <Link key={g.href} href={g.href} className="group relative flex min-h-[220px] flex-col justify-end overflow-hidden rounded-lg border border-line p-5 hover:border-lime">
              <Image src={g.img} alt="" fill sizes="33vw" className="object-cover opacity-50 transition duration-500 group-hover:scale-105" />
              <div className="absolute inset-0 bg-gradient-to-t from-navy via-navy/60 to-transparent" />
              <g.icon className="relative mb-3 h-7 w-7 text-lime" aria-hidden />
              <h3 className="relative font-display text-xl font-extrabold">{g.title}</h3>
              <p className="relative mt-1 text-sm text-mist">{g.text}</p>
              <span className="btn-primary relative mt-4 self-start !py-2">{g.cta}</span>
            </Link>
          ))}
        </div>
        <p className="mt-3 flex items-center gap-1.5 text-xs text-mist"><Lock className="h-3.5 w-3.5" aria-hidden />More Map Detective case packs are in development.</p>
      </section>

      {/* COMMUNITY */}
      <section className="wrap">
        <div className="grid gap-8 rounded-xl border border-line bg-gradient-to-br from-teal/50 to-navy2 p-8 md:grid-cols-2">
          <div>
            <h2 className="h-display text-2xl sm:text-3xl">Join the community</h2>
            <p className="mt-2 text-mist">Which city, country or mystery should we zoom into next? Tell us, and it might become the next Map Curious video.</p>
            <Link href="/suggest" className="btn-primary mt-5">Suggest the next story</Link>
          </div>
          <div>
            <h2 className="h-display text-2xl sm:text-3xl">Follow Map Curious</h2>
            <p className="mt-2 text-mist">New videos every week on your favorite platform.</p>
            <ul className="mt-5 grid grid-cols-2 gap-3">
              {SOCIALS.map((s) => (
                <li key={s.name}>
                  <a href={s.href} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 rounded-md border border-line bg-navy/60 px-3 py-2.5 text-sm hover:border-lime hover:text-lime">
                    <SocialIcon name={s.name} />{s.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </>
  );
}
