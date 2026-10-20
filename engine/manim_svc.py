"""TutorDA products & services reel (~32 s). Same editorial system as the brand film (manim_film2): paper / ink grounds,
one orange accent, Poppins + Instrument Serif italic, panel wipes, ink caption band. A numbered index (01-06) opens the
reel and each product scene carries its number top-right, so the reel reads as a guided tour, not a list of claims.
Render: FILM_AUDIO=svc tools/manim_build.sh engine/manim_svc.py Svc svc out/svc.mp4 [draft]"""
import os, sys, json, math
os.environ.setdefault("FILM_AUDIO", "svc")
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
from manim_film2 import *          # helpers, palette, Phone, Film2 (ground / rise / captions / kb / ev)
import manim_film2 as F

PRODUCTS = ["AI tutor", "Live classes", "Exam mocks", "English tests", "Games & tools", "For institutions"]

class Svc(F.Film2):
    def chapter(self, n, dark):
        g = VGroup(B(f"{n:02d}", 40, OR, SEMIBOLD), B(PRODUCTS[n - 1], 40, GREY_I if dark else GREY_P, SEMIBOLD)).arrange(RIGHT, buff=0.16)
        g.move_to([0, Y(118), 0]).align_to([X(984), 0, 0], RIGHT); g.set_z_index(12)
        return g

    def construct(self):
        C, wt = K.C, K.wt
        S = [c - 0.25 for c in C]
        T = lambda: self.renderer.time
        self._ground = Rectangle(width=9.2, height=16.4, fill_color=PAPER, fill_opacity=1, stroke_width=0).set_z_index(-20); self.add(self._ground)
        self.captions()
        hdr = wordmark(px(250)); left(hdr.move_to([0, Y(118), 0])); hdr.set_z_index(12)
        hdr_d = wordmark(px(250), dark=True); left(hdr_d.move_to([0, Y(118), 0])); hdr_d.set_z_index(12)

        # ===== 0. Everything you need to learn. In one place. (paper, index) — headline visible on frame 0 =====
        self.add(hdr)
        h1 = at(H("Everything you", 104, INK), 330); h2 = at(H("need to learn.", 104, INK), 450)
        self.add(h1, h2)
        rows = []
        for k, name in enumerate(PRODUCTS):
            y = 790 + k * 112
            num = B(f"{k + 1:02d}", 34, OR, SEMIBOLD); num.move_to([0, Y(y), 0]).align_to([X(96), 0, 0], LEFT)
            nm = H(name, 54, INK, BOLD); nm.move_to([0, Y(y), 0]).align_to([X(190), 0, 0], LEFT)
            rl = Line([X(96), Y(y + 52), 0], [X(984), Y(y + 52), 0], stroke_color=RULE, stroke_width=3)
            rows.append(VGroup(num, nm, rl))
        self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.25) for r_ in rows], lag_ratio=0.16), run_time=1.15, rate_func=EXPO)
        one = at(SER("in one place.", 140, OR), 600)
        self.until(wt(0, 5, 0.1)); self.ev("tick"); self.rise(one, rt=0.4)

        # ===== 1. AI tutor: clears your doubts, step by step, 24/7 (ink, chat) =====
        self.until(S[1])
        self.ground(INK, UP, 0.4); self.remove(h1, h2, one, *rows)
        self.remove(hdr); self.add(hdr_d); ch = self.chapter(1, True); self.add(ch)
        ttl = at(H("AI tutor", 96, WHITE_), 300)
        ph = Phone([X(540), Y(1000), 0], 0.92, screen="#121A2E")
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
        b1 = bubble(VGroup(B("How do I solve", 36, WHITE_), MathTex(r"x^2-5x+6=0\,?", color=WHITE_, font_size=46 * 0.8)).arrange(DOWN, buff=0.1, aligned_edge=LEFT), True, sp.get_y() - ph.p(40))
        ans = VGroup(B("Step 1  Product 6, sum −5", 28, "#C9CFDD"), MathTex(r"-2,\ -3", color=WHITE_, font_size=46 * 0.8),
                     B("Step 2  Factorise", 30, "#C9CFDD"), MathTex(r"(x-2)(x-3)=0", color=WHITE_, font_size=46 * 0.8),
                     VGroup(B("Step 3  So", 30, "#C9CFDD"), MathTex(r"x=2\ \text{or}\ 3", color=OR, font_size=46 * 0.8)).arrange(RIGHT, buff=0.14)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        b2 = bubble(ans, False, b1.get_bottom()[1] - ph.p(28))
        dots = VGroup(*[Dot(radius=ph.p(9), color=GREY_I) for _ in range(3)]).arrange(RIGHT, buff=ph.p(12))
        typing = bubble(dots, False, b1.get_bottom()[1] - ph.p(28))
        for k, d_ in enumerate(typing[1]): d_.add_updater(lambda m, k=k: m.set_opacity(0.3 + 0.7 * max(0, math.sin(T() * 8 - k))))
        inp = RoundedRectangle(width=ph.screen.width - ph.p(64), height=ph.p(84), corner_radius=ph.p(42), fill_color="#222C45", fill_opacity=1, stroke_width=0).move_to([X(540), ph.screen.get_bottom()[1] + ph.p(88), 0])
        inpt = B("Ask a doubt…", 30, GREY_I).move_to(inp).align_to(inp.get_left() + RIGHT * ph.p(34), LEFT)
        self.rise(ttl, rt=0.3)
        self.play(FadeIn(ph, shift=UP * 0.7), run_time=0.4, rate_func=EXPO); self.add(av, avt, nm, sp, inp, inpt)
        self.until(wt(1, 4, 0.1)); self.ev("tick"); self.play(FadeIn(b1, shift=UP * 0.2), run_time=0.25)
        self.add(typing)
        self.until(wt(1, 7, 0.15)); self.gone(typing)
        self.play(FadeIn(b2[0]), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in b2[1]], lag_ratio=0.25), run_time=0.8)
        tf = at(H("24/7", 130, OR), 300)
        self.until(wt(1, 10, 0.12)); self.ev("tick"); self.play(FadeOut(ttl, shift=UP * 0.3), FadeIn(tf, shift=UP * 0.3), run_time=0.3, rate_func=EXPO)

        # ===== 2. Live classes with expert teachers (full-bleed photo) =====
        self.until(S[2])
        self.ground(INK, UP, 0.4); self.remove(ph, av, avt, nm, sp, b1, b2, inp, inpt, tf, ch)
        ch = self.chapter(2, True); self.add(ch, hdr_d)
        tp = photo("teacher", "ed", 1080, BAND_TOP, 0.42).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        shade = Rectangle(width=9.2, height=px(560), fill_color=INK, fill_opacity=0.6, stroke_width=0).set_z_index(-4)
        shade.move_to([0, Y(BAND_TOP) + px(280), 0])
        top_sh = Rectangle(width=9.2, height=px(230), fill_color=INK, fill_opacity=0.55, stroke_width=0).set_z_index(-4).move_to([0, Y(115), 0])
        self.play(FadeIn(tp), FadeIn(shade), FadeIn(top_sh), run_time=0.3)
        self.kb(tp, T(), S[3], 1.0, 1.05)
        rd = Dot(radius=px(12), color="#FF3B3B")
        live = VGroup(RoundedRectangle(width=px(176), height=px(60), corner_radius=0.12, fill_color=INK, fill_opacity=0.9, stroke_width=0),
                      VGroup(rd, B("Live", 32, WHITE_, SEMIBOLD)).arrange(RIGHT, buff=0.14))
        live[1].move_to(live[0]); left(live.move_to([0, Y(270), 0]))
        rd.add_updater(lambda d: d.set_opacity(0.35 + 0.65 * (0.5 + 0.5 * math.cos(T() * 7))))
        g1 = at(H("Live classes", 92, WHITE_), 1250); g2 = at(SER("with expert teachers.", 112, "#FFB27A"), 1390)
        self.rise(live, g1, rt=0.4)
        self.until(wt(2, 3, 0.1)); self.rise(g2, rt=0.4)

        # ===== 3-4. Real exam-pattern mocks ... first mock of every exam is free (ink, exam phone + exam list) =====
        self.until(S[3])
        self.gone(rd); tp.clear_updaters()
        self.ground(INK, UP, 0.4); self.remove(tp, shade, top_sh, live, g1, g2, ch)
        ch = self.chapter(3, True); self.add(ch, hdr_d)
        ex = Phone([X(300), Y(900), 0], 0.78, screen="#121A2E")
        L_, T0 = ex.screen.get_left()[0] + ex.p(36), ex.top() - ex.p(110)
        et = VGroup(B("JEE Main", 40, WHITE_, SEMIBOLD), B("Mock 1", 40, OR, SEMIBOLD)).arrange(RIGHT, buff=0.14).move_to([0, T0, 0]).align_to([L_, 0, 0], LEFT)
        t_ex = C[3]
        tmr = always_redraw(lambda: B("Time left  {:02d}:{:02d}:{:02d}".format(*(lambda s: (s // 3600, s % 3600 // 60, s % 60))(max(0, int(10800 - max(0, T() - t_ex) * 41)))), 30, GREY_I).move_to([0, T0 - ex.p(56), 0]).align_to([L_, 0, 0], LEFT))
        info = VGroup(*[VGroup(B(a, 30, "#C9CFDD"), B(b, 30, WHITE_, SEMIBOLD)).arrange(RIGHT, buff=0.3) for a, b in (("Marking", "+4 / −1"), ("Pattern", "Real exam"))]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        info.next_to(tmr, DOWN, buff=0.3).align_to([L_, 0, 0], LEFT)
        pal = VGroup(*[RoundedRectangle(width=ex.p(66), height=ex.p(66), corner_radius=ex.p(12), fill_color="#222C45", fill_opacity=1, stroke_width=0) for _ in range(36)])
        pal.arrange_in_grid(rows=6, cols=6, buff=ex.p(16)).move_to([ex.screen.get_center()[0], ex.screen.get_center()[1] - ex.p(150), 0])
        ttl3 = at(H("Real exam-pattern mocks", 64, WHITE_), 300)
        if ttl3.width > px(888): ttl3.scale_to_fit_width(px(888)); left(ttl3)
        self.rise(ttl3, rt=0.3)
        self.play(FadeIn(ex, shift=UP * 0.6), run_time=0.35, rate_func=EXPO)
        self.add(et, tmr, info, pal)
        rng = np.random.default_rng(9)
        self.play(LaggedStart(*[pal[i].animate.set_fill(OR if rng.random() < 0.8 else "#4C5A7A") for i in range(20)], lag_ratio=0.1), run_time=0.6)
        exams = [("JEE Main", 4), ("NEET-UG", 5), ("GATE", 6), ("CSIR-NET", 8), ("SAT · GRE · GMAT", 8), ("TNPSC", 8)]
        chips = []
        for k, (s_, wi) in enumerate(exams):
            t_ = B(s_, 36, WHITE_, SEMIBOLD)
            r_ = RoundedRectangle(width=px(400), height=px(86), corner_radius=0.14, fill_color=INK2, fill_opacity=1, stroke_width=0)
            g_ = VGroup(r_, t_.move_to(r_).align_to(r_.get_left() + RIGHT * px(30), LEFT)).move_to([X(784), Y(500 + k * 112), 0])
            chips.append((wi, g_))
        done = set()
        for wi in (4, 5, 6, 8):
            self.until(wt(3, wi, 0.1)); self.ev("tick")
            grp = [g for w_, g in chips if w_ == wi]
            self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.35) for g in grp], lag_ratio=0.2), run_time=0.3 + 0.08 * len(grp), rate_func=EXPO)
        # first mock of every exam is free — the one spring moment
        stamp = VGroup(RoundedRectangle(width=px(400), height=px(190), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0),
                       VGroup(B("Every exam", 34, WHITE_, SEMIBOLD), H("Mock 1 free", 56, WHITE_)).arrange(DOWN, buff=0.08))
        stamp[1].move_to(stamp[0]); stamp.rotate(-4 * DEGREES).move_to([X(784), Y(1300), 0])
        self.until(wt(4, 8, 0.12)); self.ev("stamp")
        self.play(GrowFromCenter(stamp), run_time=0.45, rate_func=rate_functions.ease_out_back)

        # ===== 5. IELTS, PTE, TOEFL and Duolingo practice (paper, photo + type grid) =====
        self.until(S[5] - 0.1)
        self.gone(tmr)
        self.ground(PAPER, UP, 0.36); self.remove(ex, et, tmr, info, pal, ttl3, stamp, *[g for _, g in chips], ch)
        self.remove(hdr_d); self.add(hdr); ch = self.chapter(4, False); self.add(ch)
        ep = photo("english", "ed", 1080, 860, 0.36).move_to([0, Y(200 + 430), 0]).set_z_index(-5)
        cells = [("IELTS", 0, 96, 1170), ("PTE", 1, 560, 1170), ("TOEFL", 2, 96, 1330), ("Duolingo", 4, 560, 1330)]
        rl5 = [Line([X(96), Y(y), 0], [X(984), Y(y), 0], stroke_color=RULE, stroke_width=3) for y in (1245, 1405)]
        tx = []
        for s_, wi, x, y in cells:
            t_ = H(s_, 88, INK); t_.move_to([0, Y(y), 0]).align_to([X(x), 0, 0], LEFT); tx.append(t_)
        self.ev("tick")
        self.play(FadeIn(ep, shift=UP * 0.3), *[Create(r_) for r_ in rl5], FadeIn(tx[0], shift=UP * 0.3), run_time=0.35, rate_func=EXPO)
        self.kb(ep, T(), S[6], 1.0, 1.04)
        for (s_, wi, x, y), t_ in list(zip(cells, tx))[1:]:
            self.until(wt(5, wi, 0.1)); self.ev("tick"); self.play(FadeIn(t_, shift=UP * 0.3), run_time=0.28, rate_func=EXPO)
        cells = tx
        lab5 = B("English test practice", 40, GREY_P, SEMIBOLD); at(lab5, 1490)
        self.until(wt(5, 5, 0.1)); self.rise(lab5, rt=0.3)

        # ===== 6. Free games and tools. Free, forever. (ink, type list) =====
        self.until(S[6])
        ep.clear_updaters()
        self.ground(INK, UP, 0.4); self.remove(ep, *rl5, *cells, lab5, ch)
        self.remove(hdr); self.add(hdr_d); ch = self.chapter(5, True); self.add(ch)
        games = ("Sudoku", "Chess", "Times Table Blitz", "Math Sprint")
        rows6 = []
        for k, s_ in enumerate(games):
            y = 330 + k * 165
            ta = at(H(s_, 76, WHITE_), y); tb = B("Free", 34, OR, SEMIBOLD); tb.move_to([0, Y(y + 8), 0]).align_to([X(984), 0, 0], RIGHT)
            rl = Line([X(96), Y(y + 80), 0], [X(984), Y(y + 80), 0], stroke_color=INK3, stroke_width=3)
            rows6.append(VGroup(ta, tb, rl))
        self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.3) for r_ in rows6], lag_ratio=0.18), run_time=0.9, rate_func=EXPO)
        ff = at(SER("Free, forever.", 150, OR), 1150)
        sub = at(B("Games and learning tools, with a free account.", 38, GREY_I), 1300)
        self.until(wt(6, 4, 0.1)); self.ev("chime"); self.rise(ff, sub, rt=0.45, lag=0.15)

        # ===== 7. For schools and colleges: our AI tutor, licensed for your students (photo) =====
        self.until(S[7] - 0.1)
        self.ground(INK, UP, 0.36); self.remove(*rows6, ff, sub, ch)
        ch = self.chapter(6, True); self.add(ch, hdr_d)
        lp = photo("lab", "ed", 1080, BAND_TOP, 0.45).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        shade = Rectangle(width=9.2, height=px(600), fill_color=INK, fill_opacity=0.62, stroke_width=0).set_z_index(-4)
        shade.move_to([0, Y(BAND_TOP) + px(300), 0])
        top_sh = Rectangle(width=9.2, height=px(230), fill_color=INK, fill_opacity=0.55, stroke_width=0).set_z_index(-4).move_to([0, Y(115), 0])
        g1 = at(H("For schools", 92, WHITE_), 1110); g1b = at(H("and colleges", 92, WHITE_), 1220)
        g2 = at(SER("your own AI tutor, licensed.", 92, "#FFB27A"), 1360)
        if g2.width > px(888): g2.scale_to_fit_width(px(888)); left(g2)
        self.play(FadeIn(lp), FadeIn(shade), FadeIn(top_sh), FadeIn(g1, shift=UP * 0.3), FadeIn(g1b, shift=UP * 0.3), run_time=0.35, rate_func=EXPO)
        self.kb(lp, T(), S[8], 1.0, 1.05)
        self.until(wt(7, 6, 0.1)); self.rise(g2, rt=0.4)

        # ===== 8. TutorDA. Start free at tutorda.org (ink end card) =====
        self.until(S[8])
        lp.clear_updaters()
        self.ground(INK, UP, 0.4); self.remove(lp, shade, top_sh, g1, g1b, g2, ch, hdr_d)
        wm2 = wordmark(px(860), dark=True).move_to([0, Y(640), 0])
        self.ev("wordmark"); self.play(LaggedStart(FadeIn(wm2[:5], shift=UP * 0.4), FadeIn(wm2[5:], shift=DOWN * 0.4), lag_ratio=0.3), run_time=0.55, rate_func=EXPO)
        sf_ = B("Start free at", 50, GREY_I).move_to([0, Y(900), 0])
        url = H("tutorda.org", 120, OR).move_to([0, Y(1040), 0])
        ul = Line(url.get_corner(DL) + DOWN * 0.12, url.get_corner(DR) + DOWN * 0.12, stroke_color=OR, stroke_width=6)
        idx = B("  ·  ".join(PRODUCTS[:3]), 36, GREY_I).move_to([0, Y(1250), 0])
        idx2 = B("  ·  ".join(PRODUCTS[3:]), 36, GREY_I).move_to([0, Y(1315), 0])
        self.until(C[8] + 0.9); self.rise(sf_, rt=0.3)
        self.until(C[8] + 1.5); self.play(FadeIn(url, shift=UP * 0.3), Create(ul), run_time=0.4, rate_func=EXPO)
        self.rise(idx, idx2, rt=0.4, lag=0.15)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", "svc_events.json"), "w"))
