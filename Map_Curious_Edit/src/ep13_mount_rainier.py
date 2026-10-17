"""13 - The Volcano Seattle Can See (Mount Rainier, Washington).

Base map: the pack's NASA Blue Marble Pacific Northwest render (02_db_cooper bbox),
Washington outline from the pack's SVG.
Facts (USGS / NPS): Mount Rainier ~14,410 ft, ~60 mi SE of Seattle; most glaciated peak
in the contiguous U.S.; lahars (volcanic mudflows) are its main hazard; the Osceola
Mudflow ~5,600 years ago reached the Puget Sound lowlands (Enumclaw-Auburn-Kent);
valley towns sit on old lahar deposits; lahar warning sirens and evacuation routes in
the Puyallup and Carbon valleys; last eruption ~1,000 years ago.
Lahar paths follow the river valleys but are generalised.
"""
from episode import *

RAIN = (-121.760, 46.853)
SEA = (-122.332, 47.606)
AUB = (-122.228, 47.307)
TOWNS = [('ORTING', -122.204, 47.098), ('PUYALLUP', -122.293, 47.185), ('SUMNER', -122.240, 47.203),
         ('ENUMCLAW', -121.991, 47.204), ('KENT', -122.235, 47.381)]
SIRENS = [(-122.204, 47.098), (-122.293, 47.185), (-122.240, 47.203), (-122.15, 47.03), (-121.991, 47.204)]
VALLEYS = {
    'white': [RAIN, (-121.66, 46.95), (-121.72, 47.08), (-121.86, 47.16), (-121.99, 47.20), (-122.12, 47.25),
              AUB, (-122.235, 47.381)],
    'puyallup': [RAIN, (-121.86, 46.88), (-121.98, 46.94), (-122.10, 47.02), (-122.204, 47.098), (-122.293, 47.185),
                 (-122.42, 47.26)],
    'carbon': [RAIN, (-121.80, 46.95), (-121.95, 47.00), (-122.07, 47.04), (-122.204, 47.098)],
    'nisqually': [RAIN, (-121.80, 46.76), (-121.98, 46.74), (-122.20, 46.77), (-122.40, 46.88), (-122.56, 46.98),
                  (-122.70, 47.07)],
}
MUD = (150, 108, 66)
ICE = (215, 238, 255)
YEL = (255, 214, 90)


def miles(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


class EP(Episode):
    slug = '13_Mount_Rainier'
    gfx = '02_db_cooper'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '13_Mount_Rainier_Final.mp4'
    title = 'The Volcano Seattle Can See'
    cover_title = 'THE VOLCANO\nSEATTLE\nCAN SEE'
    cover_t = 3.4
    emphasis = ['dangerous', 'volcanoes', 'Rainier', 'fourteen', 'thousand', 'sixty', 'glacier', 'forty-eight', 'danger.',
                'mudflows', 'lahars.', 'fifty-six', 'Puget', 'Sound', 'Auburn', 'sirens', 'evacuation', 'erupted']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        self.wa = Region(svg_polys(self.G / 'region_highlight.svg'))
        g = self.geo
        self.R, self.SEA, self.AUB = g(*RAIN), g(*SEA), g(*AUB)
        self.vals = {k: spline([g(*p) for p in v], 8) for k, v in VALLEYS.items()}
        self.d_sea = miles(RAIN, SEA)
        T = self.T = dict(
            seattle=w('Seattle'), dangerous=w('dangerous'), volcanoes=w('volcanoes'), downtown=w('downtown'),
            mount=w('Mount'), fourteen=w('fourteen'), roughly=w('roughly'), sixty=w('sixty'), southeast=w('southeast'),
            it=w('It'), glacier=w('glacier'), other=w('other'), lower=w('lower'), that=w('That'), danger=w('danger'),
            if_=w('If'), heats=w('heats'), melting=w('melting'), mix=w('mix'), rock=w('rock'), creating=w('creating'),
            mudflows=w('mudflows'), lahars=w('lahars'), about2=w('About'), fifty=w('fifty-six'), flows=w('flows'),
            puget=w('Puget'), auburn=w('Auburn'), many=w('Many'), deposits=w('deposits'), so=w('so'),
            sirens=w('sirens'), marked=w('marked'), evac=w('evacuation'), and_=w('And'), rainier2=w('Rainier', 2),
            erupted=w('erupted'), thousand2=w('thousand', 2))
        mid = ((self.R[0] + self.SEA[0]) / 2, (self.R[1] + self.SEA[1]) / 2)
        wa_c = g(-120.6, 47.3)
        val_c = g(-122.08, 47.08)
        self.cam = Cam([
            frame_on(mid, 540, 600, 3.0, 0), frame_on(mid, 540, 600, 3.3, T['downtown']),
            frame_on(self.R, 540, 640, 3.4, T['mount'] + .2), frame_on(mid, 540, 600, 2.9, T['roughly'] + .2),
            frame_on(self.R, 540, 620, 3.3, T['glacier'] + .1), frame_on(wa_c, 540, 600, 1.25, T['lower'] + .3),
            frame_on(wa_c, 540, 600, 1.3, T['that'] - .2), frame_on(self.R, 540, 620, 3.4, T['danger'] + .2),
            frame_on(self.R, 560, 600, 3.3, T['creating'] - .3), frame_on(val_c, 540, 600, 3.2, T['mudflows'] + .4),
            frame_on(val_c, 540, 600, 3.0, T['puget'] + .2), frame_on(val_c, 540, 620, 3.3, T['so'] + .2),
            frame_on(self.R, 540, 640, 3.0, T['and_'] + .2), frame_on(self.R, 540, 640, 3.4, self.dur)])
        b = self.beat
        b(0.0, 'Seattle pin with Rainier on the map', 'pop', 2)
        b(.3, 'Volcano icon pops at Rainier', 'pop')
        b(T['dangerous'], 'Volcano pulses', 'tick')
        b(T['volcanoes'], 'DANGEROUS VOLCANO label pulses red', 'tick')
        b(T['downtown'], 'Sightline from downtown Seattle to the peak', 'swish')
        b(T['mount'], 'Camera pushes to the summit; MOUNT RAINIER chip', 'whoosh')
        b(T['fourteen'], 'Hero: 14,400 FT', 'thud')
        b(T['roughly'], 'Camera pulls back to Seattle', 'whoosh')
        b(T['sixty'], 'Distance line ≈60 MI', 'tick')
        b(T['southeast'], 'SOUTHEAST OF SEATTLE chip', 'tick')
        b(T['glacier'], 'Glacier ice spreads over the peak', 'swish')
        b(T['other'], 'MOST GLACIER ICE chip', 'pop')
        b(T['lower'], 'Pull back: Washington outlined, LOWER 48 chip', 'whoosh')
        b(T['that'], 'Ice glows', 'tick')
        b(T['danger'], 'Zoom in; DANGER stamp', 'thud', 2)
        b(T['heats'], 'Volcano heats up (orange glow)', 'rumble')
        b(T['melting'], 'Ice melts to blue water', 'swish')
        b(T['mix'], 'Water mixes with rock', 'tick')
        b(T['rock'], 'MELTWATER + ROCK chip', 'pop')
        b(T['creating'], 'Mudflows race down the valleys', 'rumble', 2)
        b(T['lahars'], 'LAHARS chip', 'pop')
        b(T['about2'], 'Hero: ≈5,600 YEARS AGO', 'thud')
        b(T['flows'], 'Osceola Mudflow traces down the White River', 'whoosh')
        b(T['puget'], 'PUGET SOUND label', 'tick')
        b(T['auburn'], 'AUBURN pin', 'pop')
        b(T['many'], 'Valley towns appear', 'tick')
        b(T['deposits'], 'Old lahar deposits shaded under towns', 'swish')
        b(T['sirens'], 'Warning sirens pulse', 'pop', 2)
        b(T['evac'], 'Evacuation arrows lead to high ground', 'swish')
        b(T['and_'], 'Back to the summit', 'whoosh')
        b(T['erupted'], 'Summit glows: last eruption', 'rumble')
        b(T['thousand2'], 'Hero: ≈1,000 YEARS AGO', 'thud')

    # -------------------------------------------------------------------------
    def volcano(self, cv, x, y, t, z):
        T = self.T
        al = vis(t, .3, None, .3)
        if al <= 0:
            return
        sc = (e_back((t - .3) / .45, 2.0) + .15 * vis(t, T['dangerous'], T['downtown'], .15, .4)) * min(1.25, max(.75, z / 3.0))
        ice = e_out((t - T['glacier']) / 1.2)
        melt = e_io((t - T['melting']) / 1.4) * (1 - vis(t, T['many'], None, .8))
        heat = max(vis(t, T['heats'] - .1, T['creating'] + 1.0, .4, .8),
                   vis(t, T['erupted'] - .1, None, .4) * (.7 + .3 * math.sin(t * 7) ** 2))
        r = 70 * sc

        def fn(d, P, s):
            if heat > 0:
                for k, a in ((2.0, .16), (1.4, .28)):
                    d.ellipse((*P(x - r * k, y - r * k * .8 - 20), *P(x + r * k, y + r * k * .8 - 20)), fill=col(ORANGE, a * heat))
            d.polygon([P(x - r, y + r * .35), P(x - r * .18, y - r * .9), P(x + r * .18, y - r * .9), P(x + r, y + r * .35)],
                      fill=col((104, 96, 90)), outline=col(OUTLINE), width=int(3 * s))
            cap = lerp(.32, .62, ice)
            cc = tuple(int(lerp(a, b, melt)) for a, b in zip(ICE, (60, 150, 235)))
            d.polygon([P(x - r * cap, y - r * .9 + r * 1.25 * cap), P(x - r * .18, y - r * .9), P(x + r * .18, y - r * .9),
                       P(x + r * cap, y - r * .9 + r * 1.25 * cap)], fill=col(cc), outline=col(WHITE, .8), width=int(2 * s))
            if heat > 0:
                d.ellipse((*P(x - 14, y - r * .9 - 10), *P(x + 14, y - r * .9 + 6)), fill=col((255, 120, 40), heat))
        vec(cv, (x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 1.2), fn, al, base=(104, 96, 90))

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        z = st[2]
        S = lambda p: Cam.S(st, *p)
        self.draw_map(cv, st)
        self.wa.draw(cv, st, t, T['lower'] - .1, T['danger'], fill_a=.22, alpha=.9)
        cv.alpha_composite(vignette())
        rx, ry = S(self.R)
        sx, sy = S(self.SEA)
        ax, ay = S(self.AUB)
        # old lahar deposits (wide translucent bands) -----------------------------
        da = vis(t, T['deposits'] - .1, T['and_'] + .5, .6, .6)
        if da > 0:
            for k in ('white', 'puyallup', 'carbon'):
                scr = [S(q) for q in self.vals[k]]
                route(cv, scr, 1, MUD, int(12 * z), head=False, alpha=.45 * da, outline=False, glow=False)
        # lahars racing down the valleys ----------------------------------------
        la = vis(t, T['creating'] - .1, T['many'], .2, .6)
        if la > 0:
            for i, k in enumerate(('puyallup', 'carbon', 'nisqually', 'white')):
                scr = [S(q) for q in self.vals[k]]
                p = e_out((t - T['creating'] - i * .12) / 2.0)
                route(cv, scr, p, MUD, 9, head=True, alpha=la * (1 - .6 * vis(t, T['flows'], None, .4) * (k != 'white')),
                      head_size=18)
        # Osceola mudflow highlight
        oa = vis(t, T['flows'] - .1, T['many'], .3, .5)
        if oa > 0:
            scr = [S(q) for q in self.vals['white']]
            route(cv, scr, e_io((t - T['flows'] + .1) / 2.0), ORANGE, 11, head=True, alpha=oa, head_size=22)
            mp = point_at(scr, .45)[0]
            label(cv, 'OSCEOLA MUDFLOW', mp[0] + 30, mp[1] - 10, t, T['flows'] + .4, T['many'], 26, ORANGE, anchor='l', rise=6)
        # sightline Seattle -> Rainier
        sa = vis(t, T['downtown'] - .1, T['glacier'] - .2, .3, .4)
        route(cv, [(sx, sy), (rx, ry - 30)], e_out((t - T['downtown'] + .1) / .7), WHITE, 5, head=True, alpha=sa,
              dashed=True, dash=(14, 9), head_size=18)
        label(cv, f'≈{round(self.d_sea / 5) * 5} MI', (sx + rx) / 2 + 26, (sy + ry) / 2 - 10, t, T['sixty'], T['glacier'] - .2,
              34, WHITE, anchor='l', rise=0)
        # towns, sirens, evacuation -----------------------------------------------
        for i, (nm, lon, lat) in enumerate(TOWNS):
            x, y = S(self.geo(lon, lat))
            a0 = T['many'] + .1 + i * .15
            pin(cv, x, y, t, a0, T['and_'], WHITE, 9, rings=False)
            left = nm in ('PUYALLUP', 'KENT')
            if nm != 'SUMNER':
                label(cv, nm, x + (-18 if left else 18), y + 2, t, a0 + .05, T['and_'], 24, WHITE, anchor='r' if left else 'l', rise=4)
        for i, (lon, lat) in enumerate(SIRENS):
            x, y = S(self.geo(lon, lat))
            a0 = T['sirens'] - .05 + i * .1
            sa = vis(t, a0, T['and_'], .2, .4)
            if sa > 0:
                def fn(d, P, s, x=x, y=y, a0=a0):
                    for k in (0, .5):
                        ph = ((t - a0) / 1.1 + k) % 1
                        rr = 12 + ph * 46
                        d.ellipse((*P(x - rr, y - rr), *P(x + rr, y + rr)), outline=col(RED, (1 - ph) * .9), width=int(4 * s))
                    d.rectangle((*P(x - 7, y - 26), *P(x + 7, y - 8)), fill=col(RED), outline=col(OUTLINE), width=int(2 * s))
                    d.polygon([P(x - 7, y - 26), P(x - 18, y - 33), P(x - 18, y - 1), P(x - 7, y - 8)], fill=col(YEL))
                vec(cv, (x - 70, y - 70, x + 70, y + 70), fn, sa, base=RED)
        if t >= T['evac'] - .1:
            ea = vis(t, T['evac'] - .1, T['and_'], .3, .4)
            ox, oy = S(self.geo(-122.204, 47.098))
            px_, py_ = S(self.geo(-122.293, 47.185))
            for (x0, y0), (dx, dy) in (((ox, oy), (-90, 40)), ((ox, oy), (80, -50)), ((px_, py_), (-90, 30))):
                route(cv, [(x0, y0), (x0 + dx * .5, y0 + dy * .4), (x0 + dx, y0 + dy)], e_out((t - T['evac']) / .7), LIME, 6,
                      head=True, alpha=ea, head_size=16)
        # labels and pins -----------------------------------------------------------
        pin(cv, sx, sy, t, -.12, None, TEAL, 15, rings=t < T['mount'])
        label(cv, 'SEATTLE', sx - 24, sy + 4, t, 0, None, 32, WHITE, anchor='r', rise=6)
        self.volcano(cv, rx, ry, t, z)
        label(cv, 'DANGEROUS VOLCANO', rx, ry + 80, t, T['volcanoes'], T['mount'] - .1, 30, RED, rise=8)
        chip(cv, 'MOUNT RAINIER', rx, ry - 170, t, T['mount'], T['roughly'] - .1, size=40, accent=LIME, sub='WASHINGTON')
        label(cv, 'MOUNT RAINIER', rx + 80, ry + 14, t, T['roughly'], T['lower'], 30, LIME, anchor='l', rise=6)
        label(cv, 'GLACIER ICE', rx, ry + 80, t, T['glacier'] + .2, T['lower'], 30, ICE, rise=6)
        stamp(cv, 'DANGER', rx, ry - 190, t, T['danger'], T['heats'] - .1, 70, RED)
        label(cv, 'MELTING ICE', rx + 90, ry - 40, t, T['melting'], T['creating'], 28, (120, 190, 255), anchor='l', rise=6)
        label(cv, '+ LOOSE ROCK', rx + 90, ry, t, T['rock'], T['creating'], 28, (210, 170, 120), anchor='l', rise=6)
        ps = S(self.geo(-122.62, 47.52))
        label(cv, 'PUGET SOUND', ps[0], ps[1], t, T['puget'], T['many'], 30, TEAL, anchor='r', rise=6)
        pin(cv, ax, ay, t, T['auburn'] - .05, T['many'], ORANGE, 12)
        label(cv, 'AUBURN', ax - 20, ay + 4, t, T['auburn'], T['many'], 30, WHITE, anchor='r', rise=6)
        # lower info area ------------------------------------------------------------
        chip(cv, 'ONE OF AMERICA\'S MOST', 540, 1270, t, T['dangerous'] - .2, T['mount'] - .1, size=40, accent=RED,
             sub='DANGEROUS VOLCANOES')
        hero(cv, '14,400 FT', 540, 1280, t, T['fourteen'], T['roughly'] - .1, 130, LIME)
        label(cv, 'TALL', 540, 1390, t, T['fourteen'] + .2, T['roughly'] - .1, 30, WHITE)
        chip(cv, '≈60 MI SOUTHEAST', 540, 1270, t, T['sixty'], T['glacier'] - .1, size=40, accent=WHITE, sub='OF DOWNTOWN SEATTLE')
        chip(cv, 'MOST GLACIER ICE', 540, 1270, t, T['glacier'], T['that'] - .1, size=42, accent=TEAL,
             sub='OF ANY PEAK IN THE LOWER 48')
        chip(cv, 'THE ICE IS THE DANGER', 540, 1270, t, T['that'], T['melting'] - .1, size=40, accent=RED)
        chip(cv, 'MELTWATER + ROCK', 540, 1270, t, T['melting'], T['lahars'] - .1, size=42, accent=ORANGE, sub='= MUDFLOW')
        chip(cv, 'LAHARS', 540, 1270, t, T['lahars'], T['about2'] - .1, size=56, accent=ORANGE, sub='VOLCANIC MUDFLOWS')
        hero(cv, '≈5,600', 540, 1280, t, T['about2'], T['flows'] + .3, 130, ORANGE)
        label(cv, 'YEARS AGO', 540, 1390, t, T['about2'] + .2, T['flows'] + .3, 30, WHITE)
        chip(cv, 'REACHED PUGET SOUND', 540, 1270, t, T['flows'] + .4, T['many'] - .1, size=40, accent=ORANGE,
             sub='OSCEOLA MUDFLOW')
        chip(cv, 'TOWNS ON OLD LAHAR DEPOSITS', 540, 1270, t, T['many'], T['sirens'] - .1, size=34, accent=ORANGE)
        chip(cv, 'WARNING SIRENS', 540, 1270, t, T['sirens'], T['and_'] - .1, size=42, accent=RED, sub='+ EVACUATION ROUTES')
        hero(cv, '≈1,000', 540, 1280, t, T['thousand2'] - .3, None, 130, ORANGE)
        label(cv, 'YEARS SINCE THE LAST ERUPTION', 540, 1390, t, T['thousand2'] - .1, None, 28, WHITE)
        label(cv, 'SOURCES: USGS · NPS', 540, 1595, t, T['and_'], None, 18, (200, 210, 215), rise=0)
