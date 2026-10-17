'use client';
import { useState } from 'react';
import { Play } from 'lucide-react';

/** Privacy-friendly embed: thumbnail first, the YouTube iframe (youtube-nocookie) loads on click. */
export default function YouTube({ id, title, vertical = false }: { id: string; title: string; vertical?: boolean }) {
  const [on, setOn] = useState(false);
  const box = vertical ? 'aspect-[9/16] max-w-sm' : 'aspect-video';
  if (on)
    return (
      <div className={`${box} mx-auto w-full overflow-hidden rounded-lg border border-line`}>
        <iframe className="h-full w-full" src={`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`} title={title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
      </div>
    );
  return (
    <button onClick={() => setOn(true)} className={`${box} group relative mx-auto block w-full overflow-hidden rounded-lg border border-line bg-navy2`} aria-label={`Play video: ${title}`}>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={`https://i.ytimg.com/vi/${id}/hqdefault.jpg`} alt="" className="h-full w-full object-cover opacity-80" loading="lazy" />
      <span className="absolute inset-0 grid place-items-center">
        <span className="grid h-16 w-16 place-items-center rounded-full bg-lime text-navy shadow-lg transition group-hover:scale-110">
          <Play className="ml-1 h-7 w-7 fill-navy" aria-hidden />
        </span>
      </span>
    </button>
  );
}
