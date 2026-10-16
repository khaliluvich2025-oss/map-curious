"""08 - The Highway Across the Ocean (Overseas Highway, Florida Keys).

Base map: the pack's NASA Blue Marble Florida/Cuba render (01_fort_jefferson bbox).
Facts: Overseas Highway ~113 mi, ~42 bridges incl. Seven Mile Bridge (FDOT); built on
Flagler's Overseas Railroad, which reached Key West in 1912; 1935 Labor Day hurricane
wrecked it; highway opened 1938; Key West ~90 mi from Cuba, nearer Havana than Miami.
Route line is generalised along US-1; distances computed great-circle in code.
"""
from episode import *
from engine import _head
from scipy import ndimage as nd

ROUTE = [(-80.48, 25.45), (-80.43, 25.10), (-80.53, 25.01), (-80.63, 24.92), (-80.83, 24.82), (-81.09, 24.71),
         (-81.12, 24.705), (-81.23, 24.68), (-81.36, 24.67), (-81.55, 24.65), (-81.78, 24.555)]
SEVEN = [(-81.12, 24.705), (-81.23, 24.68)]
HURR = (-80.65, 24.90)
KW, HAV, MIA = (-81.78, 24.555), (-82.359, 23.136), (-80.1918, 25.7617)
YEL = (255, 214, 90)


def miles(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


class EP(Episode):
    slug = '08_Overseas_Highway'
    gfx = '01_fort_jefferson'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '08_Overseas_Highway_Final.mp4'
    title = 'The Highway Across the Ocean'
    cover_title = 'THE HIGHWAY\nACROSS THE\nOCEAN'
    cover_t = 1.9
    emphasis = ['ocean', 'hundred', 'Overseas', 'Highway,', 'Keys.', 'forty', 'Seven', 'Mile', 'railroad.', "Flagler's",
                '1912.', '1935,', 'hurricane', 'wrecked', 'road,', '1938.', 'ninety', 'Cuba,', 'Havana', 'Miami.']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        self.florida = Region(svg_polys(self.G / 'region_highlight.svg'))
        g = self.geo
        self.route = spline([g(*p) for p in ROUTE], 10)
        self.seven = [g(*p) for p in SEVEN]
        self.KW, self.HAV, self.MIA, self.HU = g(*KW), g(*HAV), g(*MIA), g(*HURR)
        self._build_cuba()
        T = self.T = dict(
            highway=w('highway'), ocean=w('ocean'), hundred=w('hundred'), overseas=w('Overseas', 1), linking=w('linking'),
            mainland=w('mainland'), keywest=w('Key', 1), chain=w('chain'), keys=w('Keys'), forty=w('forty'),
            seven=w('Seven'), began=w('began'), railroad=w('railroad', 1), henry=w('Henry'), reached=w('reached'),
            y1912=w('1912'), but=w('But'), y1935=w('1935'), hurricane=w('hurricane'), wrecked=w('wrecked'),
            instead=w('Instead'), trains=w('trains'), turned=w('turned'), road1=w('road', 1), y1938=w('1938'),
            at=w('At'), road2=w('road', 2), sits=w('sits'), ninety=w('ninety'), cuba=w('Cuba'), closer=w('closer'),
            havana=w('Havana'), miami=w('Miami'))
        keys_mid = (666, 930)
        south = ((self.KW[0] + self.HAV[0] + self.MIA[0]) / 3, (self.KW[1] + self.HAV[1] + self.MIA[1]) / 3)
        self.cam = Cam([
            frame_on(keys_mid, 540, 640, 3.4, 0), frame_on(keys_mid, 540, 640, 3.1, T['overseas']),
            frame_on(keys_mid, 560, 600, 2.4, T['mainland'] + .6), frame_on(keys_mid, 560, 620, 2.6, T['forty']),
            frame_on(self.g7(), 540, 640, 3.4, T['seven'] + .4), frame_on(keys_mid, 540, 640, 2.8, T['began'] + .4),
            frame_on(self.HU, 540, 620, 3.2, T['hurricane'] + .3), frame_on(keys_mid, 540, 640, 2.7, T['instead'] + .4),
            frame_on(keys_mid, 540, 640, 2.6, T['at'] - .3), frame_on(south, 540, 650, 2.1, T['ninety'] + .2),
            frame_on(south, 540, 650, 2.2, self.dur)])
        self.d_cuba = miles(KW, self.cuba_pt_geo)
        self.d_hav = miles(KW, HAV)
        self.d_mia = miles(KW, MIA)
        b = self.beat
        b(0.0, 'Florida Keys from above, highway starts drawing', 'whoosh', 2)
        b(T['ocean'], 'Car drives the route across the water', 'swish')
        b(T['hundred'], '113 MILES', 'thud')
        b(T['overseas'], 'OVERSEAS HIGHWAY', 'pop')
        b(T['mainland'], 'Mainland Florida fills; camera pulls back', 'tick')
        b(T['keywest'], 'KEY WEST pin', 'pop')
        b(T['keys'], 'FLORIDA KEYS label', 'tick')
        b(T['forty'], 'Bridge ticks along the route: ~40 BRIDGES', 'tick')
        b(T['seven'], 'Seven Mile Bridge highlighted', 'pop')
        b(T['began'], 'Route turns into a railroad', 'swish')
        b(T['henry'], "FLAGLER'S OVERSEAS RAILROAD + train", 'tick')
        b(T['y1912'], '1912', 'thud')
        b(T['y1935'], '1935', 'thud')
        b(T['hurricane'], 'Hurricane spiral sweeps the Keys', 'rumble', 2)
        b(T['wrecked'], 'Track sections break', 'thud')
        b(T['instead'], 'Rails fade', 'tick')
        b(T['road1'], 'Route rebuilt as a road', 'swish')
        b(T['y1938'], '1938', 'thud')
        b(T['at'], 'Camera heads south to Key West', 'whoosh')
        b(T['ninety'], 'Cuba outlined, ~90 MI line', 'pop')
        b(T['havana'], 'Havana distance line', 'tick')
        b(T['miami'], 'Miami distance line: closer to Havana', 'pop')

    def g7(self):
        return ((self.seven[0][0] + self.seven[1][0]) / 2, (self.seven[0][1] + self.seven[1][1]) / 2)

    def _build_cuba(self):
        im = np.asarray(Image.open(self.G / 'map_terrain.jpg').convert('RGB'), np.int16)
        R, G, B = im[..., 0], im[..., 1], im[..., 2]
        land = (G > B + 4) & (R < G + 10)
        land = nd.binary_opening(land, iterations=1)
        lab, _ = nd.label(land)
        hx, hy = self.geo(-79.5, 22.0)                        # central Cuba seed
        m = nd.binary_fill_holes(lab == lab[int(hy), int(hx)])
        big = Image.fromarray((m * 255).astype(np.uint8)).resize((W * 2, H * 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.5))
        m2 = np.asarray(big) > 127
        edge = m2 & ~nd.binary_erosion(m2, iterations=5)
        fill = np.zeros((H * 2, W * 2, 4), np.uint8); fill[m2] = ORANGE + (95,)
        bord = np.zeros((H * 2, W * 2, 4), np.uint8); bord[edge] = WHITE + (235,)
        self.cuba = (Image.fromarray(fill, 'RGBA'), Image.fromarray(bord, 'RGBA'))
        ys, xs = np.where(m)
        kx, ky = self.geo(*KW)
        i = np.argmin((xs - kx) ** 2 + (ys - ky) ** 2)
        self.cuba_pt = (float(xs[i]), float(ys[i]))
        b = self.bbox
        self.cuba_pt_geo = (b[0] + self.cuba_pt[0] / W * (b[2] - b[0]), b[3] - self.cuba_pt[1] / H * (b[3] - b[1]))

    # -------------------------------------------------------------------------
    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        S = lambda p: Cam.S(st, *p)
        self.draw_map(cv, st)
        self.florida.draw(cv, st, t, T['mainland'] - .05, T['at'], fill_a=.22, alpha=.9)
        ca = vis(t, T['cuba'] - .2, None, .5)
        if ca > 0:
            cv.alpha_composite(with_alpha(render_map(self.cuba[0], st, 2.0), ca))
            cv.alpha_composite(with_alpha(render_map(self.cuba[1], st, 2.0), ca))
        cv.alpha_composite(vignette())
        scr = [S(q) for q in self.route]
        rail = vis(t, T['began'], T['road1'], .5, .6)
        road = 1 - rail
        # road line
        pr = e_io(t / 2.2)
        route(cv, scr, pr, LIME, 9, head=False, alpha=road)
        # bridge ticks
        if t >= T['forty'] - .1:
            nt = int(42 * clamp((t - T['forty'] + .1) / 1.4))
            L = cumlen(scr)
            ticks = [point_at(scr, (k + .5) / 42) for k in range(nt)]

            def fn(d, P, s):
                for (x, y), ang in ticks:
                    nx, ny = -math.sin(ang), math.cos(ang)
                    d.line([P(x - nx * 11, y - ny * 11), P(x + nx * 11, y + ny * 11)], fill=col(WHITE, .9), width=int(3 * s))
            vec(cv, bbox_of(scr, 30), fn, vis(t, T['forty'] - .1, T['began'], .2, .4))
        # seven mile bridge
        s7 = [S(q) for q in self.seven]
        route(cv, s7, e_out((t - T['seven']) / .7), YEL, 15, head=False, alpha=vis(t, T['seven'], T['began'] + .2))
        # railroad style
        if rail > 0:
            def fn(d, P, s):
                d.line([P(*q) for q in scr], fill=col((70, 54, 40)), width=int(10 * s), joint='curve')
                Ltot = cumlen(scr)[-1]
                for k in range(int(Ltot // 12)):
                    (x, y), ang = point_at(scr, (k + .5) * 12 / Ltot)
                    nx, ny = -math.sin(ang), math.cos(ang)
                    d.line([P(x - nx * 9, y - ny * 9), P(x + nx * 9, y + ny * 9)], fill=col((210, 200, 186)), width=int(3 * s))
                d.line([P(*q) for q in scr], fill=col((150, 150, 158)), width=int(3 * s), joint='curve')
            vec(cv, bbox_of(scr, 30), fn, rail)
            # breaks after the hurricane
            if t >= T['wrecked'] - .1:
                bk = vis(t, T['wrecked'] - .1, T['road1'], .2, .5)
                for p_ in (.18, .27, .36, .44):
                    (x, y), _ = point_at(scr, p_)
                    def fx(d, P, s, x=x, y=y):
                        d.line([P(x - 12, y - 12), P(x + 12, y + 12)], fill=col(RED), width=int(6 * s))
                        d.line([P(x - 12, y + 12), P(x + 12, y - 12)], fill=col(RED), width=int(6 * s))
                    vec(cv, (x - 20, y - 20, x + 20, y + 20), fx, bk, base=RED)
        # vehicles: car (road) / train (rail)
        def vehicle(p, kind, al):
            if al <= 0:
                return
            (x, y), ang = point_at(scr, clamp(p, .002, 1))

            def fn(d, P, s):
                c, s_ = math.cos(ang), math.sin(ang)
                Lh, Wh = (16, 8) if kind == 'car' else (24, 8)
                pts = [(-Lh, -Wh), (Lh, -Wh), (Lh, Wh), (-Lh, Wh)]
                q = [P(x + px * c - py * s_, y + px * s_ + py * c) for px, py in pts]
                d.polygon(q, fill=col(WHITE if kind == 'car' else (60, 60, 64)), outline=col(OUTLINE), width=int(3 * s))
                if kind == 'train':
                    d.ellipse((*P(x - 4, y - 4), *P(x + 4, y + 4)), fill=col(YEL))
            vec(cv, (x - 40, y - 40, x + 40, y + 40), fn, al, base=WHITE)
        vehicle(e_io(t / 2.6), 'car', vis(t, .1, T['overseas'] + .6))
        vehicle(e_io((t - T['henry']) / 3.0), 'train', vis(t, T['henry'], T['y1935'], .3, .3))
        vehicle(e_io((t - T['road1']) / 3.0), 'car', vis(t, T['road1'] + .1, T['at'], .3, .3))
        # hurricane
        ha = vis(t, T['hurricane'] - .2, T['instead'] - .2, .4, .5)
        if ha > 0:
            hx, hy = S(self.HU)
            hx += (1 - e_io((t - T['hurricane'] + .2) / 1.8)) * 160
            rot = t * 4

            def fn(d, P, s):
                for arm in range(3):
                    pts = []
                    for k in range(40):
                        r = 8 + k * 2.6
                        a = rot + arm * 2.09 + k * .16
                        pts.append(P(hx + r * math.cos(a), hy + r * math.sin(a)))
                    d.line(pts, fill=col((235, 240, 245), .85), width=int(9 * s), joint='curve')
                d.ellipse((*P(hx - 10, hy - 10), *P(hx + 10, hy + 10)), fill=col((30, 40, 60)))
            vec(cv, (hx - 130, hy - 130, hx + 130, hy + 130), fn, ha)
        # pins / labels
        kx, ky = S(self.KW)
        pin(cv, kx, ky, t, T['keywest'] - .05, None, LIME, 14)
        label(cv, 'KEY WEST', kx - 22, ky + 4, t, T['keywest'], None, 30, WHITE, anchor='r', rise=6)
        fl = S(self.geo(-81.3, 26.6))
        chip(cv, 'MAINLAND FLORIDA', fl[0], fl[1], t, T['mainland'], T['seven'] - .3, size=34)
        kl = S(self.geo(-80.95, 24.95))
        label(cv, 'FLORIDA KEYS', kl[0] - 20, kl[1] - 40, t, T['keys'], T['at'], 30, YEL, rise=6)
        sx, sy = S(self.g7())
        chip(cv, 'SEVEN MILE BRIDGE', sx, sy - 110, t, T['seven'] + .1, T['began'] + .2, size=36, accent=YEL)
        # distances to Cuba / Havana / Miami
        cx_, cy_ = S(self.cuba_pt); hx_, hy_ = S(self.HAV); mx, my = S(self.MIA)
        a_c, a_h, a_m = T['ninety'], T['havana'] - .2, T['miami'] - .2
        route(cv, [(kx, ky), (cx_, cy_)], e_out((t - a_c) / .6), WHITE, 5, head=True, alpha=vis(t, a_c, T['havana'] - .3), dashed=True, dash=(12, 8), head_size=18)
        label(cv, '≈90 MI', (kx + cx_) / 2 + 20, (ky + cy_) / 2, t, a_c + .3, T['havana'] - .3, 32, WHITE, anchor='l', rise=0)
        pin(cv, hx_, hy_, t, a_h, None, ORANGE, 12, rings=False)
        label(cv, 'HAVANA', hx_ - 22, hy_ + 4, t, a_h + .05, None, 30, WHITE, anchor='r', rise=6)
        route(cv, [(kx, ky), (hx_, hy_)], e_out((t - a_h) / .6), ORANGE, 6, head=False, alpha=vis(t, a_h))
        label(cv, f'≈{round(self.d_hav / 5) * 5} MI', (kx + hx_) / 2 - 18, (ky + hy_) / 2, t, a_h + .3, None, 30, ORANGE, anchor='r', rise=0)
        pin(cv, mx, my, t, a_m, None, TEAL, 12, rings=False)
        label(cv, 'MIAMI', mx + 22, my + 4, t, a_m + .05, None, 30, WHITE, anchor='l', rise=6)
        route(cv, [(kx, ky), (mx, my)], e_out((t - a_m) / .6), TEAL, 6, head=False, alpha=vis(t, a_m))
        label(cv, f'≈{round(self.d_mia / 5) * 5} MI', (kx + mx) / 2 + 22, (ky + my) / 2, t, a_m + .3, None, 30, TEAL, anchor='l', rise=0)
        cb = S(self.geo(-79.8, 22.3))
        chip(cv, 'CUBA', cb[0], cb[1], t, T['cuba'], None, size=38, accent=ORANGE)
        # lower info area --------------------------------------------------------
        hero(cv, '113 MILES', 540, 1280, t, T['hundred'] - .1, T['overseas'] + .9, 120, LIME)
        label(cv, 'ACROSS THE WATER', 540, 1385, t, T['hundred'] + .1, T['overseas'] + .9, 28, WHITE)
        chip(cv, 'OVERSEAS HIGHWAY', 540, 1270, t, T['overseas'] + 1.0, T['forty'] - .2, size=44, accent=LIME, sub='U.S. ROUTE 1')
        chip(cv, '≈40 BRIDGES', 540, 1270, t, T['forty'], T['seven'] - .1, size=44, accent=WHITE)
        chip(cv, 'FAMOUS: SEVEN MILE BRIDGE', 540, 1270, t, T['seven'], T['began'] - .1, size=36, accent=YEL)
        chip(cv, "FLAGLER'S OVERSEAS RAILROAD", 540, 1260, t, T['henry'], T['y1912'] - .1, size=36, accent=WHITE)
        hero(cv, '1912', 540, 1290, t, T['y1912'], T['y1935'] - .2, 130, LIME)
        label(cv, 'RAILROAD REACHES KEY WEST', 540, 1395, t, T['y1912'] + .1, T['y1935'] - .2, 28, WHITE)
        hero(cv, '1935', 540, 1290, t, T['y1935'], T['instead'] - .2, 130, RED)
        label(cv, 'LABOR DAY HURRICANE', 540, 1395, t, T['labor'] if 'labor' in T else T['hurricane'] - .2, T['instead'] - .2, 28, WHITE)
        hero(cv, '1938', 540, 1290, t, T['y1938'], T['at'] - .2, 130, LIME)
        label(cv, 'REOPENED AS A HIGHWAY', 540, 1395, t, T['y1938'] + .1, T['at'] - .2, 28, WHITE)
        chip(cv, 'CLOSER TO HAVANA THAN MIAMI', 540, 1270, t, T['closer'], None, size=34, accent=ORANGE)
        label(cv, 'SOURCES: FDOT · NPS · NOAA', 540, 1595, t, T['at'], None, 18, (200, 210, 215), rise=0)
