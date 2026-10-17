"""16 - The Island Born in 1963 (Surtsey, Iceland).

Base map: the pack's NASA Blue Marble Greenland/Iceland render (04_denmark_strait bbox);
Iceland highlight traced from that image's own coastline (EP4._build_land).
Facts (UNESCO World Heritage listing / Surtsey Research Society): Surtsey formed in an
undersea eruption off Iceland's south coast that broke the surface in November 1963;
eruptions lasted until June 1967; the island reached about 2.7 km2 (~1 sq mi); named
after Surtr, a fire giant of Norse mythology; protected since its birth, access limited
to researchers; seeds, insects, birds and plants colonised it; wave erosion has removed
roughly half its area.  Cross-sections are schematic (labelled on screen).
"""
from episode import *
from engine import _head
from ep04_underwater_waterfall import EP as EP4

SURTSEY = (-20.605, 63.303)
HEIMAEY = (-20.27, 63.44)
BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
SEA = 540
FLOOR = 860
CX = 560
K = 1.15
YEL = (255, 214, 90)
ROCK = (78, 72, 70)
ASH = (58, 56, 58)
STEAM = (232, 236, 240)
GREEN = (120, 200, 90)


class EP(Episode):
    slug = '16_Surtsey'
    gfx = '04_denmark_strait'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '16_Surtsey_Final.mp4'
    title = 'The Island Born in 1963'
    cover_title = 'THE ISLAND\nBORN IN\n1963'
    cover_t = 17.0
    emphasis = ['1963,', 'brand-new', 'island.', 'smoke', 'underwater', 'volcano', 'erupting.', 'day,', 'surface.',
                'Surtsey,', 'fire', 'giant', '1967.', 'one', 'square', 'mile.', 'untouched,', 'life', 'seeds,',
                'insects', 'birds', 'plants.', 'researchers', 'winning.', 'half']
    _build_land = EP4._build_land

    def setup(self):
        w = self.w
        self.base = self.base_map(.84)
        self._build_land()
        g = self.geo
        self.SU = g(*SURTSEY)
        self.HE = g(*HEIMAEY)
        self.IC = g(-18.6, 64.9)
        T = self.T = dict(
            y1963=w('1963'), north=w('North'), birth=w('birth'), brand=w('brand-new'), fisher=w('Fishermen'),
            icelands=w("Iceland's"), south=w('south'), spotted=w('spotted'), smoke=w('smoke'), rising=w('rising'),
            an=w('An'), volcano=w('volcano'), erupting=w('erupting'), within=w('Within'), broke=w('broke'),
            surface=w('surface'), named=w('named'), surtsey=w('Surtsey'), fire=w('fire'), eruptions=w('eruptions'),
            y1967=w('1967'), by=w('By'), one=w('one'), since=w('Since'), scientists=w('scientists'), kept=w('kept'),
            watching=w('watching'), bare=w('bare'), seeds=w('seeds'), insects=w('insects'), birds=w('birds'),
            plants=w('plants'), only=w('Only'), land=w('land'), but=w('But'), winning=w('winning'),
            waves=w('Waves'), worn=w('worn'), half=w('half'), area=w('area'))
        SU = self.SU
        self.up1, self.down1, self.up2 = T['an'] - .15, T['by'] - .1, T['scientists'] - .2
        self.slides = [(self.up1, 1), (self.down1, 0), (self.up2, 1)]
        self.cam = Cam([
            frame_on(SU, 480, 760, 2.4, 0), frame_on(SU, 480, 760, 2.3, T['north'] - .05),
            frame_on(SU, 540, 760, 1.5, T['north'] + 1.2), frame_on(SU, 540, 760, 1.55, T['fisher'] - .1),
            frame_on(SU, 470, 760, 3.0, T['fisher'] + 1.2), frame_on(SU, 470, 760, 3.2, self.up1 + .7),
            frame_on(SU, 470, 720, 2.6, self.down1), frame_on(SU, 470, 720, 3.4, T['since'] + .2),
            frame_on(SU, 470, 720, 3.4, self.dur)])
        b = self.beat
        b(0.0, 'Iceland highlighted, pulsing pin off the south coast', 'pop', 2)
        b(T['y1963'], 'Hero: 1963', 'thud')
        b(T['north'], 'Camera pulls out; NORTH ATLANTIC label', 'whoosh')
        b(T['birth'], 'Pin pops again with a bright ring', 'pop')
        b(T['brand'], 'A BRAND-NEW ISLAND chip', 'tick')
        b(T['fisher'], 'Push in to the south coast; fishing boat sails in', 'whoosh')
        b(T['south'], 'SOUTH COAST + WESTMAN ISLANDS labels', 'tick')
        b(T['spotted'], 'Lookout "!" over the boat', 'pop')
        b(T['smoke'], 'Dark smoke rises from the sea at the pin', 'swish')
        b(T['rising'], 'Plume grows tall', 'rumble')
        b(self.up1, 'Map lifts: schematic cross-section, volcano on the seafloor', 'bubble')
        b(T['volcano'], 'UNDERWATER VOLCANO label, magma conduit glows', 'tick')
        b(T['erupting'], 'Eruption: bubbles, cone starts growing (shake)', 'rumble', 2)
        b(T['within'], 'WITHIN A DAY chip; cone climbs toward the surface', 'tick')
        b(T['broke'], 'Cone breaks the surface; ash + steam jets', 'rumble', 3)
        b(T['surface'], 'NEW ISLAND / ASH + STEAM labels', 'pop')
        b(T['surtsey'], 'SURTSEY hero + panel label', 'thud')
        b(T['fire'], 'NAMED FOR A FIRE GIANT chip', 'flame')
        b(T['eruptions'], 'Lava fountains, island spreads wider', 'rumble')
        b(T['y1967'], 'Hero: 1967 · ERUPTIONS END', 'thud')
        b(self.down1, 'Back to the map, push in on Surtsey', 'whoosh')
        b(T['one'], 'Hero: ≈1 SQ MI', 'thud')
        b(self.up2, 'Panel returns: finished island', 'whoosh')
        b(T['kept'], 'KEPT ALMOST UNTOUCHED chip', 'pop')
        b(T['watching'], 'HOW DOES LIFE ARRIVE? chip', 'tick')
        b(T['bare'], 'BARE ROCK label', 'tick')
        b(T['seeds'], 'Seeds drift in on the wind', 'swish')
        b(T['insects'], 'Insects buzz over the island', 'tick')
        b(T['birds'], 'Birds fly in and land', 'swish')
        b(T['plants'], 'Plants sprout across the island', 'pop')
        b(T['only'], 'ONLY RESEARCHERS chip; researcher on the island', 'pop')
        b(T['land'], 'Visitor boat crossed out', 'thud', -3)
        b(T['but'], 'Waves grow', 'swish')
        b(T['winning'], 'THE SEA IS WINNING chip', 'tick')
        b(T['waves'], 'Waves batter the coast; island erodes', 'rumble')
        b(T['half'], 'Hero: ≈HALF GONE; 1967 outline vs today', 'thud')

    # -------------------------------------------------------------------------
    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    # ---- map -----------------------------------------------------------------
    def smoke(self, m, x, y, t, a0, b0, height):
        al = vis(t, a0, b0, .4, .4)
        if al <= 0:
            return
        gr = .35 + .65 * e_out((t - a0) / 1.6)
        hgt = height * gr

        def fn(d, P, s):
            for i in range(16):
                ph = ((t - a0) * .45 + i / 16) % 1
                py = y - ph * hgt
                px = x + 40 * ph + 9 * math.sin(i * 1.7 + t * 2)
                r = 12 + 48 * ph * gr
                c = tuple(int(lerp(a, b, ph)) for a, b in zip((40, 38, 40), (120, 122, 128)))
                d.ellipse((*P(px - r, py - r), *P(px + r, py + r)), fill=c + (int(220 * (1 - ph ** 1.5)),))
        vec(m, (x - 80, y - height - 60, x + 120, y + 30), fn, al, base=(60, 60, 60))

    def boat(self, m, x, y, al, crossed=0.0, sc=1.0):
        if al <= 0:
            return

        def fn(d, P, s):
            q = lambda dx, dy: P(x + dx * sc, y + dy * sc)
            d.polygon([q(-34, -6), q(34, -6), q(24, 10), q(-26, 10)], fill=col((210, 70, 60)), outline=col(OUTLINE), width=int(3 * s))
            d.rectangle((*q(-12, -22), *q(10, -6)), fill=col(WHITE), outline=col(OUTLINE), width=int(2 * s))
            d.line([q(16, -6), q(16, -40)], fill=col(OUTLINE), width=int(3 * s))
            d.line([q(16, -38), q(32, -10)], fill=col(OUTLINE), width=int(2 * s))
            if crossed > 0:
                for dx in (-1, 1):
                    d.line([q(-40, -40 * dx), q(40, 40 * dx)], fill=col(RED, crossed), width=int(9 * s))
        vec(m, (x - 50 * sc, y - 50 * sc, x + 50 * sc, y + 20 * sc + 30), fn, al, base=(210, 70, 60))

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        fill, bord = self.land['ic']
        m.alpha_composite(with_alpha(render_map(fill, st, 2.0), .85))
        m.alpha_composite(with_alpha(render_map(bord, st, 2.0), .7))
        m.alpha_composite(vignette())
        S = lambda p: Cam.S(st, *p)
        sx, sy = S(self.SU)
        il = S(self.IC)
        # first half --------------------------------------------------------------
        e1 = self.up1 + .3
        label(m, 'ICELAND', il[0], il[1], t, -.1, e1, 38, WHITE, rise=0)
        pin(m, sx, sy, t, -.15, e1, LIME, 15)
        ring(m, sx, sy, 60, t, T['birth'], T['fisher'], LIME, 6)
        ring(m, sx, sy, 60, t, T['birth'] + .25, T['fisher'], WHITE, 3, alpha=.6)
        na = S(self.geo(-30.5, 63.8))
        label(m, 'NORTH ATLANTIC', max(220, na[0]), na[1], t, T['north'] + .2, T['fisher'] + .3, 34, (170, 225, 245), rise=8)
        chip(m, 'A BRAND-NEW ISLAND', clamp(sx, 260, 820), sy - 150, t, T['brand'], T['fisher'] - .1, size=36, accent=LIME)
        # boat
        ba = vis(t, T['fisher'] + .2, e1, .4, .3)
        if ba > 0:
            p = e_out((t - T['fisher'] - .2) / 2.0)
            bx = sx - lerp(330, 190, p); by = sy + 40 + 3 * math.sin(t * 3)
            self.boat(m, bx, by, ba)
            label(m, '!', bx, by - 80, t, T['spotted'], e1, 54, YEL, rise=10)
            label(m, 'FISHERMEN', bx, by + 52, t, T['fisher'] + .4, T['smoke'] - .1, 26, WHITE, rise=4)
        coast = S(self.geo(-19.2, 63.6))
        label(m, 'SOUTH COAST', coast[0] + 20, coast[1] - 50, t, T['south'], T['smoke'] - .1, 28, WHITE, rise=6, anchor='l')
        hx, hy = S(self.HE)
        label(m, 'WESTMAN ISLANDS', hx + 50, hy + 50, t, T['south'] + .4, e1, 26, (220, 230, 235), rise=6, anchor='l')
        self.smoke(m, sx, sy, t, T['smoke'] - .1, e1, 300)
        label(m, 'DARK SMOKE', sx - 70, sy - 250, t, T['smoke'] + .2, e1, 30, WHITE, rise=6, anchor='r')
        # second half -------------------------------------------------------------
        a2 = self.down1 + .2
        pin(m, sx, sy, t, a2, None, LIME, 13)
        ring(m, sx, sy, 48, t, T['one'], None, ORANGE, 5, spin=t)
        chip(m, 'SURTSEY', clamp(sx, 220, 820), sy - 160, t, a2 + .2, None, size=44, accent=LIME, sub='SOUTH OF ICELAND')
        label(m, 'ICELAND', il[0], il[1], t, a2 + .4, None, 36, WHITE, rise=6)
        label(m, 'HEIMAEY', hx + 60, hy + 40, t, a2 + .8, None, 24, (220, 230, 235), rise=6, anchor='l')
        return m

    # ---- schematic panel -----------------------------------------------------
    def state(self, t):
        T = self.T
        top = 800
        if t >= T['erupting']:
            top = lerp(800, SEA + 30, e_io((t - T['erupting']) / (T['broke'] - T['erupting'])))
        if t >= T['broke']:
            top = lerp(SEA + 30, SEA - 70, e_out((t - T['broke']) / .9))
        if t >= T['eruptions']:
            top = lerp(SEA - 70, SEA - 78, e_io((t - T['eruptions']) / 2.4))
        pw = 14
        if t >= T['broke']:
            pw = lerp(14, 50, e_out((t - T['broke']) / .9))
        if t >= T['eruptions']:
            pw = lerp(50, 150, e_io((t - T['eruptions']) / 2.6))
        right = CX + pw + (SEA - top) / K if top < SEA else CX
        xr = None
        if t >= T['waves']:
            xr = lerp(right, CX - 10, e_io((t - T['waves']) / (T['area'] - T['waves'])))
        return top, pw, xr, right

    @staticmethod
    def prof(x, top, pw, xr=None):
        y = min(FLOOR + 10, top + K * max(0, abs(x - CX) - pw))
        if xr is not None and x > xr:
            y = max(y, SEA + 16 + 10 * clamp((x - xr) / 40))
        return y

    def panel_draw(self, d, P, s, t):
        T = self.T
        top, pw, xr, right = self.state(t)
        life = t >= self.up2 - .1
        # sky
        for i in range(10):
            y0 = lerp(BY0, SEA, i / 10); y1 = lerp(BY0, SEA, (i + 1) / 10)
            c = tuple(int(lerp(a, b, i / 9)) for a, b in zip((70, 104, 140), (150, 176, 196)))
            d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
        # sea
        for i in range(16):
            y0 = lerp(SEA, BY1, i / 16); y1 = lerp(SEA, BY1, (i + 1) / 16)
            c = tuple(int(lerp(a, b, i / 15)) for a, b in zip((34, 96, 150), (8, 30, 56)))
            d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
        erupt = clamp((t - T['erupting']) / .5) * (1 - clamp((t - T['y1967'] - .4) / 1.0))
        if life:
            erupt = 0
        # underwater plume (dark water) + bubbles
        if erupt > 0 and top > SEA - 30:
            for k in range(14):
                ph = (t * .5 + k / 14) % 1
                y = lerp(top, SEA, ph)
                r = 12 + 40 * ph
                d.ellipse((*P(CX - r + 14 * math.sin(k + t), y - r), *P(CX + r + 14 * math.sin(k + t), y + r)),
                          fill=(30, 40, 46, int(140 * erupt * (1 - ph * .4))))
            for k in range(22):
                ph = (t * .9 + k / 22) % 1
                x = CX + ((k * 37) % 120 - 60) + 6 * math.sin(t * 4 + k)
                y = lerp(top, SEA + 6, ph)
                r = 3 + 4 * ph
                d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), outline=(220, 240, 255, int(220 * erupt)), width=int(2 * s))
        # seafloor
        d.rectangle((*P(BX0, FLOOR), *P(BX1, BY1)), fill=(84, 72, 60, 255))
        # magma chamber + conduit
        mg = 0 if life else vis(t, T['volcano'] - .2, None, .5) * (1 - .6 * clamp((t - T['y1967'] - .4) / 1.0))
        if mg > 0:
            d.ellipse((*P(CX - 90, FLOOR + 30), *P(CX + 90, FLOOR + 66)), fill=col((255, 96, 40), .9 * mg), outline=col(YEL, mg), width=int(3 * s))
            d.line([P(CX, FLOOR + 30), P(CX, top + 14)], fill=col((255, 120, 40), mg), width=int(10 * s))
        # 1967 outline (dashed) once erosion begins
        xs = list(range(BX0, BX1 + 1, 6))
        # island / volcano body
        body = [(x, self.prof(x, top, pw, xr)) for x in xs]
        d.polygon([P(*q) for q in body] + [P(BX1, FLOOR + 10), P(BX0, FLOOR + 10)], fill=ROCK + (255,))
        d.line([P(*q) for q in body if q[1] < FLOOR + 5], fill=(30, 28, 28, 255), width=int(3 * s))
        # lava fountain + flows
        lava = vis(t, T['eruptions'] - .1, T['y1967'] + 1.0, .4, .8) if not life else 0
        if lava > 0:
            for k in range(10):
                ph = (t * 1.3 + k / 10) % 1
                ang = -math.pi / 2 + (k - 4.5) * .12
                vx, vy = math.cos(ang) * 90, math.sin(ang) * 160
                x = CX + vx * ph; y = top - 6 + vy * ph + 220 * ph * ph
                if y < top:
                    d.ellipse((*P(x - 6, y - 6), *P(x + 6, y + 6)), fill=col((255, 140, 50), lava))
            for sgn in (-1, 1):
                flow = [(CX + sgn * dx, self.prof(CX + sgn * dx, top, pw) - 3) for dx in range(0, int(pw + 40), 6)]
                d.line([P(*q) for q in flow], fill=col((255, 110, 40), lava), width=int(6 * s))
        # ash + steam jets (once above sea)
        if erupt > 0 and top < SEA:
            jet = erupt * clamp((SEA - top) / 30) * (1 - .5 * clamp((t - T['eruptions']) / 1.5))
            for k in range(24):
                ph = (t * .55 + k / 24) % 1
                spread = (k % 5 - 2) * 26
                y = lerp(top - 6, BY0 + 20, ph ** .8)
                x = CX + spread * ph + 70 * ph * ph + 10 * math.sin(k * 1.3 + t * 2)
                r = 14 + 62 * ph
                c = ASH if k % 3 else STEAM
                c = tuple(int(lerp(a, b, ph * .6)) for a, b in zip(c, (150, 154, 160)))
                d.ellipse((*P(x - r, y - r * .8), *P(x + r, y + r * .8)), fill=c + (int(230 * jet * (1 - ph ** 2)),))
        # dashed 1967 outline
        if xr is not None:
            oa = clamp((t - T['waves'] - .3) / .5)
            old = [(x, self.prof(x, top, pw)) for x in range(int(CX - 10), int(right) + 1, 4) if self.prof(x, top, pw) < SEA]
            old = [q for q in old if q[0] > xr - 4]
            for i in range(0, len(old) - 1, 2):
                d.line([P(*old[i]), P(*old[i + 1])], fill=col(ORANGE, oa), width=int(4 * s))
            if old:
                d.line([P(old[-1][0], old[-1][1]), P(old[-1][0] + 18, SEA)], fill=col(ORANGE, oa), width=int(4 * s))
        # life ---------------------------------------------------------------
        if life:
            def on_top(x):
                return self.prof(x, top, pw, xr)
            # seeds drifting on the wind
            sa = vis(t, T['seeds'] - .1, T['only'] + 1.0, .3, .5)
            if sa > 0:
                for k in range(7):
                    p = clamp((t - T['seeds'] - k * .12) / 1.6)
                    tx = 410 + k * 38
                    x = lerp(100, tx, e_out(p)); y = lerp(380 + (k % 3) * 22, on_top(tx) - 6, e_io(p)) + (1 - p) * 12 * math.sin(t * 5 + k)
                    if xr is not None and tx > xr:
                        continue
                    d.ellipse((*P(x - 6, y - 4), *P(x + 6, y + 4)), fill=col((176, 132, 76), sa), outline=col(OUTLINE, sa), width=int(1 * s))
                    if p < 1:
                        d.line([P(x - 26, y - 2), P(x - 10, y - 2)], fill=col(WHITE, sa * .6 * (1 - p)), width=int(2 * s))
            # insects buzzing
            ia = vis(t, T['insects'] - .1, T['only'] + 1.0, .3, .5)
            if ia > 0:
                for k in range(8):
                    x = 450 + (k * 41) % 230 + 18 * math.sin(t * 6 + k * 2)
                    y = 410 + (k * 17) % 30 + 10 * math.sin(t * 9 + k)
                    if xr is not None and x > xr:
                        continue
                    d.ellipse((*P(x - 4, y - 3), *P(x + 4, y + 3)), fill=col(OUTLINE, ia))
                    d.ellipse((*P(x - 7, y - 9), *P(x, y - 2)), fill=col(WHITE, ia * .7))
                    d.ellipse((*P(x, y - 9), *P(x + 7, y - 2)), fill=col(WHITE, ia * .7))
            # birds flying in
            if t >= T['birds'] - .1:
                for k, (tx, ty0) in enumerate(((470, 360), (560, 340), (650, 370), (520, 395))):
                    p = clamp((t - T['birds'] - k * .2) / 1.5)
                    land_y = on_top(tx) - 8
                    x = lerp(1000, tx, e_out(p)); y = lerp(ty0 - 30, lerp(ty0, land_y, clamp((p - .6) / .4)), e_out(p))
                    if xr is not None and tx > xr + 10:
                        continue
                    flap = 12 * math.sin(t * 14 + k) * (1 - clamp((p - .9) / .1))
                    d.line([P(x - 18, y - flap), P(x - 6, y), P(x, y + 4), P(x + 6, y), P(x + 18, y - flap)],
                           fill=col(WHITE), width=int(4 * s), joint='curve')
            # plants sprouting
            if t >= T['plants'] - .1:
                for k in range(12):
                    x = 440 + k * 26 + (k * 7) % 11
                    if xr is not None and x > xr - 4:
                        continue
                    gp = e_back(clamp((t - T['plants'] - k * .06) / .5), 1.6)
                    yb = on_top(x)
                    if yb > SEA - 2:
                        continue
                    h = (12 + (k * 5) % 10) * gp
                    for a in (-.5, 0, .5):
                        d.line([P(x, yb), P(x + math.sin(a) * h, yb - math.cos(a) * h)], fill=col(GREEN), width=int(4 * s))
            # researcher
            ra = vis(t, T['only'], None, .4)
            if ra > 0:
                x = lerp(470, 500, clamp((t - T['only']) / 2.5)); y = on_top(x) - 2
                d.ellipse((*P(x - 8, y - 56), *P(x + 8, y - 40)), fill=col(LIME, ra))
                d.line([P(x, y - 40), P(x, y - 18)], fill=col(WHITE, ra), width=int(5 * s))
                d.line([P(x, y - 18), P(x - 7, y)], fill=col(WHITE, ra), width=int(5 * s))
                d.line([P(x, y - 18), P(x + 7, y)], fill=col(WHITE, ra), width=int(5 * s))
                d.line([P(x, y - 34), P(x + 14, y - 26)], fill=col(WHITE, ra), width=int(4 * s))
            # wave arrows on the windward side
            wa = vis(t, T['waves'] - .2, None, .3)
            if wa > 0 and xr is not None:
                for k in range(3):
                    ph = (t * .8 + k / 3) % 1
                    x1 = lerp(980, xr + 30, ph)
                    pts = [(x1 + 70, SEA - 8), (x1, SEA - 8)]
                    d.line([P(*q) for q in pts], fill=col(WHITE, wa * (1 - ph * .5)), width=int(7 * s))
                    _head(d, P, s, pts[-1], math.pi, 16, col(WHITE, wa * (1 - ph * .5)))
                for k in range(8):
                    ph = (t * 1.6 + k / 8) % 1
                    x = xr + 6 + 10 * math.sin(k * 2.1); y = SEA - 6 - 40 * ph
                    r = 4 + 6 * ph
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=col(WHITE, wa * (1 - ph)))
        # sea surface + waves
        amp = 4 + (8 * clamp((t - T['but']) / 1.2) if t >= T['but'] else 0)
        wv = [P(x, SEA + amp * math.sin(x / 34 + t * 3)) for x in range(BX0, BX1 + 1, 10)]
        d.line(wv, fill=col(WHITE, .85), width=int(3 * s))
        d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

    def panel(self, cv, t, al):
        T = self.T
        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (18, 36, 58))
        d = ImageDraw.Draw(L, 'RGBA')
        self.panel_draw(d, lambda x, y: ((x - BX0) * 2, (y - BY0) * 2), 2, t)
        sec = L.reduce(2).convert('RGBA')
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(Image.fromarray(np.minimum(np.asarray(sec.getchannel('A')), np.asarray(m))))
        shake = 0
        for a in (T['erupting'], T['broke'], T['waves']):
            if a <= t < a + .5:
                shake = math.sin(t * 63) * 7 * (1 - (t - a) / .5)
        paste(cv, with_alpha(sec, al), BX0 + shake, BY0)
        label(cv, 'SCHEMATIC · NOT TO SCALE', 82, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='l')
        label(cv, 'SEA LEVEL', 90, SEA - 22, t, 0, None, 22, WHITE, rise=0, anchor='l')
        top, pw, xr, right = self.state(t)
        if t < self.up2 - .1:
            label(cv, 'SEAFLOOR', 90, FLOOR - 22, t, 0, T['within'], 22, (230, 215, 195), rise=0, anchor='l')
            label(cv, 'UNDERWATER VOLCANO', CX, 700, t, T['volcano'], T['within'], 30, WHITE, rise=6)
            label(cv, 'MAGMA', CX + 110, FLOOR + 48, t, T['volcano'] + .3, T['y1967'] + .5, 24, YEL, rise=0, anchor='l')
            label(cv, 'BUILDING UP', 800, 680, t, T['within'] + .2, T['broke'], 28, (170, 225, 245), rise=6)
            label(cv, 'NEW ISLAND', 260, SEA - 70, t, T['surface'], T['surtsey'] - .1, 32, LIME, rise=6)
            label(cv, 'SURTSEY', 260, SEA - 70, t, T['surtsey'], None, 38, LIME, rise=8)
            label(cv, 'ASH + STEAM', 820, 400, t, T['surface'] + .3, T['eruptions'] + .5, 28, WHITE, rise=6)
            label(cv, 'LAVA', 820, 470, t, T['eruptions'] + .3, None, 30, ORANGE, rise=6)
        else:
            label(cv, 'SURTSEY', 260, SEA - 70, t, self.up2 + .3, None, 38, LIME, rise=0)
            label(cv, 'BARE ROCK', CX, 415, t, T['bare'], T['seeds'], 32, WHITE, rise=6)
            label(cv, 'SEEDS', 180, 360, t, T['seeds'] + .1, T['only'], 28, (225, 190, 140), rise=6)
            label(cv, 'INSECTS', CX + 20, 405, t, T['insects'] + .1, T['only'], 26, WHITE, rise=6)
            label(cv, 'BIRDS', 860, 360, t, T['birds'] + .1, T['only'], 28, WHITE, rise=6)
            label(cv, 'PLANTS', CX, 620, t, T['plants'] + .1, T['only'] + .4, 28, GREEN, rise=6)
            label(cv, 'RESEARCHERS ONLY', 540, 372, t, T['only'] + .3, T['waves'] - .2, 28, LIME, rise=6)
            ba = vis(t, T['land'] - .3, T['waves'] - .2, .3, .3)
            self.boat(cv, 830, SEA - 4 + 2 * math.sin(t * 3), ba, crossed=clamp((t - T['land']) / .3), sc=1.2)
            label(cv, 'NO VISITORS', 830, 640, t, T['land'], T['waves'] - .2, 26, RED, rise=6)
            label(cv, 'WAVES', 890, 480, t, T['waves'], None, 30, WHITE, rise=6)
            if xr is not None:
                label(cv, '1967', min(right, 770) - 10, 425, t, T['worn'], None, 28, ORANGE, rise=6)
                label(cv, 'TODAY', 380, 405, t, T['half'], None, 28, LIME, rise=6)

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_bg())
            self.panel(cv, t, clamp(u * 1.5))
            ttl = 'UNDERWATER ERUPTION · 1963' if t < self.up2 - .1 else 'SURTSEY · A NATURAL LAB'
            label(cv, ttl, 540, 280, t, 0, None, 28, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area --------------------------------------------------------
        hero(cv, '1963', 540, 1290, t, T['y1963'], T['fisher'] - .1, 140, LIME)
        label(cv, 'THE NORTH ATLANTIC', 540, 1405, t, T['north'] + .1, T['brand'] - .1, 30, WHITE)
        label(cv, 'GAVE BIRTH TO AN ISLAND', 540, 1405, t, T['brand'], T['fisher'] - .1, 30, LIME)
        chip(cv, "OFF ICELAND'S SOUTH COAST", 540, 1290, t, T['icelands'], T['smoke'] - .1, size=38, accent=ORANGE)
        chip(cv, 'DARK SMOKE FROM THE SEA', 540, 1290, t, T['smoke'], self.up1 + .2, size=38, accent=WHITE)
        chip(cv, 'AN UNDERWATER VOLCANO', 540, 1290, t, T['volcano'] - .2, T['within'] - .1, size=40, accent=ORANGE, sub='ERUPTING')
        chip(cv, 'WITHIN A DAY', 540, 1290, t, T['within'], T['named'] - .1, size=44, accent=LIME, sub='A NEW ISLAND BROKE THE SURFACE')
        hero(cv, 'SURTSEY', 540, 1290, t, T['surtsey'], T['fire'] - .1, 120, LIME)
        chip(cv, 'NAMED FOR A FIRE GIANT', 540, 1290, t, T['fire'], T['eruptions'] - .1, size=40, accent=ORANGE, sub='FROM NORSE MYTHOLOGY')
        chip(cv, 'ERUPTIONS CONTINUED', 540, 1290, t, T['eruptions'], T['y1967'] - .1, size=40, accent=ORANGE)
        hero(cv, '1967', 540, 1290, t, T['y1967'], T['one'] - .2, 140, LIME)
        label(cv, 'ERUPTIONS FINALLY END', 540, 1405, t, T['y1967'] + .2, T['one'] - .2, 30, WHITE)
        hero(cv, '≈1 SQ MI', 540, 1290, t, T['one'], T['kept'] - .1, 120, LIME)
        label(cv, 'NEW LAND BY 1967', 540, 1405, t, T['one'] + .2, T['kept'] - .1, 30, WHITE)
        chip(cv, 'KEPT ALMOST UNTOUCHED', 540, 1290, t, T['kept'], T['watching'] - .1, size=40, accent=LIME, sub='UNESCO WORLD HERITAGE SITE')
        chip(cv, 'HOW DOES LIFE ARRIVE?', 540, 1290, t, T['watching'], T['seeds'] - .1, size=40, accent=TEAL, sub='ON BARE VOLCANIC ROCK')
        for k, (nm, key, x, y, c) in enumerate((('SEEDS', 'seeds', 300, 1270, (225, 190, 140)), ('INSECTS', 'insects', 780, 1270, WHITE),
                                                 ('BIRDS', 'birds', 300, 1375, WHITE), ('PLANTS', 'plants', 780, 1375, GREEN))):
            chip(cv, f'{k + 1}  {nm}', x, y, t, T[key], T['only'] - .1, size=36, accent=c)
        chip(cv, 'ONLY RESEARCHERS', 540, 1290, t, T['only'], T['but'] - .1, size=44, accent=LIME, sub='ARE ALLOWED TO LAND')
        chip(cv, 'THE SEA IS WINNING', 540, 1290, t, T['winning'] - .2, T['half'] - .1, size=42, accent=RED, sub='WAVES WEAR THE COAST AWAY')
        hero(cv, '≈HALF GONE', 540, 1290, t, T['half'], None, 116, ORANGE)
        label(cv, "OF SURTSEY'S AREA", 540, 1405, t, T['half'] + .2, None, 30, WHITE)
        label(cv, 'SOURCES: UNESCO · SURTSEY RESEARCH SOCIETY', 540, 1595, t, T['but'], None, 18, (200, 210, 215), rise=0)


@functools.lru_cache(None)
def _bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
