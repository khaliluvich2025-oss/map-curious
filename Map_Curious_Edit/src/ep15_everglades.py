"""15 - The River of Grass (Everglades, Florida).

Base map: the pack's NASA Blue Marble Florida/Cuba render (01_fort_jefferson bbox).
Facts: Everglades sheet flow runs south from Lake Okeechobee toward Florida Bay in a shallow
sheet up to ~60 mi wide (NPS/USGS); Marjory Stoneman Douglas, "The Everglades: River of Grass"
(1947); Everglades National Park dedicated Dec 1947 (NPS); drainage by canals, agriculture and
urban growth has left about half of the original Everglades (USGS/SFWMD); CERP is one of the
world's largest ecosystem restoration efforts (SFWMD/USACE).
Flow band, canal lines, EAA and urban strip are generalised schematics, not surveyed boundaries.
"""
from episode import *

LAKE = (-80.83, 26.95)
BAY = (-80.75, 25.05)
EVG = (-80.78, 25.95)
CITIES = [('W. PALM BEACH', (-80.05, 26.71)), ('FT. LAUDERDALE', (-80.14, 26.12)), ('MIAMI', (-80.19, 25.76))]
CANALS = [
    [(-80.62, 26.98), (-80.40, 27.08), (-80.20, 27.17)],                       # St. Lucie
    [(-80.62, 26.80), (-80.35, 26.75), (-80.05, 26.70)],                       # West Palm Beach canal
    [(-80.66, 26.69), (-80.45, 26.48), (-80.30, 26.36), (-80.10, 26.32)],      # Hillsboro
    [(-80.72, 26.69), (-80.58, 26.40), (-80.38, 26.14), (-80.15, 26.11)],      # North New River
    [(-80.90, 26.69), (-80.78, 26.30), (-80.52, 25.95), (-80.25, 25.80)],      # Miami Canal
    [(-81.05, 26.83), (-81.45, 26.70), (-81.85, 26.55)],                       # Caloosahatchee
    [(-80.30, 25.76), (-80.85, 25.76), (-81.20, 25.88), (-81.72, 26.12)],      # Tamiami Trail
]
EAA = [(-81.00, 26.70), (-80.62, 26.70), (-80.48, 26.52), (-80.52, 26.34), (-80.96, 26.32), (-81.06, 26.50)]
URBAN = [(-80.02, 26.80), (-80.06, 26.40), (-80.10, 26.05), (-80.15, 25.75), (-80.30, 25.50),
         (-80.50, 25.50), (-80.40, 25.75), (-80.30, 26.05), (-80.24, 26.40), (-80.20, 26.80)]
ENP = [(-81.30, 25.82), (-80.85, 25.76), (-80.55, 25.72), (-80.50, 25.50), (-80.45, 25.25), (-80.60, 25.08),
       (-80.95, 25.10), (-81.12, 25.20), (-81.22, 25.45), (-81.32, 25.65)]
GRASS = (204, 184, 102)
BROWN = (150, 118, 72)
GRAY = (165, 168, 172)
BLUE = (90, 190, 235)


def miles(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def band_geo(u, v):
    """Generalised sheet-flow band: u 0 (lake south shore) -> 1 (Florida Bay), v -1 (west) .. +1 (east)."""
    lat = 26.68 - u * 1.55
    c = -80.83 + .05 * math.sin(math.pi * u) + .05 * clamp((u - .6) / .4)
    sm = clamp(u / .35); sm = sm * sm * (3 - 2 * sm)
    hw = .20 + .28 * sm - .15 * clamp((u - .55) / .45)
    return (c + v * hw, lat)


class EP(Episode):
    slug = '15_Everglades'
    gfx = '01_fort_jefferson'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '15_Everglades_Final.mp4'
    title = 'The River of Grass'
    cover_title = "IT'S NOT\nA SWAMP.\nIT'S A RIVER"
    cover_t = 3.9
    emphasis = ['Everglades', 'swamp.', 'river.', 'Okeechobee', 'sixty', 'miles', 'Florida', 'Bay', 'slowly',
                'sawgrass.', 'Marjory', 'Stoneman', 'Douglas', 'River', 'Grass', '1947,', 'National', 'Park',
                'canals,', 'farms', 'cities', 'drained', 'half', 'restoration', 'world', 'south']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        self.florida = Region(svg_polys(self.G / 'region_highlight.svg'))
        g = self.geo
        self.LK, self.BY, self.EV = g(*LAKE), g(*BAY), g(*EVG)
        self.band = lambda u, v: g(*band_geo(u, v))
        self.canals = [spline([g(*p) for p in c], 8) for c in CANALS]
        self.eaa = [g(*p) for p in EAA]
        self.urban = [g(*p) for p in URBAN]
        self.enp = [g(*p) for p in ENP]
        self.cities = [(n, g(*p)) for n, p in CITIES]
        u60 = (26.68 - 26.0) / 1.55
        self.u60 = u60
        self.w60 = miles(band_geo(u60, -1), band_geo(u60, 1))
        rng = np.random.default_rng(15)
        self.parts = [(rng.uniform(-.95, .95), rng.uniform(0, 1), rng.uniform(.8, 1.2)) for _ in range(240)]
        self.blades = [(rng.uniform(.03, .99), rng.uniform(-.95, .95), rng.uniform(-.5, .5), rng.uniform(.7, 1.3))
                       for _ in range(520)]
        T = self.T = dict(
            evg1=w('Everglades', 1), swamp=w('swamp'), river=w('river', 1), water=w('Water', 1), spills=w('spills'),
            south=w('south', 1), lake=w('Lake'), okee=w('Okeechobee'), spreads=w('spreads'), shallow=w('shallow'),
            sheet=w('sheet'), sixty=w('sixty'), creeps=w('creeps'), florida=w('Florida'), bay=w('Bay'),
            slowly=w('slowly'), barely=w('barely'), move=w('move'), flowing=w('flowing'), tall=w('tall'), sawgrass=w('sawgrass'),
            writer=w('writer'), marjory=w('Marjory'), called=w('called'), riv=w('River'), grass=w('Grass'),
            y1947=w('1947'), same=w('same'), evg2=w('Everglades', 2), park=w('Park'), but=w('But'),
            canals=w('canals'), farms=w('farms'), cities=w('cities'), drained=w('drained'), today=w('Today'),
            half=w('half'), original=w('original'), now=w('Now'), restoration=w('restoration'), world=w('world'),
            send=w('send'), south2=w('south', 2))
        mid = ((self.LK[0] + self.BY[0]) / 2, (self.LK[1] + self.BY[1]) / 2)
        self.mid = mid
        self.cam = Cam([
            frame_on(self.EV, 540, 560, 2.3, 0), frame_on(self.EV, 540, 560, 2.5, T['swamp']),
            frame_on(mid, 540, 560, 3.1, T['water']), frame_on(mid, 540, 560, 3.2, T['sixty']),
            frame_on(self.BY, 540, 760, 3.4, T['bay'] + .4), frame_on(self.BY, 540, 740, 3.3, T['flowing']),
            frame_on(mid, 540, 560, 3.2, T['marjory']), frame_on(mid, 540, 560, 3.0, T['evg2']),
            frame_on(mid, 400, 560, 3.1, T['canals']), frame_on(mid, 390, 560, 3.0, T['drained'] + .5),
            frame_on(mid, 390, 560, 3.0, T['now']), frame_on(mid, 520, 560, 3.1, T['restoration']), frame_on(mid, 540, 560, 3.2, self.dur)])
        b = self.beat
        b(0.0, 'South Florida from above, EVERGLADES pin + label', 'whoosh', 2)
        b(T['swamp'], 'SWAMP? stamp', 'thud')
        b(T['river'], "IT'S A RIVER - flow line traces south", 'swish')
        b(T['water'], 'Lake Okeechobee lights up', 'pop')
        b(T['south'], 'Big arrow pushes south from the lake', 'swish')
        b(T['okee'], 'LAKE OKEECHOBEE label', 'tick')
        b(T['spreads'], 'Water sheet spreads south across the peninsula', 'whoosh')
        b(T['sheet'], 'Flow particles drift in the sheet', 'tick')
        b(T['sixty'], 'Width bracket + ~60 MILES WIDE', 'thud')
        b(T['creeps'], 'Camera creeps toward Florida Bay', 'swish')
        b(T['bay'], 'FLORIDA BAY pin', 'pop')
        b(T['slowly'], 'SLOW, SHALLOW SHEET chip', 'tick')
        b(T['barely'], 'BARELY MOVING magnifier ring on the flow', 'tick')
        b(T['flowing'], 'Sawgrass blades sprout across the band', 'swish')
        b(T['sawgrass'], 'SAWGRASS chip', 'pop')
        b(T['marjory'], 'MARJORY STONEMAN DOUGLAS chip', 'pop')
        b(T['riv'], 'RIVER OF GRASS hero', 'thud')
        b(T['riv'] + .3, 'Band outline glows lime', None)
        b(T['y1947'], '1947', 'thud')
        b(T['evg2'], 'Everglades National Park outline draws', 'swish')
        b(T['park'], 'EVERGLADES NATIONAL PARK chip', 'pop')
        b(T['canals'], 'Gray canals cut across the flow', 'swish')
        b(T['farms'], 'Agricultural area fills south of the lake', 'tick')
        b(T['cities'], 'Coastal cities spread + city pins', 'pop')
        b(T['drained'], 'Flow drains away, band dries brown', 'rumble')
        b(T['today'], 'Original extent dashed outline', 'tick')
        b(T['half'], '~HALF ITS ORIGINAL SIZE hero', 'thud')
        b(T['now'], 'Camera resets on the whole system', 'whoosh')
        b(T['restoration'], 'RESTORATION chip + ring on the farm area south of the lake', 'pop')
        b(T['world'], 'ONE OF THE WORLD\'S LARGEST sub-line', 'tick')
        b(T['send'], 'Water flows south again through the band', 'swish')
        b(T['south2'], 'Arrows reach Florida Bay', 'pop')

    # -------------------------------------------------------------------------
    def band_poly(self, S, u0, u1, v0=-1, v1=1, n=26):
        us = [u0 + (u1 - u0) * k / n for k in range(n + 1)]
        return [S(self.band(u, v0)) for u in us] + [S(self.band(u, v1)) for u in reversed(us)]

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        S = lambda p: Cam.S(st, *p)
        self.draw_map(cv, st)
        self.florida.draw(cv, st, t, -1, T['spreads'], fill_a=.10, alpha=.55)
        cv.alpha_composite(vignette())

        drain = vis(t, T['drained'], T['send'], .9, 1.2)          # 0 healthy .. 1 drained
        reveal = e_io((t - T['spreads']) / (T['bay'] - T['spreads']))
        # --- water sheet -------------------------------------------------------
        if reveal > 0:
            full = self.band_poly(S, 0, max(.02, reveal))
            cur = self.band_poly(S, .25, max(.26, reveal), -1, .35)

            def fn(d, P, s):
                if drain < 1:
                    d.polygon([P(*q) for q in full], fill=col(TEAL, .30 * (1 - drain)))
                if drain > 0:
                    d.polygon([P(*q) for q in full], fill=col(BROWN, .34 * drain))
                    d.polygon([P(*q) for q in cur], fill=col(TEAL, .30 * drain))
            vec(cv, bbox_of(full, 10), fn, vis(t, T['spreads'], None, .5), ss=2, base=TEAL)
        # --- sawgrass blades ----------------------------------------------------
        ga = vis(t, T['flowing'], None, .6)
        if ga > 0:
            z = st[2]
            grow = e_out((t - T['flowing']) / 1.2)

            def fn(d, P, s):
                for u, v, lean, k in self.blades:
                    gone = (u < .25 or v > .35)
                    a = .75 * (1 - drain * (.85 if gone else .25))
                    if a <= .02 or k * 1.4 - .4 > grow * 1.4 + .2:
                        continue
                    x, y = S(self.band(u, v))
                    L = (7 + 6 * k) * z / 3.2 * grow
                    c = BROWN if (gone and drain > .5) else GRASS
                    d.line([P(x, y), P(x + lean * L * .5, y - L)], fill=col(c, a), width=max(1, int(2.2 * s)))
            pts = self.band_poly(S, 0, 1)
            vec(cv, bbox_of(pts, 30), fn, ga, ss=2, base=GRASS)
        # --- flow particles -----------------------------------------------------
        pa = vis(t, T['sheet'] - .3, None, .5)
        if pa > 0:

            def fn(d, P, s):
                for v, ph, sp in self.parts:
                    u = (ph + t * .045 * sp) % 1.0
                    if u > reveal:
                        continue
                    gone = (u < .25 or v > .35)
                    a = min(1, u / .05, (1 - u) / .06) * .85
                    a *= 1 - drain * (1 if gone else .6)
                    if a <= .02:
                        continue
                    x, y = S(self.band(u, v))
                    r = 3.2 * s
                    px, py = P(x, y)
                    d.ellipse((px - r, py - r, px + r, py + r), fill=col(BLUE, a))
            pts = self.band_poly(S, 0, 1)
            vec(cv, bbox_of(pts, 20), fn, pa, ss=2, base=BLUE)
        # --- big 'it's a river' / 'south' arrow ---------------------------------
        trace = [S(self.band(u, 0)) for u in [k / 20 for k in range(21)]]
        lk = S(self.LK)
        route(cv, [(lk[0], lk[1] + 20)] + trace[1:], e_io((t - T['river']) / 1.6), TEAL, 12,
              alpha=vis(t, T['river'], T['spreads'] + .6, .3, .6), head_size=40)
        # restoration arrows (lime) south again
        if t >= T['send'] - .2:
            for k, v in enumerate((-.55, 0, .55)):
                pts = [S(self.band(u, v)) for u in [j / 16 for j in range(17)]]
                route(cv, [(lk[0] + v * 40, lk[1] + 10)] + pts[1:], e_io((t - T['send'] - k * .15) / 1.4), LIME, 9,
                      alpha=vis(t, T['send'] - .1, None, .3), head_size=30)
        # --- national park ------------------------------------------------------
        enp = [S(q) for q in self.enp]
        pe = e_io((t - T['evg2']) / 1.1)
        if pe > 0:
            ea = vis(t, T['evg2'], T['canals'], .3, .5)

            def fn(d, P, s):
                d.polygon([P(*q) for q in enp], fill=col(LIME, .18 * pe))
                seg, _ = partial(enp + [enp[0]], pe)
                if len(seg) > 1:
                    d.line([P(*q) for q in seg], fill=col(LIME), width=int(5 * s), joint='curve')
            vec(cv, bbox_of(enp, 12), fn, ea, base=LIME)
        # --- farms / cities / canals --------------------------------------------
        fa = vis(t, T['farms'], T['now'], .5, .8)
        if fa > 0:
            eaa = [S(q) for q in self.eaa]
            x0, y0, x1, y1 = bbox_of(eaa, 0)

            def fn(d, P, s):
                d.polygon([P(*q) for q in eaa], fill=col((196, 160, 80), .55), outline=col(WHITE, .8), width=int(3 * s))
                k = x0 - (y1 - y0)
                while k < x1:                                     # field rows
                    d.line([P(k, y1), P(k + (y1 - y0), y0)], fill=col((120, 150, 60), .5), width=int(2 * s))
                    k += 12
            # mask hatch to polygon by drawing on separate layer
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            vec(L, bbox_of(eaa, 8), fn, 1.0, base=(196, 160, 80))
            m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(q) for q in eaa], fill=255)
            m = m.filter(ImageFilter.GaussianBlur(.8))
            L.putalpha(Image.fromarray((np.asarray(L.getchannel('A'), np.float32) * np.asarray(m, np.float32) / 255 * fa).astype(np.uint8)))
            cv.alpha_composite(L)
            c = (sum(q[0] for q in eaa) / len(eaa), sum(q[1] for q in eaa) / len(eaa))
            label(cv, 'FARMS', c[0], c[1], t, T['farms'] + .1, T['now'], 28, WHITE, rise=6)
        ua = vis(t, T['cities'], T['now'], .5, .8)
        if ua > 0:
            ub = [S(q) for q in self.urban]
            vec(cv, bbox_of(ub, 8), lambda d, P, s: d.polygon([P(*q) for q in ub], fill=col(GRAY, .55)), ua, base=GRAY)
        for i, c in enumerate(self.canals):
            sc = [S(q) for q in c]
            a0 = T['canals'] + i * .14
            route(cv, sc, e_out((t - a0) / .8), (200, 202, 206), 5, head=False, alpha=vis(t, a0, T['send'], .2, .8), glow=False)
        for i, (n, p) in enumerate(self.cities):
            x, y = S(p)
            a0 = T['cities'] + i * .12
            pin(cv, x, y, t, a0, T['now'], WHITE, 9, rings=False)
            label(cv, n, x + 18, y + 2, t, a0 + .05, T['now'], 22, WHITE, anchor='l', rise=4)
        # --- original-size outline -----------------------------------------------
        oa = vis(t, T['today'], T['send'], .4, .6)
        if oa > 0:
            full = self.band_poly(S, 0, 1)
            route(cv, full + [full[0]], e_io((t - T['today']) / 1.2), WHITE, 4, head=False, alpha=oa, dashed=True, dash=(14, 10), glow=False)
            cur = self.band_poly(S, .25, 1, -1, .35)
            route(cv, cur + [cur[0]], e_io((t - T['half']) / 1.0), TEAL, 5, head=False, alpha=vis(t, T['half'], T['send'], .3, .6), glow=False)
        # --- 60-mile bracket ------------------------------------------------------
        ba = vis(t, T['sixty'] - .1, T['creeps'] + .3, .3, .4)
        if ba > 0:
            l, r = S(self.band(self.u60, -1)), S(self.band(self.u60, 1))
            pw = e_out((t - T['sixty'] + .1) / .6)
            cx = (l[0] + r[0]) / 2
            l2, r2 = (cx + (l[0] - cx) * pw, l[1]), (cx + (r[0] - cx) * pw, r[1])

            def fn(d, P, s):
                for wdt, c in ((10, col(OUTLINE, .6)), (5, col(WHITE))):
                    d.line([P(*l2), P(*r2)], fill=c, width=int(wdt * s))
                    for q in (l2, r2):
                        d.line([P(q[0], q[1] - 18), P(q[0], q[1] + 18)], fill=c, width=int(wdt * s))
            vec(cv, (l[0] - 30, l[1] - 40, r[0] + 30, r[1] + 40), fn, ba)
            label(cv, f'≈{round(self.w60 / 5) * 5} MI', cx, l[1] - 44, t, T['sixty'] + .2, T['creeps'] + .3, 34, WHITE, rise=6)
        # --- pins / labels on the map ---------------------------------------------
        ex, ey = S(self.EV)
        pin(cv, ex, ey, t, -1, T['water'] - .1, LIME, 14)
        label(cv, 'THE EVERGLADES', ex, ey - 62, t, -1, T['water'] - .1, 40, WHITE, rise=0)
        lx, ly = S(self.LK)
        la = vis(t, T['water'], None, .4)
        if la > 0:
            rr = 13 * st[2]
            vec(cv, (lx - rr - 6, ly - rr - 6, lx + rr + 6, ly + rr + 6),
                lambda d, P, s: d.ellipse((*P(lx - rr, ly - rr), *P(lx + rr, ly + rr)), fill=col(TEAL, .55)), la, base=TEAL)
        # 'barely see it move' magnifier ring
        mx_, my_ = S(self.band(.55, 0))
        ring(cv, mx_, my_, 70, t, T['barely'], T['flowing'], WHITE, 5)
        label(cv, 'BARELY MOVING', mx_, my_ - 96, t, T['barely'] + .1, T['flowing'], 28, WHITE, rise=6)
        # river-of-grass outline glow
        if t >= T['riv'] - .1:
            full = self.band_poly(S, 0, 1)
            route(cv, full + [full[0]], e_io((t - T['riv']) / 1.4), LIME, 5, head=False,
                  alpha=vis(t, T['riv'], T['evg2'], .3, .5), glow=False)
        # restoration focus: EAA ring
        ex_ = S(self.geo(-80.76, 26.5))
        ring(cv, ex_[0], ex_[1], 26 * st[2], t, T['restoration'], T['send'] + .5, LIME, 6, dashed=True)
        ring(cv, lx, ly, 52, t, T['water'], T['drained'], TEAL, 6)
        pin(cv, lx, ly, t, T['water'], T['marjory'], TEAL, 12, rings=False)
        label(cv, 'LAKE OKEECHOBEE', lx, ly - 86, t, T['okee'], T['sawgrass'], 32, WHITE, rise=6)
        label(cv, 'LAKE O.', lx, ly - 80, t, T['now'], None, 28, WHITE, rise=6)
        bx, by = S(self.BY)
        pin(cv, bx, by, t, T['bay'] - .05, T['marjory'], LIME, 13)
        label(cv, 'FLORIDA BAY', bx, by + 48, t, T['bay'], T['marjory'], 32, WHITE, rise=6)
        mx = S(self.geo(-80.80, 25.45))
        label(cv, 'EVERGLADES N.P.', mx[0], mx[1], t, T['evg2'] + .4, T['canals'], 28, LIME, rise=6)
        # --- lower info area --------------------------------------------------------
        stamp(cv, 'A SWAMP?', 540, 1290, t, T['swamp'], T['river'] - .05, 70, WHITE, rot=-4)
        hero(cv, "IT'S A RIVER", 540, 1290, t, T['river'], T['spreads'] - .1, 110, TEAL)
        chip(cv, 'FLOWS SOUTH FROM LAKE OKEECHOBEE', 540, 1280, t, T['spreads'], T['sixty'] - .1, size=32, accent=TEAL)
        hero(cv, '≈60 MILES WIDE', 540, 1290, t, T['sixty'], T['slowly'] - .1, 104, WHITE)
        label(cv, 'A SHALLOW SHEET OF WATER', 540, 1390, t, T['sixty'] + .2, T['slowly'] - .1, 28, TEAL)
        chip(cv, 'SLOW-MOVING SHEET FLOW', 540, 1280, t, T['slowly'], T['sawgrass'] - .1, size=38, accent=BLUE,
             sub='SO SLOW YOU CAN BARELY SEE IT MOVE')
        chip(cv, 'SAWGRASS', 540, 1280, t, T['sawgrass'], T['marjory'] - .1, size=46, accent=GRASS,
             sub='A TALL, SHARP-EDGED SEDGE')
        chip(cv, 'MARJORY STONEMAN DOUGLAS', 540, 1280, t, T['marjory'], T['riv'] - .1, size=38, accent=WHITE,
             sub='WRITER & CONSERVATIONIST')
        hero(cv, 'RIVER OF GRASS', 540, 1280, t, T['riv'], T['park'] - .1, 100, LIME)
        hero(cv, '1947', 540, 1395, t, T['y1947'], T['park'] - .1, 80, WHITE)
        chip(cv, 'EVERGLADES NATIONAL PARK', 540, 1280, t, T['park'], T['but'] - .1, size=38, accent=LIME,
             sub='DEDICATED 1947 · SAME YEAR AS THE BOOK')
        chip(cv, 'CANALS · FARMS · CITIES', 540, 1280, t, T['canals'], T['drained'] - .1, size=40, accent=GRAY)
        chip(cv, 'MUCH OF IT DRAINED', 540, 1280, t, T['drained'], T['half'] - .15, size=44, accent=RED)
        hero(cv, '≈ HALF', 540, 1280, t, T['half'], T['now'] - .1, 120, ORANGE)
        label(cv, 'ITS ORIGINAL SIZE', 540, 1395, t, T['original'], T['now'] - .1, 32, WHITE)
        chip(cv, 'RESTORATION', 540, 1275, t, T['restoration'], None, size=48, accent=LIME)
        label(cv, "ONE OF THE WORLD'S LARGEST", 540, 1356, t, T['world'] - .3, None, 28, WHITE, rise=6)
        label(cv, 'SENDING WATER SOUTH AGAIN', 540, 1404, t, T['send'], None, 30, LIME, rise=6)
        label(cv, 'SOURCES: NPS · USGS · SFWMD', 540, 1595, t, T['now'], None, 18, (200, 210, 215), rise=0)

