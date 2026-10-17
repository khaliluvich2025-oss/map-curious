"""Vertical (9:16) promo reels cut from the LF01 long-form video.

  MC_LANDSCAPE=1 python3 promo.py            -> output/LF01_Promo_<name>.mp4 (+ covers/)
Each reel: blurred background + the 16:9 frame in the middle, big captions, hook headline on top,
"FULL VIDEO ON YOUTUBE" CTA, and a 3 s end card with the long-form thumbnail.
"""
import os, sys, subprocess, math
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import EDIT, ROOT, FPS, LIME, WHITE, OUTLINE, INK, RED, font, norm_word, e_out, e_back, clamp
import lf01_map_mysteries as LFM

PW, PH = 1080, 1920
VY = 600                      # top of the 16:9 window
VH = round(PW * 1080 / 1920)  # 608
END = 3.0
THUMB = ROOT / 'ready' / 'LF01_Map_Mysteries' / 'LF01_Map_Mysteries_Thumbnail.jpg'
REELS = [
    ('Trailer', 0.0, 29.3, ['6 PLACES THAT', 'SOUND MADE UP'], 'FULL VIDEO ON YOUTUBE'),
    ('DB_Cooper', 217.3, 254.7, ['HE JUMPED FROM A JET', 'AND VANISHED'], 'FULL STORY ON YOUTUBE'),
    ('Underwater_Waterfall', 289.4, 339.5, ["EARTH'S BIGGEST WATERFALL", 'IS UNDERWATER'], 'FULL VIDEO ON YOUTUBE'),
]
EP = None


def text(d, xy, s, size, fill, stroke=8, anchor='mm'):
    d.text(xy, s, font=font(size), fill=fill, stroke_width=stroke, stroke_fill=OUTLINE, anchor=anchor)


def play(d, x, y, r):
    d.polygon([(x - r * .7, y - r), (x - r * .7, y + r), (x + r, y)], fill=WHITE)


def fit_size(s, size, maxw):
    while size > 30 and font(size).getlength(s) > maxw:
        size -= 2
    return size


def init():
    global EP
    EP = LFM.EP()


def caption_at(t):
    for g in EP.caps.groups:
        if g['start'] <= t < g['end']:
            return g
    return None


def frame(args):
    name, t0, t1, head, cta, f = args
    tl = f / FPS
    t = t0 + tl
    dur = t1 - t0
    cv = Image.new('RGB', (PW, PH), INK)
    lf = EP.frame(min(t, t1), captions=False)                      # 1920x1080
    bg = lf.resize((round(1920 * PH / 1080), PH), Image.BILINEAR)
    x0 = (bg.width - PW) // 2
    bg = bg.crop((x0, 0, x0 + PW, PH)).filter(ImageFilter.GaussianBlur(28))
    cv.paste(ImageEnhance.Brightness(bg).enhance(.38))
    cv.paste(lf.resize((PW, VH), Image.LANCZOS), (0, VY))
    d = ImageDraw.Draw(cv)
    d.line([(0, VY - 2), (PW, VY - 2)], fill=LIME, width=4)
    d.line([(0, VY + VH + 1), (PW, VY + VH + 1)], fill=LIME, width=4)
    # headline
    text(d, (PW / 2, 205), 'MAP CURIOUS', 34, LIME, 5)
    for i, ln in enumerate(head):
        sz = fit_size(ln, 84, PW - 90)
        text(d, (PW / 2, 320 + i * 100), ln, sz, LIME if i == len(head) - 1 else WHITE, 9)
    # captions (big, under the video)
    g = caption_at(t) if tl < dur else None
    if g:
        words = [w['w'] for w in g['words']]
        sz = 62
        f_ = font(sz)
        lines, cur = [], []
        for w in words:
            if cur and f_.getlength(' '.join(cur + [w])) > PW - 140:
                lines.append(cur); cur = []
            cur.append(w)
        lines.append(cur)
        y = 1330 - (len(lines) - 1) * 40
        for ln in lines:
            tw = f_.getlength(' '.join(ln)); x = (PW - tw) / 2
            for w in ln:
                c = LIME if norm_word(w) in EP.caps.emph else WHITE
                d.text((x, y), w, font=f_, fill=c, stroke_width=8, stroke_fill=OUTLINE, anchor='lm')
                x += f_.getlength(w + ' ')
            y += 80
    # CTA
    if tl < dur:
        p = .5 + .5 * math.sin(tl * 4)
        d.rounded_rectangle((170, 1505, PW - 170, 1595), radius=45, fill=(220, 30, 40), outline=WHITE, width=3)
        play(d, 250, 1550, 18)
        text(d, (PW / 2 + 25, 1550), 'FULL VIDEO ON YOUTUBE', 40, WHITE, 0)
        text(d, (PW / 2, 1640), "COMMENT AND WE'LL SEND YOU THE LINK", 34, WHITE, 6)
    # end card
    if tl >= dur:
        e = e_out((tl - dur) / .4)
        ov = Image.new('RGB', (PW, PH), INK)
        cv = Image.blend(cv, ov, e)
        d = ImageDraw.Draw(cv)
        th = Image.open(THUMB).convert('RGB').resize((980, 551), Image.LANCZOS)
        sc = .85 + .15 * e_back(clamp((tl - dur) / .5))
        th = th.resize((int(980 * sc), int(551 * sc)), Image.LANCZOS)
        cv.paste(th, ((PW - th.width) // 2, 640 + (551 - th.height) // 2))
        d = ImageDraw.Draw(cv)
        text(d, (PW / 2, 420), cta, fit_size(cta, 70, PW - 80), WHITE, 9)
        text(d, (PW / 2, 520), 'MAP CURIOUS', 44, LIME, 6)
        d.rounded_rectangle((110, 1300, PW - 110, 1410), radius=55, fill=(220, 30, 40), outline=WHITE, width=3)
        text(d, (PW / 2, 1355), 'COMMENT FOR THE LINK', 52, WHITE, 0)
        text(d, (PW / 2, 1480), "WE'LL SEND IT TO YOU", 44, WHITE, 6)
    return np.asarray(cv, np.uint8).tobytes()


def build(reel, workers):
    name, t0, t1, head, cta = reel
    out = EDIT / 'output' / f'LF01_Promo_{name}.mp4'
    n = math.ceil((t1 - t0 + END) * FPS)
    tmp = EDIT / '_render_tmp'; tmp.mkdir(exist_ok=True)
    vid = tmp / f'promo_{name}.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{PW}x{PH}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', str(vid)],
                           stdin=subprocess.PIPE)
    with Pool(workers, initializer=init) as pool:
        for buf in pool.imap(frame, [(name, t0, t1, head, cta, f) for f in range(n)], chunksize=4):
            enc.stdin.write(buf)
    enc.stdin.close(); enc.wait()
    src = EDIT / 'output' / 'LF01_Map_Mysteries_Final.mp4'
    dur = t1 - t0
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(vid), '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', str(src),
                    '-filter_complex', f'[1:a]afade=t=out:st={dur - .4:.3f}:d=0.4,apad[a]',
                    '-map', '0:v', '-map', '[a]', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-movflags', '+faststart', str(out)], check=True)
    print(out, n, 'frames')


if __name__ == '__main__':
    assert os.environ.get('MC_LANDSCAPE') == '1'
    sel = sys.argv[1:] or [r[0] for r in REELS]
    for r in REELS:
        if r[0] in sel:
            build(r, int(os.environ.get('MC_WORKERS', 4)))
