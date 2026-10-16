"""Episode base class: timing lookups, map projection, frame assembly."""
import json, math, subprocess
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from engine import *


def mp3_duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


class Episode:
    slug = ''          # voiceover slug, e.g. 01_Fort_Jefferson
    gfx = ''           # graphics folder
    out = ''           # final mp4 name
    title = ''
    cover_t = 2.0
    cover_title = ''
    emphasis = []
    vo = VO            # folder holding <slug>.mp3 and <slug>_script.txt

    def __init__(self):
        self.G = GFX / self.gfx
        self.words = json.loads((EDIT / 'timing' / f'{self.slug}.final.json').read_text(encoding='utf-8'))
        self.dur = mp3_duration(self.vo / f'{self.slug}.mp3')
        self.nframes = math.ceil(self.dur * FPS - 1e-6)
        self.caps = Captions(self.words, self.emphasis, self.nframes / FPS)
        sb = json.loads((self.G / 'storyboard.json').read_text())
        self.bbox = sb['bbox']
        self.beats = []        # (t, description) - visual beat log
        self.sfx_events = []   # (t, kind, gain offset dB)
        self.setup()

    # ---- timing helpers
    def w(self, word, n=1, end=False):
        """Start (or end) time of the n-th occurrence of `word` in the narration."""
        cs = any(ch.isupper() for ch in word)       # capitalised query -> case-sensitive match
        strip = lambda v: re.sub(r"[^A-Za-z0-9$']", '', v.replace('’', "'"))
        k = strip(word) if cs else norm_word(word); c = 0
        for x in self.words:
            if (strip(x['w']) if cs else norm_word(x['w'])) == k:
                c += 1
                if c == n:
                    return x['end'] if end else x['start']
        raise KeyError(f'{word!r} #{n} not in {self.slug}')

    def beat(self, t, desc, sfx=None, gain=0.0):
        self.beats.append((round(t, 2), desc))
        if sfx:
            self.sfx_events.append((t, sfx, gain))
        return t

    # ---- geography
    def geo(self, lon, lat):
        b = self.bbox
        return ((lon - b[0]) / (b[2] - b[0]) * W, (b[3] - lat) / (b[3] - b[1]) * H)

    def base_map(self, bright=.80, sat=1.05, contrast=1.06):
        im = Image.open(self.G / 'map_terrain.jpg').convert('RGB')
        im = ImageEnhance.Color(im).enhance(sat)
        im = ImageEnhance.Contrast(im).enhance(contrast)
        return ImageEnhance.Brightness(im).enhance(bright)

    def draw_map(self, cv, st, base=None, alpha=1.0):
        m = render_map(base or self.base, st).convert('RGBA')
        if alpha < 1:
            m = with_alpha(m, alpha)
        cv.alpha_composite(m)

    def S(self, st, lon, lat):
        return Cam.S(st, *self.geo(lon, lat))

    # ---- frame
    def setup(self):
        raise NotImplementedError

    def draw(self, cv, t):
        raise NotImplementedError

    def frame(self, t, captions=True):
        cv = Image.new('RGBA', (W, H), col(INK))
        self.draw(cv, t)
        if captions:
            self.caps.draw(cv, t)
        return cv.convert('RGB')

    def cover(self):
        cv = Image.new('RGBA', (W, H), col(INK))
        self.draw(cv, self.cover_t)
        # title block in a shaded lower band (keeps the hero visual clear)
        cv.alpha_composite(_cover_shade())
        lines = self.cover_title.split('\n')
        place(cv, label_img('MAP CURIOUS', 30, LIME), 540, 1270, 1.0, 1.0)
        y = 1360
        for i, ln in enumerate(lines):
            im = hero_img(ln, 78, LIME if i == len(lines) - 1 else WHITE)
            place(cv, im, 540, y, min(1.0, 960 / im.width), 1.0)
            y += 96
        return cv.convert('RGB')


@functools.lru_cache(None)
def _cover_shade():
    a = np.zeros((H, W), np.float32)
    y = np.arange(H, dtype=np.float32)[:, None]
    a += np.clip((y - 1060) / 140, 0, 1) * 255
    im = Image.new('RGBA', (W, H), col(OUTLINE, 0))
    im.putalpha(Image.fromarray(np.broadcast_to(np.clip(a, 0, 255), (H, W)).astype(np.uint8)))
    return im


def frame_on(p, sx, sy, z, t=0):
    """Camera key (t, cx, cy, z) that puts map point p at screen (sx, sy) at zoom z."""
    return (t, p[0] - (sx - 540) / z, p[1] - (sy - 960) / z, z)


def slide_map(cv, m, off):
    """Paste a rendered map layer shifted vertically by off px, with a soft edge shadow."""
    if off <= -H:
        return
    if off < 0:
        sh = Image.new('RGBA', (W, 60), (0, 0, 0, 0))
        g = np.linspace(170, 0, 60).astype(np.uint8)[:, None].repeat(W, 1)
        sh.putalpha(Image.fromarray(g))
        paste(cv, sh, 0, H + off)
    paste(cv, m, 0, off)
