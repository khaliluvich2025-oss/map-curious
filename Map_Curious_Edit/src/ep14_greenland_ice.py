"""14 - Greenland Is Hiding a Two-Mile-Thick Ice Sheet.

Base map: the pack's NASA Blue Marble Greenland/Iceland render (04_denmark_strait bbox);
Greenland outline traced from that image's own coastline (as in ep04/ep07); the ice
overlay is the bright (white) part of that traced Greenland mask.
Facts (NASA / NSIDC / USGS): ice sheet up to ~2 mi (~3 km) thick; covers ~80% of
Greenland; ~1.7 million km2, more than twice the area of Texas (~0.7 million km2);
its weight has depressed central Greenland's bedrock below sea level; full melt would
raise global sea level ~7.4 m (~24 ft); losing hundreds of billions of tons of ice a
year in recent decades; Greenland is the world's largest island.
Cross-section is schematic (labelled on screen); Texas icons are not to map scale.
"""
from episode import *
from scipy import ndimage as nd
from engine import _head
from ep04_underwater_waterfall import EP as EP4

BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
SEA = 640
ICE = (226, 244, 255)
ICE_D = (150, 200, 235)
OCEAN = (40, 110, 200)
YEL = (255, 214, 90)
# simplified Texas outline (lon, lat) for the size-comparison icons
TEXAS = [(-106.6, 32.0), (-103.0, 32.0), (-103.0, 36.5), (-100.0, 36.5), (-100.0, 34.56), (-99.2, 34.4), (-97.0, 33.8),
         (-95.5, 33.9), (-94.04, 33.55), (-94.04, 31.0), (-93.7, 29.7), (-94.7, 29.4), (-96.5, 28.4), (-97.4, 27.4),
         (-97.15, 25.95), (-99.1, 26.4), (-99.5, 27.5), (-100.3, 28.3), (-101.4, 29.8), (-102.4, 29.8), (-103.1, 29.0),
         (-104.5, 29.6), (-104.9, 30.6)]
# meltwater outflow arrows (map px: coast point -> out to sea)
OUTFLOW = [((690, 690), (800, 760)), ((450, 800), (560, 900)), ((300, 905), (400, 1010)), ((180, 1085), (290, 1170)),
           ((120, 1265), (230, 1330)), ((725, 395), (840, 430))]


def rock_y(x, push=1.0):
    """Bedrock surface in the schematic: coastal highs at the edges, centre sags below SEA with push."""
    u = (x - 540) / 360
    rim = SEA - 60 + 40 * max(0, abs(u) - 1) * 3
    sag = (1 - min(1, abs(u)) ** 2) * lerp(40, 150, push)
    return rim + sag - 20 * math.cos(x / 23) * .3


def dome_y(x, h):
    u = (x - 540) / 345
    if abs(u) >= 1:
        return None
    return SEA - 60 - h * (1 - u * u) ** .55


def texas_poly(cx, cy, size):
    k = math.cos(math.radians(31))
    xs = [lon * k for lon, _ in TEXAS]; ys = [-lat for _, lat in TEXAS]
    mx, my = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    sc = size / (max(xs) - min(xs))
    return [(cx + (x - mx) * sc, cy + (y - my) * sc) for x, y in zip(xs, ys)]


class EP(Episode):
    slug = '14_Greenland_Ice'
    gfx = '04_denmark_strait'
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '14_Greenland_Ice_Final.mp4'
    title = "Greenland's Two-Mile-Thick Ice Sheet"
    cover_title = "GREENLAND'S\nHIDDEN\nICE GIANT"
    cover_t = 15.8
    emphasis = ['Greenland', 'hiding', 'two', 'miles', 'thick.', 'eighty', 'percent', 'twice', 'Texas.', 'heavy',
                'below', 'level.', 'melted,', 'twenty-four', 'feet.', 'melting.', 'hundreds', 'billions', 'tons',
                'Atlantic.', "world's", 'largest', 'frozen', 'reservoir,', 'ocean.']
    _build_land = EP4._build_land

    def setup(self):
        w = self.w
        self.base = self.base_map(.86)
        self._build_land()
        self._build_ice()
        g = self.geo
        self.P = g(-36.5, 71.2)          # pin on the ice sheet
        self.COAST = g(-36.0, 66.6)      # south-east coast glaciers
        T = self.T = dict(
            greenland=w('Greenland', 1), hiding=w('hiding'), sheet=w('sheet'), two=w('two'), thick=w('thick'),
            covers=w('covers'), eighty=w('eighty'), island=w('island', 1), area=w('area'), twice=w('twice'),
            texas=w('Texas'), middle=w('middle'), heavy=w('heavy'), pushed=w('pushed'), below=w('below'),
            level=w('level'), if_=w('If'), melted=w('melted'), global_=w('global'), twentyfour=w('twenty-four'),
            and_=w('And'), melting=w('melting'), recent=w('recent'), greenland2=w('Greenland', 2), losing=w('losing'),
            hundreds=w('hundreds'), tons=w('tons'), year=w('year'), pouring=w('pouring'), atlantic=w('Atlantic'),
            zoom=w('Zoom'), worlds=w("world's"), largest=w('largest'), frozen=w('frozen'), reservoir=w('reservoir'),
            holding=w('holding'), ocean=w('ocean'))
        P, C = self.P, self.COAST
        self.cam = Cam([
            frame_on(P, 470, 620, 1.7, 0), frame_on(P, 470, 620, 2.1, T['two'] + .2),
            frame_on(P, 470, 640, 1.9, T['covers']), frame_on(P, 470, 700, 1.15, T['island'] + .6),
            frame_on(P, 470, 700, 1.2, T['middle'] - .3),
            frame_on(P, 470, 700, 1.25, T['and_']), frame_on(C, 500, 640, 1.6, T['melting'] + .6),
            frame_on(C, 500, 640, 2.5, T['losing'] + .4), frame_on(C, 500, 640, 2.6, T['year']),
            frame_on(C, 560, 620, 1.7, T['atlantic'] + .2), (T['zoom'] + 1.6, 540, 960, 1.0), (self.dur, 540, 960, 1.03)])
        self.slides = [(T['middle'] - .3, 1), (T['and_'] - .25, 0)]
        b = self.beat
        b(0.0, 'Greenland outlined on the NASA map, pin on the ice sheet', 'pop', 2)
        b(T['hiding'], 'Ice sheet glows white across Greenland', 'shimmer')
        b(T['sheet'], 'ICE SHEET chip', 'tick')
        b(T['two'], 'Hero: ≈2 MILES THICK; camera pushes in', 'thud')
        b(T['thick'], 'Thickness ruler beside the pin', 'swish')
        b(T['covers'], 'Ice overlay sweeps down the island', 'whoosh')
        b(T['eighty'], 'Hero: ≈80% OF THE ISLAND', 'thud')
        b(T['island'], 'Camera pulls out to the whole east coast', 'whoosh')
        b(T['area'], 'MORE THAN chip', 'tick')
        b(T['twice'], 'Two Texas silhouettes pop in', 'pop')
        b(T['texas'], '2× TEXAS label', 'tick')
        b(T['middle'] - .3, 'Map lifts: schematic ice-sheet cross-section', 'whoosh')
        b(T['heavy'], 'Weight arrows press down on the dome', 'rumble')
        b(T['pushed'], 'Bedrock sags under the ice', 'rumble', 2)
        b(T['below'], 'Sea-level line crosses the bedrock: BELOW SEA LEVEL', 'thud')
        b(T['level'], 'Sunken bedrock highlighted', 'tick')
        b(T['if_'], 'IF IT ALL MELTED chip', 'tick')
        b(T['melted'], 'Ice dome melts, meltwater runs to the ocean', 'swish')
        b(T['global_'], 'Ocean level rises on both sides', 'bubble')
        b(T['twentyfour'], 'Hero: ≈24 FT GLOBAL SEA-LEVEL RISE', 'thud')
        b(T['and_'] - .25, 'Back to the map', 'whoosh')
        b(T['melting'], 'Ice edge glows red: IT IS MELTING', 'rumble')
        b(T['recent'], 'IN RECENT DECADES chip; push to the SE coast', 'tick')
        b(T['losing'], 'Coastal ice flashes red', 'swish')
        b(T['hundreds'], 'Hero: HUNDREDS OF BILLIONS', 'thud')
        b(T['tons'], 'OF TONS OF ICE label', 'tick')
        b(T['year'], 'EVERY YEAR chip', 'pop')
        b(T['pouring'], 'Meltwater arrows pour off the coast', 'swish')
        b(T['atlantic'], 'ATLANTIC OCEAN label', 'pop')
        b(T['zoom'], 'Zoom out to the full map', 'whoosh')
        b(T['largest'], "WORLD'S LARGEST ISLAND chip", 'pop')
        b(T['frozen'], 'Ice sheet shimmers', 'shimmer')
        b(T['reservoir'], 'A FROZEN RESERVOIR chip', 'pop')
        b(T['holding'], 'Ocean tint pulses: HOLDING BACK THE OCEAN', 'swish')

    # -------------------------------------------------------------------------
    def _build_ice(self):
        """Ice-only overlay: bright pixels inside the traced Greenland mask."""
        gl_alpha = np.asarray(self.land['gl'][0].getchannel('A')) > 0
        im = np.asarray(Image.open(self.G / 'map_terrain.jpg').convert('RGB').resize((W * 2, H * 2), Image.BILINEAR), np.int16)
        bright = im.min(-1) > 165
        m = nd.binary_opening(gl_alpha & bright, iterations=2)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))) > 127
        edge = m & ~nd.binary_erosion(m, iterations=6)
        fill = np.zeros((H * 2, W * 2, 4), np.uint8); fill[m] = (120, 196, 255, 120)
        bord = np.zeros((H * 2, W * 2, 4), np.uint8); bord[edge] = (255, 255, 255, 235)
        hot = np.zeros((H * 2, W * 2, 4), np.uint8); hot[edge] = RED + (255,)
        ys = np.nonzero(m.any(1))[0]
        self.ice_y = (ys.min() / 2, ys.max() / 2)
        self.ice = (Image.fromarray(fill, 'RGBA'), Image.fromarray(bord, 'RGBA'), Image.fromarray(hot, 'RGBA'))

    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        S = lambda p: Cam.S(st, *p)
        # Greenland outline (from ep04 trace)
        gfill, gbord = self.land['gl']
        m.alpha_composite(with_alpha(render_map(gbord, st, 2.0), .85))
        # ice overlay
        fill, bord, hot = self.ice
        ia = vis(t, T['hiding'] - .2, None, .6)
        if ia > 0:
            sh = 1 + .25 * (vis(t, T['frozen'], T['holding'], .3, .6) * math.sin(t * 6) ** 2)
            f = render_map(fill, st, 2.0)
            if T['covers'] <= t < T['covers'] + 1.4:      # sweep top -> bottom
                p = e_io((t - T['covers']) / 1.3)
                y0, y1 = S((0, self.ice_y[0]))[1], S((0, self.ice_y[1]))[1]
                cut = lerp(y0, y1, p)
                g = np.clip((cut - np.arange(H, dtype=np.float32)) / 60 + 1, 0, 1)
                g = np.broadcast_to(g[:, None], (H, W))
                a = (np.asarray(f.getchannel('A'), np.float32) * (g * .75 + .25)).astype(np.uint8)
                f.putalpha(Image.fromarray(a))
            m.alpha_composite(with_alpha(f, min(1, ia * sh)))
            m.alpha_composite(with_alpha(render_map(bord, st, 2.0), ia * .6))
        ha = max(vis(t, T['melting'] - .1, T['pouring'] + .4, .3, .6), .6 * vis(t, T['losing'], T['year'], .2, .4))
        if ha > 0:
            hb = render_map(hot, st, 2.0)
            m.alpha_composite(with_alpha(hb.filter(ImageFilter.GaussianBlur(6)), ha * (.6 + .4 * math.sin(t * 7) ** 2)))
            m.alpha_composite(with_alpha(hb, ha * .9))
        # ocean pulse at the end
        oa = vis(t, T['holding'], None, .6) * (.12 + .08 * math.sin(t * 4))
        tint(m, OCEAN, oa)
        m.alpha_composite(vignette())
        # pin + labels
        px, py = S(self.P)
        pin(m, px, py, t, -.12, T['middle'] - .3, LIME, 16)
        chip(m, 'GREENLAND', px, py - 130, t, -.5, T['covers'] - .1, size=46, accent=LIME)
        chip(m, 'ICE SHEET', px + 40, py + 120, t, T['sheet'], T['covers'] - .1, size=36, accent=TEAL, anchor='l')
        # thickness ruler beside the pin
        ra = vis(t, T['thick'] - .1, T['covers'] - .1, .3, .3)
        if ra > 0:
            pe = e_out((t - T['thick'] + .1) / .6)
            x = px - 70
            route(m, [(x, py + 60), (x, py + 60 - 170 * pe)], 1, ICE, 7, head=True, alpha=ra, head_size=20)
            route(m, [(x, py - 110), (x, py - 110 + 170 * pe)], 1, ICE, 7, head=True, alpha=ra, head_size=20)
            label(m, '≈2 MI', x - 20, py - 25, t, T['thick'], T['covers'] - .1, 34, ICE, anchor='r', rise=6)
        gl = S(self.geo(-36.0, 74.0))
        chip(m, 'GREENLAND', gl[0], max(gl[1], 300), t, T['covers'] + .1, T['middle'] - .3, size=40, accent=LIME)
        # melting edge
        cl = S(self.COAST)
        # meltwater arrows
        for i, (a, b2) in enumerate(OUTFLOW):
            a0 = T['pouring'] + i * .12
            al = vis(t, a0, T['zoom'] + .8, .3, .5)
            if al > 0:
                p = e_out((t - a0) / .8)
                route(m, [S(a), S(b2)], p, TEAL, 8, alpha=al, head_size=22)
        at = S(self.geo(-27.0, 60.6))
        label(m, 'ATLANTIC OCEAN', min(max(at[0], 260), 800), min(at[1], 900), t, T['atlantic'], T['zoom'] + .3, 40, (150, 215, 255))
        # ending
        chip(m, 'GREENLAND', 300, 520, t, T['zoom'] + .4, None, size=40, accent=LIME)
        label(m, 'ATLANTIC OCEAN', 640, 900, t, T['holding'], None, 34, (150, 215, 255), rise=6)
        return m

    # ---- schematic cross-section ---------------------------------------------------
    def section(self, cv, t, al):
        T = self.T
        push = e_io((t - T['pushed']) / 1.4) if t >= T['pushed'] else 0
        melt = e_io((t - T['melted']) / 2.4) if t >= T['melted'] else 0
        rise = e_io((t - T['global_']) / 1.8) * 34 if t >= T['global_'] else 0
        sea = SEA - rise
        h = 200
        heavy = vis(t, T['heavy'] - .1, T['if_'], .3, .4)
        sunk = vis(t, T['below'], T['if_'] + .4, .3, .4)

        def fn(d, P, s):
            for i in range(14):
                y0 = lerp(BY0, sea, i / 14); y1 = lerp(BY0, sea, (i + 1) / 14)
                c = tuple(int(lerp(a, b, i / 13)) for a, b in zip((22, 42, 66), (60, 90, 116)))
                d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
            # ocean (both sides)
            d.rectangle((*P(BX0, sea), *P(BX1, BY1)), fill=(28, 84, 150, 255))
            for i in range(10):
                y0 = lerp(sea, BY1, i / 10)
                d.rectangle((*P(BX0, y0), *P(BX1, y0 + (BY1 - sea) / 10 + 1)), fill=(28 - i * 2, 84 - i * 4, 150 - i * 6, 255))
            # bedrock
            xs = list(range(BX0, BX1 + 1, 6))
            r0 = [(x, rock_y(x, push)) for x in xs if 170 <= x <= 910]
            land = [(170, BY1), (170, rock_y(170, push))] + r0 + [(910, rock_y(910, push)), (910, BY1)]
            d.polygon([P(*q) for q in land], fill=(104, 86, 70, 255))
            d.polygon([P(170, BY1), P(150, BY1 - 40), P(170, rock_y(170, push))], fill=(104, 86, 70, 255))
            d.polygon([P(910, BY1), P(930, BY1 - 40), P(910, rock_y(910, push))], fill=(104, 86, 70, 255))
            d.rectangle((*P(BX0, BY1 - 70), *P(BX1, BY1)), fill=(84, 70, 58, 255))
            # sunken bedrock highlight (below original sea level)
            if sunk > 0:
                pts = [(x, y) for x, y in r0 if y > SEA]
                if len(pts) > 2:
                    poly = [(pts[0][0], SEA)] + pts + [(pts[-1][0], SEA)]
                    d.polygon([P(*q) for q in poly], fill=col(ORANGE, .55 * sunk * (.7 + .3 * math.sin(t * 6) ** 2)))
            # ice dome
            top = []
            for x in range(195, 886, 6):
                y = dome_y(x, h)
                if y is not None:
                    ry = rock_y(x, push)
                    top.append((x, min(ry - (ry - y) * (1 - .93 * melt), ry)))
            bot = [(x, rock_y(x, push)) for x, _ in reversed(top)]
            if top:
                d.polygon([P(*q) for q in top + bot], fill=ICE + (255,))
                d.line([P(*q) for q in top], fill=(255, 255, 255, 255), width=int(4 * s))
                # internal layering
                for k in (.3, .55, .8):
                    ln = [(x, lerp(y, rock_y(x, push), k)) for x, y in top]
                    d.line([P(*q) for q in ln], fill=col(ICE_D, .5), width=int(2 * s))
            # meltwater streams running off the dome
            if 0 < melt < 1 or (t >= T['melted'] and t < T['global_'] + 2):
                ma = vis(t, T['melted'], T['twentyfour'] + .8, .3, .4)
                for sgn in (-1, 1):
                    for k in range(6):
                        ph = (t * .9 + k / 6) % 1
                        x = 540 + sgn * lerp(220, 380, ph)
                        y = lerp(sea - 70, sea - 6, ph)
                        d.ellipse((*P(x - 7, y - 7), *P(x + 7, y + 7)), fill=col((120, 190, 255), ma * (1 - ph * .4)))
            # weight arrows
            if heavy > 0:
                for k, x in enumerate((380, 540, 700)):
                    bob = 8 * math.sin(t * 5 + k)
                    y0 = (dome_y(x, h) or SEA) + 15 + bob
                    d.line([P(x, y0), P(x, y0 + 55)], fill=col((235, 160, 30), heavy), width=int(10 * s))
                    _head(d, P, s, (x, y0 + 68), math.pi / 2, 24, col((235, 160, 30), heavy))
            # sea-level dashed reference line (original sea level)
            for x in range(BX0 + 10, BX1 - 10, 34):
                d.line([P(x, SEA), P(x + 18, SEA)], fill=col(WHITE, .85), width=int(3 * s))
            # waves on the (rising) ocean surface
            for x0, x1 in ((BX0, 175), (905, BX1)):
                wv = [P(x, sea + 4 * math.sin(x / 30 + t * 2)) for x in range(x0, x1 + 1, 8)]
                d.line(wv, fill=col((170, 220, 255)), width=int(3 * s))
            d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (18, 36, 58))
        fn(ImageDraw.Draw(L, 'RGBA'), lambda x, y: ((x - BX0) * 2, (y - BY0) * 2), 2)
        sec = L.reduce(2).convert('RGBA')
        mk = Image.new('L', sec.size, 0)
        ImageDraw.Draw(mk).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(mk)
        shake = math.sin(t * 60) * 6 * (1 - (t - T['pushed']) / .5) if T['pushed'] <= t < T['pushed'] + .5 else 0
        paste(cv, with_alpha(sec, al), BX0, BY0 + shake)
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        label(cv, 'SEA LEVEL', 80, SEA + 22, t, 0, None, 22, WHITE, rise=0, anchor='l')
        chip(cv, 'ICE SHEET', 540, 520, t, T['middle'] - .1, T['melted'] + .4, size=30, accent=TEAL, sub='UP TO ≈2 MI THICK')
        label(cv, 'HEAVY', 860, 400, t, T['heavy'], T['if_'], 32, YEL, rise=6)
        label(cv, 'ICE MELTS', 540, 470, t, T['melted'] + .3, T['and_'] - .3, 32, (150, 215, 255), rise=6)
        label(cv, 'BEDROCK', 540, 840, t, T['middle'] + .4, None, 28, (235, 215, 190), rise=6)
        label(cv, 'BELOW SEA LEVEL', 540, 770, t, T['below'] + .1, T['if_'] + .4, 30, ORANGE, rise=6)
        label(cv, 'OCEAN', 115, 780, t, T['middle'] + .2, None, 24, (170, 220, 255), rise=0)
        label(cv, 'OCEAN', 965, 780, t, T['middle'] + .2, None, 24, (170, 220, 255), rise=0)
        if t >= T['global_']:
            ra = vis(t, T['global_'] + .3, T['and_'] - .3, .3, .2)
            if ra > 0:
                route(cv, [(130, SEA - 4), (118, SEA - 34 * e_io((t - T['global_']) / 1.8) + 2)], 1, LIME, 6, alpha=ra, head_size=16)
                label(cv, 'SEA RISES', 150, SEA - 75, t, T['global_'] + .4, T['and_'] - .3, 24, LIME, rise=4, anchor='l')

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_bg())
            self.section(cv, t, clamp(u * 1.5))
            label(cv, 'GREENLAND ICE SHEET', 540, 280, t, 0, None, 30, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area --------------------------------------------------------------
        chip(cv, 'HIDDEN UNDER ICE', 540, 1270, t, T['hiding'], T['two'] - .1, size=42, accent=TEAL)
        hero(cv, '≈2 MILES', 540, 1275, t, T['two'], T['covers'] - .15, 120, ICE)
        label(cv, 'THICK', 540, 1385, t, T['thick'] - .1, T['covers'] - .15, 34, WHITE)
        hero(cv, '≈80%', 540, 1275, t, T['eighty'], T['area'] - .1, 130, ICE)
        label(cv, 'OF THE ISLAND IS ICE', 540, 1390, t, T['eighty'] + .2, T['area'] - .1, 32, WHITE)
        chip(cv, 'AN AREA MORE THAN', 540, 1215, t, T['area'], T['middle'] - .35, size=34, accent=TEAL)
        # Texas icons
        for k, x in enumerate((420, 660)):
            a0 = T['twice'] + k * .2
            al = vis(t, a0, T['middle'] - .35, .25, .3)
            if al > 0:
                sc = e_back((t - a0) / .45, 2.0)
                poly = texas_poly(x, 1345, 165 * sc)

                def fn(d, P, s, poly=poly):
                    d.polygon([P(*q) for q in poly], fill=col(ORANGE, .9), outline=col(WHITE), width=int(3 * s))
                vec(cv, (x - 130, 1230, x + 130, 1460), fn, al, base=ORANGE)
        label(cv, '× 2', 540, 1345, t, T['twice'] + .3, T['middle'] - .35, 44, WHITE, rise=6)
        label(cv, 'MORE THAN 2× TEXAS', 540, 1460, t, T['texas'], T['middle'] - .35, 32, ORANGE, rise=6)
        chip(cv, 'IN THE MIDDLE', 540, 1270, t, T['middle'], T['heavy'] - .1, size=40, accent=ICE)
        chip(cv, 'SO HEAVY IT SINKS THE LAND', 540, 1270, t, T['heavy'], T['below'] - .1, size=36, accent=YEL)
        chip(cv, 'BEDROCK BELOW SEA LEVEL', 540, 1270, t, T['below'], T['if_'] - .1, size=38, accent=ORANGE)
        chip(cv, 'IF IT ALL MELTED…', 540, 1270, t, T['if_'], T['twentyfour'] - .1, size=40, accent=TEAL)
        hero(cv, '≈24 FT', 540, 1280, t, T['twentyfour'], T['and_'] - .2, 130, LIME)
        label(cv, 'GLOBAL SEA-LEVEL RISE', 540, 1395, t, T['twentyfour'] + .2, T['and_'] - .2, 32, WHITE)
        chip(cv, 'AND IT IS MELTING', 540, 1270, t, T['melting'] - .1, T['recent'] - .1, size=42, accent=RED)
        chip(cv, 'IN RECENT DECADES', 540, 1270, t, T['recent'], T['hundreds'] - .1, size=40, accent=RED)
        hero(cv, 'HUNDREDS', 540, 1250, t, T['hundreds'], T['pouring'] - .1, 104, LIME)
        label(cv, 'OF BILLIONS OF TONS', 540, 1345, t, T['tons'] - .4, T['pouring'] - .1, 34, WHITE, rise=6)
        chip(cv, 'OF ICE LOST EVERY YEAR', 540, 1430, t, T['year'] - .1, T['pouring'] - .1, size=32, accent=RED)
        chip(cv, 'MELTWATER → ATLANTIC', 540, 1270, t, T['pouring'], T['zoom'] - .1, size=40, accent=TEAL)
        chip(cv, "WORLD'S LARGEST ISLAND", 540, 1270, t, T['largest'] - .2, T['reservoir'] - .1, size=40, accent=LIME)
        chip(cv, 'A FROZEN RESERVOIR', 540, 1270, t, T['reservoir'] - .1, None, size=44, accent=ICE)
        label(cv, 'HOLDING BACK ≈24 FT OF OCEAN', 540, 1380, t, T['holding'], None, 30, (150, 215, 255), rise=6)
        label(cv, 'SOURCES: NASA · NSIDC · USGS', 540, 1595, t, T['zoom'], None, 18, (200, 210, 215), rise=0)


@functools.lru_cache(None)
def _bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
