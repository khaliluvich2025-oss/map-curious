'use client';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { Lightbulb, RotateCcw, Trophy } from 'lucide-react';
import { WHERE_ROUNDS, scoreFor, type Round } from '@/lib/games';
import { discoveryBySlug } from '@/lib/discoveries';
import { miles } from '@/lib/geo';

const LeafletMap = dynamic(() => import('@/components/LeafletMap'), { ssr: false, loading: () => <div className="h-full w-full animate-pulse bg-navy2" /> });
const ROUNDS = 5;

function pick(): Round[] {
  const a = [...WHERE_ROUNDS];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a.slice(0, ROUNDS);
}

export default function WhereOnEarth() {
  const [rounds, setRounds] = useState<Round[]>([]);
  const [i, setI] = useState(0);
  const [guess, setGuess] = useState<[number, number] | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [hint, setHint] = useState(false);
  const [results, setResults] = useState<{ slug: string; dist: number; pts: number }[]>([]);
  const [mapKey, setMapKey] = useState(0);

  const start = useCallback(() => {
    setRounds(pick()); setI(0); setGuess(null); setRevealed(false); setHint(false); setResults([]); setMapKey((k) => k + 1);
  }, []);
  useEffect(start, [start]);

  if (!rounds.length) return <div className="mt-6 h-[60vh] animate-pulse rounded-xl bg-navy2" />;
  const done = results.length === ROUNDS && revealed && i === ROUNDS - 1;
  const r = rounds[i];
  const d = discoveryBySlug(r.slug)!;
  const answer: [number, number] = [d.lat, d.lng];
  const total = results.reduce((s, x) => s + x.pts, 0);
  const last = results[results.length - 1];

  const submit = () => {
    if (!guess) return;
    const dist = miles(guess, answer);
    const pts = Math.max(0, scoreFor(dist) - (hint ? 150 : 0));
    setResults((x) => [...x, { slug: r.slug, dist, pts }]); setRevealed(true);
  };
  const next = () => { setI((x) => x + 1); setGuess(null); setRevealed(false); setHint(false); setMapKey((k) => k + 1); };

  return (
    <div className="mt-6 grid gap-5 lg:grid-cols-[360px_1fr]">
      <div className="card flex flex-col p-5">
        <div className="flex items-center justify-between text-sm text-mist">
          <span>Round {Math.min(i + 1, ROUNDS)} / {ROUNDS}</span>
          <span className="font-display font-extrabold text-lime">{total} pts</span>
        </div>
        {!done ? (
          <>
            <p className="eyebrow mt-5">The clue</p>
            <p className="mt-2 text-lg leading-snug">{r.clue}</p>
            {hint && <p className="mt-3 rounded-md bg-teal/40 p-3 text-sm text-mist">Hint: {r.hint}</p>}
            {!revealed ? (
              <>
                <p className="mt-4 text-sm text-mist" aria-live="polite">{guess ? 'Pin dropped. Lock it in, or click the map to move it.' : 'Click the map to drop your pin.'}</p>
                <div className="mt-auto flex flex-wrap gap-2 pt-5">
                  <button onClick={submit} disabled={!guess} className="btn-primary disabled:cursor-not-allowed disabled:opacity-40">Lock in guess</button>
                  {!hint && <button onClick={() => setHint(true)} className="btn-ghost"><Lightbulb className="h-4 w-4" aria-hidden />Hint (−150)</button>}
                </div>
              </>
            ) : (
              <div className="mt-5 rounded-md border border-lime/50 bg-lime/10 p-4" aria-live="polite">
                <p className="font-display text-lg font-extrabold">{d.place}</p>
                <p className="text-sm text-mist">You were <b className="text-white">{Math.round(last.dist).toLocaleString()} miles</b> away · <b className="text-lime">+{last.pts} pts</b></p>
                <Link href={`/discoveries/${d.slug}`} className="mt-2 inline-block text-sm text-lime underline" target="_blank">Read the story</Link>
                <button onClick={i === ROUNDS - 1 ? () => setI(i) : next} className="btn-primary mt-4 w-full">{i === ROUNDS - 1 ? 'See results' : 'Next round'}</button>
              </div>
            )}
          </>
        ) : (
          <div className="mt-5" aria-live="polite">
            <Trophy className="h-10 w-10 text-lime" aria-hidden />
            <p className="mt-3 font-display text-3xl font-extrabold">{total} <span className="text-base text-mist">/ {ROUNDS * 1000}</span></p>
            <p className="text-mist">{total > 4000 ? 'World-class navigator.' : total > 2500 ? 'Seasoned explorer.' : total > 1200 ? 'Curious traveler.' : 'Every explorer starts somewhere.'}</p>
            <ul className="mt-4 space-y-1.5 text-sm">
              {results.map((x) => <li key={x.slug} className="flex justify-between gap-3 border-b border-line pb-1.5"><span className="text-mist">{discoveryBySlug(x.slug)!.place}</span><span>{Math.round(x.dist).toLocaleString()} mi · <b className="text-lime">{x.pts}</b></span></li>)}
            </ul>
            <button onClick={start} className="btn-primary mt-5 w-full"><RotateCcw className="h-4 w-4" aria-hidden />Play again</button>
          </div>
        )}
      </div>
      <div className="h-[58vh] min-h-[380px] overflow-hidden rounded-xl border border-line lg:h-[620px]">
        <LeafletMap key={mapKey} label="Guessing map: click to place your pin" onMapClick={(lat, lng) => !revealed && setGuess([lat, ((lng + 540) % 360) - 180])}
          guess={guess} answer={revealed ? answer : null} center={[25, 0]} zoom={2} />
      </div>
    </div>
  );
}
