"""12 - The River That Flows Both Ways (Hudson River, New York).

Base map: the pack's NASA Blue Marble Northeast US render (03_centralia bbox).
Facts (NOAA / USGS / NYS DEC Hudson River Estuary Program): the Hudson rises in the
Adirondacks (Lake Tear of the Clouds) and reaches New York Harbor; its lower ~153 mi,
from the Federal Dam at Troy to the Battery, is a tidal estuary with tides twice a day
that reverse the current; in dry periods the salt front can move ~60 mi upriver (to about
Newburgh); a Native (Mohican/Lenape) name is commonly translated "the river that flows
both ways". River line is generalised; distances computed great-circle in code.
"""
from episode import *
from engine import _head

UPPER = [(-73.94, 44.10), (-74.02, 43.85), (-73.98, 43.60), (-73.80, 43.40), (-73.64, 43.31), (-73.58, 43.25),
         (-73.62, 43.00), (-73.68, 42.80), (-73.686, 42.752)]
LOWER = [(-73.686, 42.752), (-73.75, 42.65), (-73.79, 42.25), (-73.97, 41.93), (-73.94, 41.70), (-74.00, 41.50),
         (-73.96, 41.39), (-73.89, 41.07), (-73.93, 40.85), (-74.02, 40.70), (-74.04, 40.60)]
TROY, ALB, NYC, NEWB = (-73.686, 42.752), (-73.756, 42.653), (-74.006, 40.713), (-74.01, 41.50)
SRC = (-73.94, 44.10)
SALT = (255, 170, 80)
TIDE = (90, 190, 255)
YEL = (255, 214, 90)


def miles(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


class EP(Episode):
    slug = '12_Hudson_River'
    gfx = '03_centralia'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '12_Hudson_River_Final.mp4'
    title = 'The River That Flows Both Ways'
    cover_title = 'THE RIVER THAT\nFLOWS\nBOTH WAYS'
    cover_t = 18.6
    emphasis = ['two', 'directions.', 'Hudson', 'Adirondack', 'estuary,', 'sea.', 'Twice', 'tides', 'reverse', 'hundred',
                'fifty', 'Troy,', 'Albany.', 'salty', 'sixty', 'Native', 'both', 'ways."']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        g = self.geo
        self.upper = spline([g(*p) for p in UPPER], 10)
        self.lower = spline([g(*p) for p in LOWER], 12)
        self.river = self.upper + self.lower[1:]
        # salt front: fraction of the harbor->Troy path that lies within ~60 mi of the Battery
        geo_rev = LOWER[::-1]
        d = [0.0]
        for a, b in zip(geo_rev, geo_rev[1:]):
            d.append(d[-1] + miles(a, b))
        self.tidal_mi = d[-1]
        self.salt_frac = 0.0
        for i in range(1, len(d)):
            if d[i] >= 60:
                self.salt_frac = (i - 1 + (60 - d[i - 1]) / (d[i] - d[i - 1])) / (len(d) - 1)
                break
        self.TROY, self.ALB, self.NYC, self.NEWB, self.SRC = g(*TROY), g(*ALB), g(*NYC), g(*NEWB), g(*SRC)
        T = self.T = dict(
            flows1=w('flows', 1), two=w('two'), hudson=w('Hudson'), adirondack=w('Adirondack'), city=w('City'),
            but=w('But'), lower=w('lower'), estuary=w('estuary'), arm=w('arm'), sea=w('sea'), twice=w('Twice'),
            tides=w('tides'), harbor=w('Harbor'), reverse=w('reverse'), that=w('That'), hundred=w('hundred'),
            upstream=w('upstream'), troy=w('Troy'), albany=w('Albany'), dry=w('dry'), salty=w('salty'),
            sixty=w('sixty'), native=w('Native', 1), europeans=w('Europeans'), one=w('One'), translated=w('translated'),
            flows2=w('flows', 2), both=w('both'))
        tidal = g(-73.9, 41.73)
        whole = g(-73.85, 42.4)
        south = g(-73.98, 41.35)
        self.cam = Cam([
            frame_on(tidal, 540, 590, 2.3, 0), frame_on(tidal, 540, 590, 2.2, T['hudson']),
            frame_on(whole, 540, 590, 1.4, T['adirondack'] + .4), frame_on(whole, 540, 590, 1.4, T['city'] + .3),
            frame_on(tidal, 540, 590, 2.3, T['lower'] + .5), frame_on(south, 540, 600, 2.6, T['tides']),
            frame_on(south, 540, 600, 2.5, T['reverse'] + .6), frame_on(tidal, 540, 590, 2.3, T['hundred'] + .3),
            frame_on(self.TROY, 540, 520, 3.2, T['troy'] + .3), frame_on(self.TROY, 540, 520, 3.1, T['albany'] + .6),
            frame_on(south, 540, 600, 2.6, T['salty'] + .2), frame_on(south, 540, 600, 2.5, T['sixty'] + .8),
            frame_on(tidal, 540, 590, 2.2, T['native'] + .6), frame_on(tidal, 540, 590, 2.35, self.dur)])
        b = self.beat
        b(0.0, 'Hudson drawn on the map, flow arrows', 'whoosh', 2)
        b(T['two'], 'Arrows run both ways: TWO DIRECTIONS', 'pop')
        b(T['hudson'], 'HUDSON RIVER chip', 'pop')
        b(T['adirondack'], 'Camera pulls out; ADIRONDACKS source pin', 'whoosh')
        b(T['city'], 'NEW YORK CITY pin', 'pop')
        b(T['lower'], 'Lower half highlighted', 'swish')
        b(T['estuary'], 'ESTUARY chip', 'pop')
        b(T['sea'], 'Ocean pulse at the harbor', 'tick')
        b(T['twice'], '2× A DAY', 'thud')
        b(T['tides'], 'Tide pulses push up the river', 'whoosh')
        b(T['reverse'], 'Current arrows flip upstream', 'swish', 2)
        b(T['hundred'], 'Tidal reach bracket: ≈150 MILES', 'thud')
        b(T['troy'], 'TROY · FEDERAL DAM pin', 'pop')
        b(T['albany'], 'ALBANY pin', 'tick')
        b(T['dry'], 'Dry summer: camera to the lower river', 'whoosh')
        b(T['salty'], 'Salt water creeps upriver', 'swish')
        b(T['sixty'], '≈60 MILES salt front', 'thud')
        b(T['native'], 'NATIVE PEOPLES KNEW chip', 'tick')
        b(T['one'], 'Quote card builds', 'pop')
        b(T['flows2'], 'Arrows run both ways again', 'swish')

    # -------------------------------------------------------------------------
    def chevrons(self, cv, pts, t, al, upstream, color, n=9, speed=.12, size=15):
        if al <= 0:
            return
        heads = []
        for k in range(n):
            f = (k / n + (t * speed) * (-1 if upstream else 1)) % 1.0
            (x, y), ang = point_at(pts, max(f, .01))
            heads.append((x, y, ang + (math.pi if upstream else 0)))

        def fn(d, P, s):
            for x, y, a in heads:
                _head(d, P, s, (x, y), a, size + 4, col(OUTLINE, .6))
                _head(d, P, s, (x, y), a, size, col(color))
        vec(cv, bbox_of(pts, 40), fn, al, base=color)

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        S = lambda p: Cam.S(st, *p)
        self.draw_map(cv, st)
        cv.alpha_composite(vignette())
        riv = [S(q) for q in self.river]
        low = [S(q) for q in self.lower]
        rev = low[::-1]
        # base river
        route(cv, riv, e_io(t / 1.6), (110, 170, 230), 8, head=False)
        # lower (tidal) half highlight
        route(cv, low, e_io((t - T['lower']) / 1.0), TEAL, 12, head=False, alpha=vis(t, T['lower'], T['dry'], .3, .5))
        # tide pulses from the harbor
        if T['tides'] - .1 <= t < T['hundred']:
            for k in range(3):
                ph = ((t - T['tides']) / 1.6 + k / 3) % 1
                p0 = max(0.0, ph - .12)
                route(cv, rev, ph, TIDE, 16, head=False, p0=p0, alpha=vis(t, T['tides'] - .1, T['hundred'], .3, .4) * (1 - ph * .5), outline=False)
        # flow arrows: downstream / upstream
        down = max(vis(t, .3, T['two'] + .9, .3, .3), vis(t, T['lower'] + .4, T['reverse'] - .1, .3, .3),
                   vis(t, T['flows2'] - .2, None, .3) * .9)
        up = max(vis(t, T['two'] + .3, T['hudson'] + 1.0, .3, .3), vis(t, T['reverse'], T['hundred'], .3, .4),
                 vis(t, T['both'] - .1, None, .3) * .9)
        self.chevrons(cv, low, t, down, False, WHITE)
        self.chevrons(cv, low, t + .37, up, True, TIDE)
        # salt front
        if t >= T['salty'] - .1:
            sp = self.salt_frac * e_io((t - T['salty']) / 2.0)
            route(cv, rev, sp, SALT, 18, head=True, alpha=vis(t, T['salty'] - .1, T['native'] + .4, .3, .5), head_size=34)
            nx, ny = S(self.NEWB)
            label(cv, '≈60 MI', nx + 40, ny, t, T['sixty'], T['native'] + .4, 34, SALT, anchor='l', rise=6)
            label(cv, 'SALT WATER', nx + 40, ny + 44, t, T['sixty'] + .2, T['native'] + .4, 26, WHITE, anchor='l', rise=6)
        # tidal reach bracket
        ba = vis(t, T['hundred'] - .1, T['dry'], .3, .4)
        if ba > 0:
            tx, ty = S(self.TROY); hx, hy = S(self.NYC)
            bx = max(tx, hx) + 120
            route(cv, [(bx, hy), (bx, ty)], e_out((t - T['hundred']) / .7), LIME, 6, head=True, alpha=ba, head_size=20)
            route(cv, [(bx, ty), (bx, hy)], e_out((t - T['hundred']) / .7), LIME, 6, head=True, alpha=ba, head_size=20)
            label(cv, '≈150 MI', min(bx + 20, 900), (ty + hy) / 2, t, T['hundred'] + .3, T['dry'], 34, LIME, anchor='l', rise=0)
        # pins / labels
        sx, sy = S(self.SRC)
        pin(cv, sx, sy, t, T['adirondack'], T['lower'] + .3, WHITE, 12, rings=False)
        label(cv, 'ADIRONDACKS', sx + 26, sy, t, T['adirondack'] + .05, T['lower'] + .3, 28, WHITE, anchor='l', rise=6)
        cx, cy = S(self.NYC)
        pin(cv, cx, cy, t, -.1, None, LIME, 14)
        label(cv, 'NEW YORK CITY', cx - 26, cy + 4, t, T['city'] - .4, None, 28, WHITE, anchor='r', rise=6)
        hb = vis(t, T['sea'] - .1, T['twice'] + 1.2, .3, .5)
        if hb > 0:
            for k in range(3):
                ph = ((t - T['sea']) / 1.2 + k / 3) % 1
                ring(cv, cx + 10, cy + 40, 30 + ph * 110, t, T['sea'] - .1, T['twice'] + 1.2, TIDE, 5, alpha=1 - ph)
        label(cv, 'ATLANTIC', cx + 60, cy + 120, t, T['sea'], T['reverse'], 28, TIDE, anchor='l', rise=6)
        tx, ty = S(self.TROY); ax, ay = S(self.ALB)
        pin(cv, tx, ty, t, T['troy'] - .05, T['native'], YEL, 13, rings=False)
        label(cv, 'TROY · FEDERAL DAM', tx + 26, ty - 6, t, T['troy'], T['native'], 28, YEL, anchor='l', rise=6)
        pin(cv, ax, ay, t, T['albany'] - .05, T['native'], WHITE, 11, rings=False)
        label(cv, 'ALBANY', ax - 24, ay + 6, t, T['albany'], T['native'], 28, WHITE, anchor='r', rise=6)
        hl = S(self.geo(-74.35, 41.95))
        label(cv, 'HUDSON RIVER', hl[0] - 10, hl[1], t, T['hudson'] + .2, T['lower'], 30, (170, 210, 255), anchor='r', rise=6)
        # lower info area ------------------------------------------------------------
        hero(cv, 'FLOWS BOTH WAYS', 540, 1280, t, T['two'] - .2, T['hudson'] - .1, 92, LIME)
        chip(cv, 'THE HUDSON RIVER', 540, 1270, t, T['hudson'], T['lower'] - .1, size=46, accent=LIME, sub='NEW YORK')
        chip(cv, 'ESTUARY', 540, 1270, t, T['estuary'], T['twice'] - .1, size=50, accent=TEAL, sub='AN ARM OF THE SEA')
        hero(cv, '2× A DAY', 540, 1280, t, T['twice'], T['reverse'] - .1, 120, TIDE)
        label(cv, 'OCEAN TIDES PUSH IN', 540, 1385, t, T['twice'] + .2, T['reverse'] - .1, 30, WHITE)
        chip(cv, 'THE CURRENT REVERSES', 540, 1270, t, T['reverse'], T['hundred'] - .1, size=42, accent=TIDE)
        hero(cv, '≈150 MILES', 540, 1280, t, T['hundred'], T['dry'] - .1, 120, LIME)
        label(cv, 'OF TIDAL RIVER', 540, 1385, t, T['hundred'] + .2, T['dry'] - .1, 30, WHITE)
        chip(cv, 'IN DRY SUMMERS', 540, 1270, t, T['dry'], T['sixty'] - .1, size=42, accent=SALT)
        hero(cv, '≈60 MILES', 540, 1280, t, T['sixty'], T['native'] - .1, 120, SALT)
        label(cv, 'SALT WATER UPRIVER', 540, 1385, t, T['sixty'] + .2, T['native'] - .1, 30, WHITE)
        chip(cv, 'NATIVE PEOPLES KNEW', 540, 1270, t, T['native'], T['one'] - .1, size=42, accent=WHITE,
             sub='LONG BEFORE EUROPEANS')
        hero(cv, '"THE RIVER THAT', 540, 1255, t, T['translated'], None, 70, WHITE, pop=False)
        hero(cv, 'FLOWS BOTH WAYS"', 540, 1340, t, T['flows2'] - .1, None, 70, LIME)
        label(cv, 'SOURCES: NOAA · USGS · NYS DEC', 540, 1595, t, T['native'], None, 18, (200, 210, 215), rise=0)
