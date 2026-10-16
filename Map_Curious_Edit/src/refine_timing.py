"""Snap Whisper word boundaries to the real pauses measured in each MP3.

Whisper tends to start a word at the end of the previous one, i.e. inside a
pause.  Here we measure silence (10 ms RMS < -45 dBFS, >= 0.18 s) in the actual
audio and move any word start that lies inside a pause to the end of that pause
(and any word end inside a pause to its start).
Writes timing/<slug>.final.json.
"""
import json, subprocess, sys
import numpy as np
from align import VO, OUT, SLUGS


def pauses(slug, thr=-45, min_len=.18):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(VO / f'{slug}.mp3'), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 160; n = len(a) // hop
    db = 20 * np.log10(np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    q = db < thr; runs = []; st = None
    for i, v in enumerate(list(q) + [False]):
        if v and st is None:
            st = i
        if not v and st is not None:
            if (i - st) * .01 >= min_len:
                runs.append((st * .01, i * .01))
            st = None
    act = np.where(~q)[0]
    return runs, act[0] * .01, act[-1] * .01 + .01, len(a) / 16000


def main():
    for slug in (sys.argv[1:] or SLUGS):
        words = json.loads((OUT / f'{slug}.words.json').read_text(encoding='utf-8'))
        runs, sp0, sp1, dur = pauses(slug)
        moved = []
        for w in words:
            for a, b in runs:
                if a <= w['start'] < b or (w['start'] < a and w['end'] > b and b - a >= .25):
                    moved.append((w['w'], w['start'], round(b, 3))); w['start'] = round(b, 3)
                    w['end'] = max(w['end'], round(b + .12, 3))
                if a < w['end'] < b - .02:
                    w['end'] = round(a, 3)
            if w['end'] < w['start'] + .05:
                w['end'] = round(w['start'] + .12, 3)
        words[0]['start'] = max(words[0]['start'], round(sp0, 3))
        words[-1]['end'] = round(sp1, 3)
        (OUT / f'{slug}.final.json').write_text(json.dumps(words, indent=1), encoding='utf-8')
        print(f'{slug}: audio {dur:.2f}s, speech {sp0:.2f}-{sp1:.2f}s, {len(moved)} starts snapped to pause ends')
        for m in moved:
            print('   ', m)


if __name__ == '__main__':
    main()
