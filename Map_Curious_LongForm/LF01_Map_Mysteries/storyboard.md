# LF01 storyboard — 16:9 (1920×1080), 24 fps

Rules: full-screen maps; one meaningful reveal every ~2–4 s (long-form can breathe a little more than Shorts);
hold crucial clues ≥3 s; diagrams fill the frame (no small upper panels); captions centered in a bottom
safe band (y ≈ 900–1010); sources lower-right per segment; final frame matches narration end.
Each segment ends on a "next up" teaser with a globe move to the next location (doubles as a chapter break).

| Part | Visual spine | Key reveals (keyed to words) | Diagrams / cutouts | Base map |
|---|---|---|---|---|
| 01 Cold open | Fast montage of the 6 locations, 1–2 s each | waterfall ⟶ smoke from ground ⟶ jet silhouette ⟶ "1963" | — | all four packs |
| 02 Hudson | Northeast map; river traced Adirondacks → NYC | tide arrows reverse north; "≈150 MI" ruler to Troy; salt front creeping "≈60 MI" | animated tide clock; split-screen "river vs. estuary" | 03_centralia (NE US) |
| 03 Fort Jefferson | Florida → Keys → zoom on Dry Tortugas | "≈70 MI" from Key West; hexagon fort outline draws; shipping lanes | full-frame fort plan; brick counter; cannon-vs-wall graphic; settling diagram | 01_fort_jefferson |
| 04 Centralia | Pennsylvania → town pin | coal seam cross-section; fire spreading; smoke vents; 1981 sinkhole; houses fading out | full-frame underground cross-section | 03_centralia |
| 05 D.B. Cooper | Portland → Seattle → southbound flight path | ransom "$200,000"; rear-stairs jump zone (uncertainty cloud, not a point); 1980 money find on the Columbia | aircraft side-view with rear airstair; timeline | 02_db_cooper |
| 06 Denmark Strait | Greenland + Iceland highlight; strait marker | cold vs warm water colors; sinking flow; "≈2 MI" drop | full-frame ocean section; global conveyor mini-map | 04_denmark_strait |
| 07 Surtsey | Iceland south coast; Westman Islands | smoke; island breaks surface; 1963 → 1967; life arrives icons; erosion "≈half" | full-frame eruption section; life-arrival sequence | 04_denmark_strait |
| 08 Wrap | Pull back to a map with all 6 pins | each pin re-lights as it's named | comment prompt card (small, lower third) | composite |

Engineering needed before rendering: a 16:9 layout mode in `engine.py` (canvas, caption band, camera
limits), wider base maps for each region, chapter transitions, and a music bed. Shorts can later be cut from
segments 02–07 (re-using the vertical episodes already made).
