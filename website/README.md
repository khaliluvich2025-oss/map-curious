# Map Curious website

Next.js 15 (App Router) · TypeScript · Tailwind CSS · Leaflet (Esri World Imagery / CARTO tiles) · d3-geo globe · Lucide icons.

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # production build (static pages + SSG)
```

## Content
All content lives in typed data files. No database:
- `src/lib/discoveries.ts`: places (verified coordinates, story, facts, sources)
- `src/lib/videos.ts`: videos (only verified YouTube IDs are embedded)
- `src/lib/categories.ts`, `src/lib/games.ts`, `src/lib/site.ts` (socials, nav)

Images in `public/img` are frames from Map Curious's own videos (NASA Blue Marble base maps) and Esri World Imagery satellite crops (attribution in the footer).

## Deploy on Vercel
1. vercel.com → **Add New… → Project** → import the GitHub repo `khaliluvich2025-oss/map-curious`.
2. **Root Directory: `website`** (Framework preset: Next.js, defaults are fine).
3. Project name: `map-curious` → Deploy.
4. Optional env var: `NEXT_PUBLIC_SITE_URL` = the final URL (used for canonical/OG/sitemap), then redeploy.
