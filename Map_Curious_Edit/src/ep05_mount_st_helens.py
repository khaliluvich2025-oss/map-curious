"""05 - Mount St. Helens: The Morning a Mountain Lost 1,300 Feet.

Base map: the pack's NASA Blue Marble Pacific Northwest render (02_db_cooper bbox).
Facts (USGS): 18 May 1980; earthquake-triggered collapse of the north flank = largest
landslide in recorded history; lateral blast ~230 sq mi; 57 deaths; ash column
~80,000 ft (~15 mi); ash fell in 11 states; summit lowered ~1,300 ft (1,314 ft).
Mountain profile and plate diagram are schematic (labelled on screen).
"""
from episode import *
from engine import _head

BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
GROUND = 860
BEFORE = [(150, GROUND), (400, 540), (440, 488), (470, 450), (510, 432), (570, 432), (610, 450), (650, 500), (700, 560), (930, GROUND)]
AFTER = [(150, GROUND), (400, 540), (440, 520), (470, 540), (510, 575), (570, 600), (610, 615), (650, 640), (700, 680), (930, GROUND)]
TREES = list(range(730, 1005, 22))
VOLCANOES = [('BAKER', -121.8144, 48.7768), ('GLACIER PK', -121.1139, 48.1125), ('RAINIER', -121.760, 46.853),
             ('ST. HELENS', -122.1944, 46.1912), ('ADAMS', -121.4906, 46.2024), ('HOOD', -121.6959, 45.3736),
             ('JEFFERSON', -121.80, 44.674), ('3 SISTERS', -121.769, 44.103), ('MAZAMA', -122.11, 42.94),
             ('SHASTA', -122.194, 41.409), ('LASSEN', -121.508, 40.488)]
TRENCH = [(-124.9, 40.4), (-125.25, 42.0), (-125.5, 44.0), (-125.55, 46.0), (-125.75, 47.5), (-126.6, 48.7), (-127.5, 49.5)]
ASH = [(-122.1944, 46.1912), (-121.2, 46.45), (-120.5, 46.62), (-119.3, 47.0), (-117.43, 47.66), (-115.6, 47.9)]


def shape(p):
    return [(lerp(a[0], b[0], p), lerp(a[1], b[1], p)) for a, b in zip(BEFORE, AFTER)]


class EP(Episode):
    slug = '05_Mount_St_Helens'
    gfx = '02_db_cooper'            # reuse the Pacific Northwest NASA Blue Marble map + bbox
    vo = ROOT / '2026-10-16_Map_Curious_Voiceovers'
    out = '05_Mount_St_Helens_Final.mp4'
    title = 'The Morning a Mountain Lost 1,300 Feet'
    cover_title = 'THE MORNING A\nMOUNTAIN LOST\n1,300 FEET'
    cover_t = 21.2
    emphasis = ['thirteen', 'hundred', 'morning.', '1980,', 'Helens', 'Washington', 'earthquake', 'north', 'landslide',
                'sideways,', '230', 'fifteen', 'east,', 'Yakima', 'Spokane.', 'eleven', 'subduction', 'Cascade', 'Range.']

    def setup(self):
        w = self.w
        self.base = self.base_map(.84)
        self.M = self.geo(-122.1944, 46.1912)
        self.YAK = self.geo(-120.5059, 46.6021)
        self.SPO = self.geo(-117.426, 47.6588)
        self.SEA = self.geo(-122.3321, 47.6062)
        self.PDX = self.geo(-122.6765, 45.5231)
        self.wa = Region(svg_polys(self.G / 'region_highlight.svg'))
        self.trench = spline([self.geo(*p) for p in TRENCH], 16)
        self.ash = spline([self.geo(*p) for p in ASH], 16)
        T = self.T = dict(
            thirteen=w('thirteen'), morning=w('morning'), on=w('On'), may=w('May'), y1980=w('1980'), mount=w('Mount'),
            washington=w('Washington'), earthquake=w('earthquake'), north=w('north'), triggering=w('triggering'),
            landslide=w('landslide'), with_=w('With'), pressure=w('pressure'), blasted=w('blasted'), flattening=w('flattening'),
            sqmi=w('230'), fifty=w('Fifty-seven'), within=w('Within'), column=w('column'), fifteen=w('fifteen'),
            and_winds=w('winds'), darkening=w('darkening'), yakima=w('Yakima'), spokane=w('Spokane'), ash_fell=w('Ash'),
            eleven=w('eleven'), zoom=w('Zoom'), clear=w('clear'), pacific=w('Pacific'), subduction=w('subduction'),
            where=w('where'), plate=w('plate'), feeding=w('feeding'), cascade=w('Cascade'))
        M = self.M
        mid = ((M[0] + self.SPO[0]) / 2, (M[1] + self.SPO[1]) / 2)
        self.cam = Cam([
            frame_on(M, 540, 640, 2.4, 0), frame_on(M, 540, 640, 2.15, 1.1), frame_on(M, 540, 640, 2.2, T['on'] - .3),
            frame_on(M, 540, 640, 1.35, T['mount'] + .3), frame_on(M, 540, 640, 1.45, T['earthquake'] - .2),
            frame_on(M, 540, 640, 2.6, T['earthquake'] + .9), frame_on(mid, 540, 600, 1.6, T['and_winds'] - .4),
            frame_on(mid, 540, 600, 1.45, T['darkening']), frame_on(mid, 560, 600, 1.2, T['eleven'] + .4),
            frame_on((540, 960), 540, 960, 1.0, T['zoom'] + 1.6), frame_on((540, 960), 540, 960, 1.04, self.dur)])
        # map lifts away to reveal the schematic profile (1 = section shown)
        self.slides = [(1.0, 1), (T['on'] - .15, 0), (T['north'] - .55, 1), (T['and_winds'] - .3, 0)]
        b = self.beat
        b(0.0, 'Mount St. Helens pin on the Pacific Northwest map', 'pop', 2)
        b(1.0, 'Map lifts: schematic mountain profile', 'whoosh')
        b(T['thirteen'], 'Summit drops away; -1,300 FT bracket', 'rumble')
        b(T['morning'], 'ONE MORNING', 'tick')
        b(T['on'] - .15, 'Map returns', 'whoosh')
        b(T['may'], 'MAY 18, 1980', 'thud')
        b(T['mount'], 'MOUNT ST. HELENS label', 'pop')
        b(T['washington'], 'Washington fills; Seattle and Portland for context', 'tick')
        b(T['earthquake'], 'Earthquake rings, camera pushes in', 'rumble', 2)
        b(T['north'] - .55, 'Profile returns; north flank highlighted', 'whoosh')
        b(T['triggering'], 'North flank slides away: landslide', 'rumble', 2)
        b(T['landslide'], 'LARGEST LANDSLIDE IN RECORDED HISTORY', 'thud')
        b(T['with_'], 'Weight gone: magma chamber glows', None)
        b(T['pressure'], 'Pressure arrows', 'tick')
        b(T['blasted'], 'Lateral blast sweeps sideways (north)', 'whoosh', 3)
        b(T['flattening'], 'Forest flattened as the blast front passes', 'thud', -2)
        b(T['sqmi'], '230 SQ MI', 'pop')
        b(T['fifty'], '57 PEOPLE DIED (quiet beat)', None)
        b(T['within'], 'Ash column rises', 'rumble')
        b(T['fifteen'], '~15 MILES HIGH with ruler', 'pop')
        b(T['and_winds'] - .3, 'Back to the map: ash plume drifts east', 'whoosh')
        b(T['yakima'], 'Yakima darkens', 'tick')
        b(T['spokane'], 'Spokane darkens', 'tick')
        b(T['ash_fell'], 'Plume runs off the map: ASH FELL IN 11 STATES', 'pop')
        b(T['zoom'], 'Camera zooms out to the whole region', 'whoosh')
        b(T['pacific'], 'Cascadia subduction zone draws offshore', 'swish')
        b(T['subduction'], 'CASCADIA SUBDUCTION ZONE', 'tick')
        b(T['where'], 'Plate diagram: ocean plate slides beneath', 'swish')
        b(T['feeding'], 'Magma rises to the volcanoes', None)
        b(T['cascade'], 'Cascade volcanoes pop up along the range', 'pop')

    # -------------------------------------------------------------------------
    def up(self, t):
        u = 0.0
        for a, d in self.slides:
            if t >= a:
                u = lerp(1 - d, d, e_io((t - a) / .7))
        return u

    def mountain_p(self, t):
        T = self.T
        if t < T['on']:
            return e_io((t - T['thirteen']) / 1.0)             # hook: summit loss
        if t < T['triggering']:
            return 0.0                                          # replay: intact mountain
        return e_io((t - T['triggering']) / 1.6)

    def section(self, cv, t, al):
        T = self.T
        p = self.mountain_p(t)
        in_story = t >= T['north'] - .6
        slide = e_io((t - T['triggering']) / 1.6) if in_story and t >= T['triggering'] else 0
        magma = vis(t, T['with_'], T['within'], .5, .6) if in_story else 0
        blast = (t - T['blasted']) / 1.7 if in_story and t >= T['blasted'] else -1
        ashc = e_out((t - T['within']) / 2.6) if in_story and t >= T['within'] else 0
        dim57 = vis(t, T['fifty'] - .05, T['within'] - .2, .4, .4)
        hook = t < T['on']

        def fn(d, P, s):
            # sky
            for i in range(14):
                y0 = lerp(BY0, GROUND, i / 14); y1 = lerp(BY0, GROUND, (i + 1) / 14)
                c = tuple(int(lerp(a, b, i / 13)) for a, b in zip((18, 36, 58), (52, 78, 96)))
                d.rectangle((*P(BX0, y0), *P(BX1, y1 + 1)), fill=c + (255,))
            # ash column (behind mountain)
            if ashc > 0:
                top = lerp(560, 345, ashc)
                for i in range(26):
                    q = i / 25
                    y = lerp(565, top, q)
                    r = lerp(34, 120, q ** 1.6) * (1 + .06 * math.sin(t * 3 + i))
                    x = 520 + 18 * math.sin(i * 1.3 + t)
                    g = int(lerp(120, 165, q))
                    d.ellipse((*P(x - r, y - r * .7), *P(x + r, y + r * .7)), fill=(g, g - 4, g - 10, 235))
            # ground
            d.rectangle((*P(BX0, GROUND), *P(BX1, BY1)), fill=(74, 66, 52, 255))
            # mountain (morph before -> after)
            poly = shape(p)
            d.polygon([P(*q) for q in poly], fill=(110, 100, 88, 255), outline=(235, 235, 225, 255))
            d.line([P(*q) for q in poly], fill=(235, 235, 225, 255), width=int(4 * s), joint='curve')
            # snow cap (only on intact summit)
            if p < .5:
                cap = [(455, 470), (470, 450), (510, 432), (570, 432), (610, 450), (628, 472), (590, 466), (540, 478), (500, 466)]
                d.polygon([P(*q) for q in cap], fill=(240, 244, 246, int(255 * (1 - p * 2))))
            # sliding north flank block
            if 0 < slide < 1:
                blk = [BEFORE[i] for i in range(4, 10)] + [AFTER[i] for i in range(9, 3, -1)]
                dx, dy = slide * 160, slide * 120
                d.polygon([P(x + dx, y + dy) for x, y in blk], fill=(126, 108, 90, int(255 * (1 - slide))))
            # debris on the ground (north = right)
            if slide > 0:
                for i in range(30):
                    x = 700 + (i * 53) % 300 * slide
                    r = 6 + (i * 7) % 9
                    d.ellipse((*P(x - r, GROUND - r * .6), *P(x + r, GROUND + r * .3)), fill=(118, 100, 82, int(255 * min(1, slide * 2))))
            # north flank highlight
            hl = vis(t, T['north'] - .1, T['triggering'], .3, .3) if in_story else 0
            if hl > 0:
                blk = [BEFORE[i] for i in range(4, 10)] + [AFTER[i] for i in range(9, 3, -1)]
                d.polygon([P(*q) for q in blk], outline=col(ORANGE, hl * (.6 + .4 * math.sin(t * 8) ** 2)), width=int(6 * s))
            # magma chamber + pressure
            if magma > 0:
                d.ellipse((*P(470, 700), *P(620, 800)), fill=col((255, 96, 40), .85 * magma), outline=col(YEL, magma), width=int(4 * s))
                pa = clamp((t - T['pressure']) / .6)
                if pa > 0:
                    for ang in (-70, -30, 10):
                        a = math.radians(ang)
                        x0, y0 = 545 + 60 * math.cos(a), 750 + 40 * math.sin(a)
                        L = 60 * pa
                        pts = [(x0, y0), (x0 + L * math.cos(a), y0 + L * math.sin(a))]
                        d.line([P(*q) for q in pts], fill=col(YEL, magma), width=int(6 * s))
                        _head(d, P, s, pts[-1], a, 16, col(YEL, magma))
            # trees: flattened when the blast front passes
            front = 600 + max(0, blast) * 430
            for i, x in enumerate(TREES):
                flat = clamp((front - x) / 40) if blast >= 0 else 0
                ang = lerp(-math.pi / 2, -0.06, e_out(flat))
                h = 30
                x1, y1 = x + h * math.cos(ang), GROUND + h * math.sin(ang)
                d.line([P(x, GROUND), P(x1, y1)], fill=(58, 92, 52, 255) if flat < .5 else (96, 84, 60, 255), width=int(5 * s))
            # lateral blast fan
            if 0 <= blast <= 1.25:
                a = clamp(1.25 - blast) / 1.25
                for k in range(3):
                    rr = (blast * 470) - k * 40
                    if rr <= 20:
                        continue
                    pts = [(600 + rr * math.cos(math.radians(g)), 610 + rr * math.sin(math.radians(g))) for g in range(-60, 26, 4)]
                    d.line([P(*q) for q in pts], fill=col(ORANGE if k == 0 else (190, 170, 150), a * (1 - k * .3)), width=int((14 - k * 4) * s))
                for g in (-50, -30, -10, 10):
                    L = min(1, blast) * 380
                    ga = math.radians(g)
                    pts = [(615, 615), (615 + L * math.cos(ga), 615 + L * math.sin(ga))]
                    d.line([P(*q) for q in pts], fill=col((180, 160, 140), .6 * a), width=int(10 * s))
            # 57 - quiet dim
            if dim57 > 0:
                d.rectangle((*P(BX0, BY0), *P(BX1, BY1)), fill=col(OUTLINE, .55 * dim57))
            d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

        # opaque RGB canvas: translucent fills blend correctly (no alpha holes)
        L = Image.new('RGB', ((BX1 - BX0) * 2, (BY1 - BY0) * 2), (18, 36, 58))
        fn(ImageDraw.Draw(L, 'RGBA'), lambda x, y: ((x - BX0) * 2, (y - BY0) * 2), 2)
        sec = L.reduce(2).convert('RGBA')
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(Image.fromarray(np.minimum(np.asarray(sec.getchannel('A')), np.asarray(m))))
        shake = 0
        for a in (T['triggering'], T['blasted']):
            if a <= t < a + .45:
                shake = math.sin(t * 63) * 7 * (1 - (t - a) / .45)
        paste(cv, with_alpha(sec, al), BX0 + shake, BY0)
        # labels on the profile
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        label(cv, 'SOUTH', 90, 365, t, 0, None, 22, (200, 215, 225), rise=0, anchor='l')
        label(cv, 'NORTH', 990, 365, t, 0, None, 22, (200, 215, 225), rise=0, anchor='r')
        if hook:
            pr = vis(t, T['thirteen'] + .5, T['on'] - .2, .3, .3)
            if pr > 0:
                route(cv, [(330, 432), (700, 432)], 1, WHITE, 3, head=False, alpha=pr, dashed=True, dash=(10, 8))
                route(cv, [(330, 520), (700, 520)], 1, WHITE, 3, head=False, alpha=pr, dashed=True, dash=(10, 8))
                route(cv, [(330, 438), (330, 514)], e_out((t - T['thirteen'] - .5) / .4), LIME, 6, head=False, alpha=pr)
            hero(cv, '−1,300 FT', 210, 476, t, T['thirteen'] + .7, T['on'] - .2, 58, LIME)
            label(cv, 'BEFORE', 735, 432, t, T['thirteen'] + .5, T['on'] - .2, 24, WHITE, anchor='l', rise=0)
            label(cv, 'AFTER', 735, 520, t, T['thirteen'] + .9, T['on'] - .2, 24, WHITE, anchor='l', rise=0)
            label(cv, 'MOUNT ST. HELENS', 540, 400, t, 1.1, T['thirteen'] + .4, 30, WHITE, rise=8)
        else:
            label(cv, 'NORTH SIDE', 800, 520, t, T['north'], T['triggering'] + .6, 30, ORANGE, rise=8)
            label(cv, 'MAGMA', 545, 750, t, T['with_'] + .2, T['blasted'] + .3, 26, WHITE, rise=0)
            label(cv, 'BLAST', 860, 560, t, T['blasted'] + .3, T['sqmi'] + 1.2, 32, ORANGE, rise=8)
            label(cv, 'FORESTS FLATTENED', 865, 820, t, T['flattening'] + .3, T['fifty'] - .1, 24, WHITE, rise=6)
            hero(cv, '57 PEOPLE DIED', 540, 630, t, T['fifty'] + .1, T['within'] - .2, 70, WHITE, pop=False)
            if t >= T['within']:
                pr = vis(t, T['fifteen'] - .1, T['and_winds'] - .4)
                route(cv, [(960, 858), (960, 352)], e_out((t - T['fifteen'] + .1) / .6), LIME, 5, alpha=pr, head=True, head_size=18)
                label(cv, '≈15 MI', 950, 600, t, T['fifteen'] + .3, T['and_winds'] - .4, 30, LIME, anchor='r', rise=0)
                label(cv, 'ASH COLUMN', 380, 400, t, T['column'], T['and_winds'] - .4, 30, WHITE, rise=8)

    def map_layer(self, t, st):
        T = self.T
        m = render_map(self.base, st).convert('RGBA')
        haze = .35 * vis(t, T['darkening'], T['zoom'] + .5, .8, .8)
        self.wa.draw(m, st, t, T['washington'] - .1, T['earthquake'] + .3, fill_a=.22)
        S = lambda p: Cam.S(st, *p)
        # ash plume
        a_p = T['and_winds'] - .1
        if t >= a_p:
            scr = [S(q) for q in self.ash]
            pe = e_io((t - a_p) / 2.0)
            pe2 = 1.0 if t >= T['ash_fell'] else pe * .85
            pal = vis(t, a_p, None, .4) * (1 - .55 * prog(t, T['zoom'] + .4, .8))
            route(m, scr, pe2, (150, 145, 138), 120, head=False, alpha=.42 * pal, outline=False)
            route(m, scr, pe2, (170, 165, 158), 60, head=False, alpha=.45 * pal, outline=False)
            route(m, scr, pe2, WHITE, 6, alpha=.9 * pal, dashed=True, dash=(26, 16), phase=-t * 60, head_size=26)
        if haze > 0:
            for p_, a0 in ((self.YAK, T['yakima']), (self.SPO, T['spokane'])):
                x, y = S(p_)
                hz = vis(t, a0, T['zoom'] + .5, .6, .8)
                if hz > 0:
                    def fn(d, P, s, x=x, y=y):
                        for r, a in ((95, .25), (70, .3), (45, .35)):
                            d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=(40, 38, 36, int(255 * a)))
                    vec(m, (x - 100, y - 100, x + 100, y + 100), fn, hz, base=(40, 38, 36))
        m.alpha_composite(vignette())
        mx, my = S(self.M)
        pin(m, mx, my, t, -.12, None, ORANGE if t >= T['earthquake'] else LIME)
        chip(m, 'MOUNT ST. HELENS', mx, my - 120, t, -.1, 1.0, size=40, sub='WASHINGTON')
        chip(m, 'MOUNT ST. HELENS', mx + 45, my, t, T['mount'], T['earthquake'] - .2, size=38, anchor='l')
        sx, sy = S(self.SEA); px, py = S(self.PDX)
        for (x, y, nm) in ((sx, sy, 'SEATTLE'), (px, py, 'PORTLAND')):
            pin(m, x, y, t, T['washington'] + .3, T['earthquake'], WHITE, 8, rings=False)
            label(m, nm, x - 22, y, t, T['washington'] + .35, T['earthquake'], 26, WHITE, anchor='r', rise=0)
        # earthquake rings
        if T['earthquake'] <= t < T['north'] - .4:
            for k in range(3):
                ph = ((t - T['earthquake']) / .9 + k / 3) % 1
                ring(m, mx, my, 30 + ph * 170, t, T['earthquake'], None, ORANGE, 5, alpha=1 - ph)
        chip(m, 'EARTHQUAKE', 540, 330, t, T['earthquake'], T['north'] - .5, size=42, accent=ORANGE)
        # cities under the ash
        for p_, nm, a0 in ((self.YAK, 'YAKIMA', T['yakima']), (self.SPO, 'SPOKANE', T['spokane'])):
            x, y = S(p_)
            pin(m, x, y, t, a0, None, WHITE, 10, rings=False, alpha=1 - .6 * prog(t, T['zoom'], .6))
            label(m, nm, x, y + 40, t, a0 + .05, T['zoom'] + .3, 30, WHITE, rise=8)
        chip(m, 'WINDS CARRY THE ASH EAST', 540, 330, t, T['and_winds'], T['ash_fell'] - .2, size=36, accent=LIME)
        chip(m, 'ASH FELL IN 11 STATES', 540, 330, t, T['ash_fell'], T['zoom'] + .4, size=40, accent=LIME)
        # subduction zone + Cascade volcanoes
        scr = [S(q) for q in self.trench]
        pt = e_io((t - T['pacific']) / 1.6)
        route(m, scr, pt, ORANGE, 7, head=False, alpha=vis(t, T['pacific']))
        if pt > 0:
            seg, _ = partial(scr, pt)
            L = cumlen(seg)
            teeth = []
            for k in range(1, int(L[-1] // 34)):
                (x, y), ang = point_at(seg, k * 34 / L[-1])
                nx, ny = -math.sin(ang), math.cos(ang)       # normal; teeth point east (overriding plate side)
                if nx < 0:
                    nx, ny = -nx, -ny
                teeth.append([(x - 8 * math.cos(ang), y - 8 * math.sin(ang)), (x + 8 * math.cos(ang), y + 8 * math.sin(ang)), (x + 16 * nx, y + 16 * ny)])

            def fn(d, P, s):
                for tri in teeth:
                    d.polygon([P(*q) for q in tri], fill=col(ORANGE))
            vec(m, bbox_of(seg, 40), fn, vis(t, T['pacific']), base=ORANGE)
        chip(m, 'CASCADIA SUBDUCTION ZONE', 540, 330, t, T['subduction'], None, size=36, accent=ORANGE)
        for i, (nm, lon, lat) in enumerate(VOLCANOES):
            x, y = S(self.geo(lon, lat))
            a0 = T['feeding'] + .1 + i * .17
            al = vis(t, a0, None, .2)
            if al > 0:
                sc = e_back((t - a0) / .4, 2.0)

                def fn(d, P, s, x=x, y=y, sc=sc, hot=(nm == 'ST. HELENS')):
                    r = 21 * sc
                    tri = [P(x, y - r * 1.25), P(x + r, y + r * .6), P(x - r, y + r * .6)]
                    d.polygon(tri, fill=col(ORANGE if hot else WHITE), outline=col(OUTLINE), width=int(3 * s))
                vec(m, (x - 30, y - 30, x + 30, y + 30), fn, al, base=WHITE)
        label(m, 'CASCADE RANGE', S(self.geo(-120.9, 45.1))[0] + 30, S(self.geo(-120.9, 45.1))[1], t, T['cascade'], None,
              30, WHITE, anchor='l', rise=8)
        return m

    def plates_inset(self, cv, t):
        T = self.T
        al = vis(t, T['where'] - .1, None, .4)
        if al <= 0:
            return
        x0, y0, x1, y1 = 90, 1185, 990, 1545
        sink = e_io((t - T['plate']) / 1.6)
        rise = e_out((t - T['feeding']) / 1.4) if t >= T['feeding'] else 0

        def fn(d, P, s):
            d.rounded_rectangle((*P(x0, y0), *P(x1, y1)), radius=int(18 * s), fill=(12, 28, 42, 240), outline=col(WHITE, .7), width=int(3 * s))
            d.rectangle((*P(x0 + 4, y0 + 40), *P(x1 - 4, y0 + 95)), fill=(30, 80, 120, 255))                 # ocean
            d.polygon([P(500, y0 + 95), P(x1 - 4, y0 + 75), P(x1 - 4, y1 - 4), P(620, y1 - 4)], fill=(120, 104, 82, 255))   # continent
            off = sink * 40
            slab = [(x0 + 4, y0 + 95), (470 + off * .3, y0 + 95), (700 + off, y1 - 30 + off * .2), (640 + off, y1 - 4), (x0 + 4, y0 + 125)]
            d.polygon([P(*q) for q in slab], fill=(55, 120, 150, 255), outline=col(WHITE, .6))
            for k in range(3):
                ax = 160 + k * 90 + (t * 30 % 90)
                pts = [(ax, y0 + 110), (ax + 40, y0 + 110)]
                d.line([P(*q) for q in pts], fill=col(WHITE), width=int(4 * s))
                _head(d, P, s, pts[-1], 0, 12, col(WHITE))
            vx = 800
            d.polygon([P(vx - 60, y0 + 78), P(vx, y0 + 30), P(vx + 60, y0 + 76)], fill=(150, 130, 110, 255), outline=col(WHITE))
            if rise > 0:
                yy = lerp(y1 - 50, y0 + 60, rise)
                d.line([P(vx - 30, y1 - 50), P(vx, yy)], fill=col((255, 110, 40)), width=int(12 * s))
                d.ellipse((*P(vx - 14, yy - 14), *P(vx + 14, yy + 14)), fill=col(YEL))
        vec(cv, (x0, y0, x1, y1), fn, al, ss=2, base=(12, 28, 42))
        label(cv, 'OCEAN PLATE', 230, y1 - 70, t, T['where'] + .2, None, 24, (170, 225, 240), rise=0)
        label(cv, 'NORTH AMERICAN PLATE', 860, y1 - 30, t, T['where'] + .4, None, 22, WHITE, rise=0)
        label(cv, 'MAGMA RISES', 870, y0 + 150, t, T['feeding'] + .3, None, 22, YEL, rise=0, anchor='l') if False else None
        label(cv, 'SCHEMATIC', x1 - 16, y0 + 22, t, T['where'], None, 17, (210, 220, 225), rise=0, anchor='r')

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        u = self.up(t)
        if u > 0:
            cv.alpha_composite(_section_bg())
            self.section(cv, t, clamp(u * 1.5))
            label(cv, 'MOUNT ST. HELENS, WASHINGTON', 540, 280, t, 0, None, 28, WHITE, rise=0)
        if u < 1:
            slide_map(cv, self.map_layer(t, st), -H * u)
        # lower info area ------------------------------------------------------------
        hero(cv, 'IN ONE MORNING', 540, 1270, t, T['morning'] - .1, T['on'] - .2, 76, WHITE)
        hero(cv, 'MAY 18, 1980', 540, 1280, t, T['may'], T['earthquake'] - .2, 110, LIME)
        chip(cv, 'LARGEST LANDSLIDE', 540, 1260, t, T['landslide'], T['with_'] - .1, size=42, accent=ORANGE, sub='IN RECORDED HISTORY')
        chip(cv, 'PRESSURE RELEASED', 540, 1260, t, T['pressure'], T['blasted'] - .1, size=40, accent=ORANGE)
        chip(cv, 'SIDEWAYS BLAST', 540, 1260, t, T['blasted'], T['sqmi'] - .1, size=42, accent=ORANGE, sub='TOWARD THE NORTH')
        hero(cv, '≈230 SQ MI', 540, 1280, t, T['sqmi'], T['fifty'] - .1, 110, LIME)
        label(cv, 'AREA DEVASTATED', 540, 1380, t, T['sqmi'] + .2, T['fifty'] - .1, 28, WHITE)
        hero(cv, '≈15 MILES HIGH', 540, 1280, t, T['fifteen'], T['and_winds'] - .4, 96, LIME)
        label(cv, 'IN MINUTES', 540, 1380, t, T['fifteen'] + .2, T['and_winds'] - .4, 28, WHITE)
        self.plates_inset(cv, t)
        label(cv, 'SOURCE: USGS', 540, 1595, t, T['zoom'], None, 18, (200, 210, 215), rise=0)


YEL = (255, 214, 90)


@functools.lru_cache(None)
def _section_bg():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    c0, c1 = np.array([10, 24, 36], np.float32), np.array([5, 12, 19], np.float32)
    rgb = (c0 * (1 - y) + c1 * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    return Image.fromarray(np.concatenate([rgb, np.full((H, W, 1), 255, np.float32)], -1).astype(np.uint8), 'RGBA')
