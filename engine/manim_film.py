"""TutorDA brand film (~57 s, 9:16). Story: sameness -> 'no two students think alike' -> TutorDA, DA = Dynamic Assessment
-> how it works (signals, the engine loop, adaptive path, mastery) -> help 24/7 + live teachers -> breadth -> free -> tagline.
Everything is drawn here or generated (assets/gen, Z-Image-Turbo); nothing is taken from the website.
Render: tools/manim_build.sh engine/manim_film.py Film brandt out/film.mp4 [draft]"""
import os, sys, math
import numpy as np
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
from manim_common import *          # config, CRF patch, px/X/Y, baseline, ReelScene
import brandt as K
import manimpango

GEN, FILM = os.path.join(KIT, "assets", "gen"), os.path.join(KIT, "assets", "film")
manimpango.register_font(os.path.join(KIT, "assets", "fonts", "Orbitron.ttf"))
config.background_color = "#0B0B18"
BG, SURF, SURF2, LINE_C = "#0B0B18", "#161630", "#1F1F3D", "#2E2E55"
TXT, MUTED, COLD = "#E8E8FF", "#A3A8CC", "#7C8199"
OR, GOLD, INKD, GREEN, BLUE, BLUE_D, RED = "#FF8C00", "#FFD700", "#1A1000", "#22C55E", "#4F9BFF", "#1D4ED8", "#FF4D4D"
GRAD = ("#FFFFFF", OR, GOLD)

def D(s, size, grad=True, color=TXT):
    t = Text(s, font="Orbitron", weight=ULTRABOLD, font_size=size * 0.6, color=color)
    return t.set_color_by_gradient(*GRAD) if grad else t
def P(s, size, color=TXT, weight=BOLD):
    return Text(s, font="Poppins", weight=weight, color=color, font_size=size * 0.6)
def has(name): return os.path.exists(os.path.join(GEN, name + "_plate.jpg"))
def pick(*names):
    for n in names:
        if has(n): return n
    return names[-1]
def plate(name, kind="plate"):
    return ImageMobject(os.path.join(GEN, f"{name}_{kind}.jpg")).set_height(16).move_to(ORIGIN)
def chip(s, size=40, fg=TXT, bg=SURF2, stroke=None, padx=0.32, pady=0.17, op=0.94):
    t = P(s, size, fg)
    r = RoundedRectangle(width=t.width + 2 * padx, height=t.height + 2 * pady, corner_radius=(t.height + 2 * pady) / 2,
                         fill_color=bg, fill_opacity=op, stroke_color=stroke or bg, stroke_width=2.5 if stroke else 0)
    return VGroup(r, t.move_to(r))
def glow_pill(s, size, padx=0.5, pady=0.24):
    t = P(s, size, INKD)
    r = RoundedRectangle(width=t.width + 2 * padx, height=t.height + 2 * pady, corner_radius=(t.height + 2 * pady) / 2,
                         fill_opacity=1, stroke_width=0).set_fill(color=[OR, GOLD]); r.set_sheen_direction(RIGHT)
    return VGroup(r, t.move_to(r))
def glow(r, y, c=OR, x=0):
    return ImageMobject(os.path.join(FILM, "glow_blue.png" if c != OR else "glow_or.png")).set_height(2 * r).move_to([x, Y(y), 0])
def check(r=0.3, c=GREEN):
    return VGroup(Circle(radius=r, fill_color=c, fill_opacity=1, stroke_width=0),
                  VMobject(stroke_color=WHITE, stroke_width=8 * r / 0.3).set_points_as_corners([[-0.4 * r, 0, 0], [-0.1 * r, -0.33 * r, 0], [0.47 * r, 0.37 * r, 0]]))
def cross(r=0.3, c=RED):
    return VGroup(Circle(radius=r, fill_color=c, fill_opacity=1, stroke_width=0),
                  Line([-0.35 * r, -0.35 * r, 0], [0.35 * r, 0.35 * r, 0], stroke_color=WHITE, stroke_width=7),
                  Line([-0.35 * r, 0.35 * r, 0], [0.35 * r, -0.35 * r, 0], stroke_color=WHITE, stroke_width=7))

def wordmark(width):
    """Our own TutorDA wordmark: 'Tutor' in brand blue, 'DA' in orange-gold, with a soft drop for depth."""
    t = Text("TutorDA", font="Poppins", weight=BOLD, font_size=120)
    t[:5].set_color_by_gradient("#7DB8FF", BLUE, BLUE_D); t[5:].set_color_by_gradient(GOLD, OR)
    sh = t.copy().set_color("#05050C").set_opacity(0.85).shift(DOWN * 0.06 + RIGHT * 0.03)
    g = VGroup(sh, t); g.scale_to_fit_width(width); return g

class Phone(Group):
    SW, SH = 556, 1176
    def __init__(self, center, scale=1.0):
        self.screen = RoundedRectangle(width=px(self.SW), height=px(self.SH), corner_radius=px(56), fill_color="#10102A", fill_opacity=1, stroke_width=0)
        self.frame = ImageMobject(os.path.join(FILM, "phone_frame.png")).set_height(px(1220)).set_z_index(3)
        super().__init__(self.screen, self.frame); self.scale(scale).move_to(center); self.k = scale
    def top(self): return self.screen.get_top()[1]
    def p(self, v): return px(v) * self.k

class Film(ReelScene):
    K = K
    def kb(self, m, t0, t1, s0=1.0, s1=1.07, drift=(0, 0)):
        base_h, c0 = m.height, m.get_center().copy()
        def upd(mm):
            u = min(1, max(0, (self.renderer.time - t0) / (t1 - t0)))
            mm.set_height(base_h * (s0 + (s1 - s0) * u)); mm.move_to(c0 + np.array([drift[0] * u, drift[1] * u, 0]))
        m.add_updater(upd); return m
    def gone(self, *ms):
        for m in ms:
            m.clear_updaters()
            for s in m.get_family(): s.clear_updaters()
        self.remove(*ms)

    def captions(self):
        now = lambda: self.renderer.time; caps = []
        for i in range(len(K.CLIPS) - 1):
            cap = K.CLIPS[i][2]; lines = [l.split() for l in cap.split("|")]
            words = [w for l in lines for w in l]; line_txt = [" ".join(l) for l in lines]; spans = []
            for li, l in enumerate(lines):
                c = 0
                for w_ in l: spans.append((li, c, c + len(w_))); c += len(w_) + 1
            def make(k, lines=lines, line_txt=line_txt, spans=spans):
                rows = VGroup(*[Text(line_txt[li], font="Poppins", weight=BOLD, color=WHITE, font_size=44 * 0.6,
                                     t2c=({f"[{spans[k][1]}:{spans[k][2]}]": GOLD} if k >= 0 and spans[k][0] == li else {}))
                                for li in range(len(lines))])
                for li, r in enumerate(rows): r.shift(UP * (-li * px(60) - baseline(r)))
                return rows.move_to([0, Y(1775) + rows.height / 2, 0])
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
        live.add_updater(show); show(live); live.set_z_index(20); self.add(live)

    def construct(self):
        C, wt = K.C, K.wt
        S = [c - 0.28 for c in C]
        T = lambda: self.renderer.time
        scrim = ImageMobject(os.path.join(FILM, "scrim.png")).set_height(16).set_z_index(5)
        vig = ImageMobject(os.path.join(FILM, "vignette.png")).set_height(16).set_z_index(4)
        self.add(scrim, vig); self.captions()

        # ===== 0. Most learning still teaches everyone the same way. =====
        p0 = pick("class", "hook")
        bg = self.kb(plate(p0, "grey"), 0, S[1], 1.0, 1.08).set_z_index(-10); self.add(bg)
        tiles = Group(*[ImageMobject(os.path.join(GEN, p0 + "_greythumb.jpg")).set_height(16 / 4.25) for _ in range(12)])
        tiles.arrange_in_grid(rows=4, cols=3, buff=0.12).move_to([0, 0.3, 0])
        self.until(wt(0, 4, 0.05))          # "everyone"
        self.play(bg.animate.set_opacity(0.0), FadeIn(tiles, lag_ratio=0.06), run_time=0.9, rate_func=smooth)
        self.gone(bg)
        stamp = D("THE SAME WAY", 76, grad=False, color=TXT).move_to([0, 0.3, 0]).set_z_index(6)
        band = Rectangle(width=9.2, height=stamp.height + 0.45, fill_color=BG, fill_opacity=0.85, stroke_width=0).move_to(stamp).set_z_index(5)
        self.until(wt(0, 6, 0.05)); self.play(FadeIn(band), FadeIn(stamp, scale=1.2), run_time=0.25, rate_func=rush_from)

        # ===== 1. Same videos. Same pace. Same test at the end. (cold, mechanical) =====
        self.until(S[1])
        self.play(FadeOut(Group(tiles, band, stamp)), run_time=0.25)
        lines = [D(s, 92, grad=False, color=COLD) for s in ("SAME VIDEOS.", "SAME PACE.", "SAME TEST.")]
        for l_, y in zip(lines, (420, 560, 700)): l_.move_to([0, Y(y), 0]).align_to([X(90), 0, 0], LEFT)
        def card_play():
            r = RoundedRectangle(width=px(230), height=px(140), corner_radius=px(18), fill_color="#1A1A26", fill_opacity=1, stroke_color="#2A2A38", stroke_width=2)
            tri = Triangle(fill_color=COLD, fill_opacity=1, stroke_width=0).scale(0.22).rotate(-PI / 2).move_to(r)
            return VGroup(r, tri)
        conv = VGroup(*[card_play() for _ in range(9)]).arrange(RIGHT, buff=0.25).move_to([1.2, Y(900), 0])
        ticks = VGroup(*[Line(UP * 0.18, DOWN * 0.18, stroke_color=COLD, stroke_width=5) for _ in range(13)]).arrange(RIGHT, buff=0.5).move_to([0, Y(1060), 0])
        beat = Dot(radius=0.11, color=TXT).move_to(ticks[0])
        papers = VGroup()
        for k in range(5):
            r = RoundedRectangle(width=px(150), height=px(200), corner_radius=px(10), fill_color="#1A1A26", fill_opacity=1, stroke_color="#2A2A38", stroke_width=2)
            ls = VGroup(*[Line(LEFT * 0.38, RIGHT * 0.38, stroke_color="#3A3A4A", stroke_width=4) for _ in range(4)]).arrange(DOWN, buff=0.16).move_to(r)
            papers.add(VGroup(r, ls))
        papers.arrange(RIGHT, buff=0.22).move_to([0, Y(1290), 0])
        self.play(FadeIn(lines[0], shift=RIGHT * 0.4), FadeIn(conv), run_time=0.25, rate_func=rush_from)
        conv.add_updater(lambda m, dt: m.shift(LEFT * 1.4 * dt))
        self.until(wt(1, 2, 0.05)); self.play(FadeIn(lines[1], shift=RIGHT * 0.4), FadeIn(ticks), FadeIn(beat), run_time=0.22, rate_func=rush_from)
        t_b = T(); beat.add_updater(lambda m: m.move_to(ticks[int((T() - t_b) / 0.32) % 13]))
        self.until(wt(1, 4, 0.05)); self.play(FadeIn(lines[2], shift=RIGHT * 0.4), LaggedStart(*[FadeIn(p_, shift=DOWN * 0.2) for p_ in papers], lag_ratio=0.12), run_time=0.45, rate_func=rush_from)

        # ===== 2. But no two students think alike. (colour returns) =====
        self.until(S[2])
        self.play(FadeOut(VGroup(*lines, conv, ticks, beat, papers)), run_time=0.22)
        self.gone(conv, beat)
        names = [pick("p1", "hook"), pick("p2", "calm"), pick("p3", "teacher")]
        strips = Group()
        for j, n in enumerate(names):
            im = ImageMobject(os.path.join(GEN, n + "_plate.jpg")).set_height(16)
            # show a 3-unit-wide vertical slice of each portrait (crop via pixel array)
            arr = im.pixel_array; w = arr.shape[1]; cw = int(w / 3 + 2)
            sl = ImageMobject(arr[:, (w - cw) // 2:(w + cw) // 2]).set_height(16).move_to([-3 + 3 * j, 0, 0])
            strips.add(sl)
        for j, s_ in enumerate(strips): s_.shift(UP * (16 if j % 2 == 0 else -16))
        self.play(*[s_.animate.shift(DOWN * (16 if j % 2 == 0 else -16)) for j, s_ in enumerate(strips)], run_time=0.55, rate_func=rate_functions.ease_out_cubic)
        seps = VGroup(*[Line([x, 8, 0], [x, -8, 0], stroke_color=BG, stroke_width=10) for x in (-1.5, 1.5)]).set_z_index(1)
        self.add(seps)
        paths = VGroup(
            VMobject(stroke_color=GOLD, stroke_width=7).set_points_smoothly([[-3 + 0.9 * math.sin(k), Y(500) + 0.0 - 0.45 * k, 0] for k in range(9)]),
            VMobject(stroke_color=OR, stroke_width=7).set_points_as_corners([[(-0.9 if k % 2 else 0.9), Y(500) - 0.45 * k, 0] for k in range(9)]),
            ParametricFunction(lambda u: np.array([3 + 0.12 * u * math.cos(u), Y(820) + 0.12 * u * math.sin(u), 0]), t_range=[0, 4 * PI], color=BLUE, stroke_width=7)).set_z_index(2)
        self.until(wt(2, 4, 0.1)); self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.2), run_time=0.8)

        # ===== 3. Meet TutorDA. =====
        self.until(S[3])
        self.play(FadeOut(Group(strips, seps, paths)), run_time=0.25)
        wm = wordmark(px(820)).move_to([0, Y(820), 0])
        g0 = glow(5.0, 820)
        streak = Line([-6, Y(820), 0], [-4, Y(820), 0], stroke_color=GOLD, stroke_width=6)
        self.play(streak.animate.move_to([6, Y(820), 0]), run_time=0.35, rate_func=rush_into)
        self.remove(streak)
        self.play(FadeIn(g0, scale=0.5), FadeIn(wm, scale=1.15), run_time=0.45, rate_func=rate_functions.ease_out_cubic)

        # ===== 4. DA stands for Dynamic Assessment. =====
        self.until(wt(4, 0, 0.1))
        self.play(wm.animate.scale(0.72).move_to([0, Y(560), 0]), g0.animate.move_to([0, Y(700), 0]), run_time=0.45, rate_func=smooth)
        dyn = D("DYNAMIC", 112).move_to([0, Y(830), 0]); ass = D("ASSESSMENT", 104).move_to([0, Y(970), 0])
        self.until(wt(4, 3, 0.1)); self.play(FadeIn(dyn, shift=UP * 0.25), run_time=0.3, rate_func=rush_from)
        self.until(wt(4, 4, 0.1)); self.play(FadeIn(ass, shift=UP * 0.25), run_time=0.3, rate_func=rush_from)
        ul = Line([ass.get_left()[0], Y(1065), 0], [ass.get_right()[0], Y(1065), 0], stroke_color=OR, stroke_width=8)
        self.play(Create(ul), run_time=0.4)

        # header wordmark from here on
        head = wordmark(px(230)).move_to([0, Y(120), 0]).set_z_index(10)

        # ===== 5. Every answer, how fast, how sure, shows us how you think. =====
        self.until(S[5])
        qc = RoundedRectangle(width=px(880), height=px(300), corner_radius=0.3, fill_color=SURF, fill_opacity=1, stroke_color=LINE_C, stroke_width=2).move_to([0, Y(470), 0])
        ql = P("QUESTION 7", 30, OR).move_to(qc.get_top() + DOWN * px(48)).align_to(qc.get_left() + RIGHT * px(48), LEFT)
        qm = VGroup(P("Solve", 46, MUTED, MEDIUM), MathTex(r"x^2-5x+6=0", color=WHITE, font_size=64 * 0.8)).arrange(RIGHT, buff=0.3).move_to(qc.get_center() + DOWN * px(25))
        self.play(FadeOut(Group(dyn, ass, ul, g0)), wm.animate.scale(px(230) / wm.width).move_to(head), FadeIn(Group(qc, ql, qm), shift=UP * 0.3), run_time=0.4)
        self.remove(wm); self.add(head)
        sig = []
        a1 = VGroup(MathTex(r"x = 2,\ 3", color=WHITE, font_size=52 * 0.8), check(0.24)).arrange(RIGHT, buff=0.25)
        b1 = RoundedRectangle(width=px(300), height=px(150), corner_radius=0.25, fill_color=SURF2, fill_opacity=1, stroke_width=0)
        timer_v = ValueTracker(0)
        clockface = always_redraw(lambda: D(f"0:{int(timer_v.get_value()):02d}", 56, grad=False, color=GOLD).move_to([X(540), Y(775), 0]).set_z_index(3))
        conf_bg = RoundedRectangle(width=px(240), height=px(18), corner_radius=px(9), fill_color="#2A2A48", fill_opacity=1, stroke_width=0).move_to([X(855), Y(790), 0]).set_z_index(2)
        conf_v = ValueTracker(0.02)
        conf = always_redraw(lambda: RoundedRectangle(width=px(240) * conf_v.get_value(), height=px(18), corner_radius=px(9), fill_opacity=1, stroke_width=0).set_fill(color=[OR, GOLD]).move_to(conf_bg.get_left(), aligned_edge=LEFT).set_z_index(3))
        cards = VGroup(*[RoundedRectangle(width=px(285), height=px(190), corner_radius=0.25, fill_color=SURF, fill_opacity=1, stroke_color=LINE_C, stroke_width=2).move_to([X(x), Y(760), 0]) for x in (225, 540, 855)])
        labs = VGroup(*[P(s, 28, MUTED, MEDIUM).move_to([X(x), Y(690), 0]) for s, x in (("ACCURACY", 225), ("TIME", 540), ("CONFIDENCE", 855))])
        a1.scale(0.85).move_to([X(225), Y(775), 0]).set_z_index(3); labs.set_z_index(3)
        self.until(wt(5, 1, 0.1)); self.play(FadeIn(cards[0]), FadeIn(labs[0]), FadeIn(a1, scale=0.7), run_time=0.3)
        self.until(wt(5, 3, 0.1)); self.add(clockface); self.play(FadeIn(cards[1]), FadeIn(labs[1]), timer_v.animate.set_value(42), run_time=0.45)
        self.until(wt(5, 5, 0.1)); self.add(conf_bg, conf); self.play(FadeIn(cards[2]), FadeIn(labs[2]), conf_v.animate.set_value(0.8), run_time=0.45)
        # signals flow into the learner model
        rng = np.random.default_rng(5)
        nodes = VGroup(*[Dot(point=[rng.uniform(-2.6, 2.6), Y(1180) + rng.uniform(-1.3, 1.3), 0], radius=rng.uniform(0.06, 0.12), color=BLUE) for _ in range(22)])
        edges = VGroup(*[Line(nodes[i].get_center(), nodes[j].get_center(), stroke_color=BLUE, stroke_width=2, stroke_opacity=0.45)
                         for i in range(22) for j in range(i + 1, 22) if np.linalg.norm(nodes[i].get_center() - nodes[j].get_center()) < 1.25])
        core = glow(1.8, 1180, BLUE)
        flows = VGroup(*[Line(c.get_bottom(), [0, Y(1120), 0], stroke_color=OR, stroke_width=5) for c in cards])
        self.until(wt(5, 6, 0.05))
        self.play(LaggedStart(*[ShowPassingFlash(f.copy(), time_width=0.6) for f in flows], lag_ratio=0.15), FadeIn(core), Create(edges), FadeIn(nodes), run_time=0.8)
        self.play(*[n.animate.set_color(GOLD) for n in nodes[::3]], run_time=0.3)
        timer_v.clear_updaters()

        # ===== 6. So a test isn't the end of learning. It's the engine. =====
        self.until(S[6])
        self.gone(clockface, conf)
        self.play(FadeOut(Group(qc, ql, qm, a1, cards, labs, conf_bg, nodes, edges, core)), run_time=0.25)
        paper = VGroup(RoundedRectangle(width=px(420), height=px(560), corner_radius=px(18), fill_color="#F4F1EA", fill_opacity=1, stroke_width=0),
                       P("TEST", 52, "#22223A"),
                       VGroup(*[Line(LEFT * 1.1, RIGHT * 1.1, stroke_color="#C9C5BA", stroke_width=5) for _ in range(6)]).arrange(DOWN, buff=0.28))
        paper[1].move_to(paper[0].get_top() + DOWN * px(70)); paper[2].next_to(paper[1], DOWN, buff=0.35)
        paper.move_to([0, Y(820), 0]).rotate(-0.04)
        endst = D("THE END", 70, grad=False, color=RED).rotate(0.18).move_to(paper.get_center() + DOWN * px(120))
        self.play(FadeIn(paper, shift=UP * 0.4), run_time=0.3)
        self.until(wt(6, 5, 0.15)); self.play(FadeIn(endst, scale=1.6), run_time=0.18, rate_func=rush_from)
        self.until(wt(6, 8, 0.15))
        # the paper becomes the engine: a loop of four stages that keeps turning
        R0 = 2.95; cen = np.array([0, Y(860), 0])
        ring = Circle(radius=R0, stroke_color=LINE_C, stroke_width=6).move_to(cen)
        arcs = VGroup(*[Arc(radius=R0, start_angle=PI / 2 - k * PI / 2 - 0.32, angle=-(PI / 2 - 0.64), stroke_color=OR, stroke_width=9).add_tip(tip_length=0.24, tip_width=0.24).move_arc_center_to(cen) for k in range(4)])
        stg = ("ASSESS", "MODEL", "ADAPT", "FEEDBACK")
        nodes2 = VGroup()
        for k, s in enumerate(stg):
            ang = PI / 2 - k * PI / 2; pos = cen + R0 * np.array([math.cos(ang), math.sin(ang), 0])
            c_ = chip(s, 34, INKD, GOLD).move_to(pos); nodes2.add(c_)
        eng = D("ENGINE", 76).move_to(cen)
        self.play(FadeOut(endst, shift=UP * 0.6, scale=0.5), paper.animate.scale(0.25).move_to(cen).set_opacity(0), FadeIn(ring), Create(arcs), run_time=0.45)
        self.remove(paper)
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes2], lag_ratio=0.15), FadeIn(eng, scale=1.3), run_time=0.5, rate_func=rate_functions.ease_out_back)
        arcs.add_updater(lambda m, dt: m.rotate(-1.4 * dt, about_point=cen))

        # ===== 7. Your next question adapts in real time. ... mastered ... not the calendar =====
        self.until(S[7])
        self.play(FadeOut(Group(ring, arcs, nodes2, eng)), run_time=0.25); self.gone(arcs)
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 4, 1], x_length=7.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": LINE_C, "stroke_width": 3, "include_ticks": False}).move_to([0, Y(690), 0])
        lab_y = P("difficulty", 28, MUTED, MEDIUM).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        lab_x = P("your questions", 28, MUTED, MEDIUM).next_to(ax.x_axis, DOWN, buff=0.15)
        lvls = [1, 2, 3, 2, 3, 3.6]; oks = [1, 1, 0, 1, 1, 1]
        pts = [ax.c2p(i + 1, v) for i, v in enumerate(lvls)]
        self.play(Create(ax), FadeIn(lab_y), FadeIn(lab_x), run_time=0.35)
        marks = VGroup(); segs = VGroup()
        t_s, t_e = wt(7, 3, 0.1), wt(7, 6, -0.1)
        for i, p_ in enumerate(pts):
            m = (check(0.2) if oks[i] else cross(0.2)).move_to(p_)
            anims = [FadeIn(m, scale=0.5)]
            if i: s_ = Line(pts[i - 1], p_, stroke_color=OR, stroke_width=6); segs.add(s_); anims.append(Create(s_))
            marks.add(m)
            self.until(t_s + (t_e - t_s) * i / 5); self.play(*anims, run_time=0.18)
        # mastery ring
        mc = np.array([X(300), Y(1210), 0])
        mr_bg = Circle(radius=0.95, stroke_color=SURF2, stroke_width=16).move_to(mc)
        mv = ValueTracker(0.01)
        mr = always_redraw(lambda: Arc(radius=0.95, start_angle=PI / 2, angle=-2 * PI * mv.get_value(), stroke_width=16).set_stroke(color=[OR, GOLD]).move_arc_center_to(mc))
        mpct = always_redraw(lambda: P(f"{int(round(mv.get_value() * 100))}%", 44, TXT).move_to(mc))
        topic = VGroup(P("Quadratics", 40, TXT), P("mastery", 30, MUTED, MEDIUM)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(mr_bg, RIGHT, buff=0.4)
        self.until(wt(7, 9, 0.1)); self.add(mr_bg, mr, mpct); self.play(FadeIn(topic), mv.animate.set_value(1.0), run_time=1.0, rate_func=smooth)
        unl = chip("Next topic unlocked  →", 36, INKD, GOLD).move_to([X(640), Y(1330), 0])
        self.until(wt(7, 13, 0.1)); self.play(FadeIn(unl, shift=RIGHT * 0.3), Flash(mc, color=GOLD, line_length=0.3, flash_radius=1.15), run_time=0.4)
        cal = VGroup(RoundedRectangle(width=1.1, height=1.15, corner_radius=0.12, fill_color=SURF2, fill_opacity=1, stroke_width=0),
                     Rectangle(width=1.1, height=0.28, fill_color=RED, fill_opacity=1, stroke_width=0)).move_to([X(890), Y(1150), 0])
        cal[1].align_to(cal[0], UP); calx = P("31", 40, TXT).move_to(cal[0].get_center() + DOWN * 0.1)
        strike = Line(cal.get_corner(UL) + UL * 0.08, cal.get_corner(DR) + DR * 0.08, stroke_color=OR, stroke_width=9)
        self.until(wt(7, 18, 0.15)); self.play(FadeIn(VGroup(cal, calx), scale=0.7), run_time=0.2)
        self.play(Create(strike), run_time=0.25)

        # ===== 8. Stuck at midnight? AI tutor 24/7. And expert teachers teach live. =====
        self.until(S[8])
        mr.clear_updaters(); mpct.clear_updaters()
        self.play(FadeOut(Group(ax, lab_x, lab_y, marks, segs, mr_bg, mr, mpct, topic, unl, cal, calx, strike)), run_time=0.25)
        night = glow(5.0, 760, BLUE)
        moon = Difference(Circle(radius=0.42), Circle(radius=0.38).shift(RIGHT * 0.22 + UP * 0.12), fill_color="#F4F1DE", fill_opacity=1, stroke_width=0).move_to([X(900), Y(330), 0])
        clock = D("11:58 PM", 84, grad=False, color=TXT).move_to([0, Y(330), 0])
        ph = Phone([0, Y(1010), 0], 0.98)
        bar_top = ph.top() - ph.p(130)
        av = Circle(radius=ph.p(34), fill_color=OR, fill_opacity=1, stroke_width=0).move_to([ph.screen.get_left()[0] + ph.p(80), bar_top, 0])
        avf = P("AI", 26, INKD).move_to(av)
        name = VGroup(P("AI Tutor", 34, TXT), P("online", 24, GREEN, MEDIUM)).arrange(DOWN, buff=0.04, aligned_edge=LEFT).next_to(av, RIGHT, buff=0.18)
        sep = Line([ph.screen.get_left()[0], bar_top - ph.p(62), 0], [ph.screen.get_right()[0], bar_top - ph.p(62), 0], stroke_color=LINE_C, stroke_width=2)
        def bubble(content, me, y):
            r = RoundedRectangle(width=content.width + ph.p(56), height=content.height + ph.p(40), corner_radius=ph.p(30),
                                 fill_color=(OR if me else SURF2), fill_opacity=1, stroke_width=0)
            b = VGroup(r, content.move_to(r))
            x = ph.screen.get_right()[0] - ph.p(30) - r.width / 2 if me else ph.screen.get_left()[0] + ph.p(30) + r.width / 2
            return b.move_to([x, y - r.height / 2, 0])
        b1 = bubble(VGroup(P("Why is the derivative", 36, INKD), VGroup(P("of", 36, INKD), MathTex(r"x^2", color=INKD, font_size=46 * 0.8), P("equal to", 36, INKD), MathTex(r"2x\,?", color=INKD, font_size=46 * 0.8)).arrange(RIGHT, buff=0.1)).arrange(DOWN, buff=0.08, aligned_edge=LEFT), True, sep.get_y() - ph.p(40))
        ans = VGroup(P("Step 1  Use the limit:", 32, TXT, MEDIUM), MathTex(r"\frac{(x+h)^2-x^2}{h}", color=TXT, font_size=46 * 0.8),
                     P("Step 2  Expand:", 32, TXT, MEDIUM), MathTex(r"=2x+h", color=TXT, font_size=46 * 0.8),
                     VGroup(P("Step 3  Let", 32, TXT, MEDIUM), MathTex(r"h\to 0:\ 2x", color=GOLD, font_size=46 * 0.8)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        b2 = bubble(ans, False, b1.get_bottom()[1] - ph.p(30))
        typing = bubble(VGroup(*[Dot(radius=ph.p(9), color=MUTED) for _ in range(3)]).arrange(RIGHT, buff=ph.p(12)), False, b1.get_bottom()[1] - ph.p(30))
        for k, d_ in enumerate(typing[1]): d_.add_updater(lambda m, k=k: m.set_opacity(0.3 + 0.7 * max(0, math.sin(T() * 8 - k))))
        inp = RoundedRectangle(width=ph.screen.width - ph.p(70), height=ph.p(84), corner_radius=ph.p(42), fill_color=SURF2, fill_opacity=1, stroke_width=0).move_to([0, ph.screen.get_bottom()[1] + ph.p(90), 0])
        inpt = P("Ask a doubt…", 32, MUTED, MEDIUM).move_to(inp).align_to(inp.get_left() + RIGHT * ph.p(36), LEFT)
        snd = Circle(radius=ph.p(30), fill_color=OR, fill_opacity=1, stroke_width=0).move_to(inp.get_right() + LEFT * ph.p(50))
        self.play(FadeIn(night), FadeIn(moon), FadeIn(clock, shift=DOWN * 0.2), FadeIn(ph, shift=UP * 0.8), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.add(av, avf, name, sep, inp, inpt, snd)
        self.until(wt(8, 3, 0.1)); self.play(FadeIn(b1, shift=UP * 0.25), run_time=0.25)
        self.add(typing)
        self.until(wt(8, 8, 0.15)); self.gone(typing)
        self.play(FadeIn(b2[0]), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in b2[1]], lag_ratio=0.25), run_time=0.9)
        tf = D("24/7", 200).move_to([0, Y(330), 0])
        self.until(wt(8, 12, 0.12)); self.play(FadeOut(clock, scale=0.7), FadeIn(tf, scale=1.3), run_time=0.3, rate_func=rush_from)
        # live teacher
        self.until(wt(8, 13, 0.2))
        tb = self.kb(plate("teacher"), T(), S[9], 1.0, 1.06, drift=(-0.2, 0)).set_z_index(-10)
        chat = Group(ph, av, avf, name, sep, b1, b2, inp, inpt, snd)
        self.play(FadeOut(Group(night, moon, tf)), chat.animate.shift(LEFT * 9.5), FadeIn(tb), run_time=0.4, rate_func=rush_into)
        self.remove(chat)
        dot = Dot(radius=px(13), color="#FF3B3B")
        live = VGroup(RoundedRectangle(width=px(190), height=px(64), corner_radius=px(32), fill_color=BG, fill_opacity=0.85, stroke_width=0),
                      VGroup(dot, P("LIVE", 34, WHITE)).arrange(RIGHT, buff=0.14)).move_to([X(150), Y(290), 0])
        live[1].move_to(live[0])
        self.until(wt(8, 16, 0.1)); self.play(FadeIn(live, shift=RIGHT * 0.2), run_time=0.25)
        dot.add_updater(lambda d: d.set_opacity(0.35 + 0.65 * (0.5 + 0.5 * math.cos(T() * 7))))

        # ===== 9. From Class 10 to university maths, from JEE and NEET to IELTS, all in one place. =====
        self.until(S[9])
        self.gone(dot)
        self.play(FadeOut(Group(tb, live)), run_time=0.3); tb.clear_updaters()
        hub = wordmark(px(420)).move_to([0, Y(860), 0]); hg = glow(3.4, 860)
        spots = {"Class 10": (230, 470), "Class 11": (540, 400), "Class 12": (850, 470), "University maths": (300, 1250),
                 "JEE": (820, 1180), "NEET": (900, 1320), "IELTS": (560, 1420)}
        cols = {"Class 10": SURF2, "Class 11": SURF2, "Class 12": SURF2, "University maths": BLUE_D, "JEE": GOLD, "NEET": GOLD, "IELTS": OR}
        fgs = {"University maths": WHITE, "JEE": INKD, "NEET": INKD, "IELTS": INKD}
        nd = {k: chip(k, 40, fgs.get(k, TXT), cols[k], stroke=(LINE_C if cols[k] == SURF2 else None)).move_to([X(x), Y(y), 0]) for k, (x, y) in spots.items()}
        self.play(FadeIn(hg), FadeIn(hub, scale=0.8), run_time=0.3)
        lines9 = VGroup()
        def pop(keys, t):
            self.until(t)
            hc = hub.get_center()
            ls = [Line(hc + 1.3 * normalize(nd[k].get_center() - hc), nd[k].get_center(), stroke_color=OR, stroke_width=3, stroke_opacity=0.6).set_z_index(-1) for k in keys]
            lines9.add(*ls)
            self.play(LaggedStart(*[FadeIn(nd[k], scale=0.6) for k in keys], lag_ratio=0.3), *[Create(l_) for l_ in ls], run_time=0.3 + 0.1 * (len(keys) - 1), rate_func=rate_functions.ease_out_back)
        pop(["Class 10", "Class 11", "Class 12"], wt(9, 2, 0.1)); pop(["University maths"], wt(9, 4, 0.05))
        pop(["JEE"], wt(9, 7, 0.1)); pop(["NEET"], wt(9, 9, 0.1)); pop(["IELTS"], wt(9, 11, 0.1))
        ring9 = Ellipse(width=5.9, height=6.6, stroke_color=GOLD, stroke_width=4, stroke_opacity=0.8).move_to(hub)
        self.until(wt(9, 13, 0.1))
        allg = VGroup(*nd.values())
        angs = {"Class 10": 145, "Class 11": 90, "Class 12": 35, "JEE": -15, "NEET": -60, "University maths": -120, "IELTS": 195}
        tgt = [hub.get_center() + np.array([2.95 * math.cos(math.radians(angs[k])), 3.3 * math.sin(math.radians(angs[k])), 0]) for k in nd]
        self.play(*[m.animate.move_to(p_) for m, p_ in zip(allg, tgt)], FadeOut(lines9), Create(ring9), hub.animate.scale(1.25), run_time=0.7, rate_func=smooth)


        # ===== 10. Real exam-pattern mocks. Free courses, games and tools. =====
        self.until(S[10])
        for c_ in allg: c_.clear_updaters()
        self.play(FadeOut(Group(hub, hg, allg, ring9)), run_time=0.25)
        ex = Phone([0, Y(930), 0], 0.92)
        L, R_, T0 = ex.screen.get_left()[0] + ex.p(36), ex.screen.get_right()[0] - ex.p(36), ex.top() - ex.p(110)
        title = VGroup(P("JEE Main", 40, TXT), P("· Full mock", 40, OR)).arrange(RIGHT, buff=0.12).move_to([0, T0, 0]).align_to([L, 0, 0], LEFT)
        t_ex = C[10]
        timer = always_redraw(lambda: P("Time left  {:02d}:{:02d}:{:02d}".format(*(lambda s: (s // 3600, s % 3600 // 60, s % 60))(max(0, int(10800 - max(0, T() - t_ex) * 41)))), 30, GOLD, MEDIUM).move_to([0, T0 - ex.p(58), 0]).align_to([L, 0, 0], LEFT))
        rows = VGroup(*[VGroup(P(a, 30, TXT, MEDIUM), P(b, 30, GREEN if "+" in b else MUTED, MEDIUM)).arrange(RIGHT, buff=0.3) for a, b in (("Marking", "+4 / −1"), ("Questions", "75  ·  3 hours"))]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(timer, DOWN, buff=0.3).align_to([L, 0, 0], LEFT)
        pal = VGroup(*[RoundedRectangle(width=ex.p(66), height=ex.p(66), corner_radius=ex.p(14), fill_color=SURF2, fill_opacity=1, stroke_width=0) for _ in range(36)])
        pal.arrange_in_grid(rows=6, cols=6, buff=ex.p(16)).move_to([0, ex.screen.get_center()[1] - ex.p(160), 0])
        rank = chip("Estimated rank  ↗", 34, INKD, GOLD).move_to([0, ex.screen.get_bottom()[1] + ex.p(90), 0])
        self.play(FadeIn(ex, shift=UP * 0.8), run_time=0.35, rate_func=rate_functions.ease_out_cubic)
        self.add(title, timer, rows, pal)
        rng = np.random.default_rng(9)
        self.play(LaggedStart(*[pal[i].animate.set_fill(GREEN if rng.random() < 0.78 else OR) for i in range(20)], lag_ratio=0.12), run_time=0.6)
        self.play(FadeIn(rank, shift=UP * 0.2), run_time=0.25)
        self.until(wt(10, 3, 0.15))
        timer.clear_updaters()
        self.play(Group(ex, title, timer, rows, pal, rank).animate.scale(0.55).move_to([X(270), Y(860), 0]), run_time=0.4, rate_func=smooth)
        frees = VGroup()
        for k, (s, y) in enumerate((("Courses", 560), ("Games", 860), ("Tools", 1160))):
            r = RoundedRectangle(width=px(470), height=px(220), corner_radius=0.3, fill_color=SURF, fill_opacity=1, stroke_color=LINE_C, stroke_width=2).move_to([X(760), Y(y), 0])
            t = P(s, 52, TXT).move_to(r.get_center() + UP * px(25) + LEFT * px(60))
            f = chip("FREE", 32, INKD, GOLD).move_to(r.get_center() + DOWN * px(55) + LEFT * px(115))
            frees.add(VGroup(r, t, f))
        for k, wi in enumerate((4, 5, 7)):
            self.until(wt(10, wi, 0.1)); self.play(FadeIn(frees[k], shift=LEFT * 0.4), run_time=0.25, rate_func=rate_functions.ease_out_cubic)

        # ===== 11. Not one-size-fits-all. Learning that adapts to you. =====
        self.until(S[11])
        self.play(FadeOut(Group(ex, title, timer, rows, pal, rank, frees)), FadeOut(head), run_time=0.25)
        osfa = D("ONE-SIZE-FITS-ALL", 66, grad=False, color=COLD).move_to([0, Y(820), 0])
        no = D("NOT", 66, grad=False, color=OR).next_to(osfa, UP, buff=0.3)
        st = Line(osfa.get_left() + LEFT * 0.1, osfa.get_right() + RIGHT * 0.1, stroke_color=OR, stroke_width=10)
        self.play(FadeIn(no), FadeIn(osfa), run_time=0.2)
        self.until(wt(11, 1, -0.2)); self.play(Create(st), run_time=0.3)
        hp = pick("hero", "calm")
        hero = self.kb(plate(hp), wt(11, 2, 0.2), S[12], 1.04, 1.0).set_z_index(-10)
        tag1 = D("LEARNING THAT", 84).move_to([0, Y(1180), 0]); tag2 = D("ADAPTS TO YOU.", 92).move_to([0, Y(1310), 0])
        self.until(wt(11, 2, 0.2)); self.play(FadeOut(VGroup(no, osfa, st)), FadeIn(hero), run_time=0.35)
        self.play(FadeIn(tag1, shift=UP * 0.3), run_time=0.3)
        self.until(wt(11, 4, 0.1)); self.play(FadeIn(tag2, shift=UP * 0.3), run_time=0.3)

        # ===== 12. TutorDA. Start free at tutorda.org =====
        self.until(S[12])
        self.play(FadeOut(Group(tag1, tag2)), hero.animate.set_opacity(0.0), run_time=0.35); self.gone(hero)
        wm2 = wordmark(px(800)).move_to([0, Y(760), 0]); g2 = glow(5.0, 760)
        self.play(FadeIn(g2, scale=0.6), FadeIn(wm2, scale=1.12), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        sf = D("START FREE", 84).move_to([0, Y(950), 0]); url = glow_pill("tutorda.org", 80).move_to([0, Y(1110), 0])
        self.until(wt(12, 1, 0.1)); self.play(FadeIn(sf, shift=UP * 0.25), run_time=0.3)
        self.until(wt(12, 4, 0.15)); self.play(FadeIn(url, scale=0.7), run_time=0.3, rate_func=rate_functions.ease_out_back)
        self.play(ShowPassingFlash(url[0].copy().set_fill(opacity=0).set_stroke(WHITE, 8), time_width=0.5), run_time=0.6)

        # ===== END CARD =====
        self.until(S[13])
        tagl = P("Learning that adapts to you.", 46, TXT, MEDIUM).move_to([0, Y(950), 0])
        fol = D("FOLLOW TUTORDA", 56).move_to([0, Y(1240), 0])
        self.play(FadeOut(sf), url.animate.move_to([0, Y(1090), 0]).scale(0.85), FadeIn(tagl, shift=UP * 0.2), run_time=0.4)
        self.play(FadeIn(fol, shift=UP * 0.2), run_time=0.35)
        self.until(K.DUR)
