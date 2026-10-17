import type { Metadata } from 'next';
import SuggestForm from './SuggestForm';

export const metadata: Metadata = {
  title: 'Suggest a Place',
  description: 'Know a strange border, ghost town or unexplained place? Suggest it for a future Map Curious story.',
  alternates: { canonical: '/suggest' },
};

export default function SuggestPage() {
  return (
    <div className="wrap max-w-3xl py-12">
      <p className="eyebrow">Community</p>
      <h1 className="h-display mt-2 text-4xl sm:text-5xl">Suggest a place</h1>
      <p className="mt-3 text-mist">Which city, country or mystery should we zoom into next? Fill this in, and we’ll prepare a message you can send us on the platform you use most.</p>
      <SuggestForm />
    </div>
  );
}
