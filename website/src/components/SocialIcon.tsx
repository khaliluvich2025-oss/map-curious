/** Simple monochrome glyphs (not the platforms' official logos). */
export default function SocialIcon({ name, className = 'h-5 w-5' }: { name: string; className?: string }) {
  const p = { className, fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, viewBox: '0 0 24 24', 'aria-hidden': true } as const;
  switch (name) {
    case 'YouTube':
      return <svg {...p}><rect x="2.5" y="5.5" width="19" height="13" rx="3.5" /><path d="M10 9.2v5.6l4.8-2.8z" fill="currentColor" /></svg>;
    case 'Instagram':
      return <svg {...p}><rect x="3.5" y="3.5" width="17" height="17" rx="5" /><circle cx="12" cy="12" r="4" /><circle cx="17.2" cy="6.8" r="1" fill="currentColor" /></svg>;
    case 'TikTok':
      return <svg {...p}><path d="M14 3.5v11.2a3.8 3.8 0 1 1-3.8-3.8" /><path d="M14 3.5c.6 2.6 2.4 4.2 5 4.4" /></svg>;
    case 'Facebook':
      return <svg {...p}><rect x="3.5" y="3.5" width="17" height="17" rx="3" /><path d="M15 8h-1.6c-1 0-1.4.6-1.4 1.5V20M10 12.5h5" /></svg>;
    default:
      return <svg {...p}><circle cx="12" cy="12" r="9" /></svg>;
  }
}
