"""11 - The Ditch That Built New York (Erie Canal).

Base map: the pack's NASA Blue Marble Northeast US render (03_centralia bbox).
Facts (NY State Canal Corporation / NPS / Library of Congress): Erie Canal opened 1825;
~363 mi from Albany on the Hudson River to Buffalo on Lake Erie; largely dug by hand;
nicknamed "Clinton's Ditch" after Governor DeWitt Clinton; rises ~570 ft (net) via 83
original locks; cut freight costs by roughly 90%; helped make New York City the nation's
busiest port; "Wedding of the Waters": Clinton poured a keg of Lake Erie water into the
Atlantic in Nov. 1825.  Canal line is generalised; elevation profile is schematic.
"""
from episode import *

CANAL = [(-73.75, 42.65), (-73.70, 42.77), (-73.94, 42.81), (-74.19, 42.94), (-74.86, 43.04), (-75.23, 43.10),
         (-75.46, 43.21), (-76.15, 43.05), (-76.70, 43.01), (-77.00, 43.06), (-77.61, 43.16), (-78.20, 43.20),
         (-78.69, 43.17), (-78.88, 43.02), (-78.88, 42.89)]
HUDSON = [(-73.75, 42.65), (-73.79, 42.25), (-73.97, 41.93), (-73.94, 41.70), (-74.00, 41.50), (-73.96, 41.39),
          (-73.89, 41.07), (-73.93, 40.85), (-74.02, 40.70), (-74.04, 40.60), (-73.98, 40.47), (-73.82, 40.40)]
ALB, BUF, NYC = (-73.756, 42.653), (-78.878, 42.886), (-74.006, 40.713)
HARBOR = (-73.98, 40.47)
YEL = (255, 214, 90)
WATER = (60, 140, 210)
BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
PX0, PX1, PY0, PY1 = 150, 930, 820, 470          # profile: Albany (low, left) -> Buffalo (high, right)
NLOCK = 83


def stair(n=NLOCK):
    """Staircase profile points (schematic)."""
    pts = [(PX0 - 60, PY0)]
    for k in range(n):
        x0 = lerp(PX0, PX1, k / n)
        y = lerp(PY0, PY1, k / n) if k else PY0
        y1 = lerp(PY0, PY1, (k + 1) / n)
        pts += [(x0, y), (x0, y1)]
    pts += [(PX1, PY1), (PX1 + 60, PY1)]
    return pts


class EP(Episode):
    slug = '11_Erie_Canal'
    gfx = '03_centralia'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '11_Erie_Canal_Final.mp4'
    title = 'The Ditch That Built New York'
    cover_title = 'THE DITCH\nTHAT BUILT\nNEW YORK'
    cover_t = 19.6
    emphasis = ['ditch', 'hand', 'busiest', 'port.', 'Erie', 'Canal,', 'eighteen', 'twenty-five.', 'sixty-three', 'miles',
                'Albany', 'Hudson', 'Buffalo', "Clinton's", 'Ditch,', 'DeWitt', 'seventy', 'feet,', 'eighty-three', 'locks',
                'ninety', 'percent.', 'keg', 'Atlantic.']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        g = self.geo
        self.canal = spline([g(*p) for p in CANAL], 10)
        self.hudson = spline([g(*p) for p in HUDSON], 10)
        self.ALB, self.BUF, self.NYC, self.HB = g(*ALB), g(*BUF), g(*NYC), g(*HARBOR)
        T = self.T = dict(
            ditch=w('ditch'), hand=w('hand'), new1=w('New', 1), busiest=w('busiest'), port=w('port'),
            erie1=w('Erie', 1), opened=w('opened', 1), eighteen=w('eighteen'), three=w('three'), miles=w('miles'),
            upstate=w('upstate'), albany=w('Albany'), hudson=w('Hudson'), buffalo=w('Buffalo'), lake1=w('Lake', 1),
            critics=w('Critics'), clintons=w("Clinton's"), governor=w('Governor'), land=w('land'), rises=w('rises'),
            five=w('five'), builders=w('builders'), eighty=w('eighty-three'), locks=w('locks'), lift=w('lift'),
            over=w('over', 2), once=w('Once'), cost=w('cost'), shipping=w('shipping'), fell=w('fell'),
            ninety=w('ninety'), celebrate=w('celebrate'), sailed=w('sailed'), poured=w('poured'), keg=w('keg'),
            lake2=w('Lake', 2), water=w('water'), atlantic=w('Atlantic'))
        mid = ((self.ALB[0] + self.BUF[0]) / 2, (self.ALB[1] + self.BUF[1]) / 2)
        hk = ((self.NYC[0] + self.ALB[0]) / 2, (self.NYC[1] + self.ALB[1]) / 2)
        self.cam = Cam([
            frame_on(self.NYC, 540, 720, 2.6, 0), frame_on(hk, 560, 560, 2.0, T['ditch'] + .2),
            frame_on(hk, 560, 560, 1.9, T['busiest']), frame_on(mid, 540, 520, 1.45, T['erie1'] + .3),
            frame_on(mid, 540, 520, 1.5, T['upstate']), frame_on(mid, 540, 520, 1.45, T['land'] - .3),
            frame_on(mid, 540, 520, 1.45, T['once'] + .2), frame_on(mid, 540, 540, 1.5, T['celebrate'] - .3),
            frame_on(self.NYC, 520, 760, 2.2, T['sailed'] + .6), frame_on(self.NYC, 520, 760, 2.5, self.dur)])
        self.slides = [(T['land'] - .25, 1), (T['once'] - .1, 0)]
        self.steps = stair()
        b = self.beat
        b(0.0, 'New York City pin on the map, Hudson visible', 'pop', 2)
        b(T['ditch'], 'Canal line starts digging west from Albany', 'swish')
        b(T['hand'], 'DUG MOSTLY BY HAND chip + shovel', 'tick')
        b(T['new1'], 'NEW YORK CITY label pulses', 'pop')
        b(T['busiest'], "Hero: AMERICA'S BUSIEST PORT", 'thud')
        b(T['erie1'], 'Camera pulls back across upstate; ERIE CANAL chip', 'whoosh')
        b(T['eighteen'], '1825', 'thud')
        b(T['three'], 'Canal draws full length; ≈363 MILES', 'swish')
        b(T['upstate'], 'UPSTATE NEW YORK label', 'tick')
        b(T['albany'], 'ALBANY pin', 'pop')
        b(T['hudson'], 'Hudson River glows teal', 'tick')
        b(T['buffalo'], 'BUFFALO pin', 'pop')
        b(T['lake1'], 'LAKE ERIE label', 'tick')
        b(T['critics'], 'Critics chip', 'tick')
        b(T['clintons'], '"CLINTON\'S DITCH" stamp', 'thud')
        b(T['governor'], 'GOV. DEWITT CLINTON chip', 'pop')
        b(T['land'] - .25, 'Map lifts: schematic elevation profile', 'whoosh')
        b(T['rises'], 'Land slope draws Albany -> Buffalo', 'swish')
        b(T['five'], '≈570 FT ruler + hero', 'thud')
        b(T['eighty'], 'Staircase of 83 locks builds', 'rumble')
        b(T['locks'], '83 LOCKS hero', 'pop')
        b(T['lift'], 'Boat climbs the lock staircase', 'swish')
        b(T['over'], 'Boat reaches Lake Erie level', 'tick')
        b(T['once'] - .1, 'Map returns, boats run the canal', 'whoosh')
        b(T['cost'], 'Shipping cost bars', 'tick')
        b(T['fell'], 'Cost bar shrinks', 'swish')
        b(T['ninety'], '≈90% CHEAPER', 'thud')
        b(T['celebrate'], 'Camera heads down the Hudson to New York', 'whoosh')
        b(T['sailed'], 'Boat sails Albany -> New York Harbor', 'swish')
        b(T['poured'], 'Keg tips at the harbor', 'pop')
        b(T['water'], 'Lake Erie water splashes into the sea', 'swish')
        b(T['atlantic'], 'ATLANTIC OCEAN + WEDDING OF THE WATERS', 'pop')

    # -------------------------------------------------------------------------
    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    def stair_pos(self, p):
        return point_at(self.steps, clamp(p, .001, 1))[0]

    def section(self, cv, t, al):
        T = self.T
        slope = e_io((t - T['rises']) / 1.2) if t >= T['rises'] else 0
        sp = clamp((t - T['eighty'] + .1) / 1.1)

        def fn(d, P, s):
            for i in range(12):
                y0 = lerp(BY0, BY1, i / 12); y1 = lerp(BY0, BY1, (i + 1) / 12)
                c = tuple(int(lerp(a, b, i / 11)) for a, b in zip((22, 44, 70), (40, 62, 84)))
                d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
            # ground under a smooth slope
            gnd = [(BX0, PY0 + 10), (PX0, PY0 + 10)]
            for k in range(21):
                x = lerp(PX0, PX1, k / 20)
                gnd.append((x, lerp(PY0 + 10, PY1 + 10, k / 20)))
            gnd += [(BX1, PY1 + 10), (BX1, BY1), (BX0, BY1)]
            d.polygon([P(*q) for q in gnd], fill=(86, 100, 66, 255))
            # sea level / Hudson (left) and Lake Erie (right)
            d.rectangle((*P(BX0, PY0 - 8), *P(PX0 - 10, PY0 + 10)), fill=WATER + (255,))
            d.rectangle((*P(PX1 + 10, PY1 - 8), *P(BX1, PY1 + 10)), fill=WATER + (255,))
            # sloped land line
            if slope > 0:
                end = (lerp(PX0, PX1, slope), lerp(PY0, PY1, slope))
                d.line([P(PX0, PY0), P(*end)], fill=col(WHITE, .9 if sp < 1 else .35), width=int(5 * s))
            # lock staircase (water steps)
            if sp > 0:
                n = int(NLOCK * sp)
                for k in range(n):
                    x0 = lerp(PX0, PX1, k / NLOCK); x1 = lerp(PX0, PX1, (k + 1) / NLOCK)
                    y = lerp(PY0, PY1, (k + 1) / NLOCK)
                    d.rectangle((*P(x0, y - 6), *P(x1, PY0 + 10 - (PY0 - y) * 0 + 0)), fill=(70, 150, 215, 255))
                    d.line([P(x0, y - 6), P(x0, y + 10)], fill=col(OUTLINE), width=max(1, int(2 * s)))
                    d.line([P(x0, y - 6), P(x1, y - 6)], fill=col((170, 215, 255)), width=max(1, int(2 * s)))
                # re-draw ground below the steps so water sits only in the channel
                low = [(PX0, PY0 + 10)]
                for k in range(21):
                    low.append((lerp(PX0, PX1, k / 20), lerp(PY0 + 22, PY1 + 22, k / 20)))
                low += [(PX1, BY1), (PX0, BY1)]
                d.polygon([P(*q) for q in low], fill=(86, 100, 66, 255))
            # height ruler
            ra = vis(t, T['five'] - .1, T['once'], .3, .3)
            if ra > 0:
                pe = e_out((t - T['five'] + .1) / .7)
                x = PX1 + 40
                d.line([P(x, PY0), P(x, lerp(PY0, PY1, pe))], fill=col(LIME, ra), width=int(6 * s))
                for yy in (PY0, PY1):
                    if yy == PY0 or pe >= 1:
                        d.line([P(x - 18, yy), P(x + 18, yy)], fill=col(LIME, ra), width=int(5 * s))
                d.line([P(PX0 - 40, PY0), P(x, PY0)], fill=col(LIME, .5 * ra), width=int(2 * s))
            # boat climbing
            ba = vis(t, T['lift'] - .3, T['once'], .3, .3)
            if ba > 0:
                pb = e_io((t - T['lift']) / (T['once'] - .4 - T['lift']))
                bx, by = self.stair_pos(lerp(.03, .97, pb))
                d.polygon([P(bx - 26, by - 18), P(bx + 26, by - 18), P(bx + 18, by - 4), P(bx - 18, by - 4)],
                          fill=col(YEL, ba), outline=col(OUTLINE, ba), width=int(3 * s))
                d.rectangle((*P(bx - 8, by - 32), *P(bx + 10, by - 18)), fill=col(WHITE, ba), outline=col(OUTLINE, ba), width=int(2 * s))
            d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (22, 44, 70))
        fn(ImageDraw.Draw(L, 'RGBA'), lambda x, y: ((x - BX0) * 2, (y - BY0) * 2), 2)
        sec = L.reduce(2).convert('RGBA')
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(m)
        paste(cv, with_alpha(sec, al), BX0, BY0)
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        label(cv, 'ALBANY', PX0 - 10, PY0 + 50, t, T['land'], T['once'], 30, WHITE, rise=6, anchor='l')
        label(cv, 'HUDSON · SEA LEVEL', PX0 - 70, PY0 - 40, t, T['land'] + .2, T['once'], 24, (170, 215, 255), rise=6, anchor='l')
        label(cv, 'BUFFALO', PX1 + 30, PY1 + 50, t, T['land'] + .3, T['once'], 30, WHITE, rise=6, anchor='r')
        label(cv, 'LAKE ERIE', PX1 + 50, PY1 - 40, t, T['land'] + .4, T['once'], 24, (170, 215, 255), rise=6, anchor='r')
        label(cv, '≈570 FT', PX1 - 20, (PY0 + PY1) / 2 + 40, t, T['five'] + .2, T['once'], 40, LIME, rise=6, anchor='r')
        label(cv, '83 LOCKS', 380, 520, t, T['locks'], T['once'], 44, (170, 215, 255), rise=8)

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        m.alpha_composite(vignette())
        S = lambda p: Cam.S(st, *p)
        canal = [S(q) for q in self.canal]
        hud = [S(q) for q in self.hudson]
        # Hudson River (teal) - visible from the start, brighter on "Hudson"
        hb = .55 + .45 * vis(t, T['hudson'], T['critics'], .3, .5)
        route(m, hud[:int(len(hud) * .82)], 1.0, TEAL, 5 + 3 * vis(t, T['hudson'], T['critics']), head=False, alpha=hb)
        # canal digs west from Albany: partial during hook, full length on "three"
        if t >= T['ditch']:
            p = lerp(0, .18, e_out((t - T['ditch']) / 1.6))
            if t >= T['three']:
                p = lerp(.18, 1, e_io((t - T['three']) / 1.6))
            route(m, canal, p, LIME, 9, head=False, alpha=1)
            if p < 1:
                (x, y), _ = point_at(canal, max(p, .002))

                def fn(d, P, s, x=x, y=y):                         # shovel at the digging tip
                    d.line([P(x + 6, y - 6), P(x + 34, y - 46)], fill=col((190, 150, 100)), width=int(5 * s))
                    d.polygon([P(x - 6, y + 10), P(x + 14, y - 10), P(x + 2, y - 14), P(x - 14, y + 4)],
                              fill=col((200, 205, 210)), outline=col(OUTLINE), width=int(2 * s))
                vec(m, (x - 30, y - 60, x + 50, y + 30), fn, vis(t, T['ditch'], T['three'] + 1.6, .3, .3), base=WHITE)
        # boats running the canal after it opened
        ba = vis(t, T['once'], T['celebrate'], .4, .4)
        if ba > 0:
            for k in range(3):
                pp = ((t - T['once']) / 6 + k / 3) % 1
                (x, y), ang = point_at(canal, pp)

                def fn(d, P, s, x=x, y=y):
                    d.ellipse((*P(x - 11, y - 11), *P(x + 11, y + 11)), fill=col(YEL), outline=col(OUTLINE), width=int(3 * s))
                vec(m, (x - 20, y - 20, x + 20, y + 20), fn, ba, base=YEL)
        # NYC
        nx, ny = S(self.NYC)
        pin(m, nx, ny, t, -.12, T['erie1'], LIME)
        label(m, 'NEW YORK CITY', nx + 34, ny + 4, t, .2, T['erie1'], 32, WHITE, anchor='l', rise=6)
        pin(m, nx, ny, t, T['erie1'], None, LIME, 12, rings=False)
        label(m, 'NYC', nx + 22, ny + 4, t, T['erie1'] + .2, T['celebrate'], 28, WHITE, anchor='l', rise=6)
        ax, ay = S(self.ALB)
        label(m, 'ALBANY', ax - 26, ay - 30, t, T['ditch'] + .3, T['three'], 28, WHITE, anchor='r', rise=6)
        pin(m, ax, ay, t, T['albany'] - .05, None, ORANGE, 14)
        label(m, 'ALBANY', min(ax - 4, 860), ay + 46, t, T['albany'], T['celebrate'], 30, WHITE, rise=6)
        bx, by = S(self.BUF)
        pin(m, bx, by, t, T['buffalo'] - .05, None, ORANGE, 14)
        label(m, 'BUFFALO', bx + 6, by + 46, t, T['buffalo'], T['celebrate'], 30, WHITE, rise=6)
        le = S(self.geo(-79.6, 42.45))
        label(m, 'LAKE ERIE', max(le[0], 30), le[1] + 40, t, T['lake1'], T['celebrate'], 28, (170, 215, 255), anchor='l', rise=6)
        hx_, hy_ = S(self.geo(-74.2, 41.75))
        label(m, 'HUDSON RIVER', hx_ - 14, hy_, t, T['hudson'], T['critics'], 28, TEAL, anchor='r', rise=6)
        up_ = S(self.geo(-75.8, 42.55))
        label(m, 'UPSTATE NEW YORK', up_[0], up_[1], t, T['upstate'], T['critics'], 32, WHITE, rise=8)
        ec = S(self.geo(-76.3, 43.75))
        chip(m, 'ERIE CANAL', ec[0], ec[1], t, T['erie1'] + .1, T['land'] - .3, size=40, accent=LIME)
        chip(m, "“CLINTON'S DITCH”", ec[0], ec[1] + 90, t, T['clintons'], T['land'] - .3, size=36, accent=ORANGE)
        # celebration: sail down the Hudson, keg poured into the Atlantic
        sa = vis(t, T['sailed'] - .1, None, .3)
        if sa > 0:
            ps = e_io((t - T['sailed']) / (T['poured'] - T['sailed'] - .1))
            route(m, hud[:int(len(hud) * .9)], ps, YEL, 6, head=False, alpha=sa, dashed=True, dash=(14, 10))
            (x, y), _ = point_at(hud[:int(len(hud) * .9)], max(ps, .002))

            def fn(d, P, s, x=x, y=y):
                d.polygon([P(x - 22, y - 8), P(x + 22, y - 8), P(x + 15, y + 6), P(x - 15, y + 6)], fill=col(YEL), outline=col(OUTLINE), width=int(3 * s))
                d.line([P(x, y - 8), P(x, y - 38)], fill=col(OUTLINE), width=int(3 * s))
                d.polygon([P(x + 2, y - 36), P(x + 22, y - 14), P(x + 2, y - 12)], fill=col(WHITE))
            vec(m, (x - 30, y - 45, x + 30, y + 15), fn, sa, base=YEL)
        ka = vis(t, T['poured'] - .1, None, .3)
        if ka > 0:
            kx, ky = S(self.HB)
            kx += 70; ky -= 70
            tilt = lerp(0, 1.1, e_out((t - T['poured']) / .5))

            def fn(d, P, s):
                c, sn = math.cos(tilt), math.sin(tilt)
                R = lambda px, py: P(kx + px * c - py * sn, ky + px * sn + py * c)
                d.polygon([R(-26, -34), R(26, -34), R(32, 0), R(26, 34), R(-26, 34), R(-32, 0)],
                          fill=col((150, 96, 52)), outline=col(OUTLINE), width=int(3 * s))
                for yy in (-18, 18):
                    d.line([R(-30, yy), R(30, yy)], fill=col((70, 60, 54)), width=int(4 * s))
                if t >= T['keg']:
                    for i in range(14):
                        q = ((t - T['keg']) * 1.6 + i / 14) % 1
                        mx = kx + 34 + q * 10 + 6 * math.sin(i)
                        my = ky + 10 + q * 80
                        d.ellipse((*P(mx - 6, my - 6), *P(mx + 6, my + 6)), fill=col(TEAL, 1 - q * .5))
            vec(m, (kx - 60, ky - 60, kx + 90, ky + 110), fn, ka, base=(150, 96, 52))
            ring(m, kx + 40, ky + 95, 34, t, T['water'], None, TEAL, 5)
            ring(m, kx + 40, ky + 95, 60, t, T['water'] + .3, None, TEAL, 3)
            label(m, 'LAKE ERIE WATER', kx - 50, ky - 74, t, T['lake2'], None, 28, TEAL, rise=6)
        at = S(self.geo(-72.9, 40.1))
        chip(m, 'ATLANTIC OCEAN', min(at[0], 760), min(at[1], 900), t, T['atlantic'], None, size=34, accent=TEAL)
        return m

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_section_bg())
            self.section(cv, t, clamp(u * 1.5))
            label(cv, 'HUDSON RIVER → LAKE ERIE', 540, 280, t, 0, None, 28, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area ------------------------------------------------------------
        chip(cv, 'DUG MOSTLY BY HAND', 540, 1270, t, T['hand'], T['busiest'] - .1, size=42, accent=WHITE)
        hero(cv, "AMERICA'S BUSIEST", 540, 1270, t, T['busiest'] - .1, T['erie1'] - .1, 82, LIME)
        label(cv, 'PORT: NEW YORK CITY', 540, 1370, t, T['busiest'] + .1, T['erie1'] - .1, 32, WHITE)
        chip(cv, 'THE ERIE CANAL', 540, 1270, t, T['erie1'], T['eighteen'] - .1, size=48, accent=LIME)
        hero(cv, '1825', 540, 1280, t, T['eighteen'], T['three'] - .1, 130, LIME)
        label(cv, 'GRAND OPENING', 540, 1390, t, T['eighteen'] + .2, T['three'] - .1, 30, WHITE)
        hero(cv, '≈363 MILES', 540, 1280, t, T['three'], T['albany'] - .1, 120, LIME)
        label(cv, 'ACROSS UPSTATE NEW YORK', 540, 1385, t, T['miles'], T['albany'] - .1, 30, WHITE)
        chip(cv, 'ALBANY → BUFFALO', 540, 1270, t, T['albany'], T['critics'] - .1, size=44, accent=ORANGE,
             sub='HUDSON RIVER TO LAKE ERIE')
        chip(cv, 'CRITICS MOCKED IT', 540, 1270, t, T['critics'], T['governor'] - .1, size=42, accent=ORANGE)
        chip(cv, 'GOV. DEWITT CLINTON', 540, 1270, t, T['governor'], T['land'] - .3, size=42, accent=WHITE,
             sub='CHAMPIONED THE CANAL')
        chip(cv, 'THE LAND RISES WEST', 540, 1270, t, T['land'], T['five'] - .1, size=40, accent=WHITE)
        hero(cv, '≈570 FT', 540, 1280, t, T['five'], T['eighty'] - .1, 130, LIME)
        label(cv, 'UPHILL TO LAKE ERIE', 540, 1390, t, T['five'] + .2, T['eighty'] - .1, 30, WHITE)
        hero(cv, '83 LOCKS', 540, 1280, t, T['eighty'], T['once'] - .1, 120, (170, 215, 255))
        label(cv, 'A WATER STAIRCASE FOR BOATS', 540, 1385, t, T['locks'] + .1, T['once'] - .1, 30, WHITE)
        # shipping cost bars
        ca = vis(t, T['cost'] - .1, T['celebrate'] - .1, .3, .3)
        if ca > 0:
            shr = e_io((t - T['fell']) / .9) if t >= T['fell'] else 0

            def fn(d, P, s):
                for y, ln, c in ((1240, 640, (150, 96, 52)), (1320, lerp(640, 64, shr), LIME)):
                    d.rounded_rectangle((*P(250, y - 22), *P(250 + ln, y + 22)), radius=int(10 * s), fill=col(c),
                                        outline=col(OUTLINE), width=int(3 * s))
            vec(cv, (230, 1200, 920, 1360), fn, ca, base=LIME)
            label(cv, 'BEFORE', 236, 1240, t, T['cost'], T['celebrate'] - .1, 28, WHITE, rise=0, anchor='r')
            label(cv, 'CANAL', 236, 1320, t, T['cost'] + .1, T['celebrate'] - .1, 28, WHITE, rise=0, anchor='r')
            label(cv, 'COST TO SHIP A TON OF GOODS', 540, 1180, t, T['shipping'] - .1, T['celebrate'] - .1, 28, (200, 210, 215), rise=0)
        hero(cv, '≈90% CHEAPER', 540, 1420, t, T['ninety'], T['celebrate'] - .1, 80, LIME)
        chip(cv, 'WEDDING OF THE WATERS', 540, 1300, t, T['celebrate'], None, size=40, accent=TEAL, sub='NEW YORK HARBOR · 1825')
        label(cv, 'SOURCES: NY STATE CANALS · NPS', 540, 1595, t, T['celebrate'], None, 18, (200, 210, 215), rise=0)


@functools.lru_cache(None)
def _section_bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
