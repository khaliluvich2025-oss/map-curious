'use client';
import { useEffect, useRef, useState } from 'react';

/**
 * Fade-up on scroll. Content is visible in the server HTML (good for SEO / no-JS);
 * only elements that start below the fold are hidden after hydration and revealed when scrolled to.
 */
export default function Reveal({ children, delay = 0, className = '' }: { children: React.ReactNode; delay?: number; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [state, setState] = useState<'static' | 'hidden' | 'shown'>('static');

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (el.getBoundingClientRect().top < window.innerHeight) return;   // already on screen: leave as is
    setState('hidden');
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setState('shown'); io.disconnect(); } }, { rootMargin: '0px 0px -60px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const style: React.CSSProperties = state === 'static' ? {} : {
    opacity: state === 'shown' ? 1 : 0, transform: state === 'shown' ? 'none' : 'translateY(18px)',
    transition: `opacity .55s ${delay}s cubic-bezier(.22,1,.36,1), transform .55s ${delay}s cubic-bezier(.22,1,.36,1)`,
  };
  return <div ref={ref} className={className} style={style}>{children}</div>;
}
