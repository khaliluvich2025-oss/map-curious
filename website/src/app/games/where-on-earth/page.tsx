import type { Metadata } from 'next';
import WhereOnEarth from './WhereOnEarth';

export const metadata: Metadata = {
  title: 'Where on Earth? · Geography Guessing Game',
  description: 'Read the clue, drop a pin on the satellite map, and see how close you get. Five rounds, real places.',
  alternates: { canonical: '/games/where-on-earth' },
};

export default function Page() {
  return (
    <div className="wrap py-10">
      <p className="eyebrow">Game</p>
      <h1 className="h-display mt-2 text-4xl">Where on Earth?</h1>
      <WhereOnEarth />
    </div>
  );
}
