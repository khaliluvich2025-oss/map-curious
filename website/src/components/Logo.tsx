import Link from 'next/link';

export function GlobeMark({ className = 'h-8 w-8' }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden="true">
      <circle cx="16" cy="16" r="13" fill="none" stroke="#C8F34B" strokeWidth="2.4" />
      <ellipse cx="16" cy="16" rx="6" ry="13" fill="none" stroke="#C8F34B" strokeWidth="1.8" />
      <path d="M3.5 12h25M3.5 20h25" stroke="#C8F34B" strokeWidth="1.8" />
      <circle cx="22.5" cy="9.5" r="3.2" fill="#C8F34B" stroke="#081521" strokeWidth="1.4" />
    </svg>
  );
}

export default function Logo() {
  return (
    <Link href="/" className="flex items-center gap-2.5 rounded focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-lime" aria-label="Map Curious home">
      <GlobeMark />
      <span className="font-display text-xl font-extrabold tracking-tight text-lime sm:text-2xl">MAP CURIOUS</span>
    </Link>
  );
}
