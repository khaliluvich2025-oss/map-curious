"""07 - Iceland Is Being Pulled Apart.

Base map: the pack's NASA Blue Marble Greenland/Iceland render (04_denmark_strait bbox);
Greenland/Iceland highlights traced from that image's own coastlines (as in ep04).
Facts: Iceland sits on the Mid-Atlantic Ridge between the North American and Eurasian
plates, which separate by ~2 cm/yr (USGS compares Atlantic spreading to fingernail
growth); Thingvellir (Þingvellir) National Park lies in the rift valley; rising magma
feeds Iceland's volcanoes.  Ridge line is generalised; cross-sections are schematic.
"""
from episode import *
from engine import _head
from ep04_underwater_waterfall import EP as EP4

BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
SEA = 420
YEL = (255, 214, 90)
NA_C = (55, 217, 208)       # North American plate tint (teal)
EU_C = (255, 154, 75)       # Eurasian plate tint (orange)
RIDGE = [(-33.0, 57.0), (-29.5, 59.5), (-26.0, 62.0), (-22.9, 63.8), (-21.1, 64.3), (-19.0, 64.7), (-17.0, 65.3),
         (-16.8, 66.2), (-18.3, 67.3), (-17.3, 69.0), (-15.5, 70.6), (-12.0, 71.4)]
ICE_RIDGE = RIDGE[3:8]
VOLC = [(-19.67, 63.99), (-19.05, 63.63), (-19.62, 63.63), (-17.33, 64.42), (-17.53, 64.64), (-16.75, 65.03),
        (-16.78, 65.73), (-22.27, 63.90), (-23.78, 64.81), (-16.65, 64.0)]


def floor_y(x, iceland=0.0):
    """Seafloor profile with ridge crest at x=540; iceland (0..1) raises the crest above sea."""
    base = 640 + 180 * min(1, abs(x - 540) / 420) ** 1.2
    rise = iceland * 300 * max(0, 1 - abs(x - 540) / 300) ** 1.5
    rift = 28 * max(0, 1 - abs(x - 540) / 26)
    return base - rise + rift


class EP(Episode):
    slug = '07_Iceland_Rift'
    gfx = '04_denmark_strait'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '07_Iceland_Rift_Final.mp4'
    title = 'Iceland Is Being Pulled Apart'
    cover_title = 'ICELAND IS BEING\nPULLED APART'
    cover_t = 15.0
    emphasis = ['Iceland', 'pulled', 'Mid-Atlantic', 'Ridge,', 'North', 'American', 'Eurasian', 'two', 'centimeters',
                'fingernails', 'underwater,', 'rises', 'Thingvellir', 'rift', 'Magma', 'volcanoes.', 'built.']
    _build_land = EP4._build_land

    def setup(self):
        w = self.w
        self.base = self.base_map(.84)
        self._build_land()
        g = self.geo
        self.I = g(-18.7, 64.95)
        self.TH = g(-21.12, 64.26)
        self.ridge = spline([g(*p) for p in RIDGE], 14)
        self.ice_ridge = spline([g(*p) for p in ICE_RIDGE], 14)
        T = self.T = dict(
            iceland=w('Iceland', 1), pulled=w('pulled'), island=w('island', 1), mid=w('Mid-Atlantic'), crack=w('crack'),
            middle=w('middle'), north=w('North'), eurasian=w('Eurasian'), theyre=w("They're"), moving=w('moving'),
            two=w('two'), fingernails=w('fingernails'), most=w('Most'), hidden=w('hidden'), but=w('but'),
            iceland2=w('Iceland', 2), rises=w('rises', 1), at=w('At'), thing=w('Thingvellir'), walk=w('walk'),
            rift=w('rift'), between=w('between'), magma=w('Magma'), gap=w('gap'), volcanoes=w('volcanoes'),
            zoom=w('Zoom'), watching=w('watching'), built=w('built'))
        I, TH = self.I, self.TH
        wide = (0, 630, 1120, 1.2)
        self.cam = Cam([
            frame_on(I, 540, 640, 2.4, 0), frame_on(I, 540, 640, 2.2, T['island'] - .2),
            (T['mid'] + .9,) + wide[1:], (T['two'],) + (630, 1120, 1.25), (T['most'] - .4,) + (630, 1120, 1.3),
            frame_on(TH, 540, 640, 3.0, T['thing']), frame_on(TH, 540, 640, 3.1, T['walk'] - .4),
            frame_on(I, 540, 640, 2.3, T['volcanoes'] - .6), frame_on(I, 540, 640, 2.4, T['zoom']),
            (T['zoom'] + 1.6,) + wide[1:], (self.dur,) + (630, 1120, 1.24)])
        self.slides = [(T['hidden'] - .25, 1), (T['at'] - .2, 0), (T['walk'] - .35, 1), (T['volcanoes'] - .45, 0)]
        b = self.beat
        b(0.0, 'Iceland highlighted on the NASA map', 'pop', 2)
        b(T['pulled'], 'Rift line splits Iceland, arrows pull apart', 'rumble')
        b(T['island'], 'Camera starts pulling out', 'whoosh')
        b(T['mid'], 'Mid-Atlantic Ridge draws through the North Atlantic', 'swish')
        b(T['middle'], 'Ridge continues south off the map', 'tick')
        b(T['north'], 'North American Plate tint + label', 'pop')
        b(T['eurasian'], 'Eurasian Plate tint + label', 'pop')
        b(T['moving'], 'Spreading arrows along the ridge', 'swish')
        b(T['two'], '≈2 CM A YEAR', 'thud')
        b(T['fingernails'], 'ABOUT AS FAST AS FINGERNAILS GROW', 'tick')
        b(T['hidden'] - .25, 'Map lifts: ridge deep underwater (schematic)', 'bubble')
        b(T['iceland2'], 'Crest rises above sea level: Iceland', 'rumble')
        b(T['at'] - .2, 'Map returns, pushes into Thingvellir', 'whoosh')
        b(T['thing'], 'THINGVELLIR NATIONAL PARK pin', 'pop')
        b(T['walk'] - .35, 'Rift valley close-up, walker between plates', 'swish')
        b(T['between'], 'Plate labels on each cliff', 'tick')
        b(T['magma'], 'Magma rises into the gap', 'rumble')
        b(T['volcanoes'] - .45, 'Map: Iceland volcanoes pop up', 'pop')
        b(T['zoom'], 'Zoom out: whole ridge glows', 'whoosh')
        b(T['watching'], 'Plates spread again', 'swish')
        b(T['built'], 'STILL BEING BUILT', 'shimmer')

    # -------------------------------------------------------------------------
    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    def plate_tints(self, m, st, t, a):
        if a <= 0:
            return
        S = lambda p: Cam.S(st, *p)
        r = [S(q) for q in self.ridge]
        top = (r[-1][0], -400); bot = (r[0][0], H + 400)
        west = [bot] + r + [top, (-400, -400), (-400, H + 400)]
        east = [bot] + r + [top, (W + 400, -400), (W + 400, H + 400)]

        def fn(d, P, s):
            d.polygon([P(*q) for q in west], fill=col(NA_C, .16))
            d.polygon([P(*q) for q in east], fill=col(EU_C, .16))
        vec(m, (0, 0, W, H), fn, a, ss=1, base=NA_C)

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        for name, a0 in (('gl', 1e9 if t < T['north'] else T['north']), ('ic', -.4)):
            fill, bord = self.land[name]
            fa = vis(t, a0, None, .4) * (.55 if name == 'gl' else 1)
            if fa > 0:
                m.alpha_composite(with_alpha(render_map(fill, st, 2.0), fa))
                m.alpha_composite(with_alpha(render_map(bord, st, 2.0), fa * .8))
        self.plate_tints(m, st, t, max(vis(t, T['north'], T['most'] - .3, .6, .4), vis(t, T['zoom'] + .4, None, .6)))
        m.alpha_composite(vignette())
        S = lambda p: Cam.S(st, *p)
        # ridge: Iceland segment first (hook), then whole ridge
        glow = .75 + .25 * math.sin(t * 5)
        ice = [S(q) for q in self.ice_ridge]
        route(m, ice, e_io((t - T['pulled'] + .1) / .7), RED, 9, head=False, alpha=glow * vis(t, T['pulled'] - .1, T['mid'] + .3))
        rid = [S(q) for q in self.ridge]
        route(m, rid, e_io((t - T['mid']) / 1.6), RED, 8, head=False, alpha=glow * vis(t, T['mid'], T['thing'] - .3))
        route(m, rid, 1, RED, 8, head=False, alpha=glow * vis(t, T['volcanoes'] - .5, None, .5))
        # arrows pulling apart
        def spread(a0, b0, pts, n=3, L=70):
            al = vis(t, a0, b0, .3, .3)
            if al <= 0:
                return
            p = e_out((t - a0) / .8)
            for k in range(n):
                (x, y), ang = point_at(pts, (k + 1) / (n + 1))
                nx, ny = -math.sin(ang), math.cos(ang)
                for sgn, c in ((1, EU_C), (-1, NA_C)):
                    dx, dy = nx * sgn, ny * sgn
                    if (dx < 0) != (sgn < 0) and abs(dx) > .1:   # make east arrows point east
                        dx, dy = -dx, -dy
                    s0 = (x + dx * 18, y + dy * 18)
                    route(m, [s0, (s0[0] + dx * L * p, s0[1] + dy * L * p)], 1, c, 8, alpha=al, head_size=24)
        spread(T['pulled'] + .2, T['island'] + 1.0, ice, 2, 80)
        spread(T['moving'], T['most'] - .3, rid, 4, 60)
        spread(T['watching'], None, rid, 4, 60)
        # labels
        il = S(self.I)
        chip(m, 'ICELAND', il[0], il[1] + 150, t, -.1, T['mid'], size=42, accent=ORANGE)
        chip(m, 'MID-ATLANTIC RIDGE', 540, 330, t, T['mid'] + .1, T['north'] - .2, size=40, accent=RED)
        pa = S(self.geo(-38, 64.5)); pe = S(self.geo(-9.5, 64.2))
        chip(m, 'NORTH AMERICAN PLATE', max(pa[0], 250), pa[1], t, T['north'], T['most'] - .3, size=32, accent=NA_C)
        chip(m, 'EURASIAN PLATE', min(pe[0], 830), pe[1], t, T['eurasian'], T['most'] - .3, size=32, accent=EU_C)
        chip(m, 'NORTH AMERICAN', max(pa[0], 200), pa[1], t, T['zoom'] + .5, None, size=30, accent=NA_C)
        chip(m, 'EURASIAN', min(pe[0], 860), pe[1], t, T['zoom'] + .7, None, size=30, accent=EU_C)
        if t >= T['middle'] and t < T['north'] + .5:
            sb = S(self.geo(-33, 57))
            route(m, [sb, (sb[0] - 40, H + 60)], e_out((t - T['middle']) / .8), RED, 8, alpha=vis(t, T['middle'], T['north'] + .2), dashed=True, dash=(16, 10), head_size=26)
        # Thingvellir
        tx, ty = S(self.TH)
        pin(m, tx, ty, t, T['thing'] - .1, T['walk'], LIME, 16)
        chip(m, 'THINGVELLIR', tx - 20, ty - 120, t, T['thing'], T['walk'], size=40, sub='NATIONAL PARK · ICELAND')
        # volcanoes
        for i, (lon, lat) in enumerate(VOLC):
            x, y = S(self.geo(lon, lat))
            a0 = T['volcanoes'] - .3 + i * .1
            al = vis(t, a0, None, .2)
            if al > 0:
                sc = e_back((t - a0) / .4, 2.0)

                def fn(d, P, s, x=x, y=y, sc=sc):
                    r = 17 * sc
                    d.polygon([P(x, y - r * 1.25), P(x + r, y + r * .6), P(x - r, y + r * .6)], fill=col(ORANGE), outline=col(OUTLINE), width=int(3 * s))
                vec(m, (x - 30, y - 30, x + 30, y + 30), fn, al * (1 - .5 * prog(t, T['zoom'] + .8, .8)), base=ORANGE)
        return m

    # ---- schematic panels ------------------------------------------------------
    def ridge_panel(self, d, P, s, t):
        T = self.T
        ice = e_io((t - T['iceland2']) / 1.6) if t >= T['iceland2'] else 0
        magma_up = e_out((t - T['magma'] - .2) / 1.6) if t >= T['magma'] else 0
        d.rectangle((*P(BX0, BY0), *P(BX1, SEA)), fill=(20, 40, 62, 255))
        for i in range(16):
            y0 = lerp(SEA, BY1, i / 16); y1 = lerp(SEA, BY1, (i + 1) / 16)
            c = tuple(int(lerp(a, b, i / 15)) for a, b in zip((34, 96, 150), (8, 30, 56)))
            d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
        xs = list(range(BX0, BX1 + 1, 8))
        crust = [(x, floor_y(x, ice)) for x in xs]
        d.polygon([P(*q) for q in crust] + [P(BX1, BY1), P(BX0, BY1)], fill=(92, 80, 70, 255))
        # mantle / magma
        d.rectangle((*P(BX0, 860), *P(BX1, BY1)), fill=(150, 70, 40, 255))
        top = lerp(860, floor_y(540, ice) + 4, max(magma_up, .25))
        d.polygon([P(500, 862), P(580, 862), P(552, top), P(528, top)], fill=(255, 112, 40, 255))
        d.ellipse((*P(470, 840), *P(610, 900)), fill=(255, 130, 50, 255))
        if magma_up > 0:
            for k in range(8):
                ph = (t * .7 + k / 8) % 1
                y = lerp(860, top, ph)
                d.ellipse((*P(535 + 8 * math.sin(k + t * 3) - 6, y - 6), *P(535 + 8 * math.sin(k + t * 3) + 6, y + 6)), fill=col(YEL, 1 - ph * .5))
        # crust plate split line + arrows
        for sgn, c in ((-1, NA_C), (1, EU_C)):
            x0 = 540 + sgn * 70; L = 140 + 20 * math.sin(t * 2)
            y = 760
            pts = [(x0, y), (x0 + sgn * L, y)]
            d.line([P(*q) for q in pts], fill=col(c), width=int(8 * s))
            _head(d, P, s, pts[-1], 0 if sgn > 0 else math.pi, 20, col(c))
        # sea surface line + waves
        wv = [P(x, SEA + 4 * math.sin(x / 40 + t * 2)) for x in range(BX0, BX1 + 1, 12)]
        d.line(wv, fill=col(WHITE, .85), width=int(3 * s))
        d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

    def valley_panel(self, d, P, s, t):
        T = self.T
        for i in range(12):
            y0 = lerp(BY0, 700, i / 12); y1 = lerp(BY0, 700, (i + 1) / 12)
            c = tuple(int(lerp(a, b, i / 11)) for a, b in zip((70, 110, 150), (150, 180, 200)))
            d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
        wall = (84, 78, 72, 255)
        d.polygon([P(BX0, 470), P(330, 470), P(350, 560), P(372, 700), P(BX0, 700)], fill=wall)        # west cliff
        d.polygon([P(BX1, 520), P(760, 520), P(738, 600), P(712, 700), P(BX1, 700)], fill=wall)        # east cliff
        d.rectangle((*P(BX0, 700), *P(BX1, BY1)), fill=(66, 92, 58, 255))
        d.rectangle((*P(372, 690), *P(712, 712)), fill=(92, 118, 74, 255))                           # valley floor
        for x in range(BX0 + 20, 330, 40):
            d.line([P(x, 480), P(x + 10, 690)], fill=(70, 66, 60, 255), width=int(3 * s))
        for x in range(780, BX1, 40):
            d.line([P(x, 530), P(x - 10, 690)], fill=(70, 66, 60, 255), width=int(3 * s))
        # walker
        p = clamp((t - T['walk']) / 3.2)
        x = lerp(400, 680, p); y = 690
        step = math.sin(p * 40) * 8
        d.ellipse((*P(x - 9, y - 70), *P(x + 9, y - 52)), fill=col(WHITE))
        d.line([P(x, y - 52), P(x, y - 24)], fill=col(WHITE), width=int(5 * s))
        d.line([P(x, y - 24), P(x - 8 + step, y)], fill=col(WHITE), width=int(5 * s))
        d.line([P(x, y - 24), P(x + 8 - step, y)], fill=col(WHITE), width=int(5 * s))
        d.line([P(x, y - 44), P(x - 10 - step * .5, y - 30)], fill=col(WHITE), width=int(4 * s))
        # arrows on cliff tops
        for sgn, c, xx, yy in ((-1, NA_C, 230, 440), (1, EU_C, 860, 490)):
            pts = [(xx - sgn * 40, yy), (xx + sgn * 60, yy)]
            d.line([P(*q) for q in pts], fill=col(c), width=int(8 * s))
            _head(d, P, s, pts[-1], 0 if sgn > 0 else math.pi, 20, col(c))
        d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

    def panel(self, cv, t, al):
        T = self.T
        valley = T['walk'] - .5 <= t < T['magma'] - .1
        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (18, 36, 58))
        d = ImageDraw.Draw(L, 'RGBA')
        P = lambda x, y: ((x - BX0) * 2, (y - BY0) * 2)
        (self.valley_panel if valley else self.ridge_panel)(d, P, 2, t)
        sec = L.reduce(2).convert('RGBA')
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(Image.fromarray(np.minimum(np.asarray(sec.getchannel('A')), np.asarray(m))))
        fade = .35 + .65 * clamp((t - (T['magma'] - .1)) / .3) if T['magma'] - .1 <= t < T['magma'] + .2 else 1
        paste(cv, with_alpha(sec, al * fade), BX0, BY0)
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        if valley:
            label(cv, 'NORTH AMERICAN PLATE', 210, 400, t, T['between'] - .2, None, 26, (170, 245, 240), rise=6)
            label(cv, 'EURASIAN PLATE', 870, 455, t, T['between'] - .1, None, 26, (255, 200, 150), rise=6)
            label(cv, 'RIFT VALLEY', 540, 760, t, T['rift'], None, 30, WHITE, rise=6)
        else:
            label(cv, 'SEA LEVEL', 120, SEA - 20, t, 0, None, 22, WHITE, rise=0, anchor='l')
            label(cv, 'MID-ATLANTIC RIDGE', 540, 560, t, T['hidden'] + .2, T['iceland2'], 28, WHITE, rise=6)
            label(cv, 'DEEP UNDERWATER', 540, 470, t, T['hidden'] + .5, T['iceland2'], 30, (170, 225, 245), rise=6)
            label(cv, 'ICELAND', 540, 360, t, T['iceland2'] + 1.0, T['at'] - .3, 34, LIME, rise=8)
            label(cv, 'NORTH AMERICAN', 270, 800, t, T['hidden'] + .3, None, 24, (170, 245, 240), rise=0)
            label(cv, 'EURASIAN', 810, 800, t, T['hidden'] + .3, None, 24, (255, 200, 150), rise=0)
            label(cv, 'MAGMA', 640, 880, t, T['hidden'] + .5, None, 26, YEL, rise=0)

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_bg())
            self.panel(cv, t, clamp(u * 1.5))
            label(cv, 'ICELAND', 540, 280, t, 0, None, 30, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area --------------------------------------------------------
        chip(cv, 'BEING PULLED APART', 540, 1260, t, T['pulled'], T['mid'] - .1, size=42, accent=RED)
        chip(cv, 'RUNS THROUGH THE ATLANTIC', 540, 1260, t, T['middle'] - .2, T['north'] - .1, size=38, accent=RED)
        hero(cv, '≈2 CM A YEAR', 540, 1285, t, T['two'], T['most'] - .3, 110, LIME)
        chip(cv, 'ABOUT AS FAST AS FINGERNAILS GROW', 540, 1410, t, T['fingernails'] - .1, T['most'] - .3, size=30, accent=LIME)
        chip(cv, 'MOST OF THE RIDGE IS UNDERWATER', 540, 1260, t, T['hidden'], T['iceland2'] - .1, size=34, accent=TEAL)
        chip(cv, 'IN ICELAND IT RISES ABOVE THE SEA', 540, 1260, t, T['iceland2'], T['at'] - .3, size=34, accent=LIME)
        chip(cv, 'WALK BETWEEN TWO PLATES', 540, 1260, t, T['walk'], T['magma'] - .2, size=38, accent=LIME)
        chip(cv, 'MAGMA FILLS THE GAP', 540, 1260, t, T['magma'], T['volcanoes'] - .4, size=40, accent=ORANGE)
        chip(cv, 'SO MANY VOLCANOES', 540, 1260, t, T['volcanoes'] - .3, T['zoom'] - .1, size=40, accent=ORANGE)
        chip(cv, 'STILL BEING BUILT', 540, 1270, t, T['built'] - .2, None, size=46, accent=LIME)
        label(cv, 'SOURCE: USGS', 540, 1595, t, T['zoom'], None, 18, (200, 210, 215), rise=0)


@functools.lru_cache(None)
def _bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
