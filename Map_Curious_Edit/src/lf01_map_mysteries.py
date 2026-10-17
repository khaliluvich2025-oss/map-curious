"""LF01 - 6 Places on the Map That Sound Made Up (But Are Real).  16:9 long-form pilot.

Render with MC_LANDSCAPE=1 (1920x1080).  One narration file, eight parts; every beat is keyed to a
spoken word inside its part.  Base maps: the four NASA Blue Marble packs (map px 1080x1920).
Facts: see Map_Curious_LongForm/LF01_Map_Mysteries/script.md (fact-check table).
Diagrams are schematic and labelled as such.
"""
import glob, re
from episode import *
from engine import _head, MW, MH

assert W == 1920, 'render LF01 with MC_LANDSCAPE=1'
LF = ROOT / 'Map_Curious_LongForm' / 'LF01_Map_Mysteries'
YEL = (255, 214, 90)
BLUE = (90, 170, 255)
COLD = (70, 140, 235)
WARM = (240, 150, 90)
FIRE = (255, 110, 40)
SMOKE = (150, 150, 150)
CHIP_XY = (90, 120)        # info chip slot (top-left, anchored left)
HERO_XY = (1560, 210)      # hero number slot (top-right)
PX0, PX1, PY0, PY1 = 150, 1770, 110, 880    # full-screen diagram panel

SCENES = {   # name: (gfx folder, map brightness)
    'fl': ('01_fort_jefferson', .86), 'pnw': ('02_db_cooper', .86), 'ne': ('03_centralia', .86), 'na': ('04_denmark_strait', .9)}

HUDSON = [(-73.94, 44.10), (-74.02, 43.85), (-73.98, 43.60), (-73.80, 43.40), (-73.64, 43.31), (-73.58, 43.25),
          (-73.62, 43.00), (-73.68, 42.80), (-73.686, 42.752), (-73.75, 42.65), (-73.79, 42.25), (-73.97, 41.93),
          (-73.94, 41.70), (-74.00, 41.50), (-73.96, 41.39), (-73.89, 41.07), (-73.93, 40.85), (-74.02, 40.70), (-74.04, 40.60)]
TROY, NYC, NEWB, ALB = (-73.686, 42.752), (-74.006, 40.713), (-74.01, 41.50), (-73.756, 42.653)
FJ, KW = (-82.873, 24.628), (-81.78, 24.555)
CENT = (-76.343, 40.804)
PDX, SEA_, RENO, TENA = (-122.60, 45.59), (-122.31, 47.45), (-119.77, 39.53), (-122.78, 45.70)
JUMP = (-122.55, 45.93)
DS = (-24.7, 67.57)
SURT, HEIM = (-20.605, 63.303), (-20.27, 63.44)


def fo(p, z, sx=960, sy=500):
    """Camera key (cx, cy, z) that puts map point p at screen (sx, sy)."""
    return (p[0] - (sx - W / 2) / z, p[1] - (sy - H / 2) / z, z)


class EP(Episode):
    slug = 'LF01_full'
    gfx = '01_fort_jefferson'
    vo = LF
    out = 'LF01_Map_Mysteries_Final.mp4'
    title = '6 Places on the Map That Sound Made Up (But Are Real)'
    cover_title = ''
    cover_t = 0
    emphasis = ['waterfall', 'burning', 'jumped', 'real,', 'Hudson', 'estuary,', 'Twice', 'north.', 'hundred', 'fifty',
                'sixty', 'both', 'ways."', 'Dry', 'Tortugas.', 'Jefferson', '1846.', 'never', 'finished.', 'prison.',
                'Mudd,', 'Centralia', 'fire.', '1962,', 'coal', 'sinkhole', 'buyout,', 'ZIP', 'centuries.', 'Cooper.',
                'bomb.', 'jumped.', 'Columbia', 'unsolved', 'Denmark', 'Strait.', 'largest', 'waterfall', 'cold,',
                'sinks', 'two', 'miles.', 'Surtsey,', 'volcano', 'island', '1967.', 'laboratory.', 'UNESCO', 'winning.',
                'half', 'comments:']

    # ------------------------------------------------------------------ setup
    def setup(self):
        files = sorted(glob.glob(str(LF / 'LF01_part0*_script.txt')))
        counts = [len(re.sub(r'\[[^\]]*\]', '', open(f).read()).split()) for f in files]
        self.prange, i = [], 0
        for c in counts:
            self.prange.append((i, i + c)); i += c
        self.pstart = [self.words[a]['start'] for a, _ in self.prange]
        self.pend = [self.words[b - 1]['end'] for _, b in self.prange]
        self.bounds = [0.0] + [(self.pend[k] + self.pstart[k + 1]) / 2 for k in range(7)] + [self.dur + 1]
        self.maps, self.bboxes = {}, {}
        for k, (g, br) in SCENES.items():
            im = Image.open(GFX / g / 'map_terrain.jpg').convert('RGB')
            im = ImageEnhance.Brightness(ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.05)).enhance(1.06)).enhance(br)
            self.maps[k] = im
            self.bboxes[k] = json.loads((GFX / g / 'storyboard.json').read_text())['bbox']
        self.regions = {'fl': Region(svg_polys(GFX / '01_fort_jefferson' / 'region_highlight.svg')),
                        'pnw': Region(svg_polys(GFX / '02_db_cooper' / 'region_highlight.svg')),
                        'ne': Region(svg_polys(GFX / '03_centralia' / 'region_highlight.svg'), color=ORANGE)}
        self.setup_parts()

    def g(self, scene, lon, lat):
        b = self.bboxes[scene]
        return ((lon - b[0]) / (b[2] - b[0]) * MW, (b[3] - lat) / (b[3] - b[1]) * MH)

    def k(self, part, word, n=1, end=False):
        """Time of the n-th `word` inside part (1-based)."""
        a, b = self.prange[part - 1]
        cs = any(ch.isupper() for ch in word)
        strip = lambda v: re.sub(r"[^A-Za-z0-9$']", '', v.replace('’', "'"))
        key = strip(word) if cs else norm_word(word); c = 0
        for x in self.words[a:b]:
            if (strip(x['w']) if cs else norm_word(x['w'])) == key:
                c += 1
                if c == n:
                    return x['end'] if end else x['start']
        raise KeyError(f'{word!r} #{n} not in part {part}')

    def part_at(self, t):
        for i in range(8):
            if t < self.bounds[i + 1]:
                return i + 1
        return 8

    # ------------------------------------------------------------------ shared drawing
    def map_view(self, cv, scene, cam, t):
        st = cam.at(t)
        cv.alpha_composite(render_map(self.maps[scene], st).convert('RGBA'))
        return st

    def S(self, st, scene, p):
        return Cam.S(st, *self.g(scene, *p))

    def panel(self, cv, t, a, b, fn, title=None, slide=.5):
        """Full-screen schematic panel (opaque), slides up at a, down at b."""
        if t < a - .01 or (b is not None and t > b + slide):
            return 0.0
        u = e_io((t - a) / slide) if t < a + slide else 1.0
        if b is not None and t > b:
            u = 1 - e_io((t - b) / slide)
        off = (1 - u) * (H + 40)
        L = Image.new('RGB', ((PX1 - PX0) * 2, (PY1 - PY0) * 2), (16, 32, 48))
        d = ImageDraw.Draw(L, 'RGBA')
        for i in range(12):
            y0 = i / 12 * L.height
            c = tuple(int(lerp(x, y, i / 11)) for x, y in zip((24, 44, 66), (14, 26, 38)))
            d.rectangle((0, y0, L.width, y0 + L.height / 12 + 1), fill=c)
        fn(d, lambda x, y: ((x - PX0) * 2, (y - PY0) * 2), 2)
        im = L.reduce(2).convert('RGBA')
        m = Image.new('L', im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=24, fill=255)
        im.putalpha(m)
        dim = Image.new('RGBA', (W, H), col(OUTLINE, .55 * u))
        cv.alpha_composite(dim)
        paste(cv, im, PX0, PY0 + off)
        bd = Image.new('RGBA', (PX1 - PX0, PY1 - PY0), (0, 0, 0, 0))
        ImageDraw.Draw(bd).rounded_rectangle((0, 0, bd.width - 1, bd.height - 1), radius=24, outline=col(WHITE, .85), width=3)
        paste(cv, bd, PX0, PY0 + off)
        if u > .95:
            label(cv, 'SCHEMATIC · NOT TO SCALE', PX1 - 24, PY1 - 26, t, a + .3, b, 18, (220, 226, 222), rise=0, anchor='r')
            if title:
                label(cv, title, (PX0 + PX1) / 2, PY0 + 34, t, a + .3, b, 26, WHITE, rise=0)
        return u

    def section_card(self, cv, t, part, num, name):
        """'#6 THE HUDSON RIVER' badge at the start of a countdown segment."""
        a = self.pstart[part - 1]
        al = vis(t, a - .1, a + 3.2, .3, .4)
        if al <= 0:
            return
        place(cv, hero_img(f'#{num}', 110, LIME), 150, 150, .6 + .4 * e_back((t - a + .1) / .4), al)
        place(cv, label_img(name, 40, WHITE), 260 + label_img(name, 40, WHITE).width / 2, 158, 1.0, al)

    def next_chip(self, cv, t, part, word, text, n=1):
        chip(cv, 'NEXT', 1700, 820, t, self.k(part, word, n), None, size=30, accent=LIME, sub=text, anchor='r')

    def fade(self, cv, t):
        a = 0.0
        for bnd in self.bounds[1:8]:
            if abs(t - bnd) < .35:
                a = max(a, 1 - abs(t - bnd) / .35)
        tint(cv, INK, a)

    # ------------------------------------------------------------------ parts
    def setup_parts(self):
        k, b = self.k, self.beat
        P = self.pstart
        # part 1: cold open montage --------------------------------------------------------
        self.p1 = dict(water=k(1, 'waterfall'), town=k(1, 'town'), man=k(1, 'man'), these=k(1, 'These'),
                       real=k(1, 'real'), six=k(1, 'six'), last=k(1, 'last'), y1963=k(1, '1963'))
        for t_, d_ in ((0, 'Hidden waterfall: Denmark Strait'), (self.p1['town'], 'Burning town: Centralia'),
                       (self.p1['man'], 'Jet route: D.B. Cooper'), (self.p1['these'], 'Six pins pop across the maps'),
                       (self.p1['last'], 'Teaser: 1963')):
            b(t_, d_, 'whoosh')
        # part 2: Hudson ---------------------------------------------------------------------
        T = self.p2 = dict(start=P[1], hudson=k(2, 'Hudson'), begins=k(2, 'begins'), albany=k(2, 'Albany'), york=k(2, 'York', 2),
                           map_=k(2, 'map'), water=k(2, 'Water'), simple=k(2, 'Simple'), except_=k(2, 'Except'),
                           estuary=k(2, 'estuary'), twice=k(2, 'Twice'), north=k(2, 'north'), tide=k(2, 'tide', 2),
                           hundred=k(2, 'hundred'), troy=k(2, 'Troy'), dry=k(2, 'dry'), sixty=k(2, 'sixty'),
                           people=k(2, 'People'), one=k(2, 'One'), both=k(2, 'both'), so=k(2, 'So'), next_=k(2, 'Next'))
        ne = lambda p: self.g('ne', *p)
        self.cam2 = Cam([(T['start'] - .5, *fo(ne((-73.9, 42.3)), 1.8)), (T['begins'], *fo(ne((-73.95, 43.6)), 2.6)),
                         (T['albany'] + .3, *fo(ne((-73.85, 42.4)), 2.2)), (T['york'] + .6, *fo(ne((-74.0, 41.0)), 2.6)),
                         (T['map_'] + .4, *fo(ne((-73.9, 42.3)), 1.9)), (T['twice'] - .3, *fo(ne((-74.0, 41.0)), 2.8)),
                         (T['hundred'], *fo(ne((-73.85, 41.8)), 1.95)), (T['dry'], *fo(ne((-73.98, 41.2)), 2.7)),
                         (T['people'] + .3, *fo(ne((-73.9, 42.2)), 2.0)), (T['next_'], *fo(ne((-73.9, 42.2)), 1.8))])
        for key, d_ in (('start', '#6 card; NE map'), ('begins', 'Source pin in the Adirondacks'), ('albany', 'River traces south'),
                        ('york', 'NYC pin'), ('map_', 'Downhill arrow chip'), ('simple', 'SIMPLE? stamp'),
                        ('except_', 'Lower half recolours: estuary'), ('estuary', 'ESTUARY chip'),
                        ('twice', 'Tide diagram panel'), ('north', 'Current flips north'), ('hundred', 'Back to map: tide reach ruler'),
                        ('troy', 'Federal Dam at Troy pin'), ('dry', 'Salt front creeps up'), ('sixty', '≈60 MI hero'),
                        ('people', 'Map pulls back'), ('both', '"FLOWS BOTH WAYS" chip'), ('next_', 'NEXT: fortress')):
            b(T[key], d_, 'pop' if key not in ('twice', 'hundred', 'people') else 'whoosh')
        # part 3: Fort Jefferson ----------------------------------------------------------------
        T = self.p3 = dict(start=P[2], key=k(3, 'Key'), past=k(3, 'past'), tortugas=k(3, 'Tortugas'), massive=k(3, 'massive'),
                           fort2=k(3, 'Fort'), y1846=k(3, '1846'), shipping=k(3, 'shipping'), gulf=k(3, 'Gulf'),
                           bricks=k(3, 'bricks'), decades=k(3, 'decades'), never=k(3, 'never'), rifled=k(3, 'rifled'),
                           settling=k(3, 'settling'), civil=k(3, 'Civil'), prison=k(3, 'prison'), mudd=k(3, 'Mudd'),
                           booth=k(3, 'Booth'), today=k(3, 'Today'), boat=k(3, 'boat'), giant=k(3, 'giant'), now=k(3, 'Now'))
        fl = lambda p: self.g('fl', *p)
        mid = ((fl(FJ)[0] + fl(KW)[0]) / 2, (fl(FJ)[1] + fl(KW)[1]) / 2)
        self.cam3 = Cam([(T['start'] - .5, *fo(fl((-81.0, 26.5)), 1.9)), (T['key'] + .3, *fo(fl(KW), 2.6, 1200, 520)),
                         (T['past'] + .6, *fo(mid, 3.2)), (T['massive'] + .2, *fo(fl(FJ), 3.4)),
                         (T['shipping'], *fo(fl((-83.5, 25.2)), 2.0)), (T['bricks'] - .2, *fo(fl(FJ), 3.4)),
                         (T['today'], *fo(fl(FJ), 3.4)), (T['giant'], *fo(mid, 3.0)), (T['now'] + 1, *fo(mid, 2.8))])
        for key, d_ in (('start', '#5 card; Florida map'), ('key', 'Key West pin'), ('past', '≈70 MI line west'),
                        ('tortugas', 'DRY TORTUGAS label'), ('massive', 'Fort outline pulses'), ('fort2', 'FORT JEFFERSON chip'),
                        ('y1846', '1846 hero'), ('shipping', 'Shipping lanes Gulf<->Atlantic'), ('bricks', 'Fort plan panel; bricks fill'),
                        ('decades', 'Years counter'), ('never', 'NEVER FINISHED stamp'), ('rifled', 'Cannonball cracks wall'),
                        ('settling', 'Fort sinks, crack lines'), ('civil', 'Back to map: PRISON chip'), ('mudd', 'Dr. Samuel Mudd chip'),
                        ('booth', 'Booth note'), ('today', 'National Park chip; boat + seaplane routes'), ('giant', 'Pull back'),
                        ('now', 'NEXT: underground')):
            b(T[key], d_, 'pop' if key not in ('bricks', 'civil', 'giant') else 'whoosh')
        # part 4: Centralia -----------------------------------------------------------------------
        T = self.p4 = dict(start=P[3], ground=k(4, 'ground'), centralia=k(4, 'Centralia'), coal=k(4, 'coal'),
                           y1962=k(4, '1962'), dump=k(4, 'dump'), crept=k(4, 'crept'), endless=k(4, 'endless'),
                           smoke=k(4, 'Smoke'), y1981=k(4, '1981'), survived=k(4, 'survived'), y1980s=k(4, '1980s'),
                           buyout=k(4, 'buyout'), houses=k(4, 'houses'), zip_=k(4, 'ZIP'), today=k(4, 'Today'),
                           still=k(4, 'still'), centuries=k(4, 'centuries'), from_=k(4, 'From'))
        cen = self.g('ne', *CENT)
        self.cam4 = Cam([(T['start'] - .5, *fo(self.g('ne', -77.6, 41.0), 1.8)), (T['centralia'], *fo(cen, 3.0)),
                         (T['coal'] + .4, *fo(cen, 3.4)), (T['today'] - .2, *fo(cen, 3.0)), (T['from_'] + 1, *fo(cen, 2.6))])
        for key, d_ in (('start', '#4 card; Pennsylvania outlined'), ('centralia', 'Centralia pin'), ('coal', 'Cross-section panel: coal seam'),
                        ('y1962', '1962 hero; fire starts'), ('crept', 'Fire spreads into mines'), ('endless', 'Seam glows'),
                        ('smoke', 'Smoke through cracks'), ('y1981', 'Sinkhole opens'), ('survived', 'SURVIVED chip'),
                        ('y1980s', 'Back to map: houses fade'), ('buyout', 'FEDERAL BUYOUT chip'), ('zip_', 'ZIP CODE crossed out'),
                        ('today', 'Empty town grid'), ('still', 'Fire glow under the map'), ('centuries', 'COULD BURN FOR CENTURIES'),
                        ('from_', 'NEXT: the sky')):
            b(T[key], d_, 'pop' if key not in ('coal', 'y1980s') else 'whoosh')
        # part 5: D.B. Cooper ----------------------------------------------------------------------
        T = self.p5 = dict(start=P[4], november=k(5, 'November'), portland=k(5, 'Portland'), seattle=k(5, 'Seattle'),
                           dan=k(5, 'Dan'), note=k(5, 'note'), bomb=k(5, 'bomb'), seattle2=k(5, 'Seattle', 2),
                           two=k(5, 'two'), parachutes=k(5, 'parachutes'), south=k(5, 'south'), low=k(5, 'low'),
                           somewhere=k(5, 'Somewhere'), stairs=k(5, 'stairs'), jumped=k(5, 'jumped'), never=k(5, 'never'),
                           searched=k(5, 'searched'), y1980=k(5, '1980'), columbia=k(5, 'Columbia'), serial=k(5, 'serial'),
                           but=k(5, 'But'), y2016=k(5, '2016'), calls=k(5, 'calls'), whether=k(5, 'Whether'), next_=k(5, 'Next'))
        pn = lambda p: self.g('pnw', *p)
        self.cam5 = Cam([(T['start'] - .5, *fo(pn((-122.4, 46.5)), 2.0)), (T['seattle'] + .4, *fo(pn((-122.45, 46.5)), 2.4)),
                         (T['south'], *fo(pn((-121.5, 44.5)), 1.8)), (T['somewhere'], *fo(pn(JUMP), 3.2)),
                         (T['searched'] + .3, *fo(pn((-122.65, 45.82)), 3.4)), (T['but'], *fo(pn((-122.5, 46.2)), 2.4)),
                         (T['next_'] + 1, *fo(pn((-122.5, 46.2)), 2.2))])
        for key, d_ in (('start', '#3 card; PNW map'), ('november', 'NOV 24, 1971 hero'), ('portland', 'Portland pin'),
                        ('seattle', 'Flight route to Seattle'), ('dan', '"DAN COOPER" ticket chip'), ('note', 'Note card'),
                        ('bomb', 'BOMB stamp'), ('two', '$200,000 hero'), ('parachutes', '4 parachutes icons'),
                        ('south', 'Route south toward Mexico (Reno)'), ('somewhere', 'Jet side-view panel'), ('stairs', 'Rear airstair lowers'),
                        ('jumped', 'Jumper falls'), ('never', 'Back to map: uncertainty cloud'), ('y1980', 'Money find pin'),
                        ('columbia', 'COLUMBIA RIVER label'), ('serial', 'SERIAL NUMBERS MATCHED chip'), ('but', 'NO BODY · NO PARACHUTE'),
                        ('y2016', '2016 hero'), ('calls', 'UNSOLVED stamp'), ('next_', 'NEXT: under the sea')):
            b(T[key], d_, 'pop' if key not in ('somewhere', 'never') else 'whoosh')
        # part 6: Denmark Strait -------------------------------------------------------------------
        T = self.p6 = dict(start=P[5], greenland=k(6, 'Greenland'), iceland=k(6, 'Iceland'), strait=k(6, 'Strait'),
                           from_=k(6, 'From'), beneath=k(6, 'beneath'), largest=k(6, 'largest'), heres=k(6, "Here's"),
                           nordic=k(6, 'Nordic'), cold=k(6, 'Cold'), meets=k(6, 'meets'), instead=k(6, 'Instead'),
                           ridge=k(6, 'ridge'), spills=k(6, 'spills'), roughly=k(6, 'roughly'), not_=k(6, "It's"),
                           through=k(6, 'through', 2), flow=k(6, 'flow'), matters=k(6, 'matters'), heat=k(6, 'heat'),
                           nobody=k(6, 'nobody'), now=k(6, 'now'))
        na = lambda p: self.g('na', *p)
        dsx = na(DS)
        self.cam6 = Cam([(T['start'] - .5, *fo(na((-26, 67.0)), 1.8)), (T['strait'] + .3, *fo(dsx, 2.8)),
                         (T['largest'] + .5, *fo(dsx, 3.2)), (T['matters'] - .3, *fo(na((-30, 64)), 1.8)),
                         (T['now'] + 1, *fo(na((-24, 65)), 1.9))])
        for key, d_ in (('start', '#2 card; Greenland + Iceland'), ('greenland', 'GREENLAND label'), ('iceland', 'ICELAND label'),
                        ('strait', 'DENMARK STRAIT marker'), ('beneath', 'Surface ripples, dive'), ('largest', 'LARGEST WATERFALL chip'),
                        ('heres', 'Ocean section panel'), ('nordic', 'Cold water mass (blue)'), ('meets', 'Warm Atlantic water (orange)'),
                        ('instead', 'Cold sinks under warm'), ('ridge', 'Ridge highlighted'), ('spills', 'Cascade down the slope'),
                        ('roughly', '≈11,500 FT ruler'), ('not_', 'Air vs water comparison'), ('flow', 'Flow dwarfs land falls'),
                        ('matters', 'Back to map: Atlantic currents'), ('heat', 'Warm/cold conveyor arrows'), ('now', 'NEXT: 1963')):
            b(T[key], d_, 'pop' if key not in ('heres', 'matters') else 'whoosh')
        # part 7: Surtsey ---------------------------------------------------------------------------
        T = self.p7 = dict(start=P[6], fishermen=k(7, 'fishermen'), smoke=k(7, 'smoke'), first=k(7, 'first'),
                           ship2=k(7, 'ship', 2), underwater=k(7, 'underwater'), within=k(7, 'Within'), broke=k(7, 'broke'),
                           named=k(7, 'named'), surtsey=k(7, 'Surtsey'), fire=k(7, 'fire'), y1967=k(7, '1967'),
                           square=k(7, 'square'), unusual=k(7, 'unusual'), scientists=k(7, 'Scientists'), only=k(7, 'Only'),
                           seeds=k(7, 'seeds'), laboratory=k(7, 'laboratory'), watched=k(7, 'watched'), seeds2=k(7, 'seeds', 2),
                           insects2=k(7, 'insects', 2), birds=k(7, 'birds'), plants=k(7, 'plants'), today=k(7, 'Today'),
                           unesco=k(7, 'UNESCO'), but=k(7, 'But'), waves=k(7, 'Waves'), half=k(7, 'half'),
                           island=k(7, 'island', 2), disappearing=k(7, 'disappearing'))
        sx = na(SURT)
        self.cam7 = Cam([(T['start'] - .5, *fo(na((-19, 64.6)), 2.0)), (T['smoke'], *fo(sx, 3.2)), (T['within'], *fo(sx, 3.4)),
                         (T['square'], *fo(sx, 3.4)), (T['unusual'], *fo(sx, 2.8))])
        for key, d_ in (('start', '#1 card; Iceland south coast'), ('fishermen', 'Fishing boat'), ('smoke', 'Smoke plume rises'),
                        ('first', 'SHIP ON FIRE? chip'), ('underwater', 'Eruption panel'), ('within', 'Cone grows'),
                        ('broke', 'Breaks the surface'), ('named', 'SURTSEY hero'), ('fire', 'Fire giant chip'),
                        ('y1967', '1963 → 1967 hero'), ('square', 'Back to map: ≈1 SQ MI'), ('unusual', 'Lab panel: bare rock'),
                        ('only', 'RESEARCHERS ONLY'), ('seeds2', 'Seeds drift in'), ('insects2', 'Insects'), ('birds', 'Birds land'),
                        ('plants', 'Plants sprout'), ('unesco', 'UNESCO chip'), ('but', 'Waves build'), ('waves', 'Coast erodes'),
                        ('half', '≈HALF GONE hero'), ('disappearing', 'Island fades')):
            b(T[key], d_, 'pop' if key not in ('underwater', 'square', 'unusual') else 'whoosh')
        # part 8: wrap ------------------------------------------------------------------------------
        T = self.p8 = dict(start=P[7], river=k(8, 'river'), fortress=k(8, 'fortress'), town=k(8, 'town'),
                           hijacker=k(8, 'hijacker'), waterfall=k(8, 'waterfall'), island=k(8, 'island'), every=k(8, 'Every'),
                           tell=k(8, 'tell'), city=k(8, 'city'), next_=k(8, 'next'))
        for key, d_ in (('start', 'Six-tile recap grid'), ('river', 'Tile 1 lights'), ('fortress', 'Tile 2'), ('town', 'Tile 3'),
                        ('hijacker', 'Tile 4'), ('waterfall', 'Tile 5'), ('island', 'Tile 6'), ('tell', 'Comment prompt card')):
            b(T[key], d_, 'pop')

    # ------------------------------------------------------------------ frame
    def draw(self, cv, t):
        p = self.part_at(t)
        getattr(self, f'draw{p}')(cv, t)
        self.fade(cv, t)

    # ---- part 1: cold open
    def draw1(self, cv, t):
        T = self.p1
        cuts = [('na', DS, 2.6, 0, 'DENMARK STRAIT', 'A WATERFALL NOBODY HAS SEEN'),
                ('ne', CENT, 3.2, T['town'] - .15, 'CENTRALIA, PA', 'BURNING SINCE 1962'),
                ('pnw', (-122.45, 46.5), 2.2, T['man'] - .15, 'PORTLAND → SEATTLE', '$200,000 · NEVER FOUND')]
        if t < T['these'] - .2:
            sc, p, z, a0, name, sub = [c for c in cuts if t >= c[3]][-1]
            q = self.g(sc, *p)
            dz = 1 + .06 * (t - a0)
            st = (q[0], q[1] + 10, z * dz)
            cv.alpha_composite(render_map(self.maps[sc], st).convert('RGBA'))
            cv.alpha_composite(vignette())
            x, y = Cam.S(st, *q)
            pin(cv, x, y, t, a0, None, LIME, 16)
            chip(cv, name, 960, 820, t, a0 + .1, None, size=46, accent=LIME, sub=sub)
            if sc == 'pnw':
                a_, b_ = Cam.S(st, *self.g('pnw', *PDX)), Cam.S(st, *self.g('pnw', *SEA_))
                route(cv, [a_, b_], e_out((t - a0) / 1.2), WHITE, 6, head=True, dashed=True, dash=(16, 10))
            if sc == 'ne':
                ga = .5 + .3 * math.sin(t * 6)
                vec(cv, (x - 120, y - 120, x + 120, y + 120),
                    lambda d, P, s: d.ellipse((*P(x - 70, y - 50), *P(x + 70, y + 50)), fill=col(FIRE, .35 * ga)), 1.0, base=FIRE)
            return
        # six pins grid teaser
        cv.alpha_composite(Image.new('RGBA', (W, H), col(INK)))
        self.grid(cv, t, T['these'] - .2, [T['these'] + i * .18 for i in range(6)], hi=None)
        hero(cv, '6 PLACES', 960, 470, t, T['real'], T['last'] - .1, 140, LIME)
        hero(cv, '1963', 960, 470, t, T['y1963'] - .2, None, 160, ORANGE)
        label(cv, 'SOUND MADE UP · ALL REAL', 960, 580, t, T['real'] + .3, T['last'] - .1, 34, WHITE)

    def grid(self, cv, t, a0, pops, hi=None, lit=None):
        tiles = [('ne', (-73.95, 42.0), 1.0, 'HUDSON RIVER'), ('fl', FJ, 1.4, 'FORT JEFFERSON'), ('ne', CENT, 1.4, 'CENTRALIA'),
                 ('pnw', JUMP, 1.4, 'D.B. COOPER'), ('na', DS, 1.4, 'DENMARK STRAIT'), ('na', SURT, 1.4, 'SURTSEY')]
        tw, th, gx, gy = 520, 300, 60, 70
        x0 = (W - 3 * tw - 2 * gx) / 2; y0 = 110
        for i, (sc, p, z, name) in enumerate(tiles):
            a = pops[i]
            al = vis(t, a, None, .35)
            if al <= 0:
                continue
            q = self.g(sc, *p)
            box = (q[0] - tw / 2 / z, q[1] - th / 2 / z, q[0] + tw / 2 / z, q[1] + th / 2 / z)
            im = self.maps[sc].resize((tw, th), Image.BICUBIC, box=box).convert('RGBA')
            on = lit is None or (lit[i] is not None and t >= lit[i])
            if not on:
                im = ImageEnhance.Brightness(im.convert('RGB')).enhance(.45).convert('RGBA')
            x, y = x0 + (i % 3) * (tw + gx), y0 + (i // 3) * (th + gy)
            sc_ = .9 + .1 * e_back((t - a) / .4)
            fr = Image.new('RGBA', (tw + 8, th + 8), col(LIME if (lit is not None and on) else WHITE, .95))
            fr.alpha_composite(im, (4, 4))
            ImageDraw.Draw(fr).ellipse((tw / 2 - 8, th / 2 - 8, tw / 2 + 16, th / 2 + 16), fill=col(LIME), outline=col(WHITE), width=3)
            place(cv, fr, x + tw / 2, y + th / 2, sc_, al)
            place(cv, label_img(f'{6 - i}  {name}', 30, WHITE if on else (170, 175, 175)), x + tw / 2, y + th + 26, 1.0, al)

    # ---- part 2: Hudson
    def draw2(self, cv, t):
        T = self.p2
        st = self.map_view(cv, 'ne', self.cam2, t)
        cv.alpha_composite(vignette())
        S = lambda p: self.S(st, 'ne', p)
        riv = [S(p) for p in HUDSON]
        ti = 8                                           # Troy index
        pr = e_io((t - T['begins']) / (T['york'] + .4 - T['begins']))
        route(cv, riv, pr, BLUE, 7, head=pr < 1, head_size=18)
        est = vis(t, T['except_'], None, .6)
        if est > 0:
            route(cv, riv[ti:], e_out((t - T['except_']) / 1.0), TEAL, 11, head=False, alpha=est)
        # tide arrows (north) after the diagram
        ta = vis(t, T['hundred'] - .2, T['dry'] + .5, .4, .4)
        if ta > 0:
            ph = (t * .5) % 1
            for f in (.2, .45, .7):
                q = point_at(riv[ti:], 1 - (f + ph * .25) % 1)[0]
                vec(cv, (q[0] - 30, q[1] - 30, q[0] + 30, q[1] + 30),
                    lambda d, P, s, q=q: _head(d, P, s, (q[0], q[1] - 6), -math.pi / 2, 20, col(TIDE := (90, 190, 255))), ta)
        sa = vis(t, T['dry'] - .1, T['people'] + 1, .4, .5)
        if sa > 0:
            pe = e_io((t - T['dry']) / 3.0)
            ny, nw = S(NYC), S(NEWB)
            seg = [S(p) for p in HUDSON[12:]][::-1]
            route(cv, seg, pe, ORANGE, 14, head=True, alpha=sa, head_size=22)
            label(cv, 'SALT FRONT', nw[0] + 40, nw[1], t, T['dry'] + 1.0, T['people'] + 1, 30, ORANGE, anchor='l', rise=6)
        # pins + labels
        src, ny, tr = S(HUDSON[0]), S(NYC), S(TROY)
        pin(cv, *src, t, T['begins'] - .1, T['map_'], WHITE, 12, rings=False)
        label(cv, 'ADIRONDACKS', src[0] + 30, src[1], t, T['begins'], T['map_'], 30, WHITE, anchor='l', rise=6)
        pin(cv, *ny, t, T['york'], None, LIME, 14)
        label(cv, 'NEW YORK CITY', ny[0] + 30, ny[1] + 4, t, T['york'] + .1, None, 30, WHITE, anchor='l', rise=6)
        al_ = S(ALB)
        label(cv, 'ALBANY', al_[0] - 26, al_[1] + 10, t, T['albany'], None, 28, WHITE, anchor='r', rise=6)
        pin(cv, *tr, t, T['troy'] - .1, None, YEL, 12)
        label(cv, 'FEDERAL DAM · TROY', tr[0] + 28, tr[1] - 16, t, T['troy'], None, 28, YEL, anchor='l', rise=6)
        ra = vis(t, T['hundred'], T['dry'] + .3, .3, .4)
        if ra > 0:
            route(cv, [(ny[0] - 90, ny[1]), (tr[0] - 90, tr[1])], e_out((t - T['hundred']) / .8), YEL, 5, head=True, alpha=ra, head_size=16)
            route(cv, [(tr[0] - 90, tr[1]), (ny[0] - 90, ny[1])], e_out((t - T['hundred']) / .8), YEL, 5, head=True, alpha=ra, head_size=16)
            label(cv, '≈150 MI OF TIDE', ny[0] - 110, (ny[1] + tr[1]) / 2, t, T['hundred'] + .3, T['dry'] + .3, 32, YEL, anchor='r', rise=0)
        # diagram: tide reversal
        def fn(d, P, s):
            ph = math.sin((t - T['twice']) * 1.2)
            lvl = 520 - 50 * ph
            d.polygon([P(PX0, 560), P(1100, 560), P(1500, 540), P(PX1, 540), P(PX1, PY1), P(PX0, PY1)], fill=(70, 60, 50, 255))
            d.rectangle((*P(PX0, lvl), *P(PX1, 640)), fill=(40, 110, 190, 255))
            d.rectangle((*P(1300, lvl), *P(PX1, 640)), fill=(30, 90, 170, 255))
            d.line([P(PX0, lvl), P(PX1, lvl)], fill=(170, 215, 255, 255), width=int(4 * s))
            d.polygon([P(PX0, 640), P(PX1, 640), P(PX1, PY1), P(PX0, PY1)], fill=(70, 60, 50, 255))
            dirn = 1 if ph < 0 else -1      # +1 = flows south (to sea, right)
            if t < T['north']:
                dirn = 1
            for i in range(5):
                x = 300 + i * 260 + ((t * 80 * dirn) % 260)
                x = PX0 + 60 + (x - PX0 - 60) % (PX1 - PX0 - 160)
                ang = 0 if dirn > 0 else math.pi
                d.line([P(x - 40 * dirn, 590), P(x + 30 * dirn, 590)], fill=(230, 245, 255, 255), width=int(6 * s))
                _head(d, P, s, (x + 30 * dirn, 590), ang, 18, (230, 245, 255, 255))
        u = self.panel(cv, t, T['twice'] - .25, T['hundred'] - .4, fn, 'LOWER HUDSON · A TIDAL ESTUARY')
        if u > .95:
            label(cv, 'NEW YORK HARBOR · OCEAN →', 1720, 470, t, T['twice'], T['hundred'] - .4, 30, WHITE, anchor='r', rise=0)
            label(cv, '← UPRIVER (NORTH)', 220, 470, t, T['twice'], T['hundred'] - .4, 30, WHITE, anchor='l', rise=0)
            label(cv, 'EBB TIDE: FLOWS TO THE SEA', 960, 760, t, T['twice'] + .3, T['north'] - .1, 34, (170, 215, 255), rise=6)
            label(cv, 'FLOOD TIDE: THE CURRENT TURNS NORTH', 960, 760, t, T['north'], T['hundred'] - .4, 34, LIME, rise=6)
        # chips / heroes
        self.section_card(cv, t, 2, 6, 'THE HUDSON RIVER')
        chip(cv, 'WATER RUNS DOWNHILL, TO THE SEA', *CHIP_XY, t, T['map_'], T['simple'] + .8, size=34, accent=WHITE, anchor='l')
        stamp(cv, 'SIMPLE?', 1500, 260, t, T['simple'], T['estuary'], 70, ORANGE)
        chip(cv, 'ESTUARY', *CHIP_XY, t, T['estuary'], T['twice'] - .3, size=44, accent=TEAL, sub='AN ARM OF THE OCEAN', anchor='l')
        chip(cv, 'TIDES REACH THE FEDERAL DAM', *CHIP_XY, t, T['troy'], T['dry'] - .1, size=34, accent=YEL, sub='TROY, NEAR ALBANY', anchor='l')
        hero(cv, '≈60 MI', *HERO_XY, t, T['sixty'], T['people'], 120, ORANGE)
        label(cv, 'SALT WATER CREEPS UPRIVER', HERO_XY[0], HERO_XY[1] + 90, t, T['sixty'] + .2, T['people'], 26, WHITE)
        chip(cv, '"THE RIVER THAT FLOWS BOTH WAYS"', *CHIP_XY, t, T['both'] - .3, T['next_'], size=36, accent=LIME,
             sub='A NATIVE NAME, OFTEN TRANSLATED', anchor='l')
        self.next_chip(cv, t, 2, 'Next', 'A FORTRESS IN THE MIDDLE OF NOWHERE')
        label(cv, 'SOURCES: NOAA · USGS · NYS DEC', 1880, 1060, t, T['start'], None, 18, (200, 210, 215), rise=0, anchor='r')

    # ---- part 3: Fort Jefferson
    def fort_pts(self, cx, cy, r):
        return [(cx + r * math.cos(math.radians(90 + 60 * i)), cy - r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]

    def draw3(self, cv, t):
        T = self.p3
        st = self.map_view(cv, 'fl', self.cam3, t)
        self.regions['fl'].draw(cv, st, t, T['start'] + .2, T['past'], fill_a=.18, alpha=.8)
        cv.alpha_composite(vignette())
        S = lambda p: self.S(st, 'fl', p)
        kw, fj = S(KW), S(FJ)
        pin(cv, *kw, t, T['key'] - .1, None, WHITE, 12, rings=False)
        label(cv, 'KEY WEST', kw[0] + 24, kw[1] + 4, t, T['key'], None, 30, WHITE, anchor='l', rise=6)
        la = vis(t, T['past'], T['shipping'], .3, .4)
        route(cv, [kw, fj], e_out((t - T['past']) / 1.0), WHITE, 5, head=True, alpha=la, dashed=True, dash=(14, 9), head_size=18)
        label(cv, '≈70 MI', (kw[0] + fj[0]) / 2, (kw[1] + fj[1]) / 2 - 36, t, T['past'] + .4, T['shipping'], 34, WHITE, rise=0)
        fa = vis(t, T['massive'] - .1, None, .3)
        if fa > 0:
            r = 14 + 6 * vis(t, T['massive'], T['fort2'] + 1, .2, .5) * (.6 + .4 * math.sin(t * 7) ** 2)
            pts = self.fort_pts(*fj, r)
            vec(cv, (fj[0] - 40, fj[1] - 40, fj[0] + 40, fj[1] + 40),
                lambda d, P, s: d.polygon([P(*q) for q in pts], fill=col((190, 110, 80)), outline=col(WHITE), width=int(3 * s)), fa)
        label(cv, 'DRY TORTUGAS', fj[0] - 30, fj[1] - 40, t, T['tortugas'], T['bricks'], 30, YEL, anchor='r', rise=6)
        sa = vis(t, T['shipping'], T['bricks'] - .3, .4, .3)
        if sa > 0:
            for lane in ([(-87, 25.8), (-84.5, 24.9), (-82.9, 24.3), (-80.4, 24.1), (-78.5, 25.3)],
                         [(-86.5, 24.6), (-83.6, 24.1), (-81.5, 23.95), (-79.6, 24.5)]):
                route(cv, [S(p) for p in lane], e_io((t - T['shipping']) / 1.6), LIME, 6, head=True, alpha=sa, dashed=True,
                      dash=(20, 12), phase=-t * 40, head_size=18)
            gm, at = S((-86.0, 26.2)), S((-79.3, 25.8))
            label(cv, 'GULF OF MEXICO', *gm, t, T['gulf'], T['bricks'] - .3, 30, WHITE, rise=6)
            label(cv, 'ATLANTIC', *at, t, T['gulf'] + .3, T['bricks'] - .3, 30, WHITE, rise=6)
        # prison/park overlays on map
        ba = vis(t, T['boat'] - .2, T['now'], .3, .4)
        if ba > 0:
            route(cv, [kw, ((kw[0] + fj[0]) / 2, kw[1] + 40), fj], e_out((t - T['boat'] + .2) / 1.2), TEAL, 5, head=True, alpha=ba, head_size=16)
            route(cv, [kw, ((kw[0] + fj[0]) / 2, kw[1] - 70), fj], e_out((t - T['boat']) / 1.0), WHITE, 4, head=True, alpha=ba,
                  dashed=True, dash=(10, 8), head_size=16)
            label(cv, 'BOAT', (kw[0] + fj[0]) / 2, kw[1] + 70, t, T['boat'], T['now'], 26, TEAL, rise=4)
            label(cv, 'SEAPLANE', (kw[0] + fj[0]) / 2, kw[1] - 100, t, T['boat'] + .3, T['now'], 26, WHITE, rise=4)

        # diagram: fort plan
        def fn(d, P, s):
            cx, cy, r = 960, 500, 300
            d.ellipse((*P(cx - r - 70, cy - r - 70), *P(cx + r + 70, cy + r + 70)), fill=(40, 110, 170, 255))
            d.ellipse((*P(cx - r - 40, cy - r - 40), *P(cx + r + 40, cy + r + 40)), fill=(210, 200, 160, 255))
            pts = self.fort_pts(cx, cy, r)
            sink = 26 * e_io((t - T['settling']) / 1.5)
            pts = [(x, y + sink) for x, y in pts]
            d.polygon([P(*q) for q in pts], fill=(170, 95, 70, 255), outline=(250, 235, 220, 255))
            inner = self.fort_pts(cx, cy + sink, r - 70)
            d.polygon([P(*q) for q in inner], fill=(120, 150, 90, 255))
            fill = clamp((t - T['bricks']) / (T['never'] - T['bricks']))
            n = int(260 * fill)
            for i in range(n):
                a = i / 260 * 2 * math.pi
                rr = r - 35
                x, y = cx + rr * math.cos(a), cy + sink + rr * math.sin(a) * .97
                d.rectangle((*P(x - 9, y - 5), *P(x + 9, y + 5)), fill=(200, 110, 80, 255), outline=(120, 60, 40, 255))
            if t > T['rifled']:
                pc = e_out((t - T['rifled']) / .8)
                bx = lerp(PX0 + 40, pts[1][0] - 10, pc)
                by = lerp(240, pts[1][1] + 30, pc)
                d.ellipse((*P(bx - 12, by - 12), *P(bx + 12, by + 12)), fill=(30, 30, 30, 255))
                if pc >= 1:
                    q = pts[1]
                    for dx, dy in ((20, 30), (35, -10), (5, 55)):
                        d.line([P(q[0] + 10, q[1] + 30), P(q[0] + 10 + dx, q[1] + 30 + dy)], fill=(20, 20, 20, 255), width=int(4 * s))
            if t > T['settling']:
                for x in (cx - 200, cx, cx + 200):
                    _head(d, P, s, (x, cy + r + 20 + sink), math.pi / 2, 18, (255, 200, 90, 255))
        u = self.panel(cv, t, T['bricks'] - .3, T['civil'] - .2, fn, 'FORT JEFFERSON · PLAN VIEW')
        if u > .95:
            yrs = int(lerp(1846, 1875, clamp((t - T['decades']) / 2.5)))
            hero(cv, str(yrs), 1560, 300, t, T['decades'], T['never'] - .1, 90, LIME, pop=False)
            stamp(cv, 'NEVER FINISHED', 960, 300, t, T['never'], T['civil'] - .2, 64, RED)
            label(cv, 'RIFLED CANNON', 360, 230, t, T['rifled'], T['civil'] - .2, 30, ORANGE, rise=6)
            label(cv, 'THE FORT IS SETTLING', 960, 850, t, T['settling'], T['civil'] - .2, 30, YEL, rise=6)
            label(cv, 'MILLIONS OF BRICKS', 360, 760, t, T['bricks'] + .3, T['civil'] - .2, 30, (230, 150, 120), rise=6)
        self.section_card(cv, t, 3, 5, 'FORT JEFFERSON')
        chip(cv, 'FORT JEFFERSON', *CHIP_XY, t, T['fort2'], T['shipping'] - .1, size=44, accent=ORANGE, sub='DRY TORTUGAS, FLORIDA', anchor='l')
        hero(cv, '1846', *HERO_XY, t, T['y1846'], T['bricks'] - .3, 130, LIME)
        chip(cv, 'CONTROL THE SHIPPING LANES', *CHIP_XY, t, T['shipping'], T['bricks'] - .3, size=34, accent=LIME, anchor='l')
        chip(cv, 'BECAME A PRISON', *CHIP_XY, t, T['civil'] + .2, T['today'] - .1, size=42, accent=RED, sub='DURING + AFTER THE CIVIL WAR', anchor='l')
        chip(cv, 'DR. SAMUEL MUDD', 1700, 230, t, T['mudd'], T['today'] - .1, size=38, accent=WHITE,
             sub="SET THE BROKEN LEG OF LINCOLN'S ASSASSIN", anchor='r')
        chip(cv, 'DRY TORTUGAS NATIONAL PARK', *CHIP_XY, t, T['today'], T['now'], size=36, accent=TEAL, sub='BOAT OR SEAPLANE ONLY', anchor='l')
        self.next_chip(cv, t, 3, 'Now', 'UNDERGROUND')
        label(cv, 'SOURCES: NATIONAL PARK SERVICE', 1880, 1060, t, T['start'], None, 18, (200, 210, 215), rise=0, anchor='r')

    # ---- part 4: Centralia
    def draw4(self, cv, t):
        T = self.p4
        st = self.map_view(cv, 'ne', self.cam4, t)
        self.regions['ne'].draw(cv, st, t, T['start'] + .2, T['coal'], fill_a=.2, alpha=.85)
        cv.alpha_composite(vignette())
        c = self.S(st, 'ne', CENT)
        ga = max(vis(t, T['y1980s'], None, .6) * (.6 + .4 * math.sin(t * 3) ** 2), 0)
        if ga > 0:
            vec(cv, (c[0] - 220, c[1] - 160, c[0] + 220, c[1] + 160),
                lambda d, P, s: [d.ellipse((*P(c[0] - 180 * k_, c[1] - 120 * k_), *P(c[0] + 180 * k_, c[1] + 120 * k_)),
                                           fill=col(FIRE, a_)) for k_, a_ in ((1, .14), (.6, .22), (.3, .35))], ga, base=FIRE)
        # town grid: houses fade with buyout
        ha = vis(t, T['y1980s'] - .2, None, .4)
        if ha > 0:
            gone = clamp((t - T['buyout']) / (T['today'] - T['buyout']))
            for i in range(30):
                gx, gy = (i % 6) - 2.5, (i // 6) - 2
                x, y = c[0] + gx * 34, c[1] + gy * 30
                keep = ((i * 37) % 30) / 30 > gone or i in (7, 22)
                vec(cv, (x - 14, y - 14, x + 14, y + 14),
                    lambda d, P, s, x=x, y=y, keep=keep: d.rectangle((*P(x - 10, y - 9), *P(x + 10, y + 9)),
                        fill=col(WHITE if keep else (90, 90, 90), .95 if keep else .35), outline=col(OUTLINE), width=int(2 * s)),
                    ha)
        pin(cv, *c, t, T['centralia'] - .1, T['y1980s'], ORANGE, 14)
        label(cv, 'CENTRALIA', c[0] + 30, c[1] - 30, t, T['centralia'], None, 34, WHITE, anchor='l', rise=6)
        pa = self.S(st, 'ne', (-77.8, 40.9))
        label(cv, 'PENNSYLVANIA', *pa, t, T['start'] + .5, T['coal'], 34, ORANGE, rise=6)

        def fn(d, P, s):
            gy = 360
            d.rectangle((*P(PX0, 150), *P(PX1, gy)), fill=(60, 80, 100, 255))
            d.rectangle((*P(PX0, gy), *P(PX1, PY1)), fill=(96, 82, 66, 255))
            d.rectangle((*P(PX0, 560), *P(PX1, 640)), fill=(28, 26, 26, 255))
            for i in range(9):
                x = 300 + i * 150
                d.rectangle((*P(x, gy - 46), *P(x + 70, gy)), fill=(230, 226, 214, 255), outline=(30, 30, 30, 255))
                d.polygon([P(x - 8, gy - 46), P(x + 35, gy - 76), P(x + 78, gy - 46)], fill=(150, 70, 60, 255))
            fp = clamp((t - T['y1962']) / (T['smoke'] - T['y1962'] + 2))
            if t > T['y1962']:
                x0 = 250; x1 = lerp(x0, PX1 - 20, fp)
                flick = .75 + .25 * math.sin(t * 9)
                d.rectangle((*P(x0, 566), *P(x1, 634)), fill=(255, 110, 40, int(220 * flick)))
                d.rectangle((*P(x0, 580), *P(x1, 620)), fill=(255, 200, 90, int(200 * flick)))
            if t > T['smoke']:
                for i, x in enumerate((420, 700, 980, 1260, 1540)):
                    if x > lerp(250, PX1, fp):
                        continue
                    d.line([P(x, 560), P(x - 10, gy)], fill=(20, 20, 20, 255), width=int(3 * s))
                    for j in range(6):
                        ph = ((t * .5 + j / 6 + i * .13) % 1)
                        yy = lerp(gy, 170, ph); rr = 10 + 26 * ph
                        d.ellipse((*P(x - rr, yy - rr), *P(x + rr, yy + rr)), fill=(170, 170, 170, int(150 * (1 - ph))))
            if t > T['y1981']:
                hp = e_out((t - T['y1981']) / .8)
                d.ellipse((*P(1100 - 50 * hp, gy - 8), *P(1100 + 50 * hp, gy + 30 * hp)), fill=(15, 12, 10, 255))
                d.polygon([P(1060, gy + 10), P(1140, gy + 10), P(1120, gy + 150 * hp), P(1080, gy + 150 * hp)], fill=(15, 12, 10, 255))
        u = self.panel(cv, t, T['coal'] - .2, T['y1980s'] - .3, fn, 'UNDER CENTRALIA · CROSS-SECTION')
        if u > .95:
            label(cv, 'TOWN', 210, 330, t, T['coal'], T['y1980s'] - .3, 28, WHITE, anchor='l', rise=0)
            label(cv, 'COAL SEAM + OLD MINES', 210, 530, t, T['coal'] + .2, T['y1980s'] - .3, 30, (220, 220, 220), anchor='l', rise=0)
            label(cv, 'FIRE', 300, 680, t, T['y1962'] + .3, T['y1980s'] - .3, 34, FIRE, anchor='l', rise=6)
            label(cv, 'SMOKE + GASES', 1500, 230, t, T['smoke'] + .3, T['y1980s'] - .3, 30, (220, 220, 220), rise=6)
            label(cv, 'SINKHOLE · 1981', 1100, 540 - 40, t, T['y1981'] + .3, T['y1980s'] - .3, 30, RED, rise=6)
        self.section_card(cv, t, 4, 4, 'CENTRALIA')
        hero(cv, '1962', *HERO_XY, t, T['y1962'], T['y1981'] - .1, 130, FIRE)
        label(cv, 'THE FIRE STARTS', HERO_XY[0], HERO_XY[1] + 90, t, T['y1962'] + .2, T['y1981'] - .1, 26, WHITE)
        chip(cv, 'A BOY FELL IN · HE SURVIVED', *CHIP_XY, t, T['survived'], T['y1980s'] - .3, size=34, accent=RED, anchor='l')
        chip(cv, 'FEDERAL BUYOUT', *CHIP_XY, t, T['buyout'], T['zip_'] - .1, size=44, accent=ORANGE, sub='1980s · RESIDENTS MOVE AWAY', anchor='l')
        chip(cv, 'ZIP CODE 17927', *CHIP_XY, t, T['zip_'], T['today'], size=44, accent=RED, sub='DISCONTINUED (2002)', anchor='l')
        stamp(cv, 'GONE', 520, 150, t, T['zip_'] + .5, T['today'], 54, RED)
        chip(cv, 'STILL BURNING', *CHIP_XY, t, T['still'], None, size=44, accent=FIRE, sub='COULD BURN FOR CENTURIES', anchor='l')
        self.next_chip(cv, t, 4, 'From', 'A MAN WHO FELL OUT OF THE SKY')
        label(cv, 'SOURCES: PA DEP · U.S. CENSUS · USPS', 1880, 1060, t, T['start'], None, 18, (200, 210, 215), rise=0, anchor='r')

    # ---- part 5: D.B. Cooper
    def draw5(self, cv, t):
        T = self.p5
        st = self.map_view(cv, 'pnw', self.cam5, t)
        self.regions['pnw'].draw(cv, st, t, T['start'] + .2, T['south'], fill_a=.14, alpha=.7)
        cv.alpha_composite(vignette())
        S = lambda p: self.S(st, 'pnw', p)
        pd, se, rn, tb, jp = S(PDX), S(SEA_), S(RENO), S(TENA), S(JUMP)
        pin(cv, *pd, t, T['portland'] - .1, None, WHITE, 12, rings=False)
        label(cv, 'PORTLAND', pd[0] - 24, pd[1] + 6, t, T['portland'], T['never'], 30, WHITE, anchor='r', rise=6)
        pin(cv, *se, t, T['seattle'] - .1, None, WHITE, 12, rings=False)
        label(cv, 'SEATTLE', se[0] + 24, se[1], t, T['seattle'], None, 30, WHITE, anchor='l', rise=6)
        route(cv, [pd, ((pd[0] + se[0]) / 2 + 40, (pd[1] + se[1]) / 2), se], e_io((t - T['seattle'] + .3) / 1.4), WHITE, 5,
              head=True, alpha=vis(t, T['seattle'] - .3, T['south'] + 1, .3, .6), head_size=18)
        sa = vis(t, T['south'] - .1, T['never'] + 1.5, .3, .6)
        if sa > 0:
            route(cv, [se, jp, ((jp[0] + rn[0]) / 2, (jp[1] + rn[1]) / 2), rn], e_io((t - T['south']) / 2.4), ORANGE, 6, head=True,
                  alpha=sa, dashed=True, dash=(16, 10), head_size=20)
            label(cv, '→ TOWARD MEXICO', rn[0] + 30, rn[1] - 10, t, T['low'], T['never'] + 1.5, 28, ORANGE, anchor='l', rise=6)
        ua = vis(t, T['never'], None, .6)
        if ua > 0:
            vec(cv, (jp[0] - 160, jp[1] - 160, jp[0] + 160, jp[1] + 160),
                lambda d, P, s: [d.ellipse((*P(jp[0] - r_, jp[1] - r_ * .8), *P(jp[0] + r_, jp[1] + r_ * .8)), fill=col(RED, a_))
                                 for r_, a_ in ((120, .12), (80, .16), (45, .2))], ua, base=RED)
            label(cv, 'JUMP AREA (UNCERTAIN)', jp[0] + 130, jp[1] - 40, t, T['never'] + .2, T['y1980'], 28, RED, anchor='l', rise=6)
            label(cv, '?', jp[0], jp[1] + 12, t, T['never'] + .2, None, 60, WHITE, rise=8)
        pin(cv, *tb, t, T['y1980'], None, LIME, 13)
        label(cv, '$5,800 FOUND · 1980', tb[0] - 26, tb[1] - 34, t, T['y1980'] + .2, None, 30, LIME, anchor='r', rise=6)
        co = S((-123.3, 46.18))
        label(cv, 'COLUMBIA RIVER', *co, t, T['columbia'], T['but'] + 1, 28, (170, 215, 255), rise=6)

        def fn(d, P, s):
            y0 = 420
            sky = vis(t, T['somewhere'], None, .5)
            for i in range(40):
                x = (i * 197 + t * 300) % (PX1 - PX0) + PX0
                y = 160 + (i * 89) % 600
                d.line([P(x, y), P(x - 12, y + 30)], fill=(150, 180, 210, int(120 * sky)), width=int(2 * s))
            body = [(420, y0 - 40), (1350, y0 - 50), (1480, y0 - 30), (1500, y0), (1470, y0 + 30), (420, y0 + 40), (360, y0)]
            d.polygon([P(*q) for q in body], fill=(225, 228, 232, 255), outline=(40, 40, 40, 255))
            d.polygon([P(1300, y0 - 45), P(1430, y0 - 190), P(1490, y0 - 190), P(1440, y0 - 40)], fill=(200, 205, 210, 255))
            d.polygon([P(800, y0), P(1050, y0 + 160), P(1120, y0 + 160), P(980, y0)], fill=(190, 195, 200, 255))
            for i in range(14):
                d.ellipse((*P(500 + i * 55, y0 - 22), *P(518 + i * 55, y0 - 6)), fill=(60, 90, 130, 255))
            sp = e_io((t - T['stairs']) / 1.0) if t > T['stairs'] else 0
            ax, ay = 1460, y0 + 30
            ang = math.radians(10 + 45 * sp)
            ex, ey = ax + 230 * math.cos(ang), ay + 230 * math.sin(ang)
            d.line([P(ax, ay), P(ex, ey)], fill=(255, 200, 90, 255), width=int(12 * s))
            if t > T['jumped']:
                jp_ = e_in = clamp((t - T['jumped']) / 3.0)
                x = ex + 60 + 200 * jp_; y = ey + 30 + 300 * jp_ ** 1.6
                d.ellipse((*P(x - 10, y - 30), *P(x + 10, y - 10)), fill=(20, 20, 20, 255))
                d.line([P(x, y - 10), P(x, y + 30)], fill=(20, 20, 20, 255), width=int(6 * s))
                if jp_ > .35:
                    d.pieslice((*P(x - 70, y - 160), *P(x + 70, y - 20)), 180, 360, fill=(240, 240, 240, 255))
                    d.line([P(x - 70, y - 90), P(x, y - 10)], fill=(200, 200, 200, 255), width=int(2 * s))
                    d.line([P(x + 70, y - 90), P(x, y - 10)], fill=(200, 200, 200, 255), width=int(2 * s))
        u = self.panel(cv, t, T['somewhere'] - .2, T['never'] - .3, fn, 'BOEING 727 · REAR AIRSTAIR')
        if u > .95:
            label(cv, 'REAR STAIRS', 1500, 650, t, T['stairs'] + .4, T['never'] - .3, 30, YEL, rise=6)
            label(cv, 'NIGHT · RAIN · SW WASHINGTON', 420, 200, t, T['somewhere'], T['never'] - .3, 30, WHITE, anchor='l', rise=6)
        self.section_card(cv, t, 5, 3, 'D.B. COOPER')
        hero(cv, 'NOV 24, 1971', *HERO_XY, t, T['november'], T['dan'] - .1, 90, LIME)
        chip(cv, 'TICKET: "DAN COOPER"', *CHIP_XY, t, T['dan'], T['note'] - .1, size=40, accent=WHITE, sub='NORTHWEST ORIENT · PORTLAND → SEATTLE', anchor='l')
        chip(cv, '"I HAVE A BOMB"', *CHIP_XY, t, T['note'], T['two'] - .1, size=42, accent=RED, sub='A NOTE TO A FLIGHT ATTENDANT', anchor='l')
        hero(cv, '$200,000', *HERO_XY, t, T['two'], T['south'] - .1, 110, LIME)
        label(cv, '+ 4 PARACHUTES', HERO_XY[0], HERO_XY[1] + 85, t, T['parachutes'], T['south'] - .1, 30, WHITE)
        chip(cv, 'FLY SOUTH · LOW AND SLOW', *CHIP_XY, t, T['south'], T['somewhere'] - .3, size=38, accent=ORANGE, anchor='l')
        chip(cv, 'SERIAL NUMBERS MATCHED', *CHIP_XY, t, T['serial'], T['but'] - .1, size=38, accent=LIME, anchor='l')
        chip(cv, 'NO BODY · NO PARACHUTE', *CHIP_XY, t, T['but'], T['y2016'] - .1, size=40, accent=RED, sub='NO COOPER', anchor='l')
        hero(cv, '2016', *HERO_XY, t, T['y2016'], T['calls'] - .1, 130, WHITE)
        label(cv, 'FBI ENDS ACTIVE INVESTIGATION', HERO_XY[0], HERO_XY[1] + 90, t, T['y2016'] + .2, T['calls'] - .1, 24, WHITE)
        chip(cv, 'UNSOLVED', *CHIP_XY, t, T['calls'], T['next_'], size=52, accent=RED, sub='THE ONLY UNSOLVED AIR PIRACY IN U.S. AVIATION HISTORY (FBI)', anchor='l')
        self.next_chip(cv, t, 5, 'Next', 'THE BOTTOM OF THE SEA')
        label(cv, 'SOURCES: FBI', 1880, 1060, t, T['start'], None, 18, (200, 210, 215), rise=0, anchor='r')

    # ---- part 6: Denmark Strait
    def draw6(self, cv, t):
        T = self.p6
        st = self.map_view(cv, 'na', self.cam6, t)
        cv.alpha_composite(vignette())
        S = lambda p: self.S(st, 'na', p)
        gl, ic, ds = S((-40, 72)), S((-18.6, 64.9)), S(DS)
        label(cv, 'GREENLAND', *gl, t, T['greenland'], T['matters'], 40, WHITE, rise=8)
        label(cv, 'ICELAND', *ic, t, T['iceland'], T['matters'], 36, ORANGE, rise=8)
        if t >= T['strait'] - .1:
            pin(cv, *ds, t, T['strait'] - .1, T['matters'], TEAL, 15)
            label(cv, 'DENMARK STRAIT', ds[0] + 30, ds[1] - 30, t, T['strait'], T['matters'], 32, TEAL, anchor='l', rise=6)
        ra = vis(t, T['from_'], T['heres'], .3, .3)
        if ra > 0:
            ring(cv, *ds, 70 + 40 * ((t * .8) % 1), t, T['from_'], T['heres'], TEAL, 4, alpha=ra)
        ca = vis(t, T['matters'], None, .6)
        if ca > 0:
            cold = [S(p) for p in ((-12, 71), (-20, 69), (-25, 67.2), (-30, 64.5), (-36, 61.5), (-42, 57))]
            warm = [S(p) for p in ((-40, 52), (-30, 56), (-22, 60), (-14, 63.5), (-8, 66.5))]
            route(cv, cold, e_io((t - T['matters']) / 2.5), COLD, 10, head=True, alpha=ca, head_size=24)
            route(cv, warm, e_io((t - T['heat']) / 2.0), WARM, 10, head=True, alpha=ca, head_size=24)
            label(cv, 'COLD, DEEP', cold[3][0] - 30, cold[3][1], t, T['matters'] + 1, None, 28, BLUE, anchor='r', rise=6)
            label(cv, 'WARM, NEAR THE SURFACE', warm[2][0] + 30, warm[2][1] + 20, t, T['heat'] + .5, None, 28, WARM, anchor='l', rise=6)

        def fn(d, P, s):
            sea = 230
            d.rectangle((*P(PX0, 140), *P(PX1, sea)), fill=(70, 100, 130, 255))
            d.rectangle((*P(PX0, sea), *P(PX1, PY1)), fill=(20, 60, 110, 255))
            floor = [(PX0, 520), (700, 520), (880, 440), (960, 440), (1100, 600), (1400, 780), (PX1, 820), (PX1, PY1), (PX0, PY1)]
            cold_a = vis(t, T['nordic'], None, .6)
            if cold_a > 0:
                d.rectangle((*P(PX0, 330), *P(700, 520)), fill=(70, 140, 235, int(230 * cold_a)))
            warm_a = vis(t, T['meets'], None, .6)
            if warm_a > 0:
                d.rectangle((*P(1000, sea), *P(PX1, 560)), fill=(220, 130, 80, int(170 * warm_a)))
            if t > T['spills']:
                pc = e_io((t - T['spills']) / 3.0)
                path = [(700, 470), (900, 430), (1000, 470), (1150, 600), (1350, 730), (1600, 800)]
                seg, _ = partial(path, pc)
                if len(seg) > 1:
                    d.line([P(*q) for q in seg], fill=(90, 160, 255, 255), width=int(60 * s), joint='curve')
                ph = (t * .6) % 1
                for f in (0, .33, .66):
                    (x, y), ang = point_at(path, min(pc, (f + ph) % 1))
                    _head(d, P, s, (x, y), ang, 22, (230, 240, 255, 255))
            elif t > T['instead']:
                pc = e_io((t - T['instead']) / 1.5)
                d.line([P(700, lerp(330, 470, pc)), P(lerp(700, 880, pc), lerp(330, 450, pc))], fill=(90, 160, 255, 255), width=int(40 * s))
            d.polygon([P(*q) for q in floor], fill=(84, 72, 60, 255))
            d.line([P(PX0, sea), P(PX1, sea)], fill=(190, 225, 255, 255), width=int(3 * s))
            if t > T['roughly']:
                ra_ = e_out((t - T['roughly']) / .8)
                d.line([P(1640, 440), P(1640, lerp(440, 800, ra_))], fill=(200, 243, 75, 255), width=int(6 * s))
                for y in (440, 800):
                    d.line([P(1615, y), P(1665, y)], fill=(200, 243, 75, 255), width=int(5 * s))
        u = self.panel(cv, t, T['heres'] - .2, T['matters'] - .3, fn, 'DENMARK STRAIT · OCEAN CROSS-SECTION')
        if u > .95:
            label(cv, 'SEA SURFACE', 200, 210, t, T['heres'], T['matters'] - .3, 26, WHITE, anchor='l', rise=0)
            label(cv, 'COLD, DENSE WATER', 420, 300, t, T['nordic'] + .3, T['matters'] - .3, 30, BLUE, rise=6)
            label(cv, 'WARMER, LIGHTER WATER', 1360, 300, t, T['meets'] + .3, T['matters'] - .3, 30, WARM, rise=6)
            label(cv, 'UNDERSEA RIDGE', 920, 400, t, T['ridge'], T['matters'] - .3, 30, (230, 215, 195), rise=6)
            label(cv, '≈11,500 FT', 1620, 620, t, T['roughly'] + .3, T['matters'] - .3, 34, LIME, anchor='r', rise=6)
        self.section_card(cv, t, 6, 2, 'THE DENMARK STRAIT')
        chip(cv, "EARTH'S LARGEST WATERFALL", *CHIP_XY, t, T['largest'], T['heres'] - .2, size=40, accent=TEAL, sub='HIDDEN UNDER THE SEA', anchor='l')
        chip(cv, 'WATER FALLING THROUGH WATER', 960, 950 - 60, t, T['not_'], T['flow'] - .1, size=34, accent=BLUE)
        chip(cv, 'FLOW DWARFS ANY WATERFALL ON LAND', 960, 950 - 60, t, T['flow'], T['matters'] - .3, size=32, accent=LIME)
        chip(cv, 'HELPS MOVE HEAT AROUND THE PLANET', *CHIP_XY, t, T['heat'], T['now'], size=34, accent=WARM, anchor='l')
        self.next_chip(cv, t, 6, 'now', 'A PLACE BORN IN 1963')
        label(cv, 'SOURCES: NOAA', 1880, 1060, t, T['start'], None, 18, (200, 210, 215), rise=0, anchor='r')

    # ---- part 7: Surtsey
    def draw7(self, cv, t):
        T = self.p7
        st = self.map_view(cv, 'na', self.cam7, t)
        cv.alpha_composite(vignette())
        S = lambda p: self.S(st, 'na', p)
        su, he = S(SURT), S(HEIM)
        label(cv, 'ICELAND', *S((-18.6, 64.9)), t, T['start'] + .3, None, 36, ORANGE, rise=8)
        pin(cv, *su, t, T['start'] + .3, None, LIME, 14)
        label(cv, 'WESTMAN ISLANDS', he[0] + 26, he[1] - 10, t, T['fishermen'], None, 26, WHITE, anchor='l', rise=6)
        ba = vis(t, T['fishermen'] - .1, T['underwater'], .3, .3)
        if ba > 0:
            bx = su[0] - 160 + 50 * clamp((t - T['fishermen']) / 3)
            vec(cv, (bx - 40, su[1] - 40, bx + 40, su[1] + 30),
                lambda d, P, s: (d.polygon([P(bx - 26, su[1] - 4), P(bx + 26, su[1] - 4), P(bx + 16, su[1] + 10), P(bx - 16, su[1] + 10)],
                                           fill=col(RED), outline=col(OUTLINE), width=int(2 * s)),
                                 d.rectangle((*P(bx - 4, su[1] - 30), *P(bx + 2, su[1] - 4)), fill=col(WHITE))), ba)
        sm = vis(t, T['smoke'] - .1, T['underwater'] + .2, .4, .3)
        if sm > 0:
            hgt = 40 + 160 * clamp((t - T['smoke']) / 2.5)

            def fn_s(d, P, s):
                for i in range(14):
                    q = i / 13; r = 10 + 30 * q
                    x = su[0] + 10 * math.sin(t * 2 + i); y = su[1] - q * hgt
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=col((70, 70, 72), .8 * (1 - q * .5)))
            vec(cv, (su[0] - 80, su[1] - hgt - 50, su[0] + 80, su[1] + 20), fn_s, sm, base=(70, 70, 72))
        hero(cv, '≈1 SQ MI', *HERO_XY, t, T['square'], T['unusual'] - .2, 110, LIME)
        label(cv, 'NEW LAND BY 1967', HERO_XY[0], HERO_XY[1] + 85, t, T['square'] + .2, T['unusual'] - .2, 26, WHITE)

        def fn1(d, P, s):          # eruption builds the island
            sea = 430
            d.rectangle((*P(PX0, 140), *P(PX1, sea)), fill=(110, 150, 185, 255))
            d.rectangle((*P(PX0, sea), *P(PX1, PY1)), fill=(25, 80, 140, 255))
            g = clamp((t - T['underwater']) / (T['broke'] + 1 - T['underwater']))
            top = lerp(760, sea - 70, e_io(g))
            w2 = lerp(180, 520, e_io(g))
            d.polygon([P(960 - w2, 840), P(960 - 60, top), P(960 + 60, top), P(960 + w2, 840)], fill=(70, 66, 64, 255))
            d.rectangle((*P(PX0, 840), *P(PX1, PY1)), fill=(84, 72, 60, 255))
            d.ellipse((*P(900, 820), *P(1020, 860)), fill=(255, 110, 40, 255))
            if top < sea + 40:
                for i in range(18):
                    ph = (t * .7 + i / 18) % 1
                    x = 960 + 60 * math.sin(i * 1.7) * ph; y = lerp(top, 170, ph); r = 14 + 50 * ph
                    c = (240, 240, 240) if i % 3 else (60, 60, 62)
                    d.ellipse((*P(x - r, y - r), *P(x + r, y + r)), fill=c + (int(220 * (1 - ph)),))
            else:
                for i in range(12):
                    ph = (t * .8 + i / 12) % 1
                    x = 960 + 40 * math.sin(i * 2.3); y = lerp(top, sea, ph)
                    d.ellipse((*P(x - 6, y - 6), *P(x + 6, y + 6)), fill=(220, 235, 255, int(200 * (1 - ph))))
            d.line([P(PX0, sea), P(PX1, sea)], fill=(200, 230, 255, 255), width=int(3 * s))
        u1 = self.panel(cv, t, T['underwater'] - .2, T['square'] - .3, fn1, 'SURTSEY · NOVEMBER 1963')
        if u1 > .95:
            label(cv, 'SEA LEVEL', 200, 410, t, T['underwater'], T['square'] - .3, 26, WHITE, anchor='l', rise=0)
            label(cv, 'UNDERWATER VOLCANO', 960, 700, t, T['underwater'] + .3, T['broke'] - .2, 32, WHITE, rise=6)
            label(cv, 'NEW ISLAND', 1240, 330, t, T['broke'] + .4, T['square'] - .3, 36, LIME, rise=6)

        def fn2(d, P, s):          # natural lab + erosion
            sea = 470
            d.rectangle((*P(PX0, 140), *P(PX1, sea)), fill=(120, 160, 195, 255))
            d.rectangle((*P(PX0, sea), *P(PX1, PY1)), fill=(25, 80, 140, 255))
            er = e_io((t - T['waves']) / 4.0) if t > T['waves'] else 0
            right = lerp(1400, 1120, er)
            isl = [(520, 840), (700, sea - 10), (760, sea - 60), (lerp(1180, 1000, er), sea - 60), (right, sea - 10), (right + 100, 840)]
            d.polygon([P(*q) for q in isl], fill=(70, 66, 64, 255))
            if er > 0:
                d.line([P(lerp(1180, 1000, er), sea - 60), P(1180, sea - 60), P(1400, sea - 10)], fill=(255, 154, 75, 255), width=int(4 * s))
            d.rectangle((*P(PX0, 840), *P(PX1, PY1)), fill=(84, 72, 60, 255))
            if t > T['plants']:
                for i in range(10):
                    x = 780 + i * 34
                    if x > lerp(1180, 1000, er):
                        continue
                    h_ = 26 * e_out((t - T['plants'] - i * .06) / .5)
                    d.line([P(x, sea - 60), P(x, sea - 60 - h_)], fill=(120, 200, 90, 255), width=int(5 * s))
                    d.ellipse((*P(x - 10, sea - 66 - h_), *P(x + 10, sea - 52 - h_)), fill=(120, 200, 90, 255))
            if t > T['seeds2']:
                for i in range(8):
                    ph = clamp((t - T['seeds2']) / 2.5 - i * .05)
                    x = lerp(PX0 + 40, 800 + i * 40, ph); y = lerp(200 + i * 20, sea - 66, ph ** 2)
                    d.ellipse((*P(x - 5, y - 4), *P(x + 5, y + 4)), fill=(225, 190, 140, 255))
            if t > T['birds']:
                for i in range(3):
                    ph = clamp((t - T['birds']) / 2.2 - i * .1)
                    x = lerp(PX1 - 40, 820 + i * 80, ph); y = lerp(200, sea - 80, ph)
                    w_ = 22 * (1 - ph * .5) * (1 if int(t * 6 + i) % 2 else .4)
                    d.line([P(x - 22, y - w_), P(x, y), P(x + 22, y - w_)], fill=(250, 250, 250, 255), width=int(4 * s))
            amp = 6 + 14 * vis(t, T['but'], None, .6)
            d.line([P(x, sea + amp * math.sin(x / 40 + t * 3)) for x in range(PX0, PX1 + 1, 12)], fill=(220, 240, 255, 255), width=int(4 * s))
            if t > T['waves']:
                for i in range(3):
                    ph = (t * .7 + i / 3) % 1
                    x = lerp(PX1 - 40, right + 40, ph)
                    _head(d, P, s, (x, sea - 4), math.pi, 22, (230, 245, 255, int(255 * (1 - ph * .6))))
        u2 = self.panel(cv, t, T['unusual'] - .2, None, fn2, 'SURTSEY · A NATURAL LABORATORY')
        if u2 > .95:
            label(cv, 'BARE ROCK', 960, 360, t, T['unusual'] + .4, T['seeds2'], 32, WHITE, rise=6)
            label(cv, 'SEEDS', 300, 240, t, T['seeds2'] + .2, T['but'], 28, (225, 190, 140), rise=6)
            label(cv, 'INSECTS', 960, 300, t, T['insects2'], T['but'], 28, WHITE, rise=6)
            label(cv, 'BIRDS', 1600, 240, t, T['birds'] + .2, T['but'], 28, WHITE, rise=6)
            label(cv, 'PLANTS', 900, 330, t, T['plants'] + .3, T['but'], 28, (120, 200, 90), rise=6)
            label(cv, '1967 COASTLINE', 1300, 340, t, T['waves'] + 1, None, 28, ORANGE, rise=6)
            label(cv, 'WAVES', 1600, 400, t, T['waves'], None, 30, WHITE, rise=6)
        self.section_card(cv, t, 7, 1, 'SURTSEY')
        chip(cv, 'A SHIP ON FIRE?', *CHIP_XY, t, T['first'], T['underwater'] - .2, size=42, accent=RED, anchor='l')
        hero(cv, 'SURTSEY', *HERO_XY, t, T['named'], T['fire'] - .1, 100, LIME)
        chip(cv, 'NAMED FOR A FIRE GIANT', *CHIP_XY, t, T['fire'], T['y1967'] - .1, size=38, accent=ORANGE, sub='FROM NORSE MYTHOLOGY', anchor='l')
        hero(cv, '1963 → 1967', *HERO_XY, t, T['y1967'] - .2, T['square'] - .3, 90, LIME)
        chip(cv, 'RESEARCHERS ONLY', *CHIP_XY, t, T['only'], T['laboratory'] + .5, size=42, accent=LIME, sub='NO SEEDS OR INSECTS BROUGHT IN', anchor='l')
        chip(cv, 'UNESCO WORLD HERITAGE SITE', *CHIP_XY, t, T['unesco'] - .2, T['but'], size=36, accent=TEAL, anchor='l')
        chip(cv, 'THE SEA IS WINNING', *CHIP_XY, t, T['but'], T['half'] - .1, size=42, accent=RED, anchor='l')
        hero(cv, '≈HALF GONE', *HERO_XY, t, T['half'], None, 90, ORANGE)
        label(cv, "OF SURTSEY'S ORIGINAL AREA", HERO_XY[0], HERO_XY[1] + 80, t, T['half'] + .2, None, 24, WHITE)
        label(cv, 'SOURCES: UNESCO · SURTSEY RESEARCH SOCIETY', 1880, 1060, t, T['start'], None, 18, (200, 210, 215), rise=0, anchor='r')

    # ---- part 8: wrap
    def draw8(self, cv, t):
        T = self.p8
        cv.alpha_composite(Image.new('RGBA', (W, H), col(INK)))
        lit = [T['river'], T['fortress'], T['town'], T['hijacker'], T['waterfall'], T['island']]
        self.grid(cv, t, T['start'], [T['start'] + i * .08 for i in range(6)], lit=lit)
        ca = vis(t, T['tell'] - .2, None, .4)
        if ca > 0:
            tint(cv, OUTLINE, .55 * ca)
            chip(cv, 'WHERE SHOULD WE ZOOM IN NEXT?', 960, 440, t, T['tell'] - .2, None, size=56, accent=LIME,
                 sub='COMMENT A CITY OR COUNTRY')
            place(cv, label_img('MAP CURIOUS', 44, LIME), 960, 600, 1.0, vis(t, T['city'], None, .4))

    # ------------------------------------------------------------------ thumbnail
    def cover(self):
        cv = Image.new('RGBA', (W, H), col(INK))
        self.grid(cv, 99, 0, [0] * 6)
        tint(cv, OUTLINE, .55)
        place(cv, hero_img('6 PLACES THAT', 120, WHITE), 960, 390, 1.0, 1.0)
        place(cv, hero_img('SOUND MADE UP', 120, LIME), 960, 530, 1.0, 1.0)
        place(cv, label_img('(BUT ARE REAL)', 52, WHITE), 960, 650, 1.0, 1.0)
        place(cv, label_img('MAP CURIOUS', 36, LIME), 960, 760, 1.0, 1.0)
        return cv.convert('RGB')
