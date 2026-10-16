"""10 - The Deepest Lake in America (Crater Lake, Oregon).

Base map: the pack's NASA Blue Marble Pacific Northwest render (02_db_cooper bbox).
Facts (NPS / USGS): Crater Lake fills the caldera of Mount Mazama, which erupted and
collapsed about 7,700 years ago; caldera ~5-6 mi across; filled by rain and snow over
centuries; no rivers flow in or out; max depth 1,943 ft, deepest lake in the U.S.;
known for exceptional clarity and deep blue colour.
Volcano profile is schematic (labelled on screen).
"""
from episode import *
from engine import _head

CL = (-122.108, 42.944)
BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
GROUND = 820
BEFORE = [(130, GROUND), (330, 610), (440, 490), (510, 440), (570, 440), (640, 490), (750, 610), (950, GROUND)]
AFTER = [(130, GROUND), (330, 610), (410, 560), (450, 690), (630, 690), (670, 560), (750, 610), (950, GROUND)]
SURF = 585
VOLCANOES = [('BAKER', -121.8144, 48.7768), ('RAINIER', -121.760, 46.853), ('ST. HELENS', -122.1944, 46.1912),
             ('ADAMS', -121.4906, 46.2024), ('HOOD', -121.6959, 45.3736), ('JEFFERSON', -121.80, 44.674),
             ('3 SISTERS', -121.769, 44.103), ('MAZAMA', -122.11, 42.94), ('SHASTA', -122.194, 41.409),
             ('LASSEN', -121.508, 40.488)]
YEL = (255, 214, 90)
BLUE = (40, 120, 220)
LAKE = (24, 86, 190)


def shape(p, g=1.0):
    return [(lerp(a[0], b[0], p), GROUND - (GROUND - lerp(a[1], b[1], p)) * g) for a, b in zip(BEFORE, AFTER)]


class EP(Episode):
    slug = '10_Crater_Lake'
    gfx = '02_db_cooper'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '10_Crater_Lake_Final.mp4'
    title = 'The Deepest Lake in America'
    cover_title = 'THE DEEPEST\nLAKE IN\nAMERICA'
    cover_t = 32.6
    emphasis = ['deepest', 'America', 'collapsed.', 'Crater', 'Lake,', 'Oregon.', 'seventy-seven', 'Mazama', 'erupted.',
                'caldera.', 'rain', 'snow', 'No', 'none', 'nineteen', 'hundred', 'United', 'States.', 'sky,', 'clearest,',
                'bluest']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        self.CL = self.geo(*CL)
        T = self.T = dict(
            deepest=w('deepest', 1), america=w('America'), volcano=w('volcano', 1), collapsed=w('collapsed'),
            crater=w('Crater'), cascade=w('Cascade'), oregon=w('Oregon'), about=w('About'), seventy=w('seventy-seven'),
            towering=w('towering'), mount=w('Mount'), erupted=w('erupted'), blasted=w('blasted'), ash=w('ash'),
            magma=w('magma'), top=w('top'), fell=w('fell'), leaving=w('leaving'), bowl=w('bowl'), caldera=w('caldera'),
            over=w('Over'), rain=w('rain'), snow=w('snow'), filled=w('filled'), no=w('No'), flow1=w('flow', 1),
            none=w('none'), out2=w('out', 2), today=w('Today'), nineteen=w('nineteen'), deepest2=w('deepest', 2),
            united=w('United'), and_=w('And'), water=w('water'), falls=w('falls'), sky=w('sky'), clearest=w('clearest'),
            bluest=w('bluest'), earth=w('Earth'))
        C = self.CL
        oreg = self.geo(-121.4, 44.6)
        self.back = T['sky'] + .5
        self.cam = Cam([
            frame_on(C, 540, 640, 2.7, 0), frame_on(C, 540, 640, 3.1, T['collapsed'] + .4),
            frame_on(C, 540, 640, 2.9, T['crater'] + .3), frame_on(oreg, 540, 600, 1.45, T['cascade'] + .5),
            frame_on(oreg, 540, 600, 1.4, T['about'] + .2), frame_on(C, 540, 640, 2.4, self.back - .5),
            frame_on(C, 540, 640, 3.0, self.back + .8), frame_on(C, 540, 640, 3.4, self.dur)])
        self.slides = [(T['about'] - .25, 1), (self.back, 0)]
        b = self.beat
        b(0.0, 'Crater Lake pin on the Oregon map', 'pop', 2)
        b(T['deepest'], 'DEEPEST LAKE label', 'tick')
        b(T['america'], 'Hero: DEEPEST LAKE IN THE U.S.', 'thud')
        b(T['volcano'], 'Volcano icon rises over the pin', 'pop')
        b(T['collapsed'], 'Icon collapses into a blue bowl', 'rumble')
        b(T['crater'], 'CRATER LAKE chip', 'pop')
        b(T['cascade'], 'Camera pulls back; Cascade volcanoes pop up', 'whoosh')
        b(T['oregon'], 'OREGON label', 'tick')
        b(T['about'] - .25, 'Map lifts: schematic volcano profile', 'whoosh')
        b(T['seventy'], '≈7,700 YEARS AGO', 'thud')
        b(T['towering'], 'Mount Mazama grows tall', 'swish')
        b(T['mount'], 'MOUNT MAZAMA chip', 'pop')
        b(T['erupted'], 'Eruption begins', 'rumble', 2)
        b(T['blasted'], 'Ash column surges upward', 'whoosh', 2)
        b(T['ash'], 'ASH + MAGMA chip; magma chamber glows', 'tick')
        b(T['magma'], 'Magma chamber drains', None)
        b(T['top'], 'Summit highlighted', 'tick')
        b(T['fell'], 'Summit collapses (shake)', 'rumble', 3)
        b(T['leaving'], 'Empty caldera revealed', 'swish')
        b(T['bowl'], '≈5 MI ACROSS width arrow', 'tick')
        b(T['caldera'], 'CALDERA chip', 'pop')
        b(T['rain'], 'Rain falls into the caldera', 'swish')
        b(T['snow'], 'Snowflakes join; water level rises', 'tick')
        b(T['filled'], 'Lake fills to the brim', 'pop')
        b(T['no'], 'River-in arrow, crossed out', 'tick')
        b(T['out2'], 'River-out arrow, crossed out', 'tick')
        b(T['today'], 'Depth ruler draws down', 'swish')
        b(T['nineteen'], '1,943 FT', 'thud')
        b(T['deepest2'], 'DEEPEST LAKE IN THE U.S. chip', 'pop')
        b(T['water'], 'Rain again: fed from the sky', 'swish')
        b(self.back, 'Back to the map, zoom on the lake', 'whoosh')
        b(T['clearest'], 'Lake glows blue; CLEAREST chip', 'pop')

    # -------------------------------------------------------------------------
    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    def section(self, cv, t, al):
        T = self.T
        g = lerp(.55, 1.0, e_out((t - T['towering']) / 1.0))
        p = e_io((t - T['fell']) / 1.3)
        poly = shape(p, g)
        erupt = clamp((t - T['erupted']) / .6) * (1 - prog(t, T['leaving'], 1.0))
        surge = e_out((t - T['blasted']) / 2.0) if t >= T['blasted'] else 0
        magma = vis(t, T['ash'] - .2, T['leaving'], .4, .6)
        drain = clamp((t - T['magma']) / 2.2)
        fill = e_io((t - T['rain']) / (T['filled'] + .6 - T['rain'])) if t >= T['rain'] else 0
        level = lerp(690, SURF, fill)
        rain1 = vis(t, T['rain'] - .1, T['no'], .3, .5)
        rain2 = vis(t, T['water'] - .1, self.back, .3, .3)
        snow = vis(t, T['snow'], T['no'], .3, .5)
        top_hl = vis(t, T['top'] - .1, T['fell'] + .2, .2, .3)

        def fn(d, P, s):
            for i in range(14):
                y0 = lerp(BY0, GROUND, i / 14); y1 = lerp(BY0, GROUND, (i + 1) / 14)
                c = tuple(int(lerp(a, b, i / 13)) for a, b in zip((18, 36, 58), (52, 78, 96)))
                d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
            # eruption column (behind mountain)
            if erupt > 0:
                top0 = poly[3][1]
                top = lerp(top0 - 30, BY0 + 10, surge)
                for i in range(26):
                    q = i / 25
                    y = lerp(top0, top, q)
                    r = lerp(26, 40 + 130 * surge, q ** 1.5) * (1 + .07 * math.sin(t * 3 + i))
                    x = 540 + 16 * math.sin(i * 1.3 + t)
                    gg = int(lerp(115, 165, q))
                    d.ellipse((*P(x - r, y - r * .7), *P(x + r, y + r * .7)), fill=(gg, gg - 4, gg - 10, int(235 * erupt)))
            d.rectangle((*P(BX0, GROUND), *P(BX1, BY1)), fill=(74, 66, 52, 255))
            # magma chamber
            if magma > 0:
                rx, ry = 80 * (1 - .65 * drain), 34 * (1 - .5 * drain)
                d.ellipse((*P(540 - rx, 870 - ry), *P(540 + rx, 870 + ry)), fill=col((255, 96, 40), .9 * magma),
                          outline=col(YEL, magma), width=int(4 * s))
                if erupt > 0 and p < 1:
                    d.line([P(540, 870 - ry), P(540, poly[3][1] + 10)], fill=col((255, 110, 40), .8 * magma * (1 - p)), width=int(10 * s))
            # mountain
            d.polygon([P(*q) for q in poly], fill=(110, 100, 88, 255))
            d.line([P(*q) for q in poly], fill=(235, 235, 225, 255), width=int(4 * s), joint='curve')
            if p < .4 and t < T['erupted'] + 1.5:
                cap = [(poly[2][0] + 10, poly[2][1] - 12 * g), poly[3], poly[4], (poly[5][0] - 10, poly[5][1] - 12 * g),
                       (540, poly[3][1] + 40 * g)]
                d.polygon([P(*q) for q in cap], fill=(240, 244, 246, int(255 * (1 - prog(t, T['erupted'], 1.5)))))
            if top_hl > 0:
                blk = [BEFORE[2], BEFORE[3], BEFORE[4], BEFORE[5]] + [AFTER[5], AFTER[4], AFTER[3], AFTER[2]]
                blk = [(x, GROUND - (GROUND - y) * g) for x, y in blk]
                d.polygon([P(*q) for q in blk], outline=col(ORANGE, top_hl * (.6 + .4 * math.sin(t * 8) ** 2)), width=int(6 * s))
            # falling summit debris
            if 0 < p < 1:
                for i in range(18):
                    x = 450 + (i * 37) % 180
                    y = lerp(470, 680, p) + (i * 23) % 40
                    r = 7 + (i * 5) % 8
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=(126, 108, 90, int(255 * (1 - p))))
            # lake water
            if fill > 0:
                def wx(yy, left):
                    return 410 + 40 * (yy - 560) / 130 if left else 670 - 40 * (yy - 560) / 130
                wp = [(wx(level, 1), level), (450, 690), (630, 690), (wx(level, 0), level)]
                d.polygon([P(*q) for q in wp], fill=LAKE + (255,))
                d.line([P(wx(level, 1), level), P(wx(level, 0), level)], fill=col((150, 205, 255)), width=int(4 * s))
            # rain / snow
            for amt, kind, seed in ((rain1, 'r', 0), (rain2, 'r', 7), (snow, 's', 3)):
                if amt <= 0:
                    continue
                for i in range(34):
                    x = 300 + ((i * 131 + seed * 53) % 440)
                    sp = 520 if kind == 'r' else 150
                    y = BY0 + ((i * 97 + t * sp) % (SURF - BY0 - 10))
                    if kind == 'r':
                        d.line([P(x, y), P(x - 4, y + 22)], fill=col((180, 215, 255), .85 * amt), width=int(3 * s))
                    else:
                        x += 10 * math.sin(t * 2 + i)
                        for a in (0, 1.05, 2.1):
                            d.line([P(x - 7 * math.cos(a), y - 7 * math.sin(a)), P(x + 7 * math.cos(a), y + 7 * math.sin(a))],
                                   fill=col(WHITE, .9 * amt), width=int(2 * s))
            # no rivers in / out
            for a0, pts in ((T['flow1'], [(170, 470), (380, 560)]), (T['out2'] - .3, [(700, 560), (910, 470)])):
                ra = vis(t, a0, T['today'], .3, .4)
                if ra > 0:
                    pe = e_out((t - a0) / .5)
                    end = (lerp(pts[0][0], pts[1][0], pe), lerp(pts[0][1], pts[1][1], pe))
                    d.line([P(*pts[0]), P(*end)], fill=col(TEAL, ra), width=int(8 * s))
                    _head(d, P, s, end, math.atan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0]), 18, col(TEAL, ra))
                    xa = vis(t, a0 + .45, T['today'], .2, .4)
                    if xa > 0:
                        mx, my = (pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2
                        for dx in (-1, 1):
                            d.line([P(mx - 26, my - 26 * dx), P(mx + 26, my + 26 * dx)], fill=col(RED, xa), width=int(9 * s))
            # depth ruler
            if t >= T['today'] - .1:
                ra = vis(t, T['today'] - .1, T['and_'], .3, .4)
                pe = e_out((t - T['today']) / .8)
                d.line([P(540, SURF), P(540, lerp(SURF, 690, pe))], fill=col(LIME, ra), width=int(6 * s))
                for yy in (SURF, 690):
                    if yy == SURF or pe >= 1:
                        d.line([P(520, yy), P(560, yy)], fill=col(LIME, ra), width=int(5 * s))
            d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (18, 36, 58))
        fn(ImageDraw.Draw(L, 'RGBA'), lambda x, y: ((x - BX0) * 2, (y - BY0) * 2), 2)
        sec = L.reduce(2).convert('RGBA')
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(Image.fromarray(np.minimum(np.asarray(sec.getchannel('A')), np.asarray(m))))
        shake = 0
        for a in (T['erupted'], T['fell']):
            if a <= t < a + .5:
                shake = math.sin(t * 63) * 8 * (1 - (t - a) / .5)
        paste(cv, with_alpha(sec, al), BX0 + shake, BY0)
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        label(cv, 'MOUNT MAZAMA', 540, 395, t, T['mount'], T['erupted'] + .2, 32, WHITE, rise=8)
        label(cv, 'ASH', 330, 380, t, T['ash'], T['top'], 30, (225, 220, 210), rise=8)
        label(cv, 'MAGMA', 720, 875, t, T['magma'], T['leaving'], 26, YEL, rise=0, anchor='l')
        label(cv, 'SUMMIT', 760, 470, t, T['top'], T['fell'] + .4, 30, ORANGE, rise=8, anchor='l')
        ba = vis(t, T['bowl'], T['rain'] - .1, .3, .3)
        if ba > 0:
            route(cv, [(412, 528), (668, 528)], e_out((t - T['bowl']) / .5), LIME, 5, head=True, alpha=ba, head_size=16)
            route(cv, [(668, 528), (412, 528)], e_out((t - T['bowl']) / .5), LIME, 5, head=True, alpha=ba, head_size=16)
            label(cv, '≈5 MI ACROSS', 540, 490, t, T['bowl'] + .2, T['rain'] - .1, 30, LIME, rise=6)
        label(cv, 'CALDERA', 540, 640, t, T['caldera'], T['rain'] + .3, 34, WHITE, rise=8)
        label(cv, 'RAIN', 260, 420, t, T['rain'], T['no'], 28, (180, 215, 255), rise=6)
        label(cv, 'SNOW', 820, 420, t, T['snow'], T['no'], 28, WHITE, rise=6)
        label(cv, 'NO RIVERS IN', 230, 420, t, T['flow1'] + .2, T['today'], 28, TEAL, rise=6)
        label(cv, 'NONE OUT', 850, 420, t, T['out2'], T['today'], 28, TEAL, rise=6)
        label(cv, '1,943 FT', 690, 650, t, T['nineteen'], T['and_'], 34, LIME, rise=6, anchor='l')
        label(cv, 'FED BY THE SKY', 540, 400, t, T['falls'], self.back, 32, (180, 215, 255), rise=8)

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        m.alpha_composite(vignette())
        S = lambda p: Cam.S(st, *p)
        cx, cy = S(self.CL)
        z = st[2]
        # lake glow
        ga = max(vis(t, T['collapsed'] + .2, T['cascade'], .4, .5), vis(t, self.back, None, .5))
        if ga > 0:
            r = max(14, 6 * z) * (1 + .5 * vis(t, T['clearest'], None, .6) * (.8 + .2 * math.sin(t * 4)))

            def fn(d, P, s):
                for k, a in ((2.4, .18), (1.6, .3), (1.0, 1)):
                    d.ellipse((*P(cx - r * k, cy - r * k), *P(cx + r * k, cy + r * k)), fill=col(BLUE if k > 1 else (30, 110, 235), a))
            vec(m, (cx - r * 3, cy - r * 3, cx + r * 3, cy + r * 3), fn, ga, base=BLUE)
        pin(m, cx, cy, t, -.12, T['cascade'], LIME)
        # hook volcano icon -> collapses into a bowl
        ia = vis(t, T['volcano'] - .1, T['crater'] + .2, .3, .4)
        if ia > 0:
            pc = e_io((t - T['collapsed']) / .7)
            ix, iy = cx, cy - 150

            def fn(d, P, s):
                pk = lerp(iy - 70, iy + 10, pc)
                d.polygon([P(ix - 90, iy + 40), P(ix - 30, lerp(iy - 50, iy - 10, pc)), P(ix, pk), P(ix + 30, lerp(iy - 50, iy - 10, pc)),
                           P(ix + 90, iy + 40)], fill=col((120, 108, 92)), outline=col(OUTLINE), width=int(3 * s))
                if pc > .5:
                    wl = lerp(iy + 10, iy - 6, (pc - .5) * 2)
                    d.polygon([P(ix - 24, wl), P(ix, iy + 10), P(ix + 24, wl)], fill=col((40, 120, 230)))
                if pc < .3:
                    d.polygon([P(ix - 14, iy - 58), P(ix, iy - 70), P(ix + 14, iy - 58)], fill=col(WHITE))
            vec(m, (ix - 100, iy - 90, ix + 100, iy + 50), fn, ia, base=(120, 108, 92))
        label(m, 'DEEPEST LAKE', cx + 40, cy + 4, t, T['deepest'], T['crater'] - .1, 32, WHITE, anchor='l', rise=6)
        chip(m, 'CRATER LAKE', cx, cy - 300, t, T['crater'], T['cascade'] - .1, size=42, sub='OREGON')
        # Cascade volcanoes
        for i, (nm, lon, lat) in enumerate(VOLCANOES):
            x, y = S(self.geo(lon, lat))
            a0 = T['cascade'] + .05 + i * .1
            al = vis(t, a0, T['about'], .2, .3)
            if al > 0:
                sc = e_back((t - a0) / .4, 2.0)

                def fn(d, P, s, x=x, y=y, sc=sc, hot=(nm == 'MAZAMA')):
                    r = 21 * sc
                    d.polygon([P(x, y - r * 1.25), P(x + r, y + r * .6), P(x - r, y + r * .6)],
                              fill=col(LIME if hot else WHITE), outline=col(OUTLINE), width=int(3 * s))
                vec(m, (x - 30, y - 30, x + 30, y + 30), fn, al, base=WHITE)
        cr = S(self.geo(-120.6, 45.9))
        label(m, 'CASCADE RANGE', cr[0] + 30, cr[1], t, T['cascade'] + .2, T['about'], 30, WHITE, anchor='l', rise=8)
        lx, ly = S(self.geo(-122.11, 42.94))
        label(m, 'CRATER LAKE', lx + 34, ly + 4, t, T['cascade'] + .8, T['about'], 28, LIME, anchor='l', rise=6)
        og = S(self.geo(-119.9, 43.6))
        chip(m, 'OREGON', og[0], og[1], t, T['oregon'], T['about'], size=36, accent=LIME)
        # ending
        pin(m, cx, cy, t, self.back + .2, None, LIME, 14, rings=False)
        chip(m, 'CRATER LAKE', cx, cy - 170, t, self.back + .3, None, size=40, sub='OREGON')
        label(m, 'BLUE', cx + 50, cy + 70, t, T['bluest'], None, 34, (120, 180, 255), anchor='l', rise=6)
        return m

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_section_bg())
            self.section(cv, t, clamp(u * 1.5))
            label(cv, 'MOUNT MAZAMA → CRATER LAKE', 540, 280, t, 0, None, 28, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area ------------------------------------------------------------
        hero(cv, 'DEEPEST LAKE', 540, 1280, t, T['america'] - .3, T['crater'] - .2, 100, LIME)
        label(cv, 'IN THE UNITED STATES', 540, 1385, t, T['america'] - .1, T['crater'] - .2, 30, WHITE)
        chip(cv, 'CRATER LAKE NATIONAL PARK', 540, 1270, t, T['crater'] + .2, T['about'] - .3, size=36, accent=LIME,
             sub='SOUTHERN OREGON')
        hero(cv, '≈7,700', 540, 1280, t, T['seventy'], T['mount'] - .1, 130, LIME)
        label(cv, 'YEARS AGO', 540, 1390, t, T['seventy'] + .2, T['mount'] - .1, 30, WHITE)
        chip(cv, 'MOUNT MAZAMA', 540, 1270, t, T['mount'], T['blasted'] - .1, size=44, accent=WHITE, sub='A CASCADE VOLCANO')
        chip(cv, 'HUGE ERUPTION', 540, 1270, t, T['blasted'], T['ash'] - .1, size=44, accent=ORANGE)
        chip(cv, 'ASH + MAGMA BLASTED OUT', 540, 1270, t, T['ash'], T['fell'] - .1, size=38, accent=ORANGE)
        chip(cv, 'THE SUMMIT COLLAPSED', 540, 1270, t, T['fell'], T['caldera'] - .1, size=40, accent=ORANGE)
        chip(cv, 'CALDERA', 540, 1270, t, T['caldera'], T['rain'] - .1, size=48, accent=LIME, sub='A COLLAPSED VOLCANIC BOWL')
        chip(cv, 'FILLED BY RAIN + SNOW', 540, 1270, t, T['rain'], T['no'] - .1, size=40, accent=TEAL, sub='OVER CENTURIES')
        chip(cv, 'NO RIVERS IN · NONE OUT', 540, 1270, t, T['no'], T['nineteen'] - .1, size=38, accent=TEAL)
        hero(cv, '1,943 FT', 540, 1280, t, T['nineteen'], T['deepest2'] - .1, 130, LIME)
        label(cv, 'DEEP', 540, 1390, t, T['nineteen'] + .2, T['deepest2'] - .1, 30, WHITE)
        chip(cv, 'DEEPEST LAKE IN THE U.S.', 540, 1270, t, T['deepest2'], T['and_'] - .1, size=40, accent=LIME)
        chip(cv, 'FED ALMOST ONLY BY RAIN + SNOW', 540, 1270, t, T['water'], T['clearest'] - .1, size=34, accent=TEAL)
        chip(cv, 'ONE OF THE CLEAREST', 540, 1270, t, T['clearest'], None, size=40, accent=LIME, sub='LAKES ON EARTH')
        label(cv, 'SOURCES: NPS · USGS', 540, 1595, t, self.back, None, 18, (200, 210, 215), rise=0)


@functools.lru_cache(None)
def _section_bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
