# Map Curious — daily cloud run (one finished video)

You are running unattended in a cloud session with this repo checked out. Nobody will answer questions.
Produce ONE new finished Map Curious vertical video, commit it to `ready/`, push, and stop.
NEVER publish or schedule anything on social media / Metricool.

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
- `captions.txt` with blocks: `=== INSTAGRAM ===` (hook + 2–3 sentences + ~9 hashtags incl. #MapCurious),
  `=== FACEBOOK ===` (slightly longer, ~4 hashtags), `=== TIKTOK ===` (one punchy line + ~8 hashtags incl.
  #learnontiktok #mapcurious), `=== YOUTUBE SHORTS TITLE ===`, `=== YOUTUBE TAGS ===` (comma-separated),
  and a final note: "Narration is an AI voice (ElevenLabs) - use each platform's AI-content label if required."

Append `YYYY-MM-DD  NN Topic` to `ready/topics_log.txt`. Also commit the new episode file, script and the
`render.py` change. Then:
```bash
git add -A && git commit -m "Map Curious NN: <topic>" && git push origin HEAD
```
(If pushing to the default branch is refused, push a branch named `video/NN-slug` instead.)

## 9. Report
Short summary: topic, length, `ready/NN_Slug/` path, ElevenLabs credits used, anything you could not fix.
