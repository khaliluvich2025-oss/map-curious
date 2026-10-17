import Link from 'next/link';
import Logo from './Logo';
import { NAV, SOCIALS, IMAGERY_CREDIT } from '@/lib/site';
import SocialIcon from './SocialIcon';

export default function Footer() {
  return (
    <footer className="mt-24 border-t border-line bg-navy2">
      <div className="wrap grid gap-10 py-12 md:grid-cols-[1.3fr_1fr_1fr]">
        <div>
          <Logo />
          <p className="mt-3 max-w-xs text-sm text-mist">Real places. Impossible stories. A more curious world.</p>
          <div className="mt-5 flex gap-3">
            {SOCIALS.map((s) => (
              <a key={s.name} href={s.href} target="_blank" rel="noopener noreferrer" aria-label={`Map Curious on ${s.name}`}
                className="grid h-10 w-10 place-items-center rounded-md border border-line text-white transition hover:border-lime hover:text-lime">
                <SocialIcon name={s.name} />
              </a>
            ))}
          </div>
        </div>
        <nav aria-label="Footer">
          <p className="eyebrow mb-3">Explore</p>
          <ul className="grid grid-cols-2 gap-2 text-sm text-mist">
            {NAV.map((n) => <li key={n.href}><Link href={n.href} className="hover:text-lime">{n.label}</Link></li>)}
            <li><Link href="/suggest" className="hover:text-lime">Suggest a Place</Link></li>
            <li><Link href="/privacy" className="hover:text-lime">Privacy</Link></li>
          </ul>
        </nav>
        <div className="text-sm text-mist">
          <p className="eyebrow mb-3">Contact</p>
          <p>Story ideas, corrections or collaborations: message Map Curious on any of our channels.</p>
          <p className="mt-4 text-xs text-mist/70">{IMAGERY_CREDIT}</p>
        </div>
      </div>
      <div className="border-t border-line py-5 text-center text-xs text-mist/70">© {new Date().getFullYear()} Map Curious. All rights reserved.</div>
    </footer>
  );
}
