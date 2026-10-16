"""Word-level alignment of the supplied narration MP3s.

Runs faster-whisper (local, medium.en) with word timestamps on each MP3, then maps
the *script* words (delivery tags stripped) onto the recognised words so caption
text always matches the approved script while timings come from the real audio.
Output: timing/<slug>.words.json  [{w, start, end}]
"""
import json, re, sys, difflib, subprocess
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[2]
VO = ROOT / '2026-10-14_Map_Curious_Voiceovers'
if '--vo' in sys.argv:
    VO = ROOT / sys.argv[sys.argv.index('--vo') + 1]; del sys.argv[sys.argv.index('--vo'):sys.argv.index('--vo') + 2]
OUT = ROOT / 'Map_Curious_Edit' / 'timing'
SLUGS = ['01_Fort_Jefferson', '02_DB_Cooper', '03_Centralia', '04_Underwater_Waterfall']


def load_audio(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def norm(w):
    return re.sub(r"[^a-z0-9$]", '', w.lower().replace('’', "'"))


def script_words(slug):
    txt = (VO / f'{slug}_script.txt').read_text(encoding='utf-8')
    txt = re.sub(r'\[[^\]]*\]', ' ', txt)          # drop delivery tags
    return txt.split()


def main():
    import os
    model = WhisperModel(os.environ.get('MC_WHISPER', 'medium.en'), device='cpu', compute_type='int8')
    for slug in (sys.argv[1:] or SLUGS):
        words = script_words(slug)
        segs, info = model.transcribe(load_audio(VO / f'{slug}.mp3'), word_timestamps=True,
                                      condition_on_previous_text=False, beam_size=5,
                                      vad_filter=False, language='en')
        rec = [w for s in segs for w in s.words]
        # Whisper may split "$200,000" etc. differently: align on normalised tokens.
        a = [norm(w) for w in words]
        b = [norm(w.word) for w in rec]
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        timing = [None] * len(words)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                for k in range(i2 - i1):
                    timing[i1 + k] = (rec[j1 + k].start, rec[j1 + k].end)
            elif j2 > j1:   # replace: spread the recognised span over script words
                s, e = rec[j1].start, rec[j2 - 1].end
                n = i2 - i1
                for k in range(n):
                    timing[i1 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
        # fill any gaps by interpolation
        for i, t in enumerate(timing):
            if t is None:
                prev = next((timing[k][1] for k in range(i - 1, -1, -1) if timing[k]), 0)
                nxt = next((timing[k][0] for k in range(i + 1, len(timing)) if timing[k]), prev + .3)
                timing[i] = (prev, nxt)
        out = [{'w': w, 'start': round(t[0], 3), 'end': round(t[1], 3)} for w, t in zip(words, timing)]
        (OUT / f'{slug}.words.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
        recog = ' '.join(w.word.strip() for w in rec)
        ratio = sm.ratio()
        print(f'{slug}: {len(words)} script words, {len(rec)} recognised, match ratio {ratio:.3f}, '
              f'first {out[0]["start"]:.2f}s last-end {out[-1]["end"]:.2f}s')
        print('  RECOGNISED:', recog)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                print('  DIFF', tag, words[i1:i2], [rec[j].word for j in range(j1, j2)])


if __name__ == '__main__':
    main()
