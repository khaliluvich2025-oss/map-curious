import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'Privacy', description: 'How the Map Curious website handles your data.', alternates: { canonical: '/privacy' } };

export default function PrivacyPage() {
  return (
    <div className="wrap max-w-3xl py-12">
      <h1 className="h-display text-4xl">Privacy</h1>
      <div className="mt-6 space-y-4 text-mist">
        <p>This website has no user accounts and does not collect personal information through forms. The “Suggest a place” form runs entirely in your browser: it prepares a message for you to send us yourself on a social platform.</p>
        <p>Videos load from YouTube’s privacy-enhanced domain (youtube-nocookie.com) only after you press play. Map tiles are loaded from Esri and CARTO/OpenStreetMap servers, which receive standard request data such as your IP address.</p>
        <p>Games keep their scores in memory only; nothing is stored or sent.</p>
        <p>Questions? Message Map Curious on any of our social channels.</p>
      </div>
    </div>
  );
}
