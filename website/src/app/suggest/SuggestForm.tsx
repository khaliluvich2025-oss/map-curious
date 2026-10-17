'use client';
import { useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { SOCIALS } from '@/lib/site';
import SocialIcon from '@/components/SocialIcon';

/** No backend: the form builds a message, copies it, and points the visitor to our DMs. */
export default function SuggestForm() {
  const [place, setPlace] = useState('');
  const [why, setWhy] = useState('');
  const [msg, setMsg] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [err, setErr] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (place.trim().length < 2) { setErr('Please tell us the place.'); return; }
    setErr('');
    const m = `Map Curious story idea: ${place.trim()}${why.trim() ? `\nWhy it’s curious: ${why.trim()}` : ''}`;
    setMsg(m);
    try { await navigator.clipboard.writeText(m); setCopied(true); } catch { setCopied(false); }
  };

  return (
    <div className="mt-8">
      <form onSubmit={submit} className="card space-y-5 p-6" noValidate>
        <div>
          <label htmlFor="place" className="block text-sm font-semibold">Place or mystery <span className="text-lime">*</span></label>
          <input id="place" value={place} onChange={(e) => setPlace(e.target.value)} required aria-invalid={!!err} aria-describedby={err ? 'place-err' : undefined}
            placeholder="e.g. Baarle-Hertog, Belgium" className="mt-2 w-full rounded-md border border-line bg-navy px-3 py-2.5 focus:border-lime focus:outline-none" />
          {err && <p id="place-err" className="mt-1 text-sm text-red-300">{err}</p>}
        </div>
        <div>
          <label htmlFor="why" className="block text-sm font-semibold">What makes it strange? <span className="text-mist">(optional)</span></label>
          <textarea id="why" value={why} onChange={(e) => setWhy(e.target.value)} rows={4} placeholder="A border runs through a café..."
            className="mt-2 w-full rounded-md border border-line bg-navy px-3 py-2.5 focus:border-lime focus:outline-none" />
        </div>
        <button className="btn-primary">Prepare my suggestion</button>
      </form>
      {msg && (
        <div className="card mt-6 p-6" aria-live="polite">
          <p className="flex items-center gap-2 font-semibold">{copied ? <><Check className="h-4 w-4 text-lime" aria-hidden />Copied to your clipboard.</> : <><Copy className="h-4 w-4" aria-hidden />Copy this message:</>}</p>
          <pre className="mt-3 whitespace-pre-wrap rounded-md bg-navy p-3 text-sm text-mist">{msg}</pre>
          <p className="mt-4 text-sm text-mist">Now paste it in a message or comment to Map Curious:</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {SOCIALS.map((s) => <a key={s.name} href={s.href} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 rounded-md border border-line px-3 py-2 text-sm hover:border-lime hover:text-lime"><SocialIcon name={s.name} />{s.name}</a>)}
          </div>
        </div>
      )}
    </div>
  );
}
