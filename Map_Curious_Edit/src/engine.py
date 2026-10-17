"""Map Curious renderer - shared engine.

Everything is drawn procedurally per frame with Pillow at 1080x1920 and piped to
ffmpeg.  Episodes (ep01..ep04) only describe *what* happens *when*; this module
provides the camera, layer primitives, captions, sound design and export.
"""
import math, json, re, functools, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Map images are always 1080x1920 (map px).  MC_LANDSCAPE=1 switches the output canvas to 16:9 (long-form).
LANDSCAPE = os.environ.get('MC_LANDSCAPE') == '1'
MW, MH = 1080, 1920
W, H = (1920, 1080) if LANDSCAPE else (MW, MH)
FPS = 24
EDIT = Path(__file__).resolve().parents[1]
ROOT = EDIT.parent
GFX = ROOT / '2026-10-14_Map_Curious_Graphics'
VO = ROOT / '2026-10-14_Map_Curious_Voiceovers'
FONT_PATH = GFX / 'Manrope.ttf'

INK = (9, 28, 41)
LIME = (200, 243, 75)
TEAL = (55, 217, 208)
ORANGE = (255, 154, 75)
WHITE = (248, 250, 244)
RED = (255, 98, 82)
OUTLINE = (6, 15, 23)

# Caption safe box (brief): x 250-830, y 970-1148, centred on x=540.
CAP_X0, CAP_X1, CAP_Y0, CAP_Y1 = 250, 830, 970, 1148
CAP_CY = 1059
CAP_SIZE = 46
if LANDSCAPE:   # 16:9: bottom band, centred
    CAP_X0, CAP_X1, CAP_Y0, CAP_Y1 = 400, 1520, 925, 1035
    CAP_CY = 980
    CAP_SIZE = 44
CAP_MAXW = CAP_X1 - CAP_X0


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def e_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def e_io(x):
    x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def e_back(x, s=1.6):
    x = clamp(x); c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def lin(x):
    return clamp(x)


def lerp(a, b, p):
    return a + (b - a) * p


def prog(t, a, d=.45, ease=e_out):
    if d <= 0:
        return float(t >= a)
    return ease((t - a) / d)


def vis(t, a, b=None, fi=.3, fo=.3):
    """Opacity of an element that fades in at a and (optionally) out at b."""
    if t < a:
        return 0.0
    v = e_out((t - a) / fi) if fi > 0 else 1.0
    if b is not None and t > b:
        v = min(v, 1 - e_out((t - b) / fo) if fo > 0 else 0.0)
    return clamp(v)


# ---------------------------------------------------------------- fonts / images
@functools.lru_cache(None)
def font(size, weight='ExtraBold'):
    f = ImageFont.truetype(str(FONT_PATH), int(size))
    f.set_variation_by_name(weight)
    return f


@functools.lru_cache(None)
def load(path, maxdim=None, trim=True):
    im = Image.open(path).convert('RGBA')
    if trim:
        bb = im.getchannel('A').getbbox()
        if bb:
            im = im.crop(bb)
    if maxdim:
        im.thumbnail((maxdim, maxdim), Image.LANCZOS)
    return im


def with_alpha(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel('A').point(lambda v: int(v * a + .5)))
    return im


def paste(cv, im, x, y):
    """alpha_composite with clipping; (x, y) = top-left, may be off-canvas."""
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(im.width, W - x), min(im.height, H - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    if (sx0, sy0, sx1, sy1) != (0, 0, im.width, im.height):
        im = im.crop((sx0, sy0, sx1, sy1))
    cv.alpha_composite(im, (x + sx0, y + sy0))


def place(cv, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    """Draw RGBA image centred at (cx, cy)."""
    if alpha <= 0.004 or scale <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.BICUBIC)
    if abs(rot) > 0.05:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    im = with_alpha(im, alpha)
    paste(cv, im, cx - im.width / 2, cy - im.height / 2)


_SHADOW = {}


def shadowed(im_key, im, blur=18, off=(0, 14), op=150):
    """Return image with soft drop-shadow (cached by key)."""
    k = (im_key, blur, off, op)
    if k not in _SHADOW:
        _SHADOW[k] = _shadowed(im, blur, off, op)
    return _SHADOW[k]


def _shadowed(im, blur, off, op):
    pad = blur * 2 + max(abs(off[0]), abs(off[1]))
    out = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0))
    a = im.getchannel('A').point(lambda v: v * op // 255)
    blk = Image.new('RGBA', im.size, (2, 8, 14, 255)); blk.putalpha(a)
    sh.paste(blk, (pad + off[0], pad + off[1]))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh)
    out.alpha_composite(im, (pad, pad))
    return out


def drop(im, key, blur=16, off=(0, 12), op=150):
    return shadowed(key, im, blur, off, op)


# ---------------------------------------------------------------- vector layer
def vec(cv, bbox, fn, alpha=1.0, ss=3, base=WHITE):
    """Supersampled anti-aliased vector drawing inside bbox (screen coords).
    fn(d, P, s): d = ImageDraw, P(x, y) -> supersampled coords, s = scale."""
    if alpha <= 0.004:
        return
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
    x1, y1 = min(W, int(math.ceil(x1))), min(H, int(math.ceil(y1)))
    if x1 <= x0 or y1 <= y0:
        return
    if (x1 - x0) * (y1 - y0) > 900_000:
        ss = 2
    L = Image.new('RGBA', ((x1 - x0) * ss, (y1 - y0) * ss), tuple(base[:3]) + (0,))
    d = ImageDraw.Draw(L, 'RGBA')
    P = lambda x, y: ((x - x0) * ss, (y - y0) * ss)
    fn(d, P, ss)
    L = L.reduce(ss)
    cv.alpha_composite(with_alpha(L, alpha), (x0, y0))


def col(c, a=1.0):
    return tuple(c[:3]) + (int(255 * clamp(a)),)


# ---------------------------------------------------------------- paths
def spline(pts, n=24):
    """Catmull-Rom through pts."""
    if len(pts) < 3:
        out = []
        for i in range(len(pts) - 1):
            for k in range(n):
                p = k / n
                out.append((lerp(pts[i][0], pts[i + 1][0], p), lerp(pts[i][1], pts[i + 1][1], p)))
        out.append(pts[-1]); return out
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            s = k / n; s2, s3 = s * s, s * s * s
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * s + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * s2
                                   + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * s3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def cumlen(pts):
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return L


def partial(pts, p, p0=0.0):
    """Sub-path from fraction p0 to p of the length; returns pts, end angle."""
    if len(pts) < 2:
        return pts, 0.0
    L = cumlen(pts); tot = L[-1] or 1
    a_, b_ = p0 * tot, p * tot
    out = []
    for i in range(len(pts) - 1):
        la, lb = L[i], L[i + 1]
        if lb < a_ or la > b_:
            continue
        seg = lb - la or 1e-6
        s0 = clamp((a_ - la) / seg); s1 = clamp((b_ - la) / seg)
        pa = (lerp(pts[i][0], pts[i + 1][0], s0), lerp(pts[i][1], pts[i + 1][1], s0))
        pb = (lerp(pts[i][0], pts[i + 1][0], s1), lerp(pts[i][1], pts[i + 1][1], s1))
        if not out:
            out.append(pa)
        out.append(pb)
    if len(out) < 2:
        return out, 0.0
    (xa, ya), (xb, yb) = out[-2], out[-1]
    k = len(out) - 2
    while k > 0 and math.hypot(xb - xa, yb - ya) < 1e-3:
        k -= 1; xa, ya = out[k]
    return out, math.atan2(yb - ya, xb - xa)


def point_at(pts, p):
    seg, ang = partial(pts, max(p, 1e-4))
    return (seg[-1] if seg else pts[0]), ang


def bbox_of(pts, m=40):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m)


def _line(d, P, s, pts, color, width):
    q = [P(*p) for p in pts]
    if len(q) >= 2:
        d.line(q, fill=color, width=max(1, int(width * s)), joint='curve')
        r = width * s / 2
        for (x, y) in (q[0], q[-1]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=color)


def _head(d, P, s, tip, ang, size, color):
    x, y = tip
    pts = [(x + math.cos(ang) * size * .55, y + math.sin(ang) * size * .55),
           (x + math.cos(ang + 2.45) * size, y + math.sin(ang + 2.45) * size),
           (x + math.cos(ang - 2.45) * size, y + math.sin(ang - 2.45) * size)]
    d.polygon([P(*p) for p in pts], fill=color)


def route(cv, pts, p, color=LIME, width=8, head=True, alpha=1.0, dashed=False, dash=(26, 16),
          phase=0.0, glow=True, p0=0.0, outline=True, head_size=None):
    """Animated line reveal along pts (screen coords) up to fraction p."""
    if p <= 0.001 or alpha <= 0.004:
        return
    seg, ang = partial(pts, p, p0)
    if len(seg) < 2:
        return
    hs = head_size or width * 3.2

    def fn(d, P, s):
        parts = [seg]
        if dashed:
            parts = []
            L = cumlen(seg); tot = L[-1]; period = dash[0] + dash[1]
            start = -(phase % period)
            while start < tot:
                a_, b_ = max(start, 0), min(start + dash[0], tot)
                if b_ > a_:
                    parts.append(partial(seg, b_ / tot, a_ / tot)[0])
                start += period
        if outline:
            for pp in parts:
                _line(d, P, s, pp, col(OUTLINE, .55), width + 6)
            if head:
                _head(d, P, s, seg[-1], ang, hs + 4, col(OUTLINE, .55))
        for pp in parts:
            _line(d, P, s, pp, col(color), width)
        if head:
            _head(d, P, s, seg[-1], ang, hs, col(color))
    vec(cv, bbox_of(seg, hs + 20), fn, alpha, base=color)


# ---------------------------------------------------------------- camera
class Cam:
    """Keyframed map camera. keys: [(t, cx, cy, z)] in map-pixel coords."""

    def __init__(self, keys, mw=MW, mh=MH, zmin=1.0):
        self.keys = sorted(keys); self.mw, self.mh, self.zmin = mw, mh, zmin

    def at(self, t):
        k = self.keys
        if t <= k[0][0]:
            s = k[0]
        elif t >= k[-1][0]:
            s = k[-1]
        else:
            i = max(j for j in range(len(k)) if k[j][0] <= t)
            a, b = k[i], k[i + 1]
            p = e_io((t - a[0]) / (b[0] - a[0]))
            s = (t, lerp(a[1], b[1], p), lerp(a[2], b[2], p), math.exp(lerp(math.log(a[3]), math.log(b[3]), p)))
        _, cx, cy, z = s
        z = max(z, self.zmin)
        hw, hh = W / 2 / z, H / 2 / z
        cx = clamp(cx, hw, self.mw - hw) if self.mw >= 2 * hw else self.mw / 2
        cy = clamp(cy, hh, self.mh - hh) if self.mh >= 2 * hh else self.mh / 2
        return (cx, cy, z)

    @staticmethod
    def S(st, mx, my):
        cx, cy, z = st
        return ((mx - cx) * z + W / 2, (my - cy) * z + H / 2)


def render_map(base, st, scale=1.0):
    """Crop+zoom a map-space image to the camera view (sub-pixel box resize).
    `scale` = image px per map px (2 for 2x overlays)."""
    cx, cy, z = st
    hw, hh = W / 2 / z, H / 2 / z
    box = ((cx - hw) * scale, (cy - hh) * scale, (cx + hw) * scale, (cy + hh) * scale)
    box = (max(0, box[0]), max(0, box[1]), min(base.width, box[2]), min(base.height, box[3]))
    return base.resize((W, H), Image.BICUBIC, box=box, reducing_gap=None)


# ---------------------------------------------------------------- text primitives
@functools.lru_cache(None)
def text_img(text, size, color=WHITE, stroke=0, stroke_color=OUTLINE, weight='ExtraBold', tracking=0):
    f = font(size, weight)
    pad = stroke + 4
    if tracking:
        widths = [f.getlength(ch) + tracking for ch in text]
        tw = sum(widths) - tracking
    else:
        tw = f.getlength(text)
    asc, desc = f.getmetrics()
    im = Image.new('RGBA', (int(tw + pad * 2 + 2), asc + desc + pad * 2), col(color, 0))
    d = ImageDraw.Draw(im)
    if tracking:
        for pass_ in ((0, 1) if stroke else (1,)):      # outlines first, then fills (no overlap artefacts)
            x = pad
            for ch, w in zip(text, widths):
                if pass_ == 0:
                    d.text((x, pad), ch, font=f, fill=col(stroke_color), stroke_width=stroke, stroke_fill=col(stroke_color))
                else:
                    d.text((x, pad), ch, font=f, fill=col(color))
                x += w
    else:
        d.text((pad, pad), text, font=f, fill=col(color), stroke_width=stroke, stroke_fill=col(stroke_color))
    return im


@functools.lru_cache(None)
def label_img(text, size=34, color=WHITE, stroke=6, shadow=True, weight='ExtraBold', tracking=1):
    im = text_img(text, size, color, stroke, OUTLINE, weight, tracking)
    return drop(im, ('lbl', text, size, color, stroke, weight), 10, (0, 4), 170) if shadow else im


def label(cv, text, x, y, t, a, b=None, size=34, color=WHITE, rise=14, fi=.35, fo=.3, anchor='m'):
    al = vis(t, a, b, fi, fo)
    if al <= 0:
        return
    im = label_img(text, size, color)
    dy = (1 - e_out((t - a) / fi)) * rise
    cx = x if anchor == 'm' else x + im.width / 2 if anchor == 'l' else x - im.width / 2
    place(cv, im, cx, y + dy, 1.0, al)


@functools.lru_cache(None)
def chip_img(text, size=34, fg=WHITE, accent=LIME, bg=(10, 26, 38), bga=232, sub=None, sub_color=None):
    """Rounded label card with accent bar. Rendered at 3x then reduced (crisp, AA)."""
    s = 3
    f = font(size * s, 'ExtraBold')
    tw = f.getlength(text)
    asc, desc = f.getmetrics()
    padx, pady, bar = 22 * s, 13 * s, 7 * s
    hgt = int(size * 1.18 * s) + pady * 2
    subh = 0
    if sub:
        fs = font(int(size * .58) * s, 'Bold')
        subw = fs.getlength(sub); subh = int(size * .7 * s)
        tw = max(tw, subw)
        hgt += subh
    wid = int(tw + padx * 2 + bar + 12 * s)
    im = Image.new('RGBA', (wid, hgt), col(bg, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, wid - 1, hgt - 1), radius=16 * s, fill=col(bg, bga / 255), outline=col(WHITE, .14), width=2 * s)
    d.rounded_rectangle((12 * s, 14 * s, 12 * s + bar, hgt - 14 * s), radius=bar // 2, fill=col(accent))
    tx = 12 * s + bar + 16 * s
    d.text((tx, pady - int(size * .08 * s)), text, font=f, fill=col(fg))
    if sub:
        d.text((tx, pady + int(size * 1.12 * s)), sub, font=font(int(size * .58) * s, 'Bold'), fill=col(sub_color or (190, 205, 210)))
    im = im.reduce(s)
    return drop(im, ('chip', text, size, fg, accent, sub), 14, (0, 8), 160)


def chip(cv, text, x, y, t, a, b=None, size=34, fg=WHITE, accent=LIME, sub=None, anchor='m', fi=.4, fo=.3,
         reveal=True, alpha=1.0):
    al = vis(t, a, b, fi, fo) * alpha
    if al <= 0:
        return
    im = chip_img(text, size, fg, accent, sub=sub)
    p = e_out((t - a) / (fi + .1))
    if reveal and p < 1:
        w = max(1, int(im.width * (0.15 + .85 * p)))
        im = im.crop((0, 0, w, im.height)) if anchor == 'l' else im
    dy = (1 - p) * 16
    if anchor == 'l':
        paste_im = with_alpha(im, al); paste(cv, paste_im, x - 20, y - paste_im.height / 2 + dy)
    elif anchor == 'r':
        paste_im = with_alpha(im, al); paste(cv, paste_im, x - im.width + 20, y - paste_im.height / 2 + dy)
    else:
        place(cv, im, x, y + dy, 0.92 + .08 * p, al)


@functools.lru_cache(None)
def hero_img(text, size, color, stroke=10):
    im = text_img(text, size, color, stroke, OUTLINE, 'ExtraBold', 2)
    return drop(im, ('hero', text, size, color), 22, (0, 10), 190)


def hero(cv, text, x, y, t, a, b=None, size=150, color=LIME, fo=.3, pop=True):
    al = vis(t, a, b, .18, fo)
    if al <= 0:
        return
    sc = 0.55 + 0.45 * e_back((t - a) / .42) if pop else 1.0
    place(cv, hero_img(text, size, color), x, y, sc, al)


def count_text(v, prefix='$'):
    return f'{prefix}{int(round(v)):,}'


# ---------------------------------------------------------------- map markers
def pin(cv, x, y, t, a, b=None, color=LIME, r=17, rings=True, alpha=1.0):
    al = vis(t, a, b, .2, .35) * alpha
    if al <= 0:
        return
    sc = e_back((t - a) / .45, 2.2)

    def fn(d, P, s):
        if rings:
            for k in (0, .5):
                ph = ((t - a) / 1.7 + k) % 1.0
                rr = (r + 10 + ph * 70) * s
                cx, cy = P(x, y)
                d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=col(color, (1 - ph) * .85), width=int(4 * s))
        cx, cy = P(x, y); rr = r * sc * s
        d.ellipse((cx - rr - 5 * s, cy - rr - 5 * s, cx + rr + 5 * s, cy + rr + 5 * s), fill=col(OUTLINE, .6))
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col(color), outline=col(WHITE), width=int(4 * s))
    vec(cv, (x - 120, y - 120, x + 120, y + 120), fn, al, base=color)


def ring(cv, x, y, rad, t, a, b=None, color=LIME, width=5, dashed=False, alpha=1.0, spin=0.0):
    """Circle drawn on (stroke reveal)."""
    al = vis(t, a, b, .15, .3) * alpha
    if al <= 0:
        return
    p = e_out((t - a) / .7)
    n = 96
    pts = [(x + rad * math.cos(-math.pi / 2 + spin + 2 * math.pi * k / n), y + rad * math.sin(-math.pi / 2 + spin + 2 * math.pi * k / n)) for k in range(n + 1)]
    route(cv, pts, p, color, width, head=False, alpha=al, dashed=dashed, dash=(18, 12), glow=False)


def stamp(cv, text, x, y, t, a, b=None, size=64, color=RED, rot=-8):
    al = vis(t, a, b, .12, .3)
    if al <= 0:
        return
    key = ('stamp', text, size, color)
    im = _stamp_img(text, size, color)
    sc = 1.0 + 0.6 * (1 - e_out((t - a) / .22))
    place(cv, im, x, y, sc, al, rot)


@functools.lru_cache(None)
def _stamp_img(text, size, color):
    s = 3
    f = font(size * s, 'ExtraBold')
    tw = f.getlength(text); pad = 22 * s
    hh = int(size * 1.25 * s) + pad
    im = Image.new('RGBA', (int(tw + pad * 2), hh), col(color, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3 * s, 3 * s, im.width - 3 * s, hh - 3 * s), radius=10 * s, outline=col(color), width=6 * s, fill=col(OUTLINE, .55))
    d.text((pad, pad // 2 - int(size * .05 * s)), text, font=f, fill=col(color))
    return im.reduce(s)


# ---------------------------------------------------------------- photo cards
@functools.lru_cache(None)
def card_img(path, inner_w, credit=None, crop=None, border=10, credit_size=19, gray=False, zoom=1.0, focus=(0.5, 0.5)):
    return build_card(path, inner_w, credit, crop, border, credit_size, zoom, focus, cache_shadow=True)


@functools.lru_cache(None)
def _photo(path, crop):
    im = Image.open(path).convert('RGB')
    return im.crop(crop) if crop else im


def build_card(path, inner_w, credit=None, crop=None, border=10, credit_size=19, zoom=1.0, focus=(0.5, 0.5), cache_shadow=False):
    im = _photo(path, crop)
    if zoom > 1.0:
        cw, ch = im.width / zoom, im.height / zoom
        fx, fy = focus
        x0 = clamp(fx * im.width - cw / 2, 0, im.width - cw); y0 = clamp(fy * im.height - ch / 2, 0, im.height - ch)
        im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    ih = round(im.height * inner_w / im.width)
    im = im.resize((inner_w, ih), Image.LANCZOS)
    cred_h = (credit_size + 16) if credit else 0
    card = Image.new('RGBA', (inner_w + border * 2, ih + border * 2 + cred_h), col(WHITE))
    card.paste(im, (border, border))
    if credit:
        d = ImageDraw.Draw(card)
        d.text((border + 2, ih + border + 7), credit, font=font(credit_size, 'Bold'), fill=(70, 80, 88))
    if cache_shadow:
        return drop(card, ('card', path, inner_w, credit, crop, zoom, focus), 22, (0, 16), 175)
    return _shadowed(card, 22, (0, 16), 175)          # animated (Ken Burns) frames: never cached


def card(cv, path, inner_w, x, y, t, a, b=None, credit=None, crop=None, rot=0.0, kb=None, fo=.3, enter='pop'):
    """Photo card with border + credit. kb=(t0, t1, z0, z1, focus) slow Ken-Burns inside the frame."""
    al = vis(t, a, b, .25, fo)
    if al <= 0:
        return
    zoom, focus = 1.0, (0.5, 0.5)
    if kb:
        t0, t1, z0, z1, focus = kb
        zoom = round(lerp(z0, z1, e_io((t - t0) / (t1 - t0))), 3)
    im = card_img(str(path), inner_w, credit, crop)
    if zoom > 1.0:   # Ken Burns: re-crop only the photo inside the static (cached) framed card
        src = _photo(str(path), crop)
        cw, ch = src.width / zoom, src.height / zoom
        x0 = clamp(focus[0] * src.width - cw / 2, 0, src.width - cw); y0 = clamp(focus[1] * src.height - ch / 2, 0, src.height - ch)
        ih = round(src.height * inner_w / src.width)
        ph = src.resize((inner_w, ih), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
        im = im.copy(); im.paste(ph, (60 + 10, 60 + 10))
    p = e_back((t - a) / .5, 1.3) if enter == 'pop' else e_out((t - a) / .5)
    sc = 0.7 + 0.3 * p
    dy = 0 if enter == 'pop' else (1 - p) * 120
    place(cv, im, x, y + dy, sc, al, rot * (0.4 + 0.6 * clamp(p)))


def cutout(cv, path, size, x, y, t, a, b=None, rot=0.0, enter='pop', fo=.3, sway=0.0, tag=None, scale=1.0, alpha=1.0):
    al = vis(t, a, b, .25, fo) * alpha
    if al <= 0:
        return
    im = drop(load(str(path), size), ('cut', str(path), size), 18, (0, 16), 150)
    p = e_back((t - a) / .55, 1.5) if enter == 'pop' else e_out((t - a) / .55)
    sc = (0.5 + 0.5 * p) * scale
    r = rot + sway * math.sin((t - a) * 2.1)
    place(cv, im, x, y, sc, al, r)
    if tag:
        label(cv, tag, x, y + im.height * sc / 2 - 18, t, a + .3, b, size=17, color=(205, 215, 220), rise=0)


# ---------------------------------------------------------------- captions
def norm_word(w):
    return re.sub(r"[^a-z0-9$]", '', w.lower().replace('’', "'"))


class Captions:
    def __init__(self, words, emphasis, end_time):
        self.words = words
        self.emph = {norm_word(e) for e in emphasis}
        self.groups = self._group(words, end_time)

    def _width(self, ws):
        f = font(CAP_SIZE, 'ExtraBold')
        return f.getlength(' '.join(w['w'] for w in ws)) + 2 * 6

    def _group(self, words, end_time):
        phrases, cur = [], []
        for i, w in enumerate(words):
            cur.append(w)
            nxt = words[i + 1] if i + 1 < len(words) else None
            gap = (nxt['start'] - w['end']) if nxt else 9
            if re.search(r'[.,?!:;]$', w['w']) or gap > .32:
                phrases.append(cur); cur = []
        if cur:
            phrases.append(cur)
        groups = []
        for ph in phrases:
            n = len(ph); k = math.ceil(n / 3)
            sizes = [n // k + (1 if j < n % k else 0) for j in range(k)]
            i = 0
            for sz in sizes:
                g = ph[i:i + sz]; i += sz
                while len(g) > 1 and self._width(g) > CAP_MAXW:   # break sooner if too wide
                    groups.append(g[:-1]); g = g[-1:]
                groups.append(g)
        out = []
        for j, g in enumerate(groups):
            st = max(0.0, g[0]['start'] - .06)
            nxt = groups[j + 1][0]['start'] - .06 if j + 1 < len(groups) else end_time
            en = nxt if nxt - g[-1]['end'] < .7 else g[-1]['end'] + .35
            out.append({'start': st, 'end': min(en, end_time), 'words': g,
                        'text': ' '.join(w['w'] for w in g)})
        return out

    @functools.lru_cache(None)
    def _img(self, idx):
        g = self.groups[idx]
        f = font(CAP_SIZE, 'ExtraBold')
        stroke = 6
        ws = [w['w'] for w in g['words']]
        sp = f.getlength(' ')
        widths = [f.getlength(w) for w in ws]
        tw = sum(widths) + sp * (len(ws) - 1)
        asc, desc = f.getmetrics()
        pad = stroke + 3
        im = Image.new('RGBA', (int(tw + pad * 2 + 2), asc + desc + pad * 2), col(WHITE, 0))
        d = ImageDraw.Draw(im)
        x = pad
        for w, wd in zip(ws, widths):
            c = LIME if norm_word(w) in self.emph else WHITE
            d.text((x, pad), w, font=f, fill=col(c), stroke_width=stroke, stroke_fill=col(OUTLINE))
            x += wd + sp
        return drop(im, ('cap', id(self), idx), 10, (0, 4), 200), (tw + 2 * stroke, asc + desc + 2 * stroke)

    def active(self, t):
        for i, g in enumerate(self.groups):
            if g['start'] <= t < g['end']:
                return i
        return None

    def draw(self, cv, t):
        i = self.active(t)
        if i is None:
            return
        g = self.groups[i]
        im, _ = self._img(i)
        p = e_out((t - g['start']) / .14)
        place(cv, im, W / 2, CAP_CY + (1 - p) * 10, 0.94 + 0.06 * p, clamp(p * 1.4))

    def bounds(self):
        rows = []
        for i, g in enumerate(self.groups):
            _, (tw, th) = self._img(i)
            rows.append((g['text'], W / 2 - tw / 2, CAP_CY - th / 2, W / 2 + tw / 2, CAP_CY + th / 2))
        return rows

    def srt(self):
        def ts(x):
            ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
            return f'{h:02}:{m:02}:{s:02},{ms:03}'
        return '\n'.join(f"{k + 1}\n{ts(g['start'])} --> {ts(g['end'])}\n{g['text']}\n" for k, g in enumerate(self.groups))


# ---------------------------------------------------------------- overlays
@functools.lru_cache(None)
def vignette():
    a = np.zeros((H, W), np.float32)
    y = np.arange(H, dtype=np.float32)[:, None]
    if LANDSCAPE:
        x = np.arange(W, dtype=np.float32)[None, :]
        a += np.clip((y - 840) / 240, 0, 1) ** 1.4 * 150           # bottom fade under captions
        r = np.sqrt(((x - 960) / 1250) ** 2 + ((y - 520) / 760) ** 2)
        a += np.clip(r - .55, 0, 1) * 160
        im = Image.new('RGBA', (W, H), col(OUTLINE, 0))
        im.putalpha(Image.fromarray(np.clip(a, 0, 215).astype(np.uint8)))
        return im
    a += np.clip((260 - y) / 260, 0, 1) ** 1.6 * 150          # top fade (status bar)
    a += np.clip((y - 1560) / 360, 0, 1) ** 1.4 * 170         # bottom fade (UI)
    x = np.arange(W, dtype=np.float32)[None, :]
    r = np.sqrt(((x - 540) / 760) ** 2 + ((y - 900) / 1250) ** 2)
    a += np.clip(r - .55, 0, 1) * 160
    im = Image.new('RGBA', (W, H), col(OUTLINE, 0))
    im.putalpha(Image.fromarray(np.clip(a, 0, 215).astype(np.uint8)))
    return im


def tint(cv, color, a):
    if a <= 0.004:
        return
    cv.alpha_composite(Image.new('RGBA', (W, H), col(color, a)))


def svg_polys(path):
    """Parse polygon point lists from the supplied region_highlight.svg (map px coords)."""
    txt = Path(path).read_text()
    polys = []
    for m in re.finditer(r'points="([^"]+)"', txt):
        nums = [float(v) for v in re.split(r'[ ,]+', m.group(1).strip())]
        polys.append(list(zip(nums[0::2], nums[1::2])))
    return polys


class Region:
    """Vector region from SVG polygons: fill fades in, white border draws on."""

    def __init__(self, polys, color=LIME, min_len=40):
        self.polys = [p for p in polys if len(p) > 2]
        self.color = color
        self.lens = [cumlen(p)[-1] for p in self.polys]
        self.main = int(np.argmax(self.lens))

    def draw(self, cv, st, t, a, b=None, fill_a=.36, border_w=4, alpha=1.0):
        al = vis(t, a, b, .5, .4) * alpha
        if al <= 0:
            return
        pb = e_io((t - a) / 1.1)
        scr = [[Cam.S(st, *q) for q in p] for p in self.polys]
        allp = [q for p in scr for q in p]
        bb = bbox_of(allp, 10)

        def fn(d, P, s):
            fa = fill_a * e_out((t - a - .25) / .8)
            for p in scr:
                if fa > 0:
                    d.polygon([P(*q) for q in p], fill=col(self.color, fa))
            for i, p in enumerate(scr):
                if i == self.main:
                    seg, _ = partial(p + [p[0]], pb)
                    if len(seg) > 1:
                        d.line([P(*q) for q in seg], fill=col(WHITE, .95), width=int(border_w * s), joint='curve')
                elif pb > .6:
                    d.line([P(*q) for q in p + [p[0]]], fill=col(WHITE, .9 * (pb - .6) / .4), width=int(border_w * s * .8))
        vec(cv, bb, fn, al, ss=2, base=self.color)


# ---------------------------------------------------------------- sound design (procedural, original)
SR = 48000


def _env(n, att, dec):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(att, 1e-4)) * np.exp(-np.maximum(0, t - att) / dec)


def _lp(x, fc):
    """One-pole low-pass with (possibly time-varying) cutoff array."""
    fc = np.broadcast_to(np.asarray(fc, np.float64), x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y


@functools.lru_cache(None)
def sfx(kind):
    rng = np.random.default_rng(abs(hash(kind)) % 2 ** 32)
    if kind == 'whoosh':
        n = int(.55 * SR); t = np.arange(n) / SR
        noise = rng.standard_normal(n)
        fc = 300 + 2600 * np.sin(np.pi * np.clip(t / .55, 0, 1)) ** 2
        y = _lp(_lp(noise, fc), fc) * np.sin(np.pi * np.clip(t / .55, 0, 1)) ** 1.5
        y -= _lp(y, 120)
    elif kind == 'swish':          # short, light
        n = int(.3 * SR); t = np.arange(n) / SR
        y = _lp(rng.standard_normal(n), 1800 + 3000 * (t / .3)) * np.sin(np.pi * t / .3) ** 2
        y -= _lp(y, 300)
    elif kind == 'pop':
        n = int(.16 * SR); t = np.arange(n) / SR
        f = 900 * np.exp(-t * 18) + 380
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .002, .045)
    elif kind == 'tick':
        n = int(.06 * SR); t = np.arange(n) / SR
        y = np.sin(2 * np.pi * 2100 * t) * _env(n, .001, .012) * .8
    elif kind == 'thud':
        n = int(.6 * SR); t = np.arange(n) / SR
        f = 48 + 60 * np.exp(-t * 14)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .004, .18)
        y += _lp(rng.standard_normal(n), 900) * _env(n, .001, .03) * .8
    elif kind == 'clank':
        n = int(.9 * SR); t = np.arange(n) / SR
        y = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * d) * g
                for f, d, g in [(311, 6, 1), (742, 8, .7), (1187, 9, .5), (1709, 12, .35), (2633, 15, .25)])
        y += _lp(rng.standard_normal(n), 3000) * _env(n, .001, .015) * 1.5
        y *= _env(n, .001, .5)
    elif kind == 'rumble':
        n = int(1.8 * SR); t = np.arange(n) / SR
        y = _lp(_lp(rng.standard_normal(n), 140), 140) * np.sin(np.pi * t / 1.8) ** 2 * 6
    elif kind == 'bubble':
        n = int(.9 * SR); y = np.zeros(n)
        for k in range(7):
            st = int(rng.uniform(0, .6) * SR); m = int(.07 * SR); t = np.arange(m) / SR
            f0 = rng.uniform(380, 900)
            b = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 3 * t / .07)) / SR) * _env(m, .004, .02)
            y[st:st + m] += b[:max(0, min(m, n - st))] * rng.uniform(.4, 1)
    elif kind == 'flame':
        n = int(1.2 * SR); t = np.arange(n) / SR
        y = _lp(rng.standard_normal(n), 1400) * np.sin(np.pi * t / 1.2) ** 1.5
        y *= 1 + .5 * np.sin(2 * np.pi * 7 * t)
    elif kind == 'shimmer':
        n = int(.8 * SR); t = np.arange(n) / SR
        y = sum(np.sin(2 * np.pi * f * t) for f in (1320, 1980, 2640)) / 3 * _env(n, .03, .25)
    else:
        raise ValueError(kind)
    y = y / (np.abs(y).max() + 1e-9)
    return y.astype(np.float32)


SFX_LEVEL = {'whoosh': -27, 'swish': -31, 'pop': -29, 'tick': -33, 'thud': -24, 'clank': -27,
             'rumble': -26, 'bubble': -31, 'flame': -32, 'shimmer': -35}
