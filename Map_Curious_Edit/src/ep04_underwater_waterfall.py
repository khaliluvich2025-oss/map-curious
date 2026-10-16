"""04 - Underwater Waterfall (Denmark Strait cataract).

The ocean cross-section is schematic: dense cold water flowing beneath warmer
water over a ridge and down the slope - never water falling through air.
Greenland / Iceland highlights are traced from the supplied Blue Marble image's
own coastlines (the pack's region_highlight.png for this episode was empty).
"""
from episode import *
from scipy import ndimage as nd
from engine import _head

BX0, BX1, BY0, BY1 = 60, 1020, 330, 930
SURF = 405
FLOOR = [(0, 700), (250, 690), (380, 640), (440, 626), (520, 664), (640, 762), (760, 852), (900, 896), (1080, 908)]
COLD_TOP_L = [(0, 535), (300, 548), (420, 576), (470, 612)]
COLD_THICK = 58


def fy(x):
    xs, ys = zip(*FLOOR); return float(np.interp(x, xs, ys))


def cold_top(x):
    if x <= 470:
        xs, ys = zip(*COLD_TOP_L); return float(np.interp(x, xs, ys))
    return min(fy(x) - COLD_THICK, float(np.interp(x, [470, 560], [612, fy(560) - COLD_THICK])))


def warm_bottom(x):
    return float(np.interp(x, [0, 470, 700, 1080], [530, 575, 600, 610]))


MID = [(x, (cold_top(x) + fy(x)) / 2) for x in range(90, 1001, 15)]


class EP(Episode):
    slug = '04_Underwater_Waterfall'
    gfx = '04_denmark_strait'
    out = '04_Underwater_Waterfall_Final.mp4'
    title = 'How Can a Waterfall Exist Underwater?'
    cover_title = 'HOW CAN A\nWATERFALL EXIST\nUNDERWATER?'
    cover_t = 18.8
    emphasis = ['waterfall', 'underwater?', 'Greenland', 'Iceland,', 'Denmark', 'Strait.', 'Cold,', 'dense', 'Nordic', 'Seas',
                'warmer', 'denser', 'sinks', 'ridge', 'seafloor.', 'cataract.', 'air,', 'Niagara', 'Falls', 'underneath',
                'densities', 'hidden.', 'coastline,', 'waves,', 'ocean', 'floor.']

    def setup(self):
        w = self.w
        self.base = self.base_map(.84)
        self.plate = Image.open(self.G / 'illustration_ocean_plate.png').convert('RGB').resize((W, H), Image.LANCZOS)
        self.plate = ImageEnhance.Brightness(self.plate).enhance(.8).convert('RGBA')
        self._build_land()
        g = self.geo
        self.strait_mid = g(-24.7, 67.57)
        self.br_a, self.br_b = g(-26.49, 68.70), g(-22.98, 66.44)
        self.cold_route = spline([g(*p) for p in [(-13, 70.6), (-19, 68.9), (-24.6, 67.3), (-27.2, 65.9), (-31.5, 64.0), (-36.5, 62.0)]])
        self.warm_route = spline([g(*p) for p in [(-29, 58.6), (-28, 61.5), (-26.6, 64.2), (-25.6, 65.6)]])
        T = self.T = dict(
            exist=w('exist'), underwater=w('underwater', 1), look=w('Look', 1), greenland=w('Greenland'), iceland=w('Iceland'),
            denmark=w('Denmark'), cold=w('Cold'), flows=w('flows'), nordic=w('Nordic'), meets=w('meets'), warmer=w('warmer'),
            the_d=w('The', 1), sinks=w('sinks'), then=w('then'), spills=w('spills'), ridge=w('ridge'), descends=w('descends'),
            scientists=w('Scientists'), cataract=w('cataract'), it=w('It', 1), falling=w('falling'), air=w('air'),
            niagara=w('Niagara'), its=w("It's"), moving=w('moving'), because=w('because'), densities=w('densities'),
            from_=w('From'), downward=w('downward'), hidden=w('hidden'), to=w('To'), past=w('past'), coastline=w('coastline'),
            beneath3=w('beneath', 3), down=w('down'), shape=w('shape'), floor=w('floor'))
        sm = self.strait_mid
        self.cam = Cam([
            frame_on(sm, 560, 640, 1.45, 0), frame_on(sm, 560, 640, 1.5, T['exist']), frame_on(sm, 540, 620, 2.5, T['exist'] + .9),
            frame_on(sm, 540, 620, 2.5, T['look'] - .3), frame_on(sm, 560, 640, 1.5, T['look'] + .5),
            frame_on(sm, 560, 700, 1.38, T['cold'] - .2), frame_on(sm, 600, 700, 1.25, T['meets']),
            frame_on(sm, 560, 640, 2.6, T['the_d'] + .7), frame_on(sm, 560, 640, 1.4, T['to'] + .4),
            frame_on(sm, 560, 650, 1.5, T['beneath3'] - .1), frame_on(sm, 540, 640, 2.4, T['down'] + .2), frame_on(sm, 540, 640, 2.5, self.dur)])
        # section visibility windows
        self.sec_win = [(T['exist'] + .55, T['look'] - .15), (T['the_d'] + .3, T['from_'] - .1), (T['down'] - .15, None)]
        self.plate_win = [(T['exist'] + .25, T['look'] - .1), (T['the_d'], T['from_'] + 3.75), (T['beneath3'] + .2, None)]
        b = self.beat
        b(0.0, 'Greenland (lime) and Iceland (orange) highlighted on the map', 'pop', 2)
        b(.45, 'Denmark Strait marker pulses', 'tick')
        b(T['exist'], 'Camera pushes into the strait', 'whoosh')
        b(T['exist'] + .25, 'Dive below the surface (illustrative ocean plate)', 'bubble')
        b(T['exist'] + .55, 'Schematic section: cold dense flow spills over the ridge', 'rumble')
        b(T['look'] - .15, 'Back up to the map', 'whoosh')
        b(T['greenland'], 'GREENLAND label', 'pop'); b(T['iceland'], 'ICELAND label', 'pop')
        b(T['denmark'], 'Strait bracket + DENMARK STRAIT', 'tick')
        b(T['cold'], 'Cold dense flow arrow from the north', 'swish')
        b(T['nordic'], 'NORDIC SEAS label', 'tick')
        b(T['meets'], 'Warmer water arrow from the south', 'swish')
        b(T['the_d'], 'Dive: section returns, layers separate', 'bubble')
        b(T['sinks'], 'Cold layer slides beneath warm layer', 'rumble')
        b(T['spills'], 'Ridge outline draws; flow crosses the crest', 'swish')
        b(T['ridge'], 'UNDERWATER RIDGE label', 'tick')
        b(T['descends'], 'Flow descends the slope', 'rumble')
        b(T['scientists'], 'Section pushes in on the slope', None)
        b(T['cataract'] - .3, 'UNDERWATER CATARACT title chip', 'pop')
        b(T['it'], 'Comparison card: water falling through air', 'swish')
        b(T['air'], 'Red cross: not this', 'thud', -3)
        b(T['niagara'], 'NOT NIAGARA FALLS stamp', 'thud', -3)
        b(T['its'], 'Section back: warmer above, colder below', 'swish')
        b(T['moving'], 'Flow particles speed along the floor', None)
        b(T['because'], 'Density balance tips toward cold water', 'tick')
        b(T['densities'], 'LESS DENSE / MORE DENSE', 'pop')
        b(T['from_'], 'Surface view (illustration)', 'bubble')
        b(T['downward'], 'Faint hidden flow arrow beneath the surface', 'swish')
        b(T['hidden'], 'HIDDEN FROM THE SURFACE', 'tick')
        b(T['to'], 'Back to the overhead map', 'whoosh')
        b(T['coastline'] - .3, 'Coastlines glow', 'shimmer')
        b(T['beneath3'], 'Map sinks into deep blue', 'bubble')
        b(T['down'] - .15, 'Seafloor profile draws, flow returns', 'rumble')
        b(T['shape'], 'THE SHAPE OF THE OCEAN FLOOR', 'pop')

    # -------------------------------------------------------------------------
    def _build_land(self):
        im = np.asarray(Image.open(self.G / 'map_terrain.jpg').convert('RGB'), np.int16)
        R, G, B = im[..., 0], im[..., 1], im[..., 2]
        land = nd.binary_opening(~((B > R + 20) & (B >= G)), iterations=1)
        lab, n = nd.label(land)
        gx, gy = self.geo(-40, 72); ix, iy = self.geo(-18.6, 64.9)
        out = {}
        for name, (x, y), c, fa in (('gl', (gx, gy), LIME, .30), ('ic', (ix, iy), ORANGE, .55)):
            m = nd.binary_fill_holes(lab == lab[int(y), int(x)])
            big = Image.fromarray((m * 255).astype(np.uint8)).resize((W * 2, H * 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.5))
            m2 = np.asarray(big) > 127
            edge = m2 & ~nd.binary_erosion(m2, iterations=5)
            fill = np.zeros((H * 2, W * 2, 4), np.uint8); fill[m2] = c + (int(255 * fa),)
            bord = np.zeros((H * 2, W * 2, 4), np.uint8); bord[edge] = WHITE + (240,)
            out[name] = (Image.fromarray(fill, 'RGBA'), Image.fromarray(bord, 'RGBA'))
        self.land = out

    def map_layer(self, cv, t, st):
        T = self.T
        self.draw_map(cv, st)
        deep = .55 * prog(t, T['beneath3'], .9, e_io)
        glow = vis(t, T['coastline'] - .3, T['beneath3'] + .3, .3, .5)
        for name, a0 in (('gl', -.4), ('ic', -.25)):
            fill, bord = self.land[name]
            fa = vis(t, a0, None, .4)
            if fa > 0:
                cv.alpha_composite(with_alpha(render_map(fill, st, 2.0), fa * (1 - deep * .6)))
                cv.alpha_composite(with_alpha(render_map(bord, st, 2.0), fa * (.75 + .25 * glow)))
                if glow > 0:
                    gb = render_map(bord, st, 2.0).filter(ImageFilter.GaussianBlur(5))
                    cv.alpha_composite(with_alpha(gb, glow * (.6 + .4 * math.sin(t * 7) ** 2)))
        tint(cv, (4, 20, 52), deep)
        cv.alpha_composite(vignette())
        S = lambda p: Cam.S(st, *p)
        gl_l = S(self.geo(-33.5, 69.6)); ic_l = S(self.geo(-18.7, 64.95))
        chip(cv, 'GREENLAND', *gl_l, t, .0, T['exist'] + .4, size=40)
        chip(cv, 'ICELAND', ic_l[0], ic_l[1] + 70, t, .25, T['exist'] + .4, size=40, accent=ORANGE)
        chip(cv, 'GREENLAND', *gl_l, t, T['greenland'], T['the_d'], size=40)
        chip(cv, 'ICELAND', ic_l[0], ic_l[1] + 70, t, T['iceland'], T['the_d'], size=40, accent=ORANGE)
        mx, my = S(self.strait_mid)
        pin(cv, mx, my, t, .45, T['exist'] + .4, LIME, 14)
        pin(cv, mx, my, t, T['denmark'] - .1, T['the_d'], LIME, 12, rings=False)
        # bracket across the strait
        a, b2 = S(self.br_a), S(self.br_b)
        pb = e_out((t - T['denmark']) / .6)
        al = vis(t, T['denmark'], T['the_d'] - .1)
        route(cv, [a, b2], pb, WHITE, 5, head=False, alpha=al, dashed=True, dash=(12, 9))
        for (x, y) in (a, b2):
            ring(cv, x, y, 9, t, T['denmark'] + .4, T['the_d'] - .1, WHITE, 4)
        chip(cv, 'DENMARK STRAIT', 540, 320, t, T['denmark'] + .1, T['cold'] - .1, size=42, sub='BETWEEN GREENLAND & ICELAND')
        bm = ((a[0] + b2[0]) / 2, (a[1] + b2[1]) / 2)
        label(cv, 'DENMARK STRAIT', bm[0] - 30, bm[1], t, T['cold'], T['the_d'] - .1, 26, WHITE, anchor='r')
        # currents
        scr = [S(q) for q in self.cold_route]
        route(cv, scr, e_io((t - T['cold']) / 2.2), TEAL, 16, alpha=vis(t, T['cold'], T['the_d'] + .2), dashed=True,
              dash=(34, 18), phase=-t * 70, head_size=44)
        route(cv, scr, 1.0, TEAL, 10, alpha=.55 * vis(t, T['to'] + .6, T['beneath3'] + .2), dashed=True, dash=(30, 18),
              phase=-t * 70, head_size=34)
        ns = S(self.geo(-17.5, 69.4))
        label(cv, 'NORDIC SEAS', ns[0], ns[1], t, T['nordic'], T['the_d'], 34, TEAL)
        scr = [S(q) for q in self.warm_route]
        route(cv, scr, e_io((t - T['meets']) / 1.4), ORANGE, 16, alpha=vis(t, T['meets'], T['the_d'] + .2), dashed=True,
              dash=(34, 18), phase=-t * 70, head_size=44)
        chip(cv, 'COLD, DENSE WATER', 540, 320, t, T['cold'] + .1, T['meets'] - .1, size=40, accent=TEAL, sub='FLOWS SOUTH')
        chip(cv, 'MEETS WARMER WATER', 540, 320, t, T['meets'], T['the_d'] - .1, size=40, accent=ORANGE)
        chip(cv, 'COASTLINE', 540, 320, t, T['coastline'], T['beneath3'] - .1, size=40)
        chip(cv, 'BENEATH THE WAVES', 540, 320, t, T['beneath3'], T['down'] - .2, size=40, accent=TEAL)

    def section(self, cv, t, al, dim=1.0):
        T = self.T
        # timeline-driven state
        if t < T['look']:
            cold = 1.0; flow = e_io((t - (T['exist'] + .75)) / 1.3); ridge = 1.0
        else:
            cold = e_io((t - T['sinks']) / 1.0)
            flow = max(e_io((t - T['spills']) / 1.6) * .47, e_io((t - T['descends']) / 1.3) if t >= T['descends'] else 0)
            ridge = e_io((t - T['spills']) / 1.0)
            if t >= T['down'] - .2:
                cold, ridge, flow = 1.0, e_io((t - T['down']) / 1.4), e_io((t - T['down'] - .3) / 1.4)
        if t >= T['its'] - .3 and t < T['down'] - .2:
            cold, ridge, flow = 1.0, 1.0, 1.0
        speed = 1.0 + 1.5 * vis(t, T['moving'], T['because'] + .5)
        zs = 1.0 + .18 * vis(t, T['scientists'], T['it'] - .2, 1.2, .6)
        fx_, fy_ = 700, 760
        D = lambda x, y: ((x - fx_) * zs + fx_, (y - fy_) * zs + fy_)
        xr = lerp(60, 1020, cold)

        def fn(d, P, s):
            Q = lambda x, y: P(*D(x, y))
            # water gradient
            for i in range(24):
                y0 = lerp(SURF, BY1 + 200, i / 24); y1 = lerp(SURF, BY1 + 200, (i + 1) / 24)
                c = tuple(int(lerp(a, b, i / 23)) for a, b in zip((28, 92, 138), (5, 22, 40)))
                d.rectangle((*Q(BX0 - 300, y0), *Q(BX1 + 300, y1 + 1)), fill=c + (255,))
            d.rectangle((*Q(BX0 - 300, BY0 - 300), *Q(BX1 + 300, SURF)), fill=(12, 26, 40, 255))
            # warm upper water
            top = [Q(x, SURF + 3) for x in range(0, 1081, 40)]
            bot = [Q(x, warm_bottom(x)) for x in range(1080, -1, -40)]
            d.polygon(top + bot, fill=col(ORANGE, .42))
            # waves
            wv = [Q(x, SURF + 5 * math.sin(x / 38 + t * 2.2)) for x in range(-40, 1121, 12)]
            d.line(wv, fill=col(WHITE, .85), width=int(4 * s))
            # cold dense water
            if cold > 0:
                xs = [x for x in range(0, 1081, 12) if x <= xr] + [xr]
                poly = [Q(x, cold_top(x)) for x in xs] + [Q(x, fy(x) + 2) for x in reversed(xs)]
                d.polygon(poly, fill=col(TEAL, .55))
            # seafloor
            fl = [Q(x, y) for x, y in FLOOR] + [Q(1080, BY1 + 300), Q(0, BY1 + 300)]
            d.polygon(fl, fill=(57, 74, 88, 255))
            if ridge > 0:
                pts, _ = partial([(x, y) for x, y in FLOOR], ridge)
                if len(pts) > 1:
                    d.line([Q(*q) for q in pts], fill=col(WHITE), width=int(5 * s), joint='curve')
            # flow arrow + particles
            if flow > 0:
                pts, ang = partial(MID, flow)
                if len(pts) > 1:
                    qq = [Q(*q) for q in pts]
                    d.line(qq, fill=col(WHITE, .9), width=int(7 * s), joint='curve')
                    _head(d, Q, s, pts[-1], ang, 22, col(WHITE))
                L = cumlen(MID)[-1]
                for i in range(22):
                    ph = ((t * .09 * speed) + i / 22) % 1.0
                    if ph > flow:
                        continue
                    (x, y), _ = point_at(MID, ph)
                    q = Q(x, y + 14 * math.sin(i * 1.7)); r = 4.5 * s
                    d.ellipse((q[0] - r, q[1] - r, q[0] + r, q[1] + r), fill=col(WHITE, .8))
            d.rounded_rectangle((*P(BX0, BY0), *P(BX1, BY1)), radius=int(22 * s), outline=col(WHITE, .9), width=int(4 * s))

        tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vec(tmp, (BX0, BY0, BX1, BY1), fn, 1.0, ss=2, base=(30, 60, 90))
        sec = tmp.crop((BX0, BY0, BX1, BY1))
        m = Image.new('L', sec.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, sec.width - 1, sec.height - 1), radius=22, fill=255)
        sec.putalpha(Image.fromarray(np.minimum(np.asarray(sec.getchannel('A')), np.asarray(m))))
        sc = .9 + .1 * clamp(al)
        place(cv, with_alpha(sec, clamp(al) * dim), 540, (BY0 + BY1) / 2, sc, 1.0)
        if al < .6:
            return
        L = lambda x, y: D(x, y)
        la = dim
        label(cv, 'SCHEMATIC · NOT TO SCALE', 1000, 908, t, 0, None, 19, (225, 230, 225), rise=0, anchor='r')
        label(cv, 'NORTH', 90, 368, t, 0, None, 22, (200, 215, 225), rise=0, anchor='l')
        label(cv, 'SOUTH', 990, 368, t, 0, None, 22, (200, 215, 225), rise=0, anchor='r')
        if dim > .9:
            label(cv, 'WARMER WATER', *L(760, 470), t, T['the_d'] + .4, T['it'] - .2, 30, (255, 200, 150))
            label(cv, 'COLD, DENSE WATER', *L(230, 610), t, T['sinks'], T['it'] - .2, 30, (170, 245, 240))
            label(cv, 'UNDERWATER RIDGE', *L(390, 690), t, T['ridge'], T['it'] - .2, 28, WHITE)
            label(cv, 'WARMER, LIGHTER', 760, 470, t, T['its'] + .2, T['from_'] - .2, 30, (255, 200, 150))
            label(cv, 'COLDER, DENSER', 260, 610, t, T['its'] + .9, T['from_'] - .2, 30, (170, 245, 240))
            label(cv, 'COLD WATER FLOWS OVER THE RIDGE', 540, 368, t, T['exist'] + .9, T['look'] - .2, 24, WHITE, rise=0)
            label(cv, 'SEAFLOOR', 300, 800, t, T['down'] + .2, None, 30, WHITE)
            label(cv, 'DENSE COLD WATER', 760, 640, t, T['down'] + .6, None, 28, (170, 245, 240))

    def compare_card(self, cv, t):
        T = self.T
        al = vis(t, T['it'], T['its'] - .2, .35, .3)
        if al <= 0:
            return
        x0, y0, x1, y1 = 190, 370, 890, 880
        p = e_out((t - T['it']) / .4)
        xr = e_out((t - T['air']) / .35) if t >= T['air'] else 0

        def fn(d, P, s):
            d.rounded_rectangle((*P(x0, y0), *P(x1, y1)), radius=int(24 * s), fill=(12, 24, 36, 245), outline=col(WHITE, .8), width=int(3 * s))
            # sky gradient band
            d.rounded_rectangle((*P(x0 + 20, y0 + 70), *P(x1 - 20, y1 - 20)), radius=int(14 * s), fill=(60, 110, 150, 255))
            # cliff
            d.polygon([P(x0 + 20, 520), P(470, 520), P(500, 560), P(480, y1 - 20), P(x0 + 20, y1 - 20)], fill=(84, 78, 70, 255))
            # river on top + falling water through air
            d.rectangle((*P(x0 + 20, 505), *P(480, 522)), fill=(110, 180, 230, 255))
            for i in range(9):
                xx = 485 + i * 9 + 4 * math.sin(t * 6 + i)
                yy0 = 525 + ((t * 300 + i * 40) % 60)
                d.line([P(xx, 525), P(xx + 18 + i * 2, y1 - 80)], fill=(190, 225, 245, 230), width=int(6 * s))
            # pool
            d.ellipse((*P(470, y1 - 110), *P(x1 - 30, y1 - 40)), fill=(90, 160, 210, 255))
            if xr > 0:
                c = col(RED); wdt = int(16 * s)
                a1, b1 = (330, 470), (750, 830)
                a2, b2 = (750, 470), (330, 830)
                d.line([P(*a1), P(lerp(a1[0], b1[0], xr), lerp(a1[1], b1[1], xr))], fill=c, width=wdt)
                if xr > .5:
                    q = (xr - .5) * 2
                    d.line([P(*a2), P(lerp(a2[0], b2[0], q), lerp(a2[1], b2[1], q))], fill=c, width=wdt)
        tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vec(tmp, (x0 - 10, y0 - 10, x1 + 10, y1 + 10), fn, 1.0, ss=2, base=(12, 24, 36))
        place(cv, tmp.crop((x0 - 10, y0 - 10, x1 + 10, y1 + 10)), 540, (y0 + y1) / 2, .85 + .15 * p, al)
        label(cv, 'NOT WATER FALLING THROUGH AIR', 540, 410, t, T['it'] + .2, T['its'] - .2, 28, WHITE, rise=0)

    def balance(self, cv, t):
        T = self.T
        al = vis(t, T['because'], T['from_'] - .2, .3, .3)
        if al <= 0:
            return
        tilt = .2 * e_io((t - T['because'] - .3) / .8)
        cx, cy = 540, 1330

        def fn(d, P, s):
            d.polygon([P(cx, cy), P(cx - 26, cy + 70), P(cx + 26, cy + 70)], fill=col(WHITE, .9))
            ax, ay = cx - 230 * math.cos(tilt), cy - 230 * math.sin(tilt)
            bx, by = cx + 230 * math.cos(tilt), cy + 230 * math.sin(tilt)
            d.line([P(ax, ay), P(bx, by)], fill=col(WHITE), width=int(8 * s))
            for (x, y, c, sz) in ((ax, ay, ORANGE, 70), (bx, by, TEAL, 70)):
                d.line([P(x, y), P(x, y - 20)], fill=col(WHITE), width=int(4 * s))
                d.rounded_rectangle((*P(x - sz / 2, y - 20 - sz), *P(x + sz / 2, y - 20)), radius=int(10 * s), fill=col(c),
                                    outline=col(OUTLINE), width=int(4 * s))
        vec(cv, (cx - 320, cy - 160, cx + 320, cy + 90), fn, al)
        ax, ay = cx - 230 * math.cos(tilt), cy - 230 * math.sin(tilt)
        bx, by = cx + 230 * math.cos(tilt), cy + 230 * math.sin(tilt)
        label(cv, 'WARMER', ax, ay + 40, t, T['because'] + .2, T['from_'] - .2, 26, (255, 200, 150), rise=0)
        label(cv, 'COLDER', bx, by + 40, t, T['because'] + .2, T['from_'] - .2, 26, (170, 245, 240), rise=0)
        label(cv, 'LESS DENSE', ax, ay + 76, t, T['densities'], T['from_'] - .2, 24, WHITE, rise=6)
        label(cv, 'MORE DENSE', bx, by + 76, t, T['densities'], T['from_'] - .2, 24, WHITE, rise=6)

    def draw(self, cv, t):
        T = self.T
        st = self.cam.at(t)
        self.map_layer(cv, t, st)
        # plate (dive) -------------------------------------------------------------
        for a, b in self.plate_win:
            al = vis(t, a, b, .5, .45)
            if al > 0:
                wipe = e_out((t - a) / .55)
                h = int(H * wipe)
                if h > 0:
                    pl = with_alpha(self.plate.crop((0, 0, W, h)), al)
                    paste(cv, pl, 0, 0)
                    if wipe < 1:
                        route(cv, [(0, h), (W, h)], 1.0, WHITE, 5, head=False, alpha=.7 * al, outline=False)
        # section ------------------------------------------------------------------
        for a, b in self.sec_win:
            al = vis(t, a, b, .4, .35)
            if al > 0:
                dim = 1 - .75 * vis(t, T['it'], T['its'] - .3, .3, .3)
                surf_view = vis(t, T['from_'] - .1, T['to'], .4, .4)
                self.section(cv, t, al * (1 - surf_view), dim)
        self.compare_card(cv, t)
        # surface view: hidden flow
        a_h = T['downward']
        sv = vis(t, T['from_'], T['to'] - .1, .4, .4)
        if sv > 0:
            pts = spline([(150, 560), (420, 640), (640, 820), (930, 900)])
            route(cv, pts, e_io((t - a_h) / 1.2), TEAL, 18, alpha=.35 * sv * vis(t, a_h), dashed=True, dash=(30, 20),
                  phase=-t * 50, outline=False)
            chip(cv, 'FROM THE SURFACE', 540, 320, t, T['from_'], T['to'] - .2, size=40, accent=TEAL)
        if any(vis(t, a, b, .5, .45) > .3 for a, b in self.plate_win) and not any(vis(t, a, b) > .5 for a, b in self.sec_win):
            label(cv, 'ILLUSTRATION', 540, 1560, t, 0, None, 18, (210, 220, 225), rise=0)
        # lower info area -----------------------------------------------------------
        chip(cv, 'DENSER WATER SINKS', 540, 1260, t, T['sinks'], T['spills'] - .1, size=38, accent=TEAL)
        chip(cv, 'SPILLS OVER A RIDGE', 540, 1260, t, T['spills'] + .1, T['descends'] - .1, size=38, accent=TEAL)
        chip(cv, 'DESCENDS ALONG THE SEAFLOOR', 540, 1260, t, T['descends'], T['cataract'] - .4, size=36, accent=TEAL)
        chip(cv, 'UNDERWATER CATARACT', 540, 1270, t, T['cataract'] - .3, T['it'] - .1, size=46, accent=LIME, sub='WHAT SCIENTISTS CALL IT')
        stamp(cv, 'NOT NIAGARA FALLS', 540, 1300, t, T['niagara'], T['its'] - .2, 56, RED, -5)
        chip(cv, 'ONE WATER MASS BENEATH ANOTHER', 540, 1260, t, T['moving'] - .3, T['because'] - .1, size=34, accent=TEAL)
        self.balance(cv, t)
        chip(cv, 'THE FLOW IS HIDDEN', 540, 1260, t, T['hidden'] - .1, T['to'] - .2, size=40, accent=TEAL)
        chip(cv, 'THE SHAPE OF THE OCEAN FLOOR', 540, 1260, t, T['shape'], None, size=36, accent=LIME)
