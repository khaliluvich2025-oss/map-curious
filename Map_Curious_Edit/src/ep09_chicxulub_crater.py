"""09 - The Dinosaur-Killer Crater (Chicxulub, Yucatan Peninsula, Mexico).

Base map: the pack's NASA Blue Marble Florida/Cuba/Yucatan render (01_fort_jefferson bbox).
Facts: impact about 66 million years ago (USGS/NASA); impactor roughly 6 mi (~10 km) wide;
crater roughly 110 mi (~180 km) across, buried under limestone, centred near Chicxulub Puerto,
about half on land and half offshore; found in late-1970s oil (Pemex) geophysical surveys;
a ring of cenotes (sinkholes) traces the crater's buried rim. Ring drawn as a 90 km-radius
circle around (-89.52, 21.35); cenote dots placed only where that circle falls on land.
"""
from episode import *
from scipy import ndimage as nd

CENTER = (-89.52, 21.35)
RAD_KM = 90
YEL = (255, 214, 90)
STONE = (214, 196, 160)


class EP(Episode):
    slug = '09_Chicxulub_Crater'
    gfx = '01_fort_jefferson'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '09_Chicxulub_Crater_Final.mp4'
    title = 'The Dinosaur-Killer Crater'
    cover_title = 'THE CRATER\nTHAT KILLED THE\nDINOSAURS'
    cover_t = 19.6
    emphasis = ['asteroid', 'dinosaurs', 'scar', 'map.', "Mexico's", 'Yucatán', 'sixty-six', 'million', 'six', 'slammed',
                'crater', 'hundred', 'ten', 'three', 'quarters', 'buried', 'limestone,', 'land', 'Gulf', 'Oil', '1970s.',
                'ring', 'sinkholes,', 'cenotes.']

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        g = self.geo
        self.C = g(*CENTER)
        lat = math.radians(CENTER[1])
        b = self.bbox
        self.rx = RAD_KM / (111.32 * math.cos(lat)) / (b[2] - b[0]) * W
        self.ry = RAD_KM / 111.0 / (b[3] - b[1]) * H
        self._build_masks()
        T = self.T = dict(
            asteroid=w('asteroid'), dino1=w('dinosaurs', 1), scar=w('scar'), find=w('find'), map=w('map'),
            here=w('here'), northern=w('northern'), mexico=w("Mexico's"), yuc=w('Peninsula') - .4, about=w('About'),
            million=w('million'), rock=w('rock'), six=w('six', 1), slammed=w('slammed'), shallow=w('shallow'),
            blasted=w('blasted'), hundred=w('hundred'), across=w('across'), helped=w('helped'), three=w('three'),
            species=w('species'), earth=w('Earth'), dino2=w('dinosaurs', 2), today=w('Today'), buried=w('buried'),
            limestone=w('limestone'), half1=w('half', 1), land=w('land'), half2=w('half', 2), gulf=w('Gulf'),
            oil=w('Oil'), geologists=w('geologists'), spotted=w('spotted'), y1970=w('1970s'), but=w('But'),
            trace=w('trace'), edge=w('edge'), curving=w('curving'), ring=w('ring'), sinkholes=w('sinkholes'),
            cenotes=w('cenotes'))
        C = self.C
        self.cam = Cam([
            frame_on(C, 200, 640, 3.0, 0), frame_on(C, 200, 640, 2.7, T['find']),
            frame_on(C, 200, 700, 1.6, T['map'] + .5), frame_on(C, 200, 700, 1.6, T['northern'] - .2),
            frame_on(C, 200, 560, 2.5, T['mexico'] + .4), frame_on(C, 200, 600, 2.4, T['about'] + .3),
            frame_on(C, 200, 640, 3.2, T['slammed'] + .2), frame_on(C, 200, 620, 2.9, T['blasted'] + .4),
            frame_on(C, 200, 560, 2.6, T['three']), frame_on(C, 200, 560, 2.5, T['dino2'] + .2),
            frame_on(C, 200, 620, 2.4, T['today'] + .3), frame_on(C, 200, 720, 1.9, T['gulf'] + .3),
            frame_on(C, 200, 640, 2.8, T['oil'] + .4), frame_on(C, 200, 640, 2.8, T['but'] - .1),
            frame_on(C, 200, 600, 3.4, T['curving']), frame_on(C, 200, 600, 3.4, self.dur)])
        bt = self.beat
        bt(0.0, 'Yucatan coast close-up, impact pin + DINOSAUR KILLER chip', 'whoosh', 2)
        bt(.25, 'Meteor streaks in toward the pin', 'swish')
        bt(1.45, 'Impact flash + shockwave', 'thud')
        bt(T['scar'], 'Crater ring draws on (dashed)', 'pop')
        bt(T['map'], 'Camera pulls back: Gulf, Florida, Cuba', 'whoosh')
        bt(T['here'], 'HERE chip on pin', 'pop')
        bt(T['northern'], 'Camera pushes into the Yucatan', 'swish')
        bt(T['mexico'], 'MEXICO label', 'tick')
        bt(T['yuc'], 'YUCATAN PENINSULA label', 'tick')
        bt(T['about'], '66 MILLION YEARS AGO', 'thud')
        bt(T['rock'], 'Asteroid appears, ~6 MILES WIDE', 'pop')
        bt(T['slammed'], 'Asteroid hits: flash + shockwaves', 'thud', 2)
        bt(T['shallow'], 'SHALLOW SEA chip', 'tick')
        bt(T['blasted'], 'Crater ring burns in orange', 'rumble')
        bt(T['hundred'], 'Diameter line: ~110 MILES ACROSS', 'pop')
        bt(T['three'], '3/4 OF ALL SPECIES hero', 'thud')
        bt(T['species'], 'Species dots: three of four crossed out', 'tick')
        bt(T['dino2'], 'INCLUDING THE DINOSAURS chip', 'pop')
        bt(T['today'], 'Camera re-frames, ring dims', 'swish')
        bt(T['buried'], 'Limestone layers cover the crater', 'thud')
        bt(T['half1'], 'Land half fills lime: HALF ON LAND', 'pop')
        bt(T['half2'], 'Sea half fills teal: HALF UNDER THE GULF', 'pop')
        bt(T['gulf'], 'GULF OF MEXICO label, camera widens', 'tick')
        bt(T['oil'], 'Survey ship + OIL SURVEYS chip', 'swish')
        bt(T['spotted'], 'Survey lines sweep the crater', 'tick')
        bt(T['y1970'], 'LATE 1970s hero', 'thud')
        bt(T['but'], 'Camera pushes in to the rim', 'whoosh')
        bt(T['trace'], 'Cenote dots trace the rim', 'tick')
        bt(T['ring'], 'Cenote ring complete', 'pop')
        bt(T['sinkholes'], 'RING OF SINKHOLES chip', 'tick')
        bt(T['cenotes'], 'CENOTES hero', 'pop')

    def _build_masks(self):
        im = np.asarray(Image.open(self.G / 'map_terrain.jpg').convert('RGB'), np.int16)
        R, G, B = im[..., 0], im[..., 1], im[..., 2]
        land = (G > B + 4) & (R < G + 10)
        land = nd.binary_opening(land, iterations=1)
        self.landmask = land
        yy, xx = np.mgrid[0:H * 2, 0:W * 2]
        cx, cy = self.C[0] * 2, self.C[1] * 2
        ell = ((xx - cx) / (self.rx * 2)) ** 2 + ((yy - cy) / (self.ry * 2)) ** 2 <= 1
        big = Image.fromarray((land * 255).astype(np.uint8)).resize((W * 2, H * 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.5))
        l2 = np.asarray(big) > 127
        a = np.zeros((H * 2, W * 2, 4), np.uint8); a[ell & l2] = LIME + (120,)
        s = np.zeros((H * 2, W * 2, 4), np.uint8); s[ell & ~l2] = TEAL + (120,)
        self.half_land, self.half_sea = Image.fromarray(a, 'RGBA'), Image.fromarray(s, 'RGBA')
        # cenote dots: points of the rim circle that fall on land, ordered west -> south -> east
        self.cenotes = []
        for k in range(72):
            ang = math.pi + k * 2 * math.pi / 72          # start west, sweep through south (screen y down)
            x = self.C[0] + self.rx * math.cos(ang)
            y = self.C[1] - self.ry * math.sin(ang)
            if 0 <= x < W and 0 <= y < H and land[int(y), int(x)]:
                self.cenotes.append((x, y))

    def ell_pts(self, st, scale=1.0, n=120):
        return [Cam.S(st, self.C[0] + self.rx * scale * math.cos(2 * math.pi * k / n - math.pi / 2),
                      self.C[1] + self.ry * scale * math.sin(2 * math.pi * k / n - math.pi / 2)) for k in range(n + 1)]

    def impact(self, cv, x, y, t, a, big=1.0):
        """Flash + expanding shockwave rings at screen (x, y) starting at time a."""
        if t < a or t > a + 2.0:
            return
        u = t - a
        fl = clamp(1 - u / .45)
        if fl > 0:
            def fn(d, P, s):
                for k in range(6):
                    r = (30 + 140 * big * e_out(u / .3)) * (1 - k * .14)
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=col((255, 240, 200), .22))
            R = 200 * big
            vec(cv, (x - R, y - R, x + R, y + R), fn, fl, base=(255, 240, 200))
        for k in range(3):
            p = clamp((u - k * .25) / 1.3)
            if 0 < p < 1:
                r = (20 + 330 * big * e_out(p))

                def fr(d, P, s, r=r, p=p):
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), outline=col(ORANGE if k == 0 else WHITE, (1 - p) * .9),
                              width=int((8 - k * 2) * s))
                vec(cv, (x - r - 10, y - r - 10, x + r + 10, y + r + 10), fr, 1.0, base=ORANGE)

    def meteor(self, cv, t, a, d, start, end, size):
        """Rock flying from screen point start to end over [a, a+d]."""
        if t < a or t > a + d:
            return
        p = e_io((t - a) / d) ** 1.6
        x, y = lerp(start[0], end[0], p), lerp(start[1], end[1], p)
        p0 = max(0, p - .35)
        tx, ty = lerp(start[0], end[0], p0), lerp(start[1], end[1], p0)
        route(cv, [(tx, ty), (x, y)], 1.0, ORANGE, int(size * .9), head=False, alpha=.75, glow=False)
        route(cv, [(lerp(tx, x, .5), lerp(ty, y, .5)), (x, y)], 1.0, YEL, int(size * .5), head=False, alpha=.9, glow=False)

        def fn(d_, P, s):
            pts = [(x + size * (1 + .25 * math.sin(k * 2.3)) * math.cos(k * math.pi / 4),
                    y + size * (1 + .25 * math.sin(k * 2.3)) * math.sin(k * math.pi / 4)) for k in range(8)]
            d_.polygon([P(*q) for q in pts], fill=col((120, 108, 98)), outline=col(OUTLINE), width=int(3 * s))
            d_.ellipse((*P(x - size * .35, y - size * .3), *P(x, y + size * .05)), fill=col((80, 72, 66)))
        vec(cv, (x - size * 2, y - size * 2, x + size * 2, y + size * 2), fn, 1.0, base=(120, 108, 98))

    # -------------------------------------------------------------------------
    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        S = lambda p: Cam.S(st, *p)
        self.draw_map(cv, st)
        # half on land / half under the sea
        la = vis(t, T['half1'] - .1, T['oil'], .5, .5)
        if la > 0:
            cv.alpha_composite(with_alpha(render_map(self.half_land, st, 2.0), la))
        sa = vis(t, T['half2'] - .1, T['oil'], .5, .5)
        if sa > 0:
            cv.alpha_composite(with_alpha(render_map(self.half_sea, st, 2.0), sa))
        cv.alpha_composite(vignette())
        cx, cy = S(self.C)
        z = st[2]
        rx, ry = self.rx * z, self.ry * z
        ell = self.ell_pts(st)
        # limestone cover
        lm = vis(t, T['buried'] - .1, T['half1'] + .2, .5, .5)
        if lm > 0:
            grow = e_out((t - T['buried'] + .1) / .9)

            def fn(d, P, s):
                d.ellipse((*P(cx - rx, cy - ry), *P(cx + rx, cy + ry)), fill=col(STONE, .55))
                n = 9
                for k in range(1, n):
                    dy = -ry + 2 * ry * k / n
                    if (k / n) > grow:
                        continue
                    hw = rx * math.sqrt(max(0, 1 - (dy / ry) ** 2))
                    d.line([P(cx - hw, cy + dy), P(cx + hw, cy + dy)], fill=col((150, 128, 96), .9), width=int(4 * s))
            vec(cv, (cx - rx - 4, cy - ry - 4, cx + rx + 4, cy + ry + 4), fn, lm, base=STONE)
        # crater ring: dashed hint (hook) -> solid orange -> dim -> lime for cenote rim
        route(cv, ell, e_out((t - T['scar']) / .9), WHITE, 5, head=False, alpha=vis(t, T['scar'], T['blasted'] - .1),
              dashed=True, dash=(18, 12), glow=False)
        ra = vis(t, T['blasted'], None, .3) * (1 - .55 * vis(t, T['today'], None, .5)) * (1 - .75 * vis(t, T['trace'], None, .5))
        route(cv, ell, e_out((t - T['blasted']) / .8), ORANGE, 9, head=False, alpha=ra, glow=False)
        # survey lines
        if T['spotted'] - .1 <= t < T['but'] + .3:
            sp = e_io((t - T['spotted'] + .1) / 1.4)

            def fn(d, P, s):
                for k in range(-4, 5):
                    x = cx + k * rx / 4.5
                    y0, y1 = cy - ry * 1.2, cy - ry * 1.2 + 2.4 * ry * sp
                    d.line([P(x, y0), P(x, y1)], fill=col(YEL, .7), width=int(2 * s))
            vec(cv, (cx - rx * 1.2, cy - ry * 1.3, cx + rx * 1.2, cy + ry * 1.3), fn, vis(t, T['spotted'] - .1, T['but'], .3, .4), base=YEL)
        # cenote dots
        if t >= T['trace'] - .1:
            n = len(self.cenotes)
            shown = n * clamp((t - T['trace'] + .1) / max(.5, T['ring'] - T['trace'] + .2))
            pts = [S(q) for q in self.cenotes]

            def fn(d, P, s):
                for i, (x, y) in enumerate(pts):
                    if i >= shown:
                        break
                    pp = clamp(shown - i)
                    r = 9 * e_back(pp) if pp < 1 else 9
                    d.ellipse((*P(x - r - 3, y - r - 3), *P(x + r + 3, y + r + 3)), fill=col(OUTLINE, .6))
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=col(TEAL), outline=col(WHITE), width=int(2 * s))
            if pts:
                vec(cv, bbox_of(pts, 30), fn, vis(t, T['trace'] - .1, None, .2), base=TEAL)
        # diameter
        da = vis(t, T['hundred'] - .1, T['three'] - .2, .3, .4)
        route(cv, [(cx - rx + 4, cy), (cx + rx - 4, cy)], e_out((t - T['hundred'] + .1) / .6), YEL, 6, head=False, alpha=da)
        label(cv, '≈110 MI', cx + rx + 24, cy, t, T['hundred'] + .2, T['three'] - .2, 40, YEL, anchor='l', rise=0)
        # pin
        pin(cv, cx, cy, t, -.5, T['blasted'], RED, 14)
        # meteors
        self.meteor(cv, t, .2, 1.25, (1000, 60), (cx, cy), 18)
        self.impact(cv, cx, cy, t, 1.45, .8)
        ro = T['rock']
        if ro <= t < T['slammed']:
            hov = (t - ro)
            ax, ay = 820 + 8 * math.sin(hov * 3), 260 + 6 * math.cos(hov * 2.5)
            self.meteor(cv, t, ro - .001, T['slammed'] - ro + .002, (ax, ay), (ax, ay), 42 * e_back((t - ro) / .4))
        self.meteor(cv, t, T['slammed'] - .05, .45, (820, 260), (cx, cy), 42)
        self.impact(cv, cx, cy, t, T['slammed'] + .4, 1.3)
        # map labels
        hp = (cx + 70, cy - 90)
        chip(cv, 'THE DINOSAUR KILLER', 600, 300, t, -.5, T['map'], size=40, accent=RED, sub='IMPACT SITE')
        chip(cv, 'HERE', hp[0], hp[1], t, T['here'], T['northern'] + .3, size=40, accent=RED, anchor='l')
        fl = S(self.geo(-81.6, 27.0))
        label(cv, 'FLORIDA', clamp(fl[0], 120, 860), max(fl[1], 120), t, T['map'] + .4, T['northern'] + .2, 32, WHITE, rise=6)
        cu = S(self.geo(-79.4, 22.0))
        label(cv, 'CUBA', cu[0], cu[1], t, T['map'] + .5, T['northern'] + .2, 32, WHITE, rise=6)
        mx = S(self.geo(-88.6, 19.6))
        chip(cv, 'MEXICO', min(mx[0], 860), min(mx[1], 920), t, T['mexico'], T['about'], size=36, accent=ORANGE)
        yx = S(self.geo(-88.1, 20.6))
        label(cv, 'YUCATÁN PENINSULA', min(yx[0] + 60, 760), min(yx[1], 880), t, T['yuc'], T['about'], 34, YEL, rise=6)
        chip(cv, 'SHALLOW SEA', 700, 380, t, T['shallow'], T['blasted'] + .3, size=36, accent=TEAL)
        chip(cv, 'BURIED UNDER LIMESTONE', 620, 300, t, T['buried'], T['half1'] + .2, size=34, accent=STONE)
        chip(cv, 'HALF ON LAND', 640, 300, t, T['half1'] + .1, T['oil'] - .2, size=36, accent=LIME)
        chip(cv, 'HALF UNDER THE GULF', 640, 380, t, T['half2'] + .1, T['oil'] - .2, size=36, accent=TEAL)
        gm = S(self.geo(-87.0, 24.6))
        label(cv, 'GULF OF MEXICO', clamp(gm[0], 300, 760), clamp(gm[1], 500, 900), t, T['gulf'], T['oil'], 36, WHITE, rise=6)
        # survey ship
        if T['oil'] <= t < T['but']:
            sx = lerp(900, 640, e_io((t - T['oil']) / 2.5))
            sy = cy - ry - 60

            def fn(d, P, s):
                d.polygon([P(sx - 40, sy), P(sx + 40, sy), P(sx + 28, sy + 18), P(sx - 28, sy + 18)], fill=col(WHITE), outline=col(OUTLINE), width=int(3 * s))
                d.rectangle((*P(sx - 10, sy - 20), *P(sx + 12, sy)), fill=col(YEL), outline=col(OUTLINE), width=int(2 * s))
            vec(cv, (sx - 60, sy - 40, sx + 60, sy + 40), fn, vis(t, T['oil'], T['but'] - .3, .3, .3), base=WHITE)
        chip(cv, 'OIL COMPANY SURVEYS', 600, 300, t, T['oil'], T['but'] - .2, size=36, accent=YEL)
        chip(cv, 'RING OF SINKHOLES', 640, 300, t, T['sinkholes'] - .1, None, size=36, accent=TEAL)
        # lower info area --------------------------------------------------------
        hero(cv, '66 MILLION', 540, 1280, t, T['about'] + .1, T['rock'] - .1, 120, LIME)
        label(cv, 'YEARS AGO', 540, 1385, t, T['about'] + .3, T['rock'] - .1, 32, WHITE)
        chip(cv, 'AN ASTEROID ≈6 MILES WIDE', 540, 1290, t, T['rock'], T['slammed'] + .3, size=36, accent=ORANGE)
        hero(cv, 'IMPACT', 540, 1290, t, T['slammed'] + .4, T['blasted'] - .1, 130, RED)
        hero(cv, '≈110 MILES', 540, 1280, t, T['hundred'], T['three'] - .2, 120, YEL)
        label(cv, 'ACROSS', 540, 1385, t, T['hundred'] + .2, T['three'] - .2, 32, WHITE)
        hero(cv, '≈3/4', 540, 1270, t, T['three'], T['today'] - .2, 130, RED)
        label(cv, 'OF ALL SPECIES WIPED OUT', 540, 1370, t, T['three'] + .2, T['today'] - .2, 30, WHITE)
        sa_ = vis(t, T['species'], T['today'] - .2, .3, .3)
        if sa_ > 0:
            def fn(d, P, s):
                for k in range(4):
                    x, y = 540 + (k - 1.5) * 110, 1480
                    pk = clamp((t - T['species'] - k * .25) / .3)
                    d.ellipse((*P(x - 34, y - 34), *P(x + 34, y + 34)), fill=col(LIME if k == 3 else (90, 100, 105)), outline=col(WHITE), width=int(3 * s))
                    if k < 3 and pk > 0:
                        r = 30 * e_out(pk)
                        d.line([P(x - r, y - r), P(x + r, y + r)], fill=col(RED), width=int(9 * s))
                        d.line([P(x - r, y + r), P(x + r, y - r)], fill=col(RED), width=int(9 * s))
            vec(cv, (300, 1420, 780, 1540), fn, sa_, base=WHITE)
        chip(cv, 'INCLUDING THE DINOSAURS', 540, 1590, t, T['dino2'], T['today'] - .2, size=34, accent=RED)
        hero(cv, 'LATE 1970s', 540, 1285, t, T['y1970'] - .1, T['but'] + .2, 120, YEL)
        label(cv, 'CRATER FOUND IN OIL SURVEY DATA', 540, 1390, t, T['y1970'] + .1, T['but'] + .2, 28, WHITE)
        hero(cv, 'CENOTES', 540, 1285, t, T['cenotes'] - .1, None, 120, TEAL)
        label(cv, 'SINKHOLES TRACING THE BURIED RIM', 540, 1390, t, T['cenotes'] + .1, None, 28, WHITE)
        label(cv, 'SOURCES: USGS · NASA · LPI', 540, 1595, t, T['but'], None, 18, (200, 210, 215), rise=0)
