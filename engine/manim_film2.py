"""TutorDA brand film v2 — editorial direction.
Paper (#F3EEE5) and ink (#0E1525) grounds, one orange accent, Poppins (brand) + Instrument Serif italic for the
emotional words, left-aligned 96 px grid, panel wipes and type that rises in; no glows, gradients or neon.
A fixed ink footer band carries the captions. Photos are our own generated plates (assets/gen) with an editorial grade.
Render: tools/manim_build.sh engine/manim_film2.py Film2 brandt out/film2.mp4 [draft]"""
import os, sys, math
import numpy as np
from PIL import Image
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
from manim_common import *
import importlib, json
K = importlib.import_module(os.environ.get('FILM_AUDIO', 'brandt'))
import manimpango

GEN, FILM, FONTS = os.path.join(KIT, "assets", "gen"), os.path.join(KIT, "assets", "film"), os.path.join(KIT, "assets", "fonts")
for f in ("Poppins-Regular", "Poppins-SemiBold", "Poppins-ExtraBold", "InstrumentSerif-Regular", "InstrumentSerif-Italic"):
    manimpango.register_font(os.path.join(FONTS, f + ".ttf"))
INK, INK2, INK3 = "#0E1525", "#18223A", "#26314B"
PAPER, PAPER2 = "#F3EEE5", "#E9E2D6"
RULE, GREY_P, GREY_I = "#D6CEC0", "#8C8579", "#8A93A8"
OR, OR_D, BLUE, BLUE_L, WHITE_ = "#FF6B12", "#D9530A", "#2453C9", "#9DB8FF", "#FFFFFF"
config.background_color = PAPER
EXPO = rate_functions.ease_out_expo if hasattr(rate_functions, "ease_out_expo") else rate_functions.ease_out_cubic
BAND_TOP = 1590                                   # caption band (ink) from here to the bottom

def H(s, size, color=INK, weight=ULTRABOLD):
    return Text(s, font="Poppins", weight=weight, color=color, font_size=size * 0.6)
def B(s, size, color=INK, weight=MEDIUM):
    return Text(s, font="Poppins", weight=weight, color=color, font_size=size * 0.6)
def SER(s, size, color=INK, italic=True):
    return Text(s, font="Instrument Serif", slant=ITALIC if italic else NORMAL, color=color, font_size=size * 0.6)
def left(m, x=96): return m.align_to([X(x), 0, 0], LEFT)
def at(m, y, x=96): return left(m.move_to([0, Y(y), 0]), x)
_cache = {}
def photo(name, kind, wpx, hpx, fy=0.42):
    """Crop a generated plate to wpx:hpx around a vertical focus and return an ImageMobject at 1:1 pixel size."""
    key = (name, kind, wpx, hpx, fy)
    if key not in _cache:
        im = Image.open(os.path.join(GEN, f"{name}_{kind}.jpg")).convert("RGB"); W, Hh = im.size
        ar = wpx / hpx
        if W / Hh > ar: cw, ch = int(Hh * ar), Hh
        else: cw, ch = W, int(W / ar)
        x0 = (W - cw) // 2; y0 = int(min(max(fy * Hh - ch / 2, 0), Hh - ch))
        _cache[key] = np.array(im.crop((x0, y0, x0 + cw, y0 + ch)).resize((wpx, hpx), Image.LANCZOS).convert("RGBA"))
    return ImageMobject(_cache[key]).set_width(px(wpx))
def has(n): return os.path.exists(os.path.join(GEN, n + "_ed.jpg"))
def pick(*ns):
    for n in ns:
        if has(n): return n
    return ns[-1]
def wordmark(width, dark=False):
    t = Text("TutorDA", font="Poppins", weight=ULTRABOLD, font_size=120)
    t[:5].set_color(WHITE_ if dark else BLUE); t[5:].set_color(OR)
    return t.scale_to_fit_width(width)
def card(wpx, hpx, fill=WHITE_, stroke=None, r=0.22):
    return RoundedRectangle(width=px(wpx), height=px(hpx), corner_radius=r, fill_color=fill, fill_opacity=1,
                            stroke_color=stroke or fill, stroke_width=2 if stroke else 0)
def tag(s, size=30, fg=INK, bg=PAPER2, padx=0.24, pady=0.12):
    t = B(s, size, fg, SEMIBOLD)
    r = RoundedRectangle(width=t.width + 2 * padx, height=t.height + 2 * pady, corner_radius=0.12, fill_color=bg, fill_opacity=1, stroke_width=0)
    return VGroup(r, t.move_to(r))
def tick(r=0.2, c=OR):
    return VGroup(Circle(radius=r, fill_color=c, fill_opacity=1, stroke_width=0),
                  VMobject(stroke_color=WHITE_, stroke_width=7 * r / 0.2).set_points_as_corners([[-0.42 * r, 0, 0], [-0.1 * r, -0.33 * r, 0], [0.45 * r, 0.36 * r, 0]]))

class Phone(Group):
    SW, SH = 556, 1176
    def __init__(self, center, scale=1.0, screen=INK2):
        self.screen = RoundedRectangle(width=px(self.SW), height=px(self.SH), corner_radius=px(56), fill_color=screen, fill_opacity=1, stroke_width=0)
        self.frame = ImageMobject(os.path.join(FILM, "phone_frame.png")).set_height(px(1220)).set_z_index(3)
        super().__init__(self.screen, self.frame); self.scale(scale).move_to(center); self.k = scale
    def top(self): return self.screen.get_top()[1]
    def p(self, v): return px(v) * self.k

class Film2(ReelScene):
    K = K
    def ground(self, color, direction=UP, rt=0.5):
        """Panel wipe to a new ground colour (the panel slides in over everything, then becomes the background)."""
        pan = Rectangle(width=9.2, height=16.4, fill_color=color, fill_opacity=1, stroke_width=0).set_z_index(13)  # over the content, under the caption band
        pan.move_to(-direction * 16.4)
        self.ev("wipe")
        self.add(pan); self.play(pan.animate.move_to(ORIGIN), run_time=rt, rate_func=rate_functions.ease_in_out_cubic)
        for m in list(self.mobjects):                       # clear the previous scene entirely
            if m is not pan and m not in self._keep:
                for f in m.get_family(): f.clear_updaters()
                self.remove(m)
        pan.set_z_index(-20); self._ground = pan
    def ev(self, name):
        if not hasattr(self, "_events"): self._events = []
        self._events.append([name, round(self.renderer.time, 3)])
    def rise(self, *ms, rt=0.45, lag=0.08, d=0.35):
        self.play(LaggedStart(*[FadeIn(m, shift=UP * d) for m in ms], lag_ratio=lag), run_time=rt, rate_func=EXPO)
    def out(self, *ms, rt=0.28):
        self.play(*[FadeOut(m, shift=UP * 0.2) for m in ms], run_time=rt, rate_func=rate_functions.ease_in_quad)
    def gone(self, *ms):
        for m in ms:
            for s in m.get_family(): s.clear_updaters()
        self.remove(*ms)
    def kb(self, m, t0, t1, s0=1.0, s1=1.05):
        base_w, c0 = m.width, m.get_center().copy()
        def upd(mm):
            u = min(1, max(0, (self.renderer.time - t0) / (t1 - t0)))
            mm.set_width(base_w * (s0 + (s1 - s0) * u)); mm.move_to(c0)
        m.add_updater(upd); return m

    def captions(self):
        pill = getattr(self, "CAP_PILL", False)          # v2 (28 Oct): floating caption inside Instagram's safe zone, no band
        cap_y = getattr(self, "CAP_Y", BAND_TOP + 150)
        if pill:
            self._keep = []
        else:
            band = Rectangle(width=9.2, height=px(1920 - BAND_TOP), fill_color=INK, fill_opacity=1, stroke_width=0)
            band.move_to([0, Y(BAND_TOP) - band.height / 2, 0]).set_z_index(14); self.add(band); self._keep = [band]
        now = lambda: self.renderer.time; caps = []
        for i in range(len(K.CLIPS) - 1):
            cap = K.CLIPS[i][2]; lines = [l.split() for l in cap.split("|")]
            words = [w for l in lines for w in l]; line_txt = [" ".join(l) for l in lines]; spans = []
            for li, l in enumerate(lines):
                c = 0
                for w_ in l: spans.append((li, c, c + len(w_))); c += len(w_) + 1
            def make(k, lines=lines, line_txt=line_txt, spans=spans):
                rows = VGroup(*[Text(line_txt[li], font="Poppins", weight=SEMIBOLD, color="#EDEFF5", font_size=42 * 0.6,
                                     t2c=({f"[{spans[k][1]}:{spans[k][2]}]": OR} if k >= 0 and spans[k][0] == li else {}))
                                for li in range(len(lines))])
                for li, r in enumerate(rows): r.shift(UP * (-li * px(58) - baseline(r)))
                rows.move_to([getattr(self, "CAP_X", 0), Y(cap_y), 0])
                if not pill: return rows
                bg = RoundedRectangle(width=max(r.width for r in rows) + px(56), height=rows.height + px(44), corner_radius=0.16,
                                      fill_color=INK, fill_opacity=0.92, stroke_width=0).move_to(rows)
                return VGroup(bg, rows)
            variants = [make(k) for k in range(-1, len(words))]
            starts = np.array(K.WT[i]["starts"]) + K._shift(i)
            t0 = -1.0 if i == 0 else K.C[i] - 0.05
            t1 = (K.C[i + 1] - 0.03) if i + 1 < len(K.C) else K.E[i] + 0.3
            caps.append((t0, t1, starts, variants))
        live = VGroup(); live.key = None
        def show(m):
            t = now(); idx = next((j for j, c in enumerate(caps) if c[0] <= t < c[1]), None)
            k = None if idx is None else int(np.searchsorted(caps[idx][2], t, side="right")) - 1
            if (idx, k) != m.key: m.become(caps[idx][3][k + 1].copy() if idx is not None else VGroup()); m.key = (idx, k)
        live.add_updater(show); show(live); live.set_z_index(20); self.add(live); self._keep.append(live)

    def construct(self):
        C, wt = K.C, K.wt
        S = [c - 0.3 for c in C]
        T = lambda: self.renderer.time
        self._ground = Rectangle(width=9.2, height=16.4, fill_color=PAPER, fill_opacity=1, stroke_width=0).set_z_index(-20); self.add(self._ground)
        self.captions()

        # ===== 0. Most learning still teaches everyone the same way. (paper, one photo becomes nine copies) =====
        p0 = pick("class", "hook")
        ph0 = photo(p0, "edgrey", 888, 1150, 0.45).move_to([0, Y(170 + 575), 0])
        self.add(ph0)
        grid = Group(*[photo(p0, "edgrey", 280, 362, 0.45) for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=px(24)).move_to(ph0)
        self.until(wt(0, 4, 0.05))
        self.play(FadeOut(ph0, scale=0.33), LaggedStart(*[FadeIn(g, scale=1.08) for g in grid], lag_ratio=0.07), run_time=0.62, rate_func=EXPO)
        sw = SER("the same way.", 128, INK)
        band0 = Rectangle(width=9.2, height=sw.height + px(70), fill_color=PAPER, fill_opacity=1, stroke_width=0).move_to(grid)
        sw.move_to(band0)
        self.until(wt(0, 6, 0.08)); self.play(FadeIn(band0), FadeIn(sw, shift=UP * 0.25), run_time=0.35, rate_func=EXPO)

        # ===== 1. Same videos. Same pace. Same test at the end. =====
        self.until(S[1])
        self.out(Group(grid, band0, sw), rt=0.25)
        ls = [at(H(s, 128, GREY_P), y) for s, y in (("Same videos.", 470), ("Same pace.", 640), ("Same test.", 810))]
        sq = VGroup(*[RoundedRectangle(width=px(96), height=px(96), corner_radius=0.1, fill_color=PAPER2, fill_opacity=1, stroke_width=0) for _ in range(7)]).arrange(RIGHT, buff=px(36))
        left(sq.move_to([0, Y(1130), 0]))
        dot = Square(side_length=px(96), fill_color=INK, fill_opacity=1, stroke_width=0).move_to(sq[0])
        self.rise(ls[0], rt=0.4)
        self.until(wt(1, 2, 0.05)); self.rise(ls[1], sq, rt=0.4)
        self.add(dot); t_b = T(); dot.add_updater(lambda m: m.move_to(sq[int((T() - t_b) / 0.36) % 7]))
        self.until(wt(1, 4, 0.05)); self.rise(ls[2], rt=0.4)

        # ===== 2. But no two students think alike. (ink, colour triptych) =====
        self.until(S[2])
        self.gone(dot)
        self.ground(INK, UP, 0.45); self.remove(*ls, sq)
        names = [pick("p1", "hook"), pick("p2", "calm"), pick("p3", "hero", "teacher")]
        trip = Group(*[photo(n, "ed", 280, 980, 0.38) for n in names]).arrange(RIGHT, buff=px(24))
        left(trip.move_to([0, Y(190 + 490), 0]))
        l1 = at(H("No two students", 76, WHITE_, BOLD), 1300); l2 = at(SER("think alike.", 150, OR), 1430)
        self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.6) for t_ in trip], FadeIn(l1, shift=UP * 0.3), lag_ratio=0.15), run_time=0.6, rate_func=EXPO)
        self.until(wt(2, 4, 0.1)); self.rise(l2, rt=0.4)

        # ===== 3. Meet TutorDA. (paper) =====
        self.until(S[3])
        self.ground(PAPER, UP, 0.42); self.remove(trip, l1, l2)
        wm = wordmark(px(860)).move_to([0, Y(760), 0])
        self.ev("wordmark"); self.play(LaggedStart(FadeIn(wm[:5], shift=UP * 0.5), FadeIn(wm[5:], shift=DOWN * 0.5), lag_ratio=0.35), run_time=0.6, rate_func=EXPO)

        # ===== 4. DA stands for Dynamic Assessment. =====
        self.until(wt(4, 0, 0.12))
        hdr = wordmark(px(250)); left(hdr.move_to([0, Y(118), 0]))
        self.play(Transform(wm, hdr), run_time=0.55, rate_func=rate_functions.ease_in_out_cubic)
        self.remove(wm); self.add(hdr); hdr.set_z_index(12)
        dy = Text("Dynamic", font="Poppins", weight=ULTRABOLD, color=INK, font_size=150 * 0.6); dy[0].set_color(OR)
        asm = Text("Assessment", font="Poppins", weight=ULTRABOLD, color=INK, font_size=150 * 0.6); asm[0].set_color(OR)
        at(dy, 600); at(asm, 790)
        if asm.width > px(888): asm.scale_to_fit_width(px(888)); left(asm)
        rule = Line([X(96), Y(930), 0], [X(984), Y(930), 0], stroke_color=RULE, stroke_width=3)
        note = at(B("The DA in TutorDA.", 44, GREY_P), 1010)
        self.until(wt(4, 3, 0.1)); self.rise(dy, rt=0.4)
        self.until(wt(4, 4, 0.1)); self.rise(asm, rt=0.4)
        self.play(Create(rule), FadeIn(note, shift=UP * 0.15), run_time=0.45)

        # ===== 5. Every answer, how fast, how sure, shows us how you think. (ink, product UI) =====
        self.until(S[5])
        self.ground(INK, UP, 0.36); self.remove(dy, asm, rule, note)
        hdr_d = wordmark(px(250), dark=True); left(hdr_d.move_to([0, Y(118), 0])); hdr_d.set_z_index(12)
        self.remove(hdr); self.add(hdr_d)
        qc = card(888, 250, WHITE_); left(qc.move_to([0, Y(330), 0]))
        ql = B("Question 7", 30, GREY_P, SEMIBOLD); left(ql.move_to([0, Y(255), 0]), 140)
        qm = VGroup(B("Solve", 46, INK), MathTex(r"x^2-5x+6=0", color=INK, font_size=62 * 0.8)).arrange(RIGHT, buff=0.3); left(qm.move_to([0, Y(345), 0]), 140)
        self.rise(Group(qc, ql, qm), rt=0.3)
        tiles = VGroup(*[card(280, 210, INK2) for _ in range(3)]).arrange(RIGHT, buff=px(24)); left(tiles.move_to([0, Y(590), 0]))
        tl = [B(s, 28, GREY_I, SEMIBOLD) for s in ("Accuracy", "Time", "Confidence")]
        for t_, c_ in zip(tl, tiles): t_.move_to(c_.get_top() + DOWN * px(44)).align_to(c_.get_left() + RIGHT * px(30), LEFT)
        acc = VGroup(MathTex(r"x=2,\,3", color=WHITE_, font_size=44 * 0.8), tick(0.17)).arrange(RIGHT, buff=0.2)
        acc.move_to(tiles[0].get_center() + DOWN * px(25)).align_to(tiles[0].get_left() + RIGHT * px(30), LEFT)
        tv = ValueTracker(0)
        tm = H("0:00", 72, WHITE_)
        def _tm(m):
            m.become(H(f"0:{int(tv.get_value()):02d}", 72, WHITE_)); m.move_to(tiles[1].get_center() + DOWN * px(28)).align_to(tiles[1].get_left() + RIGHT * px(30), LEFT)
        tm.add_updater(_tm); _tm(tm)
        cbg = RoundedRectangle(width=px(220), height=px(14), corner_radius=px(7), fill_color=INK3, fill_opacity=1, stroke_width=0)
        cbg.move_to(tiles[2].get_center() + DOWN * px(30)).align_to(tiles[2].get_left() + RIGHT * px(30), LEFT).set_z_index(2)
        cv = ValueTracker(0.03)
        cf = cbg.copy().set_fill(OR, 1).set_z_index(3); cf.stretch_to_fit_width(px(6)); cf.align_to(cbg, LEFT)
        self.until(wt(5, 1, 0.1)); self.play(*[FadeIn(m, shift=UP * 0.3) for m in (tiles[0], tl[0], acc)], run_time=0.3, rate_func=EXPO)
        self.until(wt(5, 3, 0.1)); self.play(FadeIn(tiles[1], shift=UP * 0.3), FadeIn(tl[1], shift=UP * 0.3), run_time=0.2, rate_func=EXPO)
        self.add(tm); self.play(tv.animate.set_value(42), run_time=0.3)
        self.until(wt(5, 5, 0.1)); self.play(FadeIn(tiles[2], shift=UP * 0.3), FadeIn(tl[2], shift=UP * 0.3), run_time=0.2, rate_func=EXPO)
        self.add(cbg, cf); self.play(cf.animate.stretch_to_fit_width(px(176)).align_to(cbg, LEFT), run_time=0.3)
        prof = card(888, 470, INK2); left(prof.move_to([0, Y(1100), 0]))
        pt = B("How you think", 34, WHITE_, SEMIBOLD); left(pt.move_to([0, Y(925), 0]), 140)
        rows = VGroup()
        for k, (topic, v, lab) in enumerate((("Algebra", 0.86, "strong"), ("Geometry", 0.55, "building"), ("Calculus", 0.22, "new"))):
            y = 1020 + k * 95
            n = B(topic, 32, "#C9CFDD"); left(n.move_to([0, Y(y), 0]), 140)
            bb = RoundedRectangle(width=px(400), height=px(16), corner_radius=px(8), fill_color=INK3, fill_opacity=1, stroke_width=0); left(bb.move_to([0, Y(y), 0]), 400)
            bf = RoundedRectangle(width=px(400) * v, height=px(16), corner_radius=px(8), fill_color=OR if k == 0 else ("#FFB27A" if k == 1 else "#7C86A0"), fill_opacity=1, stroke_width=0)
            left(bf.move_to([0, Y(y), 0]), 400)
            lb = B(lab, 28, GREY_I); lb.move_to([0, Y(y), 0]).align_to([X(940), 0, 0], RIGHT)
            rows.add(VGroup(n, bb, bf, lb))
        self.until(wt(5, 6, 0.05))
        self.play(FadeIn(prof, shift=UP * 0.3), FadeIn(pt, shift=UP * 0.3),
                  LaggedStart(*[AnimationGroup(FadeIn(r[0]), FadeIn(r[1]), GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows], lag_ratio=0.25), run_time=0.8, rate_func=EXPO)

        # ===== 6. So a test isn't the end of learning. It's the engine. (paper) =====
        self.until(S[6])
        self.gone(tm, cf)
        self.ground(PAPER, UP, 0.42); self.remove(qc, ql, qm, tiles, *tl, acc, tm, cbg, cf, prof, pt, rows)
        self.remove(hdr_d); self.add(hdr)
        end = at(SER("the end.", 210, INK), 640)
        pre = at(B("A test isn't", 60, GREY_P), 450)
        strike = Line(end.get_left() + LEFT * 0.1 + DOWN * 0.05, end.get_right() + RIGHT * 0.1 + DOWN * 0.05, stroke_color=OR, stroke_width=12)
        self.until(wt(6, 2, 0.15)); self.rise(pre, rt=0.35)
        self.until(wt(6, 5, 0.12)); self.rise(end, rt=0.35)
        self.ev("strike"); self.play(Create(strike), run_time=0.25)
        self.until(wt(6, 8, 0.1))
        cen = np.array([X(540), Y(1000), 0]); R0 = 2.75
        loop = Circle(radius=R0, stroke_color=INK, stroke_width=4).move_to(cen)
        labs = VGroup()
        for k, s in enumerate(("Assess", "Model", "Adapt", "Feedback")):
            a = PI / 2 - k * PI / 2; pos = cen + R0 * np.array([math.cos(a), math.sin(a), 0])
            labs.add(tag(s, 32, INK, PAPER2).move_to(pos))
        eng = SER("the engine.", 104, OR).move_to(cen)
        orb = Dot(radius=0.13, color=OR); ang = ValueTracker(PI / 2)
        orb.add_updater(lambda m: m.move_to(cen + R0 * np.array([math.cos(ang.get_value()), math.sin(ang.get_value()), 0])))
        self.play(Group(pre, end, strike).animate.shift(UP * 1.6).set_opacity(0.0), Create(loop), run_time=0.45)
        self.remove(pre, end, strike)
        self.add(orb); self.play(LaggedStart(*[FadeIn(l_, scale=0.85) for l_ in labs], lag_ratio=0.15), FadeIn(eng, shift=UP * 0.2), run_time=0.5, rate_func=EXPO)
        ang.add_updater(lambda m, dt: m.increment_value(-2.2 * dt))
        self.add(ang)

        # ===== 7. Your next question adapts in real time... mastered... not the calendar. (paper) =====
        self.until(S[7])
        self.out(Group(loop, labs, eng, orb), rt=0.25); self.gone(orb, ang)
        ttl = at(H("Adapts in real time", 64, INK), 300)
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 4, 1], x_length=px(860), y_length=px(420), tips=False,
                  axis_config={"stroke_color": RULE, "stroke_width": 3, "include_ticks": False})
        left(ax.move_to([0, Y(620), 0]), 110)
        yl = B("difficulty", 26, GREY_P); yl.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.12)
        self.rise(ttl, rt=0.35); self.play(Create(ax), FadeIn(yl), run_time=0.3)
        lv = [1, 2, 3, 2, 3, 3.7]; ok = [1, 1, 0, 1, 1, 1]
        pts = [ax.c2p(i + 1, v) for i, v in enumerate(lv)]
        marks, segs = VGroup(), VGroup()
        t_s, t_e = wt(7, 3, 0.1), wt(7, 6, -0.1)
        for i, p_ in enumerate(pts):
            m = Dot(p_, radius=0.13, color=OR) if ok[i] else Circle(radius=0.13, stroke_color=GREY_P, stroke_width=5).move_to(p_)
            an = [FadeIn(m, scale=0.4)]
            if i: s_ = Line(pts[i - 1], p_, stroke_color=INK, stroke_width=5); segs.add(s_); an.append(Create(s_))
            marks.add(m); self.until(t_s + (t_e - t_s) * i / 5); self.play(*an, run_time=0.18)
        mc = np.array([X(250), Y(1220), 0])
        rbg = Circle(radius=0.9, stroke_color=PAPER2, stroke_width=14).move_to(mc)
        mv = ValueTracker(0.01)
        ring = always_redraw(lambda: Arc(radius=0.9, start_angle=PI / 2, angle=-2 * PI * mv.get_value(), stroke_color=OR, stroke_width=14).move_arc_center_to(mc))
        pct = always_redraw(lambda: H(f"{int(round(mv.get_value() * 100))}%", 40, INK).move_to(mc))
        mtop = VGroup(H("Quadratics", 52, INK), B("mastered", 36, GREY_P)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        left(mtop.move_to([0, Y(1190), 0]), 430)
        unl = tag("Next topic unlocked  →", 32, WHITE_, INK); left(unl.move_to([0, Y(1330), 0]), 430)
        self.until(wt(7, 9, 0.1)); self.add(rbg, ring, pct); self.play(mv.animate.set_value(1.0), FadeIn(mtop, shift=UP * 0.2), run_time=1.0, rate_func=smooth)
        self.until(wt(7, 13, 0.05)); self.rise(unl, rt=0.35)
        cal = VGroup(RoundedRectangle(width=1.0, height=1.05, corner_radius=0.1, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3),
                     Rectangle(width=1.0, height=0.26, fill_color=INK, fill_opacity=1, stroke_width=0))
        cal[1].align_to(cal[0], UP); cal.move_to([X(915), Y(300), 0]); c31 = H("31", 34, INK).move_to(cal[0].get_center() + DOWN * 0.1)
        cx = Line(cal.get_corner(UL) + UL * 0.06, cal.get_corner(DR) + DR * 0.06, stroke_color=OR, stroke_width=8)
        self.until(wt(7, 18, 0.15)); self.rise(VGroup(cal, c31), rt=0.25); self.play(Create(cx), run_time=0.22)

        # ===== 8. Stuck at midnight? AI tutor 24/7. Expert teachers teach live. (ink) =====
        self.until(S[8])
        ring.clear_updaters(); pct.clear_updaters()
        self.ground(INK, UP, 0.42); self.remove(ttl, ax, yl, marks, segs, rbg, ring, pct, mtop, unl, cal, c31, cx)
        self.remove(hdr); self.add(hdr_d)
        clock = at(H("11:58 pm", 96, WHITE_), 300)
        ph = Phone([X(540), Y(990), 0], 0.94, screen="#121A2E")
        bt = ph.top() - ph.p(120)
        av = Circle(radius=ph.p(32), fill_color=OR, fill_opacity=1, stroke_width=0).move_to([ph.screen.get_left()[0] + ph.p(78), bt, 0])
        avt = B("AI", 26, WHITE_, SEMIBOLD).move_to(av)
        nm = VGroup(B("AI tutor", 34, WHITE_, SEMIBOLD), B("online", 24, "#4ADE80")).arrange(DOWN, buff=0.04, aligned_edge=LEFT).next_to(av, RIGHT, buff=0.18)
        sp = Line([ph.screen.get_left()[0], bt - ph.p(60), 0], [ph.screen.get_right()[0], bt - ph.p(60), 0], stroke_color=INK3, stroke_width=2)
        def bubble(content, me, y):
            r = RoundedRectangle(width=content.width + ph.p(56), height=content.height + ph.p(40), corner_radius=ph.p(28),
                                 fill_color=(OR if me else "#222C45"), fill_opacity=1, stroke_width=0)
            b = VGroup(r, content.move_to(r))
            x = ph.screen.get_right()[0] - ph.p(28) - r.width / 2 if me else ph.screen.get_left()[0] + ph.p(28) + r.width / 2
            return b.move_to([x, y - r.height / 2, 0])
        b1 = bubble(VGroup(B("Why is the derivative", 36, WHITE_), VGroup(B("of", 36, WHITE_), MathTex(r"x^2", color=WHITE_, font_size=46 * 0.8), B("equal to", 36, WHITE_), MathTex(r"2x\,?", color=WHITE_, font_size=46 * 0.8)).arrange(RIGHT, buff=0.1)).arrange(DOWN, buff=0.08, aligned_edge=LEFT), True, sp.get_y() - ph.p(40))
        ans = VGroup(B("Step 1  Start from the limit", 30, "#C9CFDD"), MathTex(r"\frac{(x+h)^2-x^2}{h}", color=WHITE_, font_size=46 * 0.8),
                     B("Step 2  Expand and simplify", 30, "#C9CFDD"), MathTex(r"=2x+h", color=WHITE_, font_size=46 * 0.8),
                     VGroup(B("Step 3  Let", 30, "#C9CFDD"), MathTex(r"h\to 0", color=WHITE_, font_size=44 * 0.8), MathTex(r"\Rightarrow 2x", color=OR, font_size=46 * 0.8)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        b2 = bubble(ans, False, b1.get_bottom()[1] - ph.p(28))
        dots = VGroup(*[Dot(radius=ph.p(9), color=GREY_I) for _ in range(3)]).arrange(RIGHT, buff=ph.p(12))
        typing = bubble(dots, False, b1.get_bottom()[1] - ph.p(28))
        for k, d_ in enumerate(typing[1]): d_.add_updater(lambda m, k=k: m.set_opacity(0.3 + 0.7 * max(0, math.sin(T() * 8 - k))))
        inp = RoundedRectangle(width=ph.screen.width - ph.p(64), height=ph.p(84), corner_radius=ph.p(42), fill_color="#222C45", fill_opacity=1, stroke_width=0).move_to([X(540), ph.screen.get_bottom()[1] + ph.p(88), 0])
        inpt = B("Ask a doubt…", 30, GREY_I).move_to(inp).align_to(inp.get_left() + RIGHT * ph.p(34), LEFT)
        self.rise(clock, rt=0.35)
        self.play(FadeIn(ph, shift=UP * 0.7), run_time=0.45, rate_func=EXPO); self.add(av, avt, nm, sp, inp, inpt)
        self.until(wt(8, 3, 0.1)); self.play(FadeIn(b1, shift=UP * 0.2), run_time=0.25)
        self.add(typing)
        self.until(wt(8, 8, 0.15)); self.gone(typing)
        self.play(FadeIn(b2[0]), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in b2[1]], lag_ratio=0.25), run_time=0.9)
        tf = at(H("24/7", 150, OR), 300)
        self.until(wt(8, 12, 0.12)); self.play(FadeOut(clock, shift=UP * 0.3), FadeIn(tf, shift=UP * 0.3), run_time=0.3, rate_func=EXPO)
        self.until(wt(8, 13, 0.2))
        tp = photo("teacher", "ed", 1080, BAND_TOP, 0.4).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        self.kb(tp, T(), S[9], 1.0, 1.04)
        chat = Group(ph, av, avt, nm, sp, b1, b2, inp, inpt, tf)
        self.play(FadeIn(tp), chat.animate.shift(UP * 0.4).set_opacity(0), run_time=0.4)
        self.remove(chat)
        rd = Dot(radius=px(12), color="#FF3B3B")
        live = VGroup(RoundedRectangle(width=px(176), height=px(60), corner_radius=0.12, fill_color=INK, fill_opacity=0.9, stroke_width=0),
                      VGroup(rd, B("Live", 32, WHITE_, SEMIBOLD)).arrange(RIGHT, buff=0.14))
        live[1].move_to(live[0]); left(live.move_to([0, Y(250), 0]))
        self.until(wt(8, 16, 0.1)); self.rise(live, rt=0.3)
        rd.add_updater(lambda d: d.set_opacity(0.35 + 0.65 * (0.5 + 0.5 * math.cos(T() * 7))))

        # ===== 9. From Class 10 to university maths, JEE and NEET to IELTS. All in one place. (paper, type list) =====
        self.until(S[9])
        self.gone(rd); tp.clear_updaters()
        self.ground(PAPER, UP, 0.42); self.remove(tp, live)
        self.remove(hdr_d); self.add(hdr)
        items = (("Class 10–12", "School", 2), ("University maths", "Degree", 4), ("JEE · NEET", "Entrance", 7), ("IELTS", "English", 11))
        rows9 = []
        for k, (a, b, wi) in enumerate(items):
            y = 330 + k * 200
            ta = at(H(a, 92, INK), y); tb = B(b, 32, GREY_P); tb.move_to([0, Y(y + 10), 0]).align_to([X(984), 0, 0], RIGHT)
            rl = Line([X(96), Y(y + 95), 0], [X(984), Y(y + 95), 0], stroke_color=RULE, stroke_width=3)
            rows9.append((wi, VGroup(ta, tb, rl)))
        if rows9[1][1][0].width > px(700): rows9[1][1][0].scale_to_fit_width(px(700)); left(rows9[1][1][0])
        for wi, g in rows9:
            self.until(wt(9, wi, 0.12)); self.play(FadeIn(g[0], shift=UP * 0.3), FadeIn(g[1]), Create(g[2]), run_time=0.35, rate_func=EXPO)
        aio = at(SER("all in one place.", 140, OR), 1260)
        self.until(wt(9, 13, 0.1)); self.rise(aio, rt=0.45)

        # ===== 10. Real exam-pattern mocks. Free courses, games and tools. (ink) =====
        self.until(S[10])
        self.ground(INK, UP, 0.42); self.remove(*[g for _, g in rows9], aio)
        self.remove(hdr); self.add(hdr_d)
        ex = Phone([X(300), Y(860), 0], 0.78, screen="#121A2E")
        L, T0 = ex.screen.get_left()[0] + ex.p(36), ex.top() - ex.p(110)
        et = VGroup(B("JEE Main", 40, WHITE_, SEMIBOLD), B("Full mock", 40, OR, SEMIBOLD)).arrange(RIGHT, buff=0.14).move_to([0, T0, 0]).align_to([L, 0, 0], LEFT)
        t_ex = C[10]
        tmr = always_redraw(lambda: B("Time left  {:02d}:{:02d}:{:02d}".format(*(lambda s: (s // 3600, s % 3600 // 60, s % 60))(max(0, int(10800 - max(0, T() - t_ex) * 41)))), 30, GREY_I).move_to([0, T0 - ex.p(56), 0]).align_to([L, 0, 0], LEFT))
        info = VGroup(*[VGroup(B(a, 30, "#C9CFDD"), B(b, 30, WHITE_, SEMIBOLD)).arrange(RIGHT, buff=0.3) for a, b in (("Marking", "+4 / −1"), ("Questions", "75 · 3 hours"))]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        info.next_to(tmr, DOWN, buff=0.3).align_to([L, 0, 0], LEFT)
        pal = VGroup(*[RoundedRectangle(width=ex.p(66), height=ex.p(66), corner_radius=ex.p(12), fill_color="#222C45", fill_opacity=1, stroke_width=0) for _ in range(36)])
        pal.arrange_in_grid(rows=6, cols=6, buff=ex.p(16)).move_to([ex.screen.get_center()[0], ex.screen.get_center()[1] - ex.p(150), 0])
        rk = tag("Estimated rank  ↗", 30, WHITE_, OR).move_to([ex.screen.get_center()[0], ex.screen.get_bottom()[1] + ex.p(90), 0])
        self.play(FadeIn(ex, shift=UP * 0.6), run_time=0.4, rate_func=EXPO)
        self.add(et, tmr, info, pal)
        rng = np.random.default_rng(9)
        self.play(LaggedStart(*[pal[i].animate.set_fill(OR if rng.random() < 0.8 else "#4C5A7A") for i in range(22)], lag_ratio=0.1), run_time=0.7)
        self.rise(rk, rt=0.3)
        frees = VGroup()
        for k, s in enumerate(("Courses", "Games", "Tools")):
            c_ = card(380, 210, INK2); c_.move_to([X(770), Y(560 + k * 250), 0])
            t_ = H(s, 52, WHITE_); t_.move_to(c_.get_center() + UP * px(28)).align_to(c_.get_left() + RIGHT * px(36), LEFT)
            f_ = B("Free", 34, OR, SEMIBOLD); f_.move_to(c_.get_center() + DOWN * px(48)).align_to(c_.get_left() + RIGHT * px(36), LEFT)
            frees.add(VGroup(c_, t_, f_))
        for k, wi in enumerate((4, 5, 7)):
            self.until(wt(10, wi, 0.1)); self.play(FadeIn(frees[k], shift=LEFT * 0.35), run_time=0.3, rate_func=EXPO)

        # ===== 11. Not one-size-fits-all. Learning that adapts to you. (paper -> hero photo) =====
        self.until(S[11])
        self.gone(tmr)
        self.ground(PAPER, UP, 0.42); self.remove(ex, et, tmr, info, pal, rk, frees)
        self.remove(hdr_d); self.add(hdr)
        n1 = at(H("Not one-size-", 120, GREY_P), 560); n2 = at(H("fits-all.", 120, GREY_P), 720)
        stk = VGroup(Line(n1.get_left(), n1.get_right(), stroke_color=OR, stroke_width=12), Line(n2.get_left(), n2.get_right(), stroke_color=OR, stroke_width=12))
        self.rise(n1, n2, rt=0.35)
        self.until(wt(11, 1, -0.25)); self.ev("strike2"); self.play(LaggedStart(*[Create(s_) for s_ in stk], lag_ratio=0.4), run_time=0.4)
        hp = pick("hero", "calm")
        hero = photo(hp, "ed", 1080, BAND_TOP, 0.42).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        shade = Rectangle(width=9.2, height=px(560), fill_color=INK, fill_opacity=0.0, stroke_width=0).set_z_index(-4)
        shade.move_to([0, Y(BAND_TOP) + px(280), 0]).set_fill(opacity=0.55)
        self.until(wt(11, 2, 0.25))
        self.play(FadeOut(VGroup(n1, n2, stk)), FadeIn(hero), FadeIn(shade), FadeOut(hdr), run_time=0.4)
        self.kb(hero, T(), S[12], 1.0, 1.04)
        g1 = at(H("Learning that", 84, WHITE_), 1240); g2 = at(SER("adapts to you.", 150, "#FFB27A"), 1390)
        self.rise(g1, rt=0.35)
        self.until(wt(11, 4, 0.1)); self.rise(g2, rt=0.4)

        # ===== 12. TutorDA. Start free at tutorda.org (ink) =====
        self.until(S[12])
        hero.clear_updaters()
        self.ground(INK, UP, 0.45); self.remove(hero, shade, g1, g2)
        wm2 = wordmark(px(860), dark=True).move_to([0, Y(640), 0])
        self.ev("wordmark_end"); self.play(LaggedStart(FadeIn(wm2[:5], shift=UP * 0.4), FadeIn(wm2[5:], shift=DOWN * 0.4), lag_ratio=0.3), run_time=0.55, rate_func=EXPO)
        sf = B("Start free at", 50, GREY_I).move_to([0, Y(900), 0])
        url = H("tutorda.org", 120, OR).move_to([0, Y(1040), 0])
        ul = Line(url.get_corner(DL) + DOWN * 0.12, url.get_corner(DR) + DOWN * 0.12, stroke_color=OR, stroke_width=6)
        self.until(wt(12, 1, 0.1)); self.rise(sf, rt=0.35)
        self.until(wt(12, 4, 0.2)); self.play(FadeIn(url, shift=UP * 0.3), Create(ul), run_time=0.45, rate_func=EXPO)

        # ===== END CARD (paper) =====
        self.until(S[13])
        self.ground(PAPER, UP, 0.45); self.remove(wm2, sf, url, ul)
        wm3 = wordmark(px(760)).move_to([0, Y(700), 0])
        tg = SER("Learning that adapts to you.", 74, INK).move_to([0, Y(880), 0])
        rl = Line([X(390), Y(990), 0], [X(690), Y(990), 0], stroke_color=RULE, stroke_width=3)
        site = B("tutorda.org", 46, OR, SEMIBOLD).move_to([0, Y(1070), 0])
        fol = B("Follow TutorDA", 36, GREY_P).move_to([0, Y(1150), 0])
        self.rise(wm3, rt=0.45); self.rise(tg, rl, site, fol, rt=0.6, lag=0.15)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", "film2_events.json"), "w"))
