"""TutorDA introduction reel (Manim). Everything TutorDA offers, in ~32 s, current voice.
Facts used are all from tutorda.org: Class 10-12 interactive courses (Maths/Physics/Chemistry, labs, worked solutions),
adaptive practice with step-by-step answers, mock tests (Mock 1 free), maths games and free tools, institution partnerships.
No unverified statistics.
Render: tools/manim_build.sh engine/manim_intro.py Intro intro out/intro.mp4 [draft]"""
import os, sys
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
import intro as K
from manim_common import *

LOGO = os.path.join(KIT, "out", "_logo.png")

def tile(icon, label, tint, w=3.4, h=2.4):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.3, fill_color=tint, fill_opacity=1, stroke_width=0)
    icon.move_to(box.get_center() + UP * 0.32)
    lab = T(label, 50).move_to(box.get_center() + DOWN * 0.72)
    return VGroup(box, icon, lab)

def icon_maths(): return M(r"\int\! \pi", 84, NAVY)
def icon_science():
    g = VGroup(*[Ellipse(width=1.3, height=0.46, stroke_color=TEAL_D, stroke_width=6).rotate(a) for a in (0, PI / 3, -PI / 3)])
    return g.add(Dot(radius=0.09, color=TEAL_D))
def icon_exams():
    board = RoundedRectangle(width=0.95, height=1.2, corner_radius=0.1, stroke_color=AMBER_D, stroke_width=6)
    lines = VGroup(*[Line(LEFT * 0.28, RIGHT * 0.12, stroke_color=AMBER_D, stroke_width=5).shift(UP * (0.25 - 0.22 * i) + RIGHT * 0.05) for i in range(3)])
    tick = VMobject(stroke_color=TEAL_D, stroke_width=8).set_points_as_corners([[-0.3, -0.38, 0], [-0.12, -0.52, 0], [0.32, -0.12, 0]])
    clip = RoundedRectangle(width=0.42, height=0.16, corner_radius=0.05, fill_color=AMBER_D, fill_opacity=1, stroke_width=0).move_to(UP * 0.6)
    return VGroup(board, lines, tick, clip)
def icon_english(): return T("Aa", 96, RED)

def icon_school():
    body = Rectangle(width=1.2, height=0.75, stroke_color=NAVY, stroke_width=6).shift(DOWN * 0.15)
    roof = Polygon([-0.75, 0.23, 0], [0.75, 0.23, 0], [0, 0.72, 0], stroke_color=NAVY, stroke_width=6)
    door = Rectangle(width=0.26, height=0.38, fill_color=NAVY, fill_opacity=1, stroke_width=0).shift(DOWN * 0.33)
    return VGroup(body, roof, door)
def icon_college():
    top = Polygon([0, 0.45, 0], [0.8, 0.12, 0], [0, -0.2, 0], [-0.8, 0.12, 0], fill_color=NAVY, fill_opacity=1, stroke_width=0)
    cap = Arc(radius=0.45, start_angle=PI + 0.3, angle=PI - 0.6, stroke_color=NAVY, stroke_width=6).shift(DOWN * 0.05)
    tassel = Line([0.55, 0.05, 0], [0.55, -0.45, 0], stroke_color=AMBER, stroke_width=6)
    return VGroup(cap, top, tassel)
def icon_coaching():
    board = RoundedRectangle(width=1.3, height=0.85, corner_radius=0.08, fill_color=TEAL_D, fill_opacity=1, stroke_width=0)
    sym = T("+ − × ÷", 34, WHITE).move_to(board)
    legs = VGroup(Line([-0.4, -0.43, 0], [-0.55, -0.75, 0]), Line([0.4, -0.43, 0], [0.55, -0.75, 0])).set_stroke(NAVY, 6)
    return VGroup(board, sym, legs)

def chip(s, size=40, fg=INK, bg=TINT_N, w=None):
    t = T(s, size, fg)
    r = RoundedRectangle(width=w or t.width + 0.5, height=t.height + 0.32, corner_radius=0.18, fill_color=bg, fill_opacity=1, stroke_width=0)
    return VGroup(r, t.move_to(r))

def card(w, h, title):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.25, fill_color="#F8FAFC", fill_opacity=1, stroke_color="#CBD5E1", stroke_width=2.5)
    ttl = T(title, 40, INK).move_to(box.get_top() + DOWN * 0.38)
    return VGroup(box, ttl)

class Intro(ReelScene):
    K = K
    def leave(self, group, t):
        self.until(t); self.play(FadeOut(group, shift=LEFT * 0.5), run_time=0.3, rate_func=rush_into)

    def construct(self):
        header = self.setup_ui("MATHS  ·  SCIENCE  ·  EXAMS  ·  ENGLISH", LOGO)
        C, wt = K.C, K.wt

        # ===== A: four worlds -> one place (frame 0 shows the four tiles) =====
        tiles = VGroup(tile(icon_maths(), "Maths", TINT_N), tile(icon_science(), "Science", TINT_T),
                       tile(icon_exams(), "Exams", TINT_Y), tile(icon_english(), "English", TINT_R))
        for tl, (x, y) in zip(tiles, ((X(343), Y(625)), (X(737), Y(625)), (X(343), Y(955)), (X(737), Y(955)))): tl.move_to([x, y, 0])
        for tl in tiles: tl.set_opacity(0.55)  # readable on frame 0; each lights up fully on its word
        self.add(tiles)
        for k, wi in enumerate((0, 1, 2, 4)):
            self.until(wt(0, wi, 0.08)); self.play(tiles[k].animate.set_opacity(1).scale(1.08), run_time=0.18)
            self.play(tiles[k].animate.scale(1 / 1.08), run_time=0.14)
        big = ImageMobject(LOGO).scale_to_fit_height(px(150)).move_to([0, Y(760), 0])
        one = T("All in one place", 64).move_to([0, Y(930), 0])
        self.until(wt(0, 5, 0.12))
        self.play(tiles.animate.scale(0.25).move_to([0, Y(760), 0]).set_opacity(0), run_time=0.45, rate_func=smooth)
        self.play(FadeIn(big, scale=0.6), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(one, shift=UP * 0.15), run_time=0.3)
        self.leave(Group(big, one), K.SCENES[0])

        # ===== B: interactive courses =====
        ttl = T("Interactive courses", 64).move_to([0, Y(330), 0])
        cols = VGroup()
        for j, (cls, x) in enumerate((("Class 10", X(255)), ("Class 11", X(540)), ("Class 12", X(825)))):
            head = pill(cls, 42, WHITE, NAVY, padx=0.25, pady=0.12).move_to([x, Y(470), 0])
            subs = VGroup(*[chip(s, 40, INK, TINT_Y if s == "Maths" else (TINT_T if s == "Physics" else TINT_R), w=px(262)).move_to([x, Y(570 + 95 * i), 0])
                            for i, s in enumerate(("Maths", "Physics", "Chemistry"))])
            cols.add(VGroup(head, subs))
        self.play(FadeIn(ttl, shift=UP * 0.15), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.2), run_time=0.55)
        # "Class 10, 11 and 12": one lagged pulse across the three headers, timed to the spoken numbers
        t4, t7 = wt(1, 4, 0.08), wt(1, 7, 0.08); self.until(t4)
        self.play(LaggedStart(*[cols[j][0].animate(rate_func=there_and_back).scale(1.12) for j in range(3)],
                              lag_ratio=0.5),
                  run_time=min(0.9, t7 - t4 + 0.25))
        labc = card(px(415), px(340), "Live labs").move_to([X(310), Y(1080), 0])
        solc = card(px(415), px(340), "Worked solutions").move_to([X(735), Y(1080), 0])
        ax = Axes(x_range=[0, 6.3, 1], y_range=[-1.2, 1.2, 1], x_length=px(340), y_length=px(150), tips=False,
                  axis_config={"stroke_color": INK2, "stroke_width": 2, "include_ticks": False}).move_to(labc[0].get_center() + DOWN * 0.12)
        amp = ValueTracker(0.45)
        wave = always_redraw(lambda: ax.plot(lambda x: amp.get_value() * math.sin(x), color=TEAL_D, stroke_width=6))
        sl_y = labc[0].get_bottom()[1] + px(42); sl_x0, sl_x1 = labc[0].get_left()[0] + px(70), labc[0].get_right()[0] - px(70)
        track_ = Line([sl_x0, sl_y, 0], [sl_x1, sl_y, 0], stroke_color="#CBD5E1", stroke_width=6)
        knob = always_redraw(lambda: Dot([sl_x0 + (sl_x1 - sl_x0) * (amp.get_value() - 0.3) / 0.7, sl_y, 0], radius=px(15), color=AMBER))
        s0 = solc[0].get_center()
        steps = VGroup(M(r"x^2-5x+6=0", 40), M(r"(x-2)(x-3)=0", 40), M(r"x=2,\;3", 40)).arrange(DOWN, buff=0.16).move_to(s0 + DOWN * 0.3)
        tick = VMobject(stroke_color=TEAL_D, stroke_width=8).set_points_as_corners([[-0.14, 0, 0], [-0.02, -0.12, 0], [0.2, 0.14, 0]]).next_to(steps[2], RIGHT, buff=0.15)
        self.until(wt(1, 9, 0.12)); self.play(FadeIn(labc, shift=UP * 0.15), Create(ax), FadeIn(track_), run_time=0.35)
        self.add(knob); self.play(Create(wave), run_time=0.4)
        self.until(wt(1, 12, 0.12)); self.play(FadeIn(solc, shift=UP * 0.15), LaggedStart(*[Write(s) for s in steps], lag_ratio=0.3),
                                               amp.animate(rate_func=smooth).set_value(1.0), run_time=0.75)  # the lab slider moves, the graph responds
        self.play(Create(tick), run_time=0.22)
        wave.clear_updaters(); knob.clear_updaters()
        self.leave(VGroup(ttl, cols, labc, solc, ax, wave, track_, knob, steps, tick), K.SCENES[1])

        # ===== C: adaptive practice =====
        qbox = RoundedRectangle(width=px(820), height=px(170), corner_radius=0.25, fill_color=TINT_N, fill_opacity=1, stroke_width=0).move_to([0, Y(440), 0])
        q = VGroup(T("Solve", 52, INK2), M(r"2x+3=11", 76)).arrange(RIGHT, buff=0.35).move_to(qbox)
        lvl_lab = T("Level", 42, INK2).move_to([X(185), Y(630), 0])
        segs = VGroup(*[RoundedRectangle(width=px(195), height=px(62), corner_radius=0.22, fill_color="#E2E8F0", fill_opacity=1, stroke_width=0) for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to([X(615), Y(630), 0])
        seg_l = VGroup(*[T(s, 34, INK).move_to(sg) for s, sg in zip(("Easy", "Medium", "Hard"), segs)]).set_z_index(2)
        for l in seg_l: l.align_to(seg_l[1], UP)  # same cap line ("Easy" has a descender)
        self.play(FadeIn(qbox, shift=UP * 0.15), FadeIn(q, shift=UP * 0.15), FadeIn(VGroup(lvl_lab, segs, seg_l)), run_time=0.35)
        self.until(wt(2, 2, 0.1))
        fills = [segs[i].copy().set_fill(c) for i, c in enumerate((TEAL, YEL, AMBER))]
        self.play(LaggedStart(*[Transform(segs[i], fills[i]) for i in range(3)], lag_ratio=0.45), run_time=0.8)
        # equations aligned on "=", step labels in one left-aligned column
        sol = VGroup(*[MathTex(a, "=", b, color=c, font_size=f * 0.8) for a, b, c, f in
                       (("2x", "11-3", INK, 78), ("2x", "8", INK, 78), ("x", "4", NAVY, 88))]).arrange(DOWN, buff=0.45)
        for e in sol: e.shift(RIGHT * (X(470) - e[1].get_center()[0]))
        sol.shift(UP * (Y(950) - sol.get_center()[1]))
        nums = VGroup(*[T(f"Step {i+1}", 38, AMBER_D) for i in range(3)])
        for n, e in zip(nums, sol): n.move_to([0, e[1].get_center()[1], 0]).align_to([X(150), 0, 0], LEFT)
        self.until(wt(2, 6, 0.12)); self.play(LaggedStart(*[AnimationGroup(FadeIn(n), Write(s)) for n, s in zip(nums, sol)], lag_ratio=0.35), run_time=0.75)
        ok = Circle(radius=0.32, fill_color=TEAL_D, fill_opacity=1, stroke_width=0).next_to(sol[2], RIGHT, buff=0.4)
        okt = VMobject(stroke_color=WHITE, stroke_width=8).set_points_as_corners([[-0.13, 0, 0], [-0.03, -0.11, 0], [0.15, 0.12, 0]]).move_to(ok)
        self.until(wt(2, 7, 0.1)); self.play(FadeIn(VGroup(ok, okt), scale=0.6), Indicate(sol[2], color=TEAL_D, scale_factor=1.12), run_time=0.45)
        self.leave(VGroup(qbox, q, lvl_lab, segs, seg_l, sol, nums, ok, okt), K.SCENES[2])

        # ===== D: mock tests =====
        ttl = T("Mock tests", 64).move_to([0, Y(330), 0])
        bigc = [chip(s, 52, NAVY, TINT_N, w=px(390)) for s in ("JEE Main", "NEET-UG", "IELTS", "PTE")]
        for c_, (x, y) in zip(bigc, ((X(320), Y(500)), (X(760), Y(500)), (X(320), Y(615)), (X(760), Y(615)))): c_.move_to([x, y, 0])
        more = VGroup(*[chip(s, 34, INK2, "#F1F5F9", w=px(195)) for s in ("GATE", "CSIR-NET", "SAT", "TOEFL", "Duolingo", "GRE", "GMAT", "TNPSC")])
        more.arrange_in_grid(rows=2, cols=4, buff=(0.15, 0.15)).move_to([0, Y(790), 0])
        self.play(FadeIn(ttl, shift=UP * 0.15), run_time=0.35)
        for c_, wi in zip(bigc, (3, 4, 5, 6)):
            self.until(wt(3, wi, 0.12)); self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.3)
        self.until(wt(3, 8, 0.15)); self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in more], lag_ratio=0.12), run_time=0.6)
        free = pill("Mock 1  FREE", 76, NAVY, YEL, padx=0.45, pady=0.22, stroke=AMBER_D).rotate(-0.07).move_to([0, Y(1050), 0])
        note = T("for every exam", 40, INK2).move_to([0, Y(1165), 0])
        self.until(wt(3, 10, 0.1)); self.play(FadeIn(free, scale=0.5), run_time=0.45, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.25)
        self.leave(VGroup(ttl, *bigc, more, free, note), K.SCENES[3])

        # ===== E: games and free tools =====
        gl = T("Maths games", 64).move_to([0, Y(330), 0])
        games = VGroup(*[chip(s, 40, INK, c, w=px(390)) for s, c in (("Math Sprint", TINT_Y), ("Algebra Escape", TINT_T), ("Times Table Blitz", TINT_N), ("Sudoku", TINT_R))])
        games.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.18)).move_to([0, Y(480), 0])
        tl_ = T("Free tools", 64).move_to([0, Y(680), 0])
        ax2 = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2], x_length=px(560), y_length=px(380), tips=False,
                   axis_config={"stroke_color": INK2, "stroke_width": 2.5, "include_ticks": False}).move_to([0, Y(1000), 0])
        par = ax2.plot(lambda x: x * x, x_range=[-2.9, 2.9], color=AMBER_D, stroke_width=7)
        fl = M(r"y = x^2", 52, AMBER_D).move_to(ax2.c2p(0, 6.2))
        gp = T("Graph plotter", 36, INK2).next_to(ax2, DOWN, buff=0.15)
        self.play(FadeIn(gl, shift=UP * 0.15), run_time=0.3)
        self.until(wt(4, 1, 0.1)); self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in games], lag_ratio=0.15), run_time=0.5)
        self.until(wt(4, 4, 0.1)); self.play(FadeIn(tl_, shift=UP * 0.15), run_time=0.3)
        self.until(wt(4, 6, 0.1)); self.play(games[2].animate.scale(1.1), rate_func=there_and_back, run_time=0.4)
        self.until(wt(4, 9, 0.25)); self.play(Create(ax2), FadeIn(gp), run_time=0.25)
        self.play(Create(par), FadeIn(fl), run_time=0.5)
        self.leave(VGroup(gl, games, tl_, ax2, par, fl, gp), K.SCENES[4])

        # ===== F: institutions =====
        ttl = T("For institutions", 64).move_to([0, Y(330), 0])
        ins = []
        for (ic, lab, x) in ((icon_school(), "Schools", X(255)), (icon_college(), "Colleges", X(540)), (icon_coaching(), "Coaching\ncentres", X(825))):
            box = RoundedRectangle(width=px(262), height=px(270), corner_radius=0.25, fill_color=TINT_N, fill_opacity=1, stroke_width=0).move_to([x, Y(620), 0])
            ic.scale(1.25)
            ic.move_to(box)
            lb = Text(lab, font="Poppins", weight=BOLD, color=INK, font_size=42 * 0.6, line_spacing=0.8).move_to([x, Y(840), 0])
            ins.append(VGroup(box, ic, lb))
        self.until(wt(5, 0, 0.05)); self.play(FadeIn(ttl, shift=UP * 0.15), FadeIn(ins[0], shift=UP * 0.2), run_time=0.3)
        for g, wi in zip(ins[1:], (1, 3)):
            self.until(wt(5, wi, 0.1)); self.play(FadeIn(g, shift=UP * 0.2), run_time=0.3)
        pp = pill("Partner with TutorDA", 60, NAVY, YEL, padx=0.4, pady=0.2).move_to([0, Y(1040), 0])
        offer = VGroup(T("Course content  ·  AI maths tutor", 38, INK2), T("Student information system", 38, INK2)).arrange(DOWN, buff=0.14).move_to([0, Y(1175), 0])
        self.until(wt(5, 6, 0.12)); self.play(FadeIn(pp, shift=UP * 0.2), run_time=0.35)
        self.play(FadeIn(offer), run_time=0.3)
        self.leave(VGroup(ttl, *ins, pp, offer), K.SCENES[5])

        # ===== G: call to action =====
        s1 = T("Start free", 128).move_to([0, Y(600), 0])
        s2 = T("today", 88, AMBER_D).move_to([0, Y(745), 0])
        site = pill("tutorda.org", 88, NAVY, YEL, padx=0.5, pady=0.25).move_to([0, Y(950), 0])
        perks = T("Free games  ·  Free tools  ·  Mock 1 free", 40, INK2).move_to([0, Y(1100), 0])
        self.play(Write(s1), run_time=0.45)
        self.until(wt(6, 2, 0.1)); self.play(FadeIn(s2, shift=UP * 0.15), run_time=0.3)
        self.until(wt(6, 4, 0.2)); self.play(FadeIn(site, scale=0.8), run_time=0.35)
        self.play(ShowPassingFlash(site[0].copy().set_fill(opacity=0).set_stroke(AMBER_D, 9), time_width=0.6), FadeIn(perks), run_time=0.7)
        self.until(K.SCENES[6])
        self.play(FadeOut(VGroup(s1, s2, site, perks)), FadeOut(header), run_time=0.3)

        # ===== END CARD =====
        big_logo = ImageMobject(LOGO).scale_to_fit_height(px(76 * 1.75)).move_to([0, Y(800), 0])
        f1 = T("Follow TutorDA", 60).move_to([0, Y(960), 0])
        f2 = T("Maths  ·  Science  ·  Exams  ·  English", 40, AMBER_D).move_to([0, Y(1045), 0])
        f3 = pill("www.tutorda.org", 58, NAVY, YEL, padx=0.4, pady=0.2).move_to([0, Y(1190), 0])
        self.play(FadeIn(big_logo, scale=0.85), run_time=0.4, rate_func=rush_from)
        self.play(LaggedStart(FadeIn(f1, shift=UP * 0.15), FadeIn(f2, shift=UP * 0.15), FadeIn(f3, scale=0.9), lag_ratio=0.25), run_time=0.6)
        self.until(K.DUR)
