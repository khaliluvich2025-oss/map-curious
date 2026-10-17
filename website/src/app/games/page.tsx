import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { Lock, Search, Target } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Games',
  description: 'Play Where on Earth?, the geography guessing game, and Map Detective, a map-based investigation game.',
  alternates: { canonical: '/games' },
};

export default function GamesPage() {
  return (
    <div className="wrap py-10">
      <p className="eyebrow">Play</p>
      <h1 className="h-display mt-2 text-4xl sm:text-5xl">Games</h1>
      <p className="mt-3 max-w-2xl text-mist">Test what you know about the world, and how well you read a map.</p>
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <Link href="/games/where-on-earth" className="group card overflow-hidden hover:border-lime">
          <div className="relative aspect-video"><Image src="/img/world.jpg" alt="" fill sizes="50vw" className="object-cover transition duration-500 group-hover:scale-105" /></div>
          <div className="p-6">
            <Target className="h-7 w-7 text-lime" aria-hidden />
            <h2 className="mt-3 font-display text-2xl font-extrabold">Where on Earth?</h2>
            <p className="mt-2 text-mist">Five rounds. Read the clue, drop your pin on the satellite map, and score points for how close you get.</p>
            <span className="btn-primary mt-5">Play now</span>
          </div>
        </Link>
        <Link href="/games/map-detective" className="group card overflow-hidden hover:border-lime">
          <div className="relative aspect-video"><Image src="/img/db-cooper.jpg" alt="" fill sizes="50vw" className="object-cover transition duration-500 group-hover:scale-105" /></div>
          <div className="p-6">
            <Search className="h-7 w-7 text-lime" aria-hidden />
            <h2 className="mt-3 font-display text-2xl font-extrabold">Map Detective</h2>
            <p className="mt-2 text-mist">Case #001: The Vanishing Cartographer. Examine the evidence, read the map, and find where she went. A fictional case.</p>
            <span className="btn-primary mt-5">Open case file</span>
          </div>
        </Link>
      </div>
      <p className="mt-6 flex items-center gap-2 text-sm text-mist"><Lock className="h-4 w-4" aria-hidden />More investigation packs are in development.</p>
    </div>
  );
}
