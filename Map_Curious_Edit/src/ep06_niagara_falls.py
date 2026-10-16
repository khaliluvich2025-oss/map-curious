"""06 - Niagara Falls Is Moving.

Base map: the pack's NASA Blue Marble Northeast US render (03_centralia bbox).
Facts: American Falls dewatered June-Nov 1969 (US Army Corps of Engineers) to study
erosion; falls began at the Niagara Escarpment ~12,000 years ago and have retreated
~7 miles (~11 km) upstream, carving the Niagara Gorge; hard Lockport dolostone caprock
over softer shale is undercut until the ledge collapses; flow diversion for hydropower
has greatly slowed erosion.  Side and plan diagrams are schematic (labelled on screen).
"""
from episode import *
from engine import _head

BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
YEL = (255, 214, 90)
WATER = (52, 120, 178)
LAND = (92, 108, 70)
# plan view (north up)
ESC_Y, FALLS_TODAY, ERIE_Y, ONT_Y = 470, 560, 858, 408
RIVER = [(520, ONT_Y), (540, ESC_Y), (540, 560), (580, 650), (600, 760), (560, ERIE_Y)]


def river_x(y):
    ys = [p[1] for p in RIVER]; xs = [p[0] for p in RIVER]
    return float(np.interp(y, ys, xs))


class EP(Episode):
    slug = '06_Niagara_Falls'
    gfx = '03_centralia'                 # reuse the Northeast US NASA Blue Marble map + bbox
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '06_Niagara_Falls_Final.mp4'
    title = 'Niagara Falls Is Moving'
    cover_title = 'NIAGARA FALLS\nIS MOVING'
    cover_t = 38.5
    emphasis = ['1969,', 'shut', 'moving.', 'Erie', 'Ontario,', 'border', 'Canada.', 'twelve', 'Escarpment.', 'seven',
                'upstream,', 'Gorge.', 'rock.', 'hard', 'shale.', 'scours', 'breaks', 'slower,', 'hydropower.', 'creeping']

    def setup(self):
        w = self.w
        self.base = self.base_map(.84)
        self.F = self.geo(-79.0742, 43.0799)
        self.BUF = self.geo(-78.8784, 42.8864)
        self.TOR = self.geo(-79.3832, 43.6532)
        self.river = spline([self.geo(*p) for p in [(-78.905, 42.88), (-78.97, 42.98), (-79.03, 43.06), (-79.07, 43.10),
                                                      (-79.045, 43.17), (-79.065, 43.26)]], 12)
        T = self.T = dict(
            y1969=w('1969'), engineers=w('engineers'), shut=w('shut'), part=w('part'), they=w('They'), slow=w('slow'),
            moving=w('moving'), river=w('River'), carries=w('carries'), erie1=w('Erie', 1), ontario=w('Ontario'),
            border=w('border'), canada=w('Canada'), about=w('About'), twelve=w('twelve'), began=w('began'),
            escarpment=w('Escarpment'), since=w('Since'), seven=w('seven'), upstream=w('upstream'), carving=w('carving'),
            gorge=w('Gorge'), secret=w('secret'), rock=w('rock'), hard=w('hard'), cap=w('cap'), softer=w('softer'),
            falling=w('Falling'), scours=w('scours'), underneath=w('underneath'), ledge=w('ledge'), breaks=w('breaks'),
            today=w('Today'), slower=w('slower'), diverted=w('diverted'), hydropower=w('hydropower'), but=w('But'),
            creeping=w('creeping'), erie2=w('Erie', 2))
        F = self.F
        self.cam = Cam([
            frame_on(F, 540, 650, 2.7, 0), frame_on(F, 540, 650, 2.4, 1.2), frame_on(F, 540, 650, 2.3, T['river'] - .35),
            frame_on(F, 560, 640, 1.35, T['carries'] + .5), frame_on(F, 560, 640, 1.45, T['about'] - .3),
            frame_on(F, 560, 640, 1.5, self.dur)])
        self.slides = [(1.15, 1), (T['river'] - .35, 0), (T['about'] - .3, 1)]
        b = self.beat
        b(0.0, 'Niagara Falls pin between Lake Erie and Lake Ontario', 'pop', 2)
        b(T['y1969'], '1969 date reveal', 'thud')
        b(1.15, 'Map lifts: schematic side view of the falls', 'whoosh')
        b(T['shut'], 'Cofferdam drops in, water curtain stops', 'thud', -2)
        b(T['part'], 'AMERICAN FALLS TURNED OFF', 'tick')
        b(T['slow'], 'STUDYING EROSION', 'tick')
        b(T['moving'], 'Upstream arrow: THE FALLS ARE MOVING', 'swish')
        b(T['river'] - .35, 'Map returns', 'whoosh')
        b(T['carries'], 'Niagara River flow draws from Erie to Ontario', 'swish')
        b(T['erie1'], 'LAKE ERIE', 'tick')
        b(T['ontario'], 'LAKE ONTARIO', 'tick')
        b(T['border'], 'Border line + CANADA / UNITED STATES', 'pop')
        b(T['about'] - .3, 'Map lifts: schematic plan view', 'whoosh')
        b(T['twelve'], '12,000 YEARS AGO', 'thud')
        b(T['escarpment'], 'Niagara Escarpment ridge highlighted', 'tick')
        b(T['since'], 'Falls retreat upstream, gorge opens behind them', 'rumble')
        b(T['seven'], '7 MILES bracket', 'pop')
        b(T['gorge'], 'NIAGARA GORGE', 'tick')
        b(T['secret'], 'Side view returns', 'swish')
        b(T['hard'], 'HARD CAPROCK layer', 'tick')
        b(T['softer'], 'SOFT SHALE layer', 'tick')
        b(T['scours'], 'Water undercuts the shale', 'rumble')
        b(T['breaks'], 'Ledge breaks off, edge moves upstream', 'thud')
        b(T['today'], 'Plan view: today', 'swish')
        b(T['slower'], 'EROSION SLOWED', 'tick')
        b(T['diverted'], 'Water diverted to power stations', 'swish')
        b(T['creeping'], 'Arrow toward Lake Erie', 'pop')

    # -------------------------------------------------------------------------
    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    def side(self, d, P, s, t):
        """Schematic side view (flow left -> right; upstream is left)."""
        T = self.T
        hook = t < T['about']
        if hook:
            E, u, flow = 640, 70, 1 - e_out((t - T['shut'] - .15) / .7)
            dam = e_out((t - T['shut'] + .1) / .45)
        else:
            u = 95 * e_io((t - T['scours']) / 2.2) if t >= T['scours'] else 0
            br = e_io((t - T['breaks']) / .8) if t >= T['breaks'] else 0
            E = 700 - (u if br >= 1 else 0)
            flow, dam = 1.0, 0
            if br >= 1:
                u = 0
        # sky
        for i in range(10):
            y0 = lerp(BY0, 470, i / 10); y1 = lerp(BY0, 470, (i + 1) / 10)
            c = tuple(int(lerp(a, b, i / 9)) for a, b in zip((22, 44, 70), (60, 92, 116)))
            d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
        d.rectangle((*P(BX0, 470), *P(BX1, BY1)), fill=(54, 46, 40, 255))           # gorge background
        # upstream river + caprock + shale
        d.rectangle((*P(BX0, 440), *P(E, 472)), fill=WATER + (255,))
        d.rectangle((*P(BX0, 470), *P(E, 540)), fill=(150, 152, 162, 255))           # hard cap
        for x in range(BX0 + 10, int(E), 46):
            d.line([P(x, 474), P(x, 536)], fill=(128, 130, 140, 255), width=int(2 * s))
        shale = [(BX0, 540), (E, 540), (E - u * .35, 580), (E - u, 640), (E - u, 800), (E - u * .5, 860), (BX0, 860)]
        d.polygon([P(*q) for q in shale], fill=(146, 98, 76, 255))
        for y in range(560, 860, 22):
            d.line([P(BX0, y), P(E - u - 6, y)], fill=(126, 84, 64, 255), width=int(2 * s))
        d.rectangle((*P(BX0, 860), *P(BX1, BY1)), fill=(80, 68, 56, 255))
        # plunge pool
        d.rectangle((*P(E - u, 790), *P(BX1, 862)), fill=WATER + (255,))
        # talus
        for i in range(7):
            x = E + 40 + i * 38; r = 14 + (i * 7) % 10
            d.ellipse((*P(x - r, 852 - r * .8), *P(x + r, 852 + r * .4)), fill=(136, 138, 146, 255))
        # breaking ledge
        if not hook and T['breaks'] <= t < T['breaks'] + 1.2:
            br = clamp((t - T['breaks']) / .8)
            x0, x1 = 700 - 95, 700
            cx, cy = (x0 + x1) / 2 + br * 60, 505 + br * br * 300
            ang = br * 1.1
            blk = [(-47, -35), (47, -35), (47, 35), (-47, 35)]
            pts = [(cx + px * math.cos(ang) - py * math.sin(ang), cy + px * math.sin(ang) + py * math.cos(ang)) for px, py in blk]
            d.polygon([P(*q) for q in pts], fill=(150, 152, 162, int(255 * (1 - clamp((t - T['breaks'] - .8) / .4)))))
        # water curtain
        if flow > 0.02:
            for k in range(9):
                off = k * 7
                pts = [(E - 4 + off * .2, 446 + off * .4)]
                for j in range(1, 12):
                    q = j / 11
                    pts.append((E + 14 + q * (60 + off), 446 + q * q * (350 - off * .3)))
                d.line([P(*p) for p in pts], fill=(205, 232, 250, int(220 * flow)), width=int(5 * s))
            for k in range(14):
                ph = (t * 1.6 + k / 14) % 1
                x = E + 20 + ph * 70 + (k % 3) * 8; y = 450 + ph * ph * 340
                r = 4 * s / s
                d.ellipse((*P(x - 4, y - 4), *P(x + 4, y + 4)), fill=(240, 250, 255, int(230 * flow)))
            for k in range(6):                                  # mist
                ph = (t * .5 + k / 6) % 1
                x = E + 70 + k * 22; y = 790 - ph * 60; r = 18 + ph * 20
                d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=(230, 240, 250, int(70 * (1 - ph) * flow)))
        # cofferdam (1969)
        if dam > 0:
            dy = (1 - dam) * -160
            d.rectangle((*P(330, 412 + dy), *P(372, 474 + dy)), fill=(110, 104, 96, 255), outline=(230, 230, 220, 255), width=int(3 * s))
        d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))
        return E, u

    def plan(self, d, P, s, t):
        """Schematic plan view, north up: Lake Ontario top, Lake Erie bottom."""
        T = self.T
        d.rectangle((*P(BX0, BY0), *P(BX1, BY1)), fill=LAND + (255,))
        d.rectangle((*P(BX0, ESC_Y), *P(BX1, BY1)), fill=(100, 116, 74, 255))
        d.rectangle((*P(BX0, BY0), *P(BX1, ONT_Y)), fill=WATER + (255,))
        d.rectangle((*P(BX0, ERIE_Y), *P(BX1, BY1)), fill=WATER + (255,))
        # escarpment hatch (teeth face north = downslope)
        hl = vis(t, T['escarpment'], T['since'] + 1.5, .3, .6)
        d.line([P(BX0, ESC_Y), P(BX1, ESC_Y)], fill=col((170, 130, 90)) if not hl else col(ORANGE), width=int(5 * s))
        for x in range(BX0 + 12, BX1, 26):
            d.polygon([P(x - 8, ESC_Y), P(x + 8, ESC_Y), P(x, ESC_Y - 14)], fill=col((150, 112, 78)) if not hl else col(ORANGE))
        # falls position
        if t < T['since']:
            yF = ESC_Y + 4
        elif t < T['gorge']:
            yF = lerp(ESC_Y + 4, FALLS_TODAY, e_io((t - T['since']) / (T['gorge'] - T['since'])))
        else:
            yF = FALLS_TODAY
        # gorge
        if yF > ESC_Y + 5:
            left = [(river_x(y) - 26, y) for y in np.linspace(ESC_Y - 2, yF, 10)]
            right = [(river_x(y) + 26, y) for y in np.linspace(yF, ESC_Y - 2, 10)]
            d.polygon([P(*q) for q in left + right], fill=(58, 48, 40, 255))
        # river
        flow_w = 1 - .45 * vis(t, T['diverted'], None, .8)
        d.line([P(*q) for q in RIVER], fill=WATER + (255,), width=int(22 * s), joint='curve')
        # diversion tunnels -> power stations
        dv = e_out((t - T['diverted']) / 1.0) if t >= T['diverted'] else 0
        if dv > 0:
            for sx in (380, 720):
                pts = [(river_x(640) + (-10 if sx < 540 else 10), 640), (sx, 560), (sx, ESC_Y + 16)]
                seg, ang = partial(pts, dv)
                if len(seg) > 1:
                    L = cumlen(seg); ph = (t * 50) % 30
                    for a0 in np.arange(-ph, L[-1], 30):
                        a1 = min(a0 + 18, L[-1])
                        if a1 > max(a0, 0):
                            sub = partial(seg, a1 / L[-1], max(a0, 0) / L[-1])[0]
                            d.line([P(*q) for q in sub], fill=col(TEAL), width=int(8 * s))
                    _head(d, P, s, seg[-1], ang, 18, col(TEAL))
                if dv >= 1:
                    d.rectangle((*P(sx - 30, ESC_Y + 18), *P(sx + 30, ESC_Y + 52)), fill=(220, 224, 228, 255), outline=col(OUTLINE), width=int(3 * s))
                    d.polygon([P(sx - 8, ESC_Y + 22), P(sx + 4, ESC_Y + 22), P(sx - 2, ESC_Y + 34), P(sx + 8, ESC_Y + 34),
                               P(sx - 6, ESC_Y + 50), P(sx - 1, ESC_Y + 38), P(sx - 10, ESC_Y + 38)], fill=col(YEL))
        # border along the river
        bp = e_out((t - T['about'] - .2) / .8)
        seg, _ = partial(RIVER, bp)
        if len(seg) > 1:
            L = cumlen(seg)
            for a0 in np.arange(0, L[-1], 22):
                sub = partial(seg, min(a0 + 12, L[-1]) / L[-1], a0 / L[-1])[0]
                d.line([P(*q) for q in sub], fill=col(WHITE, .9), width=int(3 * s))
        # falls marker
        fx = river_x(yF)
        d.rectangle((*P(fx - 34, yF - 7), *P(fx + 34, yF + 7)), fill=col(WHITE), outline=col(OUTLINE), width=int(2 * s))
        for k in range(3):
            ph = ((t - T['about']) / 1.5 + k / 3) % 1
            r = 20 + ph * 50
            d.ellipse((*P(fx - r, yF - r), *P(fx + r, yF + r)), outline=col(LIME, (1 - ph) * .9), width=int(4 * s))
        # old position marker
        if t >= T['since'] + .3:
            ox = river_x(ESC_Y + 4)
            d.rectangle((*P(ox - 30, ESC_Y - 2), *P(ox + 30, ESC_Y + 10)), outline=col(WHITE, .8), width=int(3 * s))
        # arrow toward Lake Erie
        ca = e_out((t - T['creeping']) / 1.2) if t >= T['creeping'] else 0
        if ca > 0:
            pts = [(river_x(y), y) for y in np.linspace(FALLS_TODAY + 30, ERIE_Y - 20, 12)]
            seg, ang = partial(pts, ca)
            if len(seg) > 1:
                d.line([P(*q) for q in seg], fill=col(LIME), width=int(8 * s), joint='curve')
                _head(d, P, s, seg[-1], ang, 24, col(LIME))
        d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))
        return fx, yF

    def panel(self, cv, t, al):
        T = self.T
        mode_side = t < T['about'] or T['secret'] - .2 <= t < T['today'] - .2
        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (18, 36, 58))
        d = ImageDraw.Draw(L, 'RGBA')
        P = lambda x, y: ((x - BX0) * 2, (y - BY0) * 2)
        info = self.side(d, P, 2, t) if mode_side else self.plan(d, P, 2, t)
        sec = L.reduce(2).convert('RGBA')
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(Image.fromarray(np.minimum(np.asarray(sec.getchannel('A')), np.asarray(m))))
        # quick crossfade at mode switches
        fade = 1.0
        for a in (T['about'], T['secret'] - .2, T['today'] - .2):
            if a <= t < a + .3:
                fade = .35 + .65 * (t - a) / .3
        shake = math.sin(t * 61) * 6 * (1 - (t - T['breaks']) / .4) if T['breaks'] + .6 <= t < T['breaks'] + 1.0 else 0
        paste(cv, with_alpha(sec, al * fade), BX0 + shake, BY0)
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        if mode_side:
            E, u = info
            label(cv, 'UPSTREAM', 90, 365, t, 0, None, 22, (200, 215, 225), rise=0, anchor='l')
            label(cv, 'DOWNSTREAM', 990, 365, t, 0, None, 22, (200, 215, 225), rise=0, anchor='r')
            if t < T['about']:
                label(cv, 'AMERICAN FALLS, 1969', 540, 400, t, 1.3, T['river'] - .4, 28, WHITE, rise=8)
                label(cv, 'TEMPORARY DAM', 352, 640, t, T['shut'] + .4, T['river'] - .4, 24, WHITE, rise=6)
                al2 = vis(t, T['moving'], T['river'] - .4)
                route(cv, [(560, 600), (300, 600)], e_out((t - T['moving']) / .6), LIME, 10, alpha=al2, head_size=34)
                label(cv, 'UPSTREAM', 430, 650, t, T['moving'] + .3, T['river'] - .4, 30, LIME, rise=6)
            else:
                label(cv, 'HARD CAPROCK', 300, 505, t, T['hard'], T['today'] - .3, 30, WHITE, rise=6)
                label(cv, 'SOFT SHALE', 300, 700, t, T['softer'], T['today'] - .3, 30, WHITE, rise=6)
                label(cv, 'UNDERCUT', 760, 700, t, T['scours'] + .6, T['breaks'], 28, YEL, rise=6)
                if t >= T['breaks'] + .8:
                    route(cv, [(700, 425), (605, 425)], e_out((t - T['breaks'] - .8) / .5), LIME, 8, alpha=vis(t, T['breaks'] + .8, T['today'] - .3), head_size=26)
                    label(cv, 'EDGE MOVES UPSTREAM', 655, 395, t, T['breaks'] + .9, T['today'] - .3, 24, LIME, rise=0)
        else:
            fx, yF = info
            label(cv, 'LAKE ONTARIO', 540, 370, t, T['about'], None, 30, WHITE, rise=0)
            label(cv, 'LAKE ERIE', 540, 895, t, T['about'], None, 30, WHITE, rise=0)
            label(cv, 'CANADA', 230, 700, t, T['about'] + .3, None, 30, (235, 240, 230), rise=0)
            label(cv, 'U.S.', 850, 700, t, T['about'] + .3, None, 30, (235, 240, 230), rise=0)
            label(cv, 'NIAGARA ESCARPMENT', 240, 445, t, T['escarpment'], T['today'] - .3, 24, ORANGE, rise=6)
            label(cv, 'FALLS', fx + 50, yF, t, T['about'] + .2, None, 26, LIME, anchor='l', rise=0)
            if T['seven'] - .1 <= t < T['today'] - .3:
                pr = vis(t, T['seven'] - .1, T['today'] - .3)
                route(cv, [(680, ESC_Y + 4), (680, FALLS_TODAY)], 1, LIME, 5, head=False, alpha=pr)
                route(cv, [(668, ESC_Y + 4), (692, ESC_Y + 4)], 1, LIME, 5, head=False, alpha=pr)
                route(cv, [(668, FALLS_TODAY), (692, FALLS_TODAY)], 1, LIME, 5, head=False, alpha=pr)
                label(cv, '≈7 MILES', 705, (ESC_Y + FALLS_TODAY) / 2, t, T['seven'], T['today'] - .3, 28, LIME, anchor='l', rise=0)
            label(cv, 'GORGE', 455, 520, t, T['gorge'], T['today'] - .3, 26, WHITE, rise=6)
            label(cv, 'POWER STATIONS', 540, 538, t, T['hydropower'], T['creeping'] - .2, 22, YEL, rise=6)

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        S = lambda p: Cam.S(st, *p)
        scr = [S(q) for q in self.river]
        route(m, scr, e_io((t - T['carries']) / 1.4), TEAL, 9, alpha=vis(t, T['carries']), dashed=True, dash=(20, 12),
              phase=-t * 50, head_size=30)
        m.alpha_composite(vignette())
        fx, fy = S(self.F)
        pin(m, fx, fy, t, -.12, None, LIME)
        chip(m, 'NIAGARA FALLS', fx, fy - 125, t, -.1, 1.15, size=42, sub='U.S. – CANADA')
        e = S(self.geo(-80.15, 42.45)); o = S(self.geo(-78.0, 43.62))
        chip(m, 'LAKE ERIE', e[0] + 40, e[1], t, T['erie1'], None, size=38, accent=TEAL)
        chip(m, 'LAKE ONTARIO', o[0], o[1], t, T['ontario'], None, size=38, accent=TEAL)
        c = S(self.geo(-80.3, 44.25)); us = S(self.geo(-77.8, 42.35))
        label(m, 'CANADA', c[0], c[1], t, T['border'] + .1, None, 40, WHITE)
        label(m, 'UNITED STATES', us[0], us[1], t, T['canada'], None, 40, WHITE)
        bx, by = S(self.BUF); tx, ty = S(self.TOR)
        pin(m, bx, by, t, T['erie1'] + .3, None, WHITE, 8, rings=False)
        label(m, 'BUFFALO', bx + 18, by + 4, t, T['erie1'] + .35, None, 24, WHITE, anchor='l', rise=0)
        pin(m, tx, ty, t, T['ontario'] + .3, None, WHITE, 8, rings=False)
        label(m, 'TORONTO', tx - 18, ty + 4, t, T['ontario'] + .35, None, 24, WHITE, anchor='r', rise=0)
        return m

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_bg())
            self.panel(cv, t, clamp(u * 1.5))
            label(cv, 'NIAGARA FALLS', 540, 280, t, 0, None, 30, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area ----------------------------------------------------------
        hero(cv, '1969', 540, 1290, t, T['y1969'], T['part'] - .1, 130, LIME)
        chip(cv, 'AMERICAN FALLS TURNED OFF', 540, 1270, t, T['part'], T['slow'] - .1, size=38, accent=LIME, sub='FOR ABOUT FIVE MONTHS')
        chip(cv, 'STUDYING EROSION', 540, 1270, t, T['slow'], T['moving'] - .1, size=40, accent=TEAL)
        hero(cv, 'THE FALLS ARE MOVING', 540, 1285, t, T['moving'], T['river'] - .4, 64, WHITE)
        chip(cv, 'U.S.–CANADA BORDER', 540, 1270, t, T['border'], T['about'] - .4, size=40)
        hero(cv, '≈12,000 YEARS AGO', 540, 1285, t, T['twelve'], T['since'] - .1, 82, LIME)
        hero(cv, '≈7 MILES UPSTREAM', 540, 1285, t, T['seven'], T['secret'] - .3, 82, LIME)
        chip(cv, 'NIAGARA GORGE', 540, 1400, t, T['gorge'], T['secret'] - .3, size=36, accent=WHITE)
        chip(cv, 'THE SECRET IS IN THE ROCK', 540, 1270, t, T['rock'], T['scours'] - .1, size=38, accent=LIME)
        chip(cv, 'WATER UNDERCUTS THE SHALE', 540, 1270, t, T['scours'], T['breaks'] - .1, size=38, accent=YEL)
        chip(cv, 'THE LEDGE BREAKS OFF', 540, 1270, t, T['breaks'], T['today'] - .2, size=40, accent=ORANGE)
        chip(cv, 'EROSION HAS SLOWED', 540, 1270, t, T['slower'] - .1, T['diverted'] - .1, size=40, accent=TEAL)
        chip(cv, 'WATER DIVERTED FOR HYDROPOWER', 540, 1270, t, T['diverted'], T['creeping'] - .2, size=34, accent=TEAL)
        chip(cv, 'STILL MOVING TOWARD LAKE ERIE', 540, 1270, t, T['creeping'], None, size=36, accent=LIME)
        label(cv, 'SOURCES: USGS · NPS · NIAGARA PARKS', 540, 1595, t, T['today'], None, 18, (200, 210, 215), rise=0)


@functools.lru_cache(None)
def _bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
