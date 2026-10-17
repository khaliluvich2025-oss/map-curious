# Map Curious — daily cloud run (one finished video)

> **OWNER RULE (2026-10-17) — overrides anything below and anything in the routine prompt:**
> Do NOT schedule, publish, edit or delete anything in Metricool. Step 9 is DISABLED.
> Finished videos need the owner's (Khalil's) approval first. After step 8 (commit + push to `ready/`),
> stop and send a notification: "Video NN <topic> ready for approval: ready/NN_Slug/".
> Scheduling happens only when the owner approves in a live session, and then as ONE YouTube Shorts post
> plus ONE combined Facebook/Instagram/TikTok post at the same approved time, MapCurious brand 6812967 only.


You are running unattended in a cloud session with this repo checked out. Nobody will answer questions.
Produce ONE new finished Map Curious vertical video, commit it to `ready/`, push, then schedule it in
Metricool (step 9) at the next New York slot (9 AM, 1 PM, 6 PM or 10 PM ET), and stop. Post ONLY through step 9, ONLY to the MapCurious brand,
and only after the video passed the checks in step 7.

Paths below are relative to the repo root.

## 0. Setup
```bash
bash setup.sh
export MC_WHISPER=small.en MC_WORKERS=3
```
(MC_WORKERS may be raised to 4–6 if `nproc` is ≥ 8.)

## 1. Topic
Read `ready/topics_log.txt` and NEVER repeat a topic in it. Pick a surprising, factual,
US-audience geography/history story that fits ONE of these existing NASA Blue Marble maps
(no new map downloads):

| `gfx` folder (in 2026-10-14_Map_Curious_Graphics) | region | extras |
|---|---|---|
| `01_fort_jefferson` | Gulf of Mexico, Florida, Cuba, Bahamas, Yucatán | Florida SVG polygons; Cuba land mask trick in ep08 |
| `02_db_cooper` | Pacific NW: WA, OR, N. CA, NV, ID | Washington SVG polygons |
| `03_centralia` | Northeast US: PA, NY, Great Lakes (Erie/Ontario), Chesapeake | Pennsylvania SVG polygons |
| `04_denmark_strait` | Greenland, Iceland, North Atlantic | Greenland/Iceland masks via `EP4._build_land` |

Keep map zoom ≤ ~3.4. Only facts you are confident about from official sources
(USGS, NPS, NOAA, state DOTs/agencies); use "about/roughly" for numbers.

## 2. Script
~105–120 words (→ 42–53 s). Bill delivery tags: `[curious]`, `[short pause]`, `[serious]`, `[confident]`.
Strong first-sentence hook. Episode number NN = (highest NN in `ready/` folder names, or 08 if none) + 1.
Slug like `09_Hoover_Dam`. Save the script (with tags) to `2026-10-16_Map_Curious_Voiceovers/NN_Slug_script.txt`.

## 3. Narration — ONE take only (~$0.15)
Preferred: the ElevenLabs connector (tool names may be prefixed):
`creative_generate_speech` with model `eleven_v4`, voice_id `pqHfZKP75CvOlQylNhV4` ("Bill - Wise, Mature, Balanced"),
`generations_count: 1`, prompt = the script. Then poll `creative_get_flow_run_status` (flow_id + session_ids from
the result) until completed and download `content_url` with curl to
`2026-10-16_Map_Curious_Voiceovers/NN_Slug.mp3`.

Fallback if no connector but `$ELEVENLABS_API_KEY` is set:
```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json,sys;print(json.dumps({"text":open(sys.argv[1]).read(),"model_id":"eleven_v3"}))' 2026-10-16_Map_Curious_Voiceovers/NN_Slug_script.txt)" \
  -o 2026-10-16_Map_Curious_Voiceovers/NN_Slug.mp3
```
If neither works: STOP, commit nothing, and report that narration was unavailable.

## 4. Timing
```bash
cd Map_Curious_Edit/src
python3 align.py --vo 2026-10-16_Map_Curious_Voiceovers NN_Slug
python3 refine_timing.py --vo 2026-10-16_Map_Curious_Voiceovers NN_Slug
```
Add `'NN': 'epNN_slug'` to `EPISODES` in `render.py`.

## 5. Episode file `Map_Curious_Edit/src/epNN_slug.py`
Copy the closest template: map-only → `ep08_overseas_highway.py`; map + schematic panel → `ep05/06/07`.
Class `EP(Episode)` with `slug, gfx, vo = ROOT / '2026-10-16_Map_Curious_Voiceovers', out, title, cover_title,
cover_t, emphasis`, plus `setup()` / `draw()`.
- Key every beat to a spoken word with `self.w('word', n)`. Capitalised queries match case-sensitively; count occurrences.
- A visual change every ~1.5–2.5 s (~25–35 beats), logged with `self.beat(t, desc, sfx)`.
- Hook in the first 2 s: map visible at frame 0 with a pin/label.
- Keep labels out of the caption band (y 970–1148) and away from x > 930; clamp chips inside the frame.
- Diagrams must be LARGE: full frame width in the area y ~250–950, not a small upper panel over empty dark space.
- Schematic panels: draw on an opaque RGB canvas (see ep05/06/07 `panel()`); label "SCHEMATIC · NOT TO SCALE".
- Lower info area (y ~1250–1420) for hero numbers and chips.

## 6. Preview → fix → render
```bash
python3 render.py NN --contact 0,<dur>,1.5      # view Map_Curious_Edit/qa/NN_contact_*.jpg, fix obvious problems once
python3 render.py NN                             # writes output/, covers/, srt/
```
If the render crashes (BrokenProcessPool), retry with `MC_WORKERS=2`.

## 7. Check the real MP4
1080x1920, 24 fps, duration ≈ MP3, `ffmpeg -vf blackdetect=d=0.1:pix_th=0.10` finds no black,
and a frame sheet (`ffmpeg -i F -vf "fps=1,scale=160:-1,tile=10x6" -frames:v 1 sheet.jpg`) looks right.

## 8. Deliver (commit to the repo)
Create `ready/NN_Slug/` containing:
- `NN_Slug_Final.mp4`, `NN_Slug_Cover.jpg`, `NN_Slug_Final.srt`
- `captions.txt` with blocks: `=== INSTAGRAM ===` (hook + 2–3 sentences + ~9 hashtags incl. #MapCurious; EVERY platform block must also include the owner-required #SMMW20 #inbound19),
  `=== FACEBOOK ===` (slightly longer, ~4 hashtags), `=== TIKTOK ===` (one punchy line + ~8 hashtags incl.
  #learnontiktok #mapcurious), `=== YOUTUBE SHORTS TITLE ===`, `=== YOUTUBE TAGS ===` (comma-separated),
  and a final note: "Narration is an AI voice (ElevenLabs) - use each platform's AI-content label if required."

Append `YYYY-MM-DD  NN Topic` to `ready/topics_log.txt`. Also commit the new episode file, script and the
`render.py` change. Then:
```bash
git add -A && git commit -m "Map Curious NN: <topic>" && git push origin HEAD
```
(If pushing to the default branch is refused, push a branch named `video/NN-slug` instead.)

## 9. DISABLED — see the owner rule at the top. (Kept for reference only; do not run.)
The repo is public, so the pushed video has a public URL:
`https://raw.githubusercontent.com/khaliluvich2025-oss/map-curious/main/ready/NN_Slug/NN_Slug_Final.mp4`
(if you pushed a branch instead of main, use that branch name). Check it first:
`curl -sI <url>` must return 200 and the right Content-Length. If not, wait 60 s and retry (max 3 tries).

Use the Metricool connector (tool names may be prefixed):
1. `getBrandSettings` → use ONLY the brand whose label is `MapCurious` (blogId should be 6812967). Never touch other brands.
2. Publish time — New York slots: **09:00, 13:00, 18:00, 22:00 America/New_York**.
   Pick the FIRST slot that is at least 30 minutes after now (`TZ=America/New_York date '+%Y-%m-%d %H:%M'`)
   AND has no MapCurious post already scheduled at that time (check with `getScheduledPosts` for blogId 6812967
   over the next 3 days); if none is left today, continue with 09:00 tomorrow, and so on. One video per slot. Offset: `TZ=America/New_York date -d '<slot date+time>' +%:z`.
   `date` = `YYYY-MM-DDTHH:00:00<offset>`; `publicationDate` = `{"dateTime":"YYYY-MM-DDTHH:00:00","timezone":"America/New_York"}`.
   Never double up a slot; never move or touch existing posts.
3. Create FOUR separate scheduled posts with `createScheduledPost` (one network each, `autoPublish: true`, `draft: false`,
   `media: [<raw URL>]`), texts taken from `captions.txt`:
   - Instagram: `providers:[{"network":"instagram"}]`, `instagramData: {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}`, text = INSTAGRAM block.
   - Facebook: `providers:[{"network":"facebook"}]`, `facebookData: {"type":"REEL","title":<YouTube title>}`, text = FACEBOOK block.
   - TikTok: `providers:[{"network":"tiktok"}]`, `tiktokData: {"privacyOption":"PUBLIC_TO_EVERYONE","disableComment":false,"disableDuet":false,"disableStitch":false,"title":<YouTube title without #shorts>,"isAigc":true}` (title is REQUIRED), text = TIKTOK block.
   - YouTube: `providers:[{"network":"youtube"}]`, `youtubeData: {"title":<YouTube title>,"type":"short","privacy":"public","tags":[<YouTube tags>],"category":"EDUCATION","madeForKids":false,"isAiGeneratedContent":true}`,
     text = a 2–3 sentence description + "Sources: …" + `#Shorts #MapCurious`.
   Include the other required fields (`descendants: []`, `firstCommentText: ""`, `hasNotReadNotes: false`, `mediaAltText: []`,
   `shortener: false`, `smartLinkData: {"ids": []}`).
4. If a post fails, retry that one post once. Never create duplicates; never edit or delete existing posts.
   If posting still fails, leave the video in `ready/` and report the exact error.

## 10. Report
Short summary: topic, length, `ready/NN_Slug/` path, ElevenLabs credits used, Metricool post links/time
(or the posting error), anything you could not fix.
