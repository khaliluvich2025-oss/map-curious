'use client';
import { useEffect, useRef } from 'react';
import { geoGraticule10, geoOrthographic, geoPath, geoDistance } from 'd3-geo';
import { feature } from 'topojson-client';
import type { Topology } from 'topojson-specification';
import type { FeatureCollection } from 'geojson';
import land110 from 'world-atlas/land-110m.json';

/** Orthographic globe on a 2D canvas: slow spin, drag to rotate, glowing lime markers on the visible side. */
export default function Globe({ markers, className = '' }: { markers: { lat: number; lng: number }[]; className?: string }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const rot = useRef<[number, number]>([20, -22]);
  const drag = useRef<{ x: number; y: number; r: [number, number] } | null>(null);

  useEffect(() => {
    const canvas = ref.current!;
    const ctx = canvas.getContext('2d')!;
    const topo = land110 as unknown as Topology;
    const land = feature(topo, topo.objects.land) as unknown as FeatureCollection;
    const grat = geoGraticule10();
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let raf = 0, last = performance.now(), visible = true;

    const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; });
    io.observe(canvas);

    const draw = (now: number) => {
      raf = requestAnimationFrame(draw);
      if (!visible) return;
      const dt = Math.min(64, now - last); last = now;
      if (!reduce && !drag.current) rot.current = [rot.current[0] + dt * 0.006, rot.current[1]];
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      const size = canvas.clientWidth;
      if (canvas.width !== Math.round(size * dpr)) { canvas.width = canvas.height = Math.round(size * dpr); }
      const s = canvas.width;
      const r = s * 0.46;
      const proj = geoOrthographic().scale(r).translate([s / 2, s / 2]).rotate(rot.current).clipAngle(90);
      const path = geoPath(proj, ctx);
      ctx.clearRect(0, 0, s, s);
      // atmosphere
      const g = ctx.createRadialGradient(s / 2, s / 2, r * 0.9, s / 2, s / 2, r * 1.12);
      g.addColorStop(0, 'rgba(55,170,190,0.35)'); g.addColorStop(1, 'rgba(55,170,190,0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(s / 2, s / 2, r * 1.12, 0, Math.PI * 2); ctx.fill();
      // ocean
      const o = ctx.createRadialGradient(s * 0.38, s * 0.35, r * 0.1, s / 2, s / 2, r);
      o.addColorStop(0, '#1d5566'); o.addColorStop(1, '#0a2533');
      ctx.fillStyle = o; ctx.beginPath(); path({ type: 'Sphere' }); ctx.fill();
      // graticule
      ctx.beginPath(); path(grat); ctx.strokeStyle = 'rgba(200,243,75,0.08)'; ctx.lineWidth = dpr; ctx.stroke();
      // land
      ctx.beginPath(); path(land); ctx.fillStyle = '#2f5a3e'; ctx.fill();
      ctx.strokeStyle = 'rgba(220,240,200,0.35)'; ctx.lineWidth = 0.8 * dpr; ctx.stroke();
      // terminator-ish shading
      const sh = ctx.createLinearGradient(s * 0.2, s * 0.1, s * 0.95, s * 0.95);
      sh.addColorStop(0, 'rgba(255,255,255,0.06)'); sh.addColorStop(1, 'rgba(0,0,0,0.45)');
      ctx.fillStyle = sh; ctx.beginPath(); path({ type: 'Sphere' }); ctx.fill();
      // markers
      const centre: [number, number] = [-rot.current[0], -rot.current[1]];
      const pulse = (now / 1600) % 1;
      for (const m of markers) {
        if (geoDistance([m.lng, m.lat], centre) > Math.PI / 2 - 0.05) continue;
        const p = proj([m.lng, m.lat]); if (!p) continue;
        ctx.beginPath(); ctx.arc(p[0], p[1], (5 + pulse * 14) * dpr, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(200,243,75,${0.8 * (1 - pulse)})`; ctx.lineWidth = 1.5 * dpr; ctx.stroke();
        ctx.beginPath(); ctx.arc(p[0], p[1], 4 * dpr, 0, Math.PI * 2);
        ctx.fillStyle = '#C8F34B'; ctx.shadowColor = '#C8F34B'; ctx.shadowBlur = 12 * dpr; ctx.fill(); ctx.shadowBlur = 0;
      }
    };
    raf = requestAnimationFrame(draw);
    return () => { cancelAnimationFrame(raf); io.disconnect(); };
  }, [markers]);

  return (
    <canvas ref={ref} aria-hidden className={`aspect-square w-full cursor-grab touch-pan-y active:cursor-grabbing ${className}`}
      onPointerDown={(e) => { drag.current = { x: e.clientX, y: e.clientY, r: rot.current }; }}
      onPointerUp={() => { drag.current = null; }}
      onPointerLeave={() => { drag.current = null; }}
      onPointerMove={(e) => {
        const d = drag.current; if (!d) return;
        rot.current = [d.r[0] + (e.clientX - d.x) * 0.3, Math.max(-60, Math.min(60, d.r[1] - (e.clientY - d.y) * 0.3))];
      }} />
  );
}
