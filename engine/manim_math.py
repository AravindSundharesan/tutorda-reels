"""TutorDA JEE Main maths reels (30 s), brand-film system (paper ground, ink caption band, orange accent).
King: integral of sin^100/(sin^100+cos^100) on [0, pi/2] by the King property (a+b-x), answer pi/4.
Sols: number of real solutions of x^2 = 2^x by graphs, answer 3 (x = 2, 4 and x ~ -0.7667).
Numbers checked in Python before writing (scipy quad / brentq).
Render: FILM_AUDIO=aud_king tools/manim_build.sh engine/manim_math.py King aud_king out/king.mp4 [draft]
        FILM_AUDIO=aud_sols tools/manim_build.sh engine/manim_math.py Sols aud_sols out/sols.mp4 [draft]"""
import os, sys, json, math
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
from manim_tgt import *
import manim_tgt as TG

def M(s, size=56, color=None):
    return MathTex(s, color=color or INK, font_size=size)

def fitw(m, wpx):
    if m.width > px(wpx): m.scale_to_fit_width(px(wpx))
    return m

def cx(m, y):  # centre horizontally at a pixel row
    return m.move_to([0, Y(y), 0])


class MathReel(TG.Tgt):
    def chip(self, s, fg=WHITE_, bg=None, size=34):
        return tag(s, size, fg, bg or OR, padx=0.3, pady=0.14)

    def answer_box(self, m, color=OR):
        r = SurroundingRectangle(m, color=color, buff=0.32, corner_radius=0.18, stroke_width=8)
        return r

    def end_card(self, i, line):
        C = K.C
        wm = wordmark(px(760), dark=True).move_to([0, Y(560), 0])
        ln = SER(line, 92, "#FFB27A").move_to([0, Y(800), 0]); fitw(ln, 900).move_to([0, Y(800), 0])
        # bookmark glyph + Save this
        bm = Polygon([-0.22, 0.32, 0], [0.22, 0.32, 0], [0.22, -0.32, 0], [0, -0.14, 0], [-0.22, -0.32, 0], fill_color=OR, fill_opacity=1, stroke_width=0)
        sv = VGroup(bm, B("Save this for your next mock", 44, WHITE_, SEMIBOLD)).arrange(RIGHT, buff=0.3).move_to([0, Y(980), 0])
        fl = B("Follow TutorDA for more JEE tricks", 40, GREY_I).move_to([0, Y(1080), 0])
        url = H("tutorda.org", 96, OR).move_to([0, Y(1230), 0])
        self.ev("wordmark")
        self.play(LaggedStart(FadeIn(wm, shift=UP * 0.3), FadeIn(ln, shift=UP * 0.3), lag_ratio=0.3), run_time=0.6, rate_func=EXPO)
        self.until(C[i] + 0.9); self.ev("tick"); self.play(FadeIn(sv, shift=UP * 0.2), FadeIn(fl, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.until(C[i] + 1.6); self.rise(url, rt=0.4)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class King(MathReel):
    EVENTS = "king"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        INT = r"\int_0^{\pi/2}"
        FR_S = r"\frac{\sin^{100}x}{\sin^{100}x+\cos^{100}x}"
        FR_C = r"\frac{\cos^{100}x}{\cos^{100}x+\sin^{100}x}"
        # ===== 0. This integral looks impossible. Power one hundred. (visible on frame 0) =====
        self.add(self.hdr); lb = self.label("JEE Main", False); self.add(lb)
        q1 = at(H("Looks impossible?", 92, INK), 320)
        I1 = fitw(M(r"I=" + INT + FR_S + r"\,dx", 92), 900); cx(I1, 640)
        sub = at(B("Definite integrals · solve it in 10 seconds", 34, GREY_P, SEMIBOLD), 1460)
        self.add(q1, I1, sub)
        p100 = self.chip("power 100", size=34).move_to([X(820), Y(470), 0])
        self.until(wt(0, 4, 0.1)); self.ev("tick"); self.play(FadeIn(p100, shift=DOWN * 0.2), Indicate(I1, color=INK, scale_factor=1.04), run_time=0.45)

        # ===== 1. Here's the ten-second trick JEE loves. (property card) =====
        self.until(S[1])
        self.play(FadeOut(VGroup(q1, sub, p100), shift=UP * 0.2), I1.animate.scale(0.82).move_to([0, Y(380), 0]), run_time=0.32, rate_func=EXPO)
        pc = card(888, 330, INK); cx(pc, 820)
        pl = B("The trick JEE loves", 34, "#FFB27A", SEMIBOLD).move_to(pc.get_top() + DOWN * px(56))
        prop = fitw(M(r"\int_0^{a}f(x)\,dx=\int_0^{a}f(a-x)\,dx", 70, WHITE_), 800).move_to(pc.get_center() + DOWN * px(30))
        self.ev("tick"); self.play(FadeIn(pc, shift=UP * 0.3), FadeIn(pl), FadeIn(prop, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        ten = self.chip("10 seconds", size=36).move_to([X(540), Y(1110), 0])
        self.until(wt(1, 2, 0.1)); self.play(GrowFromCenter(ten), run_time=0.3)

        # ===== 2. Swap x for pi/2 - x. Sine turns into cos, cos into sine. =====
        self.until(S[2])
        sw = M(r"x\;\longrightarrow\;\tfrac{\pi}{2}-x", 84, OR); cx(sw, 760)
        self.play(FadeOut(VGroup(pc, pl, prop, ten), shift=UP * 0.2), FadeIn(sw, shift=UP * 0.3), run_time=0.4, rate_func=EXPO)
        id1 = M(r"\sin\!\left(\tfrac{\pi}{2}-x\right)=\cos x", 72); cx(id1, 960)
        id2 = M(r"\cos\!\left(\tfrac{\pi}{2}-x\right)=\sin x", 72); cx(id2, 1110)
        self.until(wt(2, 6, 0.1)); self.ev("tick"); self.play(FadeIn(id1, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        self.until(wt(2, 11, 0.1)); self.ev("tick"); self.play(FadeIn(id2, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)

        # ===== 3. Same integral, upside down. Now add the two versions. =====
        self.until(S[3])
        I2 = fitw(M(r"I=" + INT + FR_C + r"\,dx", 92), 900).scale(0.82); cx(I2, 640)
        self.play(FadeOut(VGroup(sw, id1, id2), shift=UP * 0.2), TransformFromCopy(I1, I2), run_time=0.6, rate_func=EXPO)
        flip = self.chip("flipped", size=30).next_to(I2, RIGHT, buff=-1.2).shift(UP * 0.55)
        self.play(FadeIn(flip, scale=0.8), run_time=0.25)
        plus = M(r"+", 90, OR).move_to([X(130), Y(510), 0])
        rule = Line([X(96), Y(770), 0], [X(984), Y(770), 0], stroke_color=INK, stroke_width=5)
        self.until(wt(3, 5, 0.1)); self.ev("tick"); self.play(FadeIn(plus, scale=0.6), Create(rule), FadeOut(flip), run_time=0.35)

        # ===== 4. Top and bottom match -> integral of one -> pi/2 =====
        self.until(S[4])
        s1 = fitw(M(r"2I=" + INT + r"\frac{\sin^{100}x+\cos^{100}x}{\sin^{100}x+\cos^{100}x}\,dx", 92), 900).scale(0.82); cx(s1, 950)
        self.ev("tick"); self.play(FadeIn(s1, shift=UP * 0.3), run_time=0.4, rate_func=EXPO)
        match = self.chip("top = bottom", size=32).move_to([X(820), Y(1110), 0])
        self.play(FadeIn(match, shift=UP * 0.15), run_time=0.25)
        s2 = M(r"2I=" + INT + r"1\,dx", 92); cx(s2, 950)
        self.until(wt(4, 9, 0.1)); self.ev("tick"); self.play(FadeOut(match), TransformMatchingTex(s1, s2), run_time=0.5)
        s3 = M(r"2I=\frac{\pi}{2}", 100); cx(s3, 950)
        self.until(wt(4, 13, 0.1)); self.ev("tick"); self.play(TransformMatchingTex(s2, s3), run_time=0.45)

        # ===== 5. So 2I = pi/2, and I = pi/4 (the one spring moment) =====
        self.until(S[5])
        ans = M(r"I=\frac{\pi}{4}", 120); cx(ans, 1320)
        box = self.answer_box(ans)
        self.until(wt(5, 5, 0.1)); self.ev("stamp")
        self.play(GrowFromCenter(ans), run_time=0.45, rate_func=rate_functions.ease_out_back)
        self.play(Create(box), run_time=0.35)

        # ===== 6. The power never mattered. =====
        self.until(S[6])
        self.play(FadeOut(VGroup(I1, I2, plus, rule, s3), shift=UP * 0.3), VGroup(ans, box).animate.scale(0.7).move_to([X(540), Y(420), 0]), run_time=0.45, rate_func=EXPO)
        rows = VGroup(*[M(r"n=" + n + r"\;\;\Rightarrow\;\;I=\frac{\pi}{4}", 64) for n in ("1", "3", "100", "10^6")]).arrange(DOWN, buff=0.3)
        cx(rows, 900)
        nv = at(SER("The power never mattered.", 96, OR), 1350); fitw(nv, 888)
        self.ev("tick"); self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in rows], lag_ratio=0.25), FadeIn(nv, shift=UP * 0.2), run_time=0.8, rate_func=EXPO)

        # ===== 7. End =====
        self.until(S[7]); self.to(INK, ans, box, rows, nv, lb); self.remove(self.hdr_d)
        self.end_card(7, "Same trick, any power.")


class Sols(MathReel):
    EVENTS = "sols"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        # ===== 0. How many real solutions does x^2 = 2^x have? (visible on frame 0) =====
        self.add(self.hdr); lb = self.label("JEE Main", False); self.add(lb)
        q1 = at(H("How many real", 92, INK), 300); q2 = at(H("solutions?", 92, INK), 410)
        eq = M(r"x^2=2^x", 200); cx(eq, 650)
        opts = VGroup()
        for k, (L, v) in enumerate((("A", "1"), ("B", "2"), ("C", "3"), ("D", "4"))):
            c_ = RoundedRectangle(width=px(420), height=px(120), corner_radius=0.16, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            t_ = VGroup(B(L, 40, OR, SEMIBOLD), H(v, 60, INK)).arrange(RIGHT, buff=0.4).move_to(c_)
            g = VGroup(c_, t_); r_, k_ = divmod(k, 2); g.move_to([X(96 + 210 + k_ * 468), Y(920 + r_ * 150), 0]); opts.add(g)
        self.add(q1, q2, eq, opts)

        # ===== 1. Comment your answer. Most people say two. =====
        bub = VGroup(RoundedRectangle(width=px(888), height=px(120), corner_radius=0.2, fill_color=INK, fill_opacity=1, stroke_width=0))
        bt = B("Comment your answer before the reveal", 38, WHITE_, SEMIBOLD).move_to(bub[0])
        tail = Polygon([X(180), Y(1290), 0], [X(230), Y(1290), 0], [X(170), Y(1330), 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        bub.add(bt); cx(bub, 1230)
        self.until(wt(1, 0, 0.1)); self.ev("tick"); self.play(FadeIn(bub, shift=UP * 0.2), FadeIn(tail, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        most = B("most people", 30, GREY_P, SEMIBOLD).next_to(opts[1], UP, buff=0.12).align_to(opts[1], RIGHT)
        self.until(wt(1, 6, 0.1)); self.ev("tick")
        self.play(opts[1][0].animate.set_fill(INK).set_stroke(INK), opts[1][1][1].animate.set_color(WHITE_), FadeIn(most, shift=UP * 0.1), run_time=0.3)

        # ===== 2. Two works: 4 = 4. Four works too: 16 = 16. =====
        self.until(S[2])
        c1 = VGroup(M(r"x=2:\quad 2^2=4=2^2", 76), tick(0.22)).arrange(RIGHT, buff=0.35); cx(c1, 640)
        c2 = VGroup(M(r"x=4:\quad 4^2=16=2^4", 76), tick(0.22)).arrange(RIGHT, buff=0.35); cx(c2, 820)
        self.ev("tick"); self.play(FadeOut(VGroup(q1, q2, opts, bub, tail, most), shift=UP * 0.2), eq.animate.scale(0.6).move_to([0, Y(360), 0]), FadeIn(c1, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.until(wt(2, 5, 0.1)); self.ev("tick"); self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        two = at(SER("So the answer is 2?", 96, GREY_P), 1080)
        self.play(FadeIn(two, shift=UP * 0.2), run_time=0.35)

        # ===== 3. But draw both graphs. =====
        self.until(S[3])
        ax = Axes(x_range=[-3, 5, 1], y_range=[0, 20, 4], x_length=px(860), y_length=px(940), tips=False,
                  axis_config={"color": INK, "stroke_width": 3, "include_numbers": False})
        ax.move_to([X(560), Y(830), 0])
        xl = VGroup(*[B(str(v), 34, GREY_P).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (-2, 2, 4)])
        f1 = ax.plot(lambda x: x ** 2, x_range=[-3, math.sqrt(20)], color=INK, stroke_width=7)
        f2 = ax.plot(lambda x: 2 ** x, x_range=[-3, math.log2(20)], color=OR, stroke_width=7)
        l1 = M(r"y=x^2", 52).next_to(ax.c2p(-1.9, 8.5), RIGHT, buff=0.1)
        l2 = M(r"y=2^x", 52, OR).next_to(ax.c2p(4.3, 19.5), LEFT, buff=0.15)
        self.play(FadeOut(VGroup(c1, c2, two, eq), shift=UP * 0.2), Create(ax), FadeIn(xl), run_time=0.45)
        self.ev("tick"); self.play(Create(f1), Create(f2), FadeIn(l1), FadeIn(l2), run_time=0.8, rate_func=rate_functions.ease_in_out_sine)

        # ===== 4. For negative x the parabola climbs, 2^x drops to zero, so they must cross. =====
        self.until(S[4])
        reg = Rectangle(width=ax.c2p(0, 0)[0] - ax.c2p(-3, 0)[0], height=ax.c2p(0, 20)[1] - ax.c2p(0, 0)[1], fill_color=OR, fill_opacity=0.07, stroke_width=0)
        reg.move_to([(ax.c2p(-3, 0)[0] + ax.c2p(0, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, 20)[1]) / 2, 0]).set_z_index(-1)
        neg = B("x < 0", 34, OR, SEMIBOLD).move_to(ax.c2p(-1.5, 19))
        self.ev("tick"); self.play(FadeIn(reg), FadeIn(neg), run_time=0.3)
        up = Arrow(ax.c2p(-2.0, 4.6), ax.c2p(-2.7, 8.6), color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.3)
        dn = Arrow(ax.c2p(-1.3, 2.4), ax.c2p(-2.6, 1.0), color=OR, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.3)
        self.until(wt(4, 5, 0.1)); self.play(GrowArrow(up), run_time=0.35)
        self.until(wt(4, 10, 0.1)); self.play(GrowArrow(dn), run_time=0.35)
        # zoom inset (upper left, empty area of the plot)
        x0 = -0.7666646959621232; y0 = x0 ** 2
        ins_bg = RoundedRectangle(width=px(420), height=px(380), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=4)
        ins_bg.move_to([X(96 + 230), Y(470), 0])
        ia = Axes(x_range=[-1.6, 0.4, 0.5], y_range=[0, 2.6, 1], x_length=px(340), y_length=px(290), tips=False, axis_config={"color": INK, "stroke_width": 2})
        ia.move_to(ins_bg.get_center() + DOWN * px(8))
        g1 = ia.plot(lambda x: x ** 2, x_range=[-1.6, 0.4], color=INK, stroke_width=5)
        g2 = ia.plot(lambda x: 2 ** x, x_range=[-1.6, 0.4], color=OR, stroke_width=5)
        zoom = B("zoom", 26, OR, SEMIBOLD).next_to(ins_bg.get_corner(UL), DR, buff=0.12)
        lead = DashedLine(ax.c2p(x0, y0), ins_bg.get_bottom() + RIGHT * px(40), color=OR, stroke_width=3)
        self.until(wt(4, 12, 0.1)); self.ev("tick")
        self.play(FadeIn(ins_bg), Create(ia), Create(g1), Create(g2), FadeIn(zoom), Create(lead), run_time=0.6)

        # ===== 5. Near -0.77, there's a third solution. =====
        self.until(S[5])
        d0 = Dot(ia.c2p(x0, y0), radius=px(12), color=OR); d0b = Dot(ax.c2p(x0, y0), radius=px(10), color=OR)
        xv = M(r"x\approx-0.767", 42, OR).next_to(ins_bg, RIGHT, buff=0.12).align_to(ins_bg, DOWN).shift(UP * px(70))
        self.until(wt(5, 1, 0.1)); self.ev("tick")
        self.play(GrowFromCenter(d0), GrowFromCenter(d0b), FadeIn(xv, shift=LEFT * 0.2), run_time=0.4)
        d2 = Dot(ax.c2p(2, 4), radius=px(10), color=INK); d4 = Dot(ax.c2p(4, 16), radius=px(10), color=INK)
        n3 = at(B("3 crossings", 40, INK, SEMIBOLD), 1460)
        self.until(wt(5, 3, 0.1)); self.play(GrowFromCenter(d2), GrowFromCenter(d4), FadeIn(n3), run_time=0.35)

        # ===== 6. The answer is three. =====
        self.until(S[6])
        ans = VGroup(B("Answer", 40, GREY_P, SEMIBOLD), H("3", 170, OR), B("real solutions", 44, INK, SEMIBOLD)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 1440)
        self.ev("stamp"); self.play(FadeOut(n3), GrowFromCenter(a_), run_time=0.45, rate_func=rate_functions.ease_out_back)

        # ===== 7. End =====
        self.until(S[7])
        self.to(INK, ax, xl, f1, f2, l1, l2, reg, neg, up, dn, ins_bg, ia, g1, g2, zoom, lead, d0, d0b, xv, d2, d4, a_, lb); self.remove(self.hdr_d)
        self.end_card(7, "Draw it before you trust it.")


class SinX(MathReel):
    EVENTS = "sinx"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        R = [2.852342, 7.068174, 8.423204]
        # ===== 0. How many times does y = x/10 cut the sine curve? (visible on frame 0) =====
        self.add(self.hdr); lb = self.label("JEE Main", False); self.add(lb)
        q1 = at(H("How many solutions?", 92, INK), 300); fitw(q1, 888)
        eq = M(r"\sin x=\frac{x}{10}", 170); cx(eq, 620)
        opts = VGroup()
        for k, (L, v) in enumerate((("A", "2"), ("B", "3"), ("C", "5"), ("D", "7"))):
            c_ = RoundedRectangle(width=px(420), height=px(120), corner_radius=0.16, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            t_ = VGroup(B(L, 40, OR, SEMIBOLD), H(v, 60, INK)).arrange(RIGHT, buff=0.4).move_to(c_)
            g = VGroup(c_, t_); r_, k_ = divmod(k, 2); g.move_to([X(96 + 210 + k_ * 468), Y(900 + r_ * 150), 0]); opts.add(g)
        self.add(q1, eq, opts)

        # ===== 1. Comment your guess. Most people say two or three. =====
        bub = VGroup(RoundedRectangle(width=px(888), height=px(120), corner_radius=0.2, fill_color=INK, fill_opacity=1, stroke_width=0))
        bub.add(B("Comment your guess before the reveal", 38, WHITE_, SEMIBOLD).move_to(bub[0])); cx(bub, 1230)
        tail = Polygon([X(180), Y(1290), 0], [X(230), Y(1290), 0], [X(170), Y(1330), 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        self.until(wt(1, 0, 0.1)); self.ev("tick"); self.play(FadeIn(bub, shift=UP * 0.2), FadeIn(tail, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        most = B("most people", 30, GREY_P, SEMIBOLD).next_to(opts[0], UP, buff=0.12).align_to(opts[0], LEFT)
        self.until(wt(1, 6, 0.1)); self.ev("tick")
        self.play(*[o[0].animate.set_stroke(OR, width=5) for o in opts[:2]], FadeIn(most, shift=UP * 0.1), run_time=0.3)

        # ===== 2. Sine stays in [-1, 1], so only -10..10 matters =====
        self.until(S[2])
        ax = Axes(x_range=[-12, 12, 2], y_range=[-1.6, 1.6, 1], x_length=px(900), y_length=px(520), tips=False,
                  axis_config={"color": INK, "stroke_width": 3})
        ax.move_to([X(540), Y(820), 0])
        sn = ax.plot(np.sin, x_range=[-12, 12], color=INK, stroke_width=6)
        e2 = M(r"\sin x=\frac{x}{10}", 80); cx(e2, 320)
        self.ev("tick")
        self.play(FadeOut(VGroup(q1, opts, bub, tail, most), shift=UP * 0.2), ReplacementTransform(eq, e2), Create(ax), run_time=0.45, rate_func=EXPO)
        self.play(Create(sn), run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        b1 = DashedLine(ax.c2p(-12, 1), ax.c2p(12, 1), color=GREY_P, stroke_width=3); b2 = DashedLine(ax.c2p(-12, -1), ax.c2p(12, -1), color=GREY_P, stroke_width=3)
        bl = VGroup(M(r"y=1", 40, GREY_P).next_to(ax.c2p(12, 1), UP, buff=0.08).shift(LEFT * 0.4), M(r"y=-1", 40, GREY_P).next_to(ax.c2p(12, -1), DOWN, buff=0.08).shift(LEFT * 0.4))
        self.until(wt(2, 3, 0.1)); self.play(Create(b1), Create(b2), FadeIn(bl), run_time=0.35)
        ln_ = ax.plot(lambda x: x / 10, x_range=[-12, 12], color=OR, stroke_width=7)
        lt = M(r"y=\frac{x}{10}", 48, OR).move_to(ax.c2p(4.6, 1.38))
        self.until(wt(2, 10, 0.1)); self.ev("tick"); self.play(Create(ln_), FadeIn(lt), run_time=0.5)
        shL = Rectangle(width=ax.c2p(-10, 0)[0] - ax.c2p(-12, 0)[0], height=px(520), fill_color=GREY_P, fill_opacity=0.18, stroke_width=0).move_to([(ax.c2p(-12, 0)[0] + ax.c2p(-10, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
        shR = shL.copy().move_to([(ax.c2p(10, 0)[0] + ax.c2p(12, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
        v1 = DashedLine(ax.c2p(-10, -1.6), ax.c2p(-10, 1.6), color=OR, stroke_width=3); v2 = DashedLine(ax.c2p(10, -1.6), ax.c2p(10, 1.6), color=OR, stroke_width=3)
        vl = VGroup(B("−10", 34, OR, SEMIBOLD).next_to(ax.c2p(-10, -1.6), DOWN, buff=0.12), B("10", 34, OR, SEMIBOLD).next_to(ax.c2p(10, -1.6), DOWN, buff=0.12))
        self.until(wt(2, 14, 0.1)); self.ev("tick"); self.play(FadeIn(shL), FadeIn(shR), Create(v1), Create(v2), FadeIn(vl), run_time=0.4)

        # crossing counter
        cnt_l = B("Crossings", 36, GREY_P, SEMIBOLD); cnt_v = H("0", 120, OR)
        cnt = VGroup(cnt_l, cnt_v).arrange(RIGHT, buff=0.35, aligned_edge=DOWN); cx(cnt, 1320)
        state = {"n": 0}
        def setn(n):
            state["n"] = n; nv = H(str(n), 120, OR).move_to(cnt_v); cnt_v.become(nv)

        # ===== 3. Count on the right: one, two, three =====
        self.until(S[3]); self.play(FadeIn(cnt, shift=UP * 0.2), run_time=0.3)
        dots = {}
        for k, (w_, x) in enumerate(zip((7, 8, 9), R)):
            d = Dot(ax.c2p(x, x / 10), radius=px(13), color=OR).set_z_index(5)
            t_ = B(str(k + 1), 32, INK, SEMIBOLD).next_to(d, UP if k != 1 else DOWN, buff=0.12)
            self.until(wt(3, w_, 0.08)); self.ev("tick"); self.play(GrowFromCenter(d), FadeIn(t_), run_time=0.22); setn(k + 1); dots[x] = (d, t_)

        # ===== 4. Left side is a mirror image: three more =====
        self.until(S[4])
        mir = [(Dot(ax.c2p(-x, -x / 10), radius=px(13), color=OR).set_z_index(5)) for x in R]
        mt = [B(str(k + 4), 32, INK, SEMIBOLD).next_to(m, DOWN if k != 1 else UP, buff=0.12) for k, m in enumerate(mir)]
        mlab = B("mirror image", 34, OR, SEMIBOLD).move_to(ax.c2p(-6, 1.45))
        self.play(FadeIn(mlab), run_time=0.25)
        self.until(wt(4, 7, 0.1)); self.ev("tick")
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(m), FadeIn(t)) for m, t in zip(mir, mt)], lag_ratio=0.25), run_time=0.6); setn(6)

        # ===== 5. Plus the origin. Seven solutions. =====
        self.until(S[5])
        o = Dot(ax.c2p(0, 0), radius=px(15), color=INK).set_z_index(6)
        self.until(wt(5, 2, 0.1)); self.ev("tick"); self.play(GrowFromCenter(o), run_time=0.25); setn(7)
        ans = VGroup(B("Answer", 40, GREY_P, SEMIBOLD), H("7", 170, OR), B("solutions", 44, INK, SEMIBOLD)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 1320)
        self.until(wt(5, 3, 0.1)); self.ev("stamp"); self.play(FadeOut(cnt), GrowFromCenter(a_), run_time=0.45, rate_func=rate_functions.ease_out_back)

        # ===== 6. End =====
        self.until(S[6])
        self.to(INK, e2, ax, sn, b1, b2, bl, ln_, lt, shL, shR, v1, v2, vl, *[v for p in dots.values() for v in p], *mir, *mt, mlab, o, a_, lb); self.remove(self.hdr_d)
        self.end_card(6, "Sketch first, then count.")


class EPi(MathReel):
    EVENTS = "epi"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        fe, fp = 1 / math.e, math.log(math.pi) / math.pi
        # ===== 0. Which is bigger: e^pi or pi^e? (visible on frame 0) =====
        self.add(self.hdr); lb = self.label("JEE Main", False); self.add(lb)
        q1 = at(H("Which is bigger?", 100, INK), 320)
        a1 = M(r"e^{\pi}", 210); a2 = M(r"\pi^{e}", 210, OR); vs = B("vs", 48, GREY_P, SEMIBOLD)
        row = VGroup(a1, vs, a2).arrange(RIGHT, buff=0.9); cx(row, 700)
        self.add(q1, row)

        # ===== 1. Comment before you scroll. No calculator. =====
        bub = VGroup(RoundedRectangle(width=px(888), height=px(120), corner_radius=0.2, fill_color=INK, fill_opacity=1, stroke_width=0))
        bub.add(B("Comment your pick before you scroll", 38, WHITE_, SEMIBOLD).move_to(bub[0])); cx(bub, 1060)
        tail = Polygon([X(180), Y(1120), 0], [X(230), Y(1120), 0], [X(170), Y(1160), 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        self.until(wt(1, 0, 0.1)); self.ev("tick"); self.play(FadeIn(bub, shift=UP * 0.2), FadeIn(tail, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        nc = self.chip("No calculator", size=36); cx(nc, 1260)
        self.until(wt(1, 4, 0.1)); self.ev("tick"); self.play(GrowFromCenter(nc), run_time=0.3)

        # ===== 2. Take logs: pi ln e  vs  e ln pi =====
        self.until(S[2])
        l1 = M(r"\pi\ln e", 130); l2 = M(r"e\ln\pi", 130, OR); vs2 = B("vs", 48, GREY_P, SEMIBOLD)
        lrow = VGroup(l1, vs2, l2).arrange(RIGHT, buff=0.8); cx(lrow, 700)
        tl = self.chip("take ln", size=34); cx(tl, 500)
        self.ev("tick")
        self.play(FadeOut(VGroup(q1, bub, tail, nc), shift=UP * 0.2), FadeIn(tl, shift=DOWN * 0.1), run_time=0.3)
        self.until(wt(2, 3, 0.1)); self.play(ReplacementTransform(a1, l1), ReplacementTransform(a2, l2), ReplacementTransform(vs, vs2), run_time=0.55)

        # ===== 3. Divide by pi*e: ln x / x at e and at pi =====
        self.until(S[3])
        d1 = M(r"\frac{\ln e}{e}", 130); d2 = M(r"\frac{\ln\pi}{\pi}", 130, OR); vs3 = B("vs", 48, GREY_P, SEMIBOLD)
        drow = VGroup(d1, vs3, d2).arrange(RIGHT, buff=0.8); cx(drow, 700)
        td = self.chip(r"divide by πe", size=34); cx(td, 500)
        self.ev("tick"); self.play(ReplacementTransform(tl, td), ReplacementTransform(l1, d1), ReplacementTransform(l2, d2), ReplacementTransform(vs2, vs3), run_time=0.55)
        fx = M(r"f(x)=\frac{\ln x}{x}", 110); cx(fx, 1180)
        self.until(wt(3, 8, 0.1)); self.ev("tick"); self.play(FadeIn(fx, shift=UP * 0.2), run_time=0.35)
        lab = VGroup(M(r"f(e)", 60).next_to(d1, DOWN, buff=0.25), M(r"f(\pi)", 60, OR).next_to(d2, DOWN, buff=0.25))
        self.until(wt(3, 12, 0.1)); self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.3)

        # ===== 4. Draw y = ln x / x. It peaks exactly at x = e. =====
        self.until(S[4])
        ax = Axes(x_range=[0.8, 9, 1], y_range=[-0.25, 0.45, 0.1], x_length=px(880), y_length=px(640), tips=False, axis_config={"color": INK, "stroke_width": 3})
        ax.move_to([X(540), Y(860), 0])
        g = ax.plot(lambda x: math.log(x) / x, x_range=[0.8, 9], color=INK, stroke_width=7)
        gl = M(r"y=\frac{\ln x}{x}", 56).next_to(ax.c2p(6.2, 0.36), RIGHT, buff=0.05)
        top = VGroup(M(r"\frac{\ln e}{e}", 70), B("vs", 34, GREY_P, SEMIBOLD), M(r"\frac{\ln\pi}{\pi}", 70, OR)).arrange(RIGHT, buff=0.4); cx(top, 300)
        self.ev("tick")
        self.play(FadeOut(VGroup(td, fx, lab), shift=UP * 0.2), ReplacementTransform(VGroup(d1, vs3, d2), top), Create(ax), run_time=0.45, rate_func=EXPO)
        self.play(Create(g), FadeIn(gl), run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        pk = Dot(ax.c2p(math.e, fe), radius=px(14), color=INK).set_z_index(5)
        pv = DashedLine(ax.c2p(math.e, -0.25), ax.c2p(math.e, fe), color=INK, stroke_width=3)
        pl = VGroup(B("peak", 34, INK, SEMIBOLD), M(r"x=e", 48)).arrange(RIGHT, buff=0.2).next_to(ax.c2p(math.e, fe), UP, buff=0.25)
        self.until(wt(4, 8, 0.1)); self.ev("tick"); self.play(GrowFromCenter(pk), Create(pv), FadeIn(pl, shift=DOWN * 0.1), run_time=0.4)

        # ===== 5. Pi is past the peak, so its value is lower. =====
        self.until(S[5])
        pp = Dot(ax.c2p(math.pi, fp), radius=px(14), color=OR).set_z_index(5)
        ppv = DashedLine(ax.c2p(math.pi, -0.25), ax.c2p(math.pi, fp), color=OR, stroke_width=3)
        pil = M(r"\pi", 52, OR).next_to(ax.c2p(math.pi, -0.25), DOWN, buff=0.1); el = M(r"e", 52).next_to(ax.c2p(math.e, -0.25), DOWN, buff=0.1)
        self.ev("tick"); self.play(GrowFromCenter(pp), Create(ppv), FadeIn(pil), FadeIn(el), run_time=0.4)
        ins_bg = RoundedRectangle(width=px(430), height=px(300), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=4)
        ins_bg.move_to([X(96 + 235 + 410), Y(1010), 0])
        rows = VGroup(VGroup(M(r"f(e)", 44), M(r"\approx0.3679", 44)).arrange(RIGHT, buff=0.2),
                      VGroup(M(r"f(\pi)", 44, OR), M(r"\approx0.3644", 44, OR)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows.move_to(ins_bg.get_center() + DOWN * px(16)); zt = B("zoom", 26, OR, SEMIBOLD).next_to(ins_bg.get_corner(UL), DR, buff=0.12)
        lower = B("lower", 34, OR, SEMIBOLD).next_to(pp, DOWN, buff=0.35).shift(RIGHT * 0.55)
        self.until(wt(5, 9, 0.1)); self.ev("tick"); self.play(FadeIn(ins_bg), FadeIn(rows), FadeIn(zt), FadeIn(lower), run_time=0.4)

        # ===== 6. So e^pi is bigger. =====
        self.until(S[6])
        ans = M(r"e^{\pi}>\pi^{e}", 130); ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 1360)
        chk = B("23.14 > 22.46", 34, GREY_P, SEMIBOLD).next_to(a_, DOWN, buff=0.15)
        self.ev("stamp"); self.play(GrowFromCenter(a_), run_time=0.45, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(chk), run_time=0.2)

        # ===== 7. End =====
        self.until(S[7])
        self.to(INK, top, ax, g, gl, pk, pv, pl, pp, ppv, pil, el, ins_bg, rows, zt, lower, a_, chk, lb); self.remove(self.hdr_d)
        self.end_card(7, "Draw the function, then compare.")


class ModCos(MathReel):
    EVENTS = "modcos"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        r0 = 0.7390851332151607
        # ===== 0. How many solutions does |x| = cos x have? (visible on frame 0) =====
        self.add(self.hdr); lb = self.label("JEE Main", False); self.add(lb)
        q1 = at(H("How many solutions?", 92, INK), 300); fitw(q1, 888)
        eq = M(r"|x|=\cos x", 170); cx(eq, 620)
        opts = VGroup()
        for k, (L, v) in enumerate((("A", "0"), ("B", "2"), ("C", "4"), ("D", r"\infty"))):
            c_ = RoundedRectangle(width=px(420), height=px(120), corner_radius=0.16, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            t_ = VGroup(B(L, 40, OR, SEMIBOLD), M(v, 66)).arrange(RIGHT, buff=0.4).move_to(c_)
            g = VGroup(c_, t_); r_, k_ = divmod(k, 2); g.move_to([X(96 + 210 + k_ * 468), Y(900 + r_ * 150), 0]); opts.add(g)
        self.add(q1, eq, opts)

        # ===== 1. Comment your guess. Cos waves forever, so it looks like a lot. =====
        bub = VGroup(RoundedRectangle(width=px(888), height=px(120), corner_radius=0.2, fill_color=INK, fill_opacity=1, stroke_width=0))
        bub.add(B("Comment your guess before the reveal", 38, WHITE_, SEMIBOLD).move_to(bub[0])); cx(bub, 1230)
        tail = Polygon([X(180), Y(1290), 0], [X(230), Y(1290), 0], [X(170), Y(1330), 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        self.until(wt(1, 0, 0.1)); self.ev("tick"); self.play(FadeIn(bub, shift=UP * 0.2), FadeIn(tail, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        lot = B("looks like a lot", 30, GREY_P, SEMIBOLD).next_to(opts[3], UP, buff=0.12).align_to(opts[3], RIGHT)
        self.until(wt(1, 8, 0.1)); self.ev("tick")
        self.play(opts[3][0].animate.set_stroke(OR, width=5), FadeIn(lot, shift=UP * 0.1), run_time=0.3)

        # ===== 2. Cos never goes above 1, so the V only matters from -1 to 1 =====
        self.until(S[2])
        ax = Axes(x_range=[-6, 6, 1], y_range=[-1.4, 2.6, 1], x_length=px(900), y_length=px(600), tips=False,
                  axis_config={"color": INK, "stroke_width": 3})
        ax.move_to([X(540), Y(840), 0])
        cs = ax.plot(np.cos, x_range=[-6, 6], color=INK, stroke_width=6)
        cl = M(r"y=\cos x", 46).move_to(ax.c2p(-4.4, -1.25))
        e2 = M(r"|x|=\cos x", 84); cx(e2, 320)
        self.ev("tick")
        self.play(FadeOut(VGroup(q1, opts, bub, tail, lot), shift=UP * 0.2), ReplacementTransform(eq, e2), Create(ax), run_time=0.45, rate_func=EXPO)
        self.play(Create(cs), FadeIn(cl), run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        b1 = DashedLine(ax.c2p(-6, 1), ax.c2p(6, 1), color=GREY_P, stroke_width=3)
        bl = M(r"y=1", 40, GREY_P).next_to(ax.c2p(6, 1), UP, buff=0.08).shift(LEFT * 0.45)
        self.until(wt(2, 4, 0.1)); self.ev("tick"); self.play(Create(b1), FadeIn(bl), run_time=0.35)
        vv = ax.plot(lambda x: abs(x), x_range=[-2.6, 2.6], color=OR, stroke_width=8, use_smoothing=False)
        vl = M(r"y=|x|", 48, OR).move_to(ax.c2p(4.3, 2.0))
        self.until(wt(2, 8, 0.12)); self.ev("tick"); self.play(Create(vv), FadeIn(vl), run_time=0.5)
        h = ax.c2p(0, 2.6)[1] - ax.c2p(0, -1.4)[1]; yc = (ax.c2p(0, 2.6)[1] + ax.c2p(0, -1.4)[1]) / 2
        shL = Rectangle(width=ax.c2p(-1, 0)[0] - ax.c2p(-6, 0)[0], height=h, fill_color=GREY_P, fill_opacity=0.16, stroke_width=0).move_to([(ax.c2p(-6, 0)[0] + ax.c2p(-1, 0)[0]) / 2, yc, 0])
        shR = shL.copy().move_to([(ax.c2p(1, 0)[0] + ax.c2p(6, 0)[0]) / 2, yc, 0])
        v1 = DashedLine(ax.c2p(-1, -1.4), ax.c2p(-1, 2.6), color=OR, stroke_width=3); v2 = DashedLine(ax.c2p(1, -1.4), ax.c2p(1, 2.6), color=OR, stroke_width=3)
        vlb = VGroup(B("−1", 34, OR, SEMIBOLD).next_to(ax.c2p(-1, -1.4), DOWN, buff=0.12), B("1", 34, OR, SEMIBOLD).next_to(ax.c2p(1, -1.4), DOWN, buff=0.12))
        nz = B("|x| > 1: no chance", 28, GREY_P, SEMIBOLD).move_to(ax.c2p(-4.3, 2.25))
        self.until(wt(2, 11, 0.1)); self.ev("tick"); self.play(FadeIn(shL), FadeIn(shR), Create(v1), Create(v2), FadeIn(vlb), FadeIn(nz), run_time=0.4)

        cnt_l = B("Crossings", 36, GREY_P, SEMIBOLD); cnt_v = H("0", 120, OR)
        cnt = VGroup(cnt_l, cnt_v).arrange(RIGHT, buff=0.35, aligned_edge=DOWN); cx(cnt, 1340)
        def setn(n): cnt_v.become(H(str(n), 120, OR).move_to(cnt_v))

        # ===== 3. Right side: line climbs from 0, cos falls from 1, they cross once =====
        self.until(S[3]); self.play(FadeIn(cnt, shift=UP * 0.2), run_time=0.3)
        a1 = Arrow(ax.c2p(0.08, 0.02), ax.c2p(0.95, 0.9), color=OR, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.25).shift(RIGHT * 0.25 + DOWN * 0.18)
        a2 = Arrow(ax.c2p(0.05, 1.12), ax.c2p(1.0, 0.68), color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.25).shift(UP * 0.28)
        self.until(wt(3, 5, 0.1)); self.play(GrowArrow(a1), run_time=0.35)
        self.until(wt(3, 10, 0.1)); self.play(GrowArrow(a2), run_time=0.35)
        d1 = Dot(ax.c2p(r0, r0), radius=px(14), color=OR).set_z_index(5)
        t1 = B("1", 32, INK, SEMIBOLD).next_to(d1, RIGHT, buff=0.15).shift(DOWN * 0.1)
        self.until(wt(3, 14, 0.08)); self.ev("tick"); self.play(GrowFromCenter(d1), FadeIn(t1), FadeOut(a1), FadeOut(a2), run_time=0.3); setn(1)

        # ===== 4. Left side is a mirror image: one more =====
        self.until(S[4])
        mlab = B("mirror image", 34, OR, SEMIBOLD).move_to(ax.c2p(-3.9, 1.3))
        self.play(FadeIn(mlab), run_time=0.25)
        d2 = Dot(ax.c2p(-r0, r0), radius=px(14), color=OR).set_z_index(5)
        t2 = B("2", 32, INK, SEMIBOLD).next_to(d2, LEFT, buff=0.15).shift(DOWN * 0.1)
        self.until(wt(4, 7, 0.08)); self.ev("tick"); self.play(GrowFromCenter(d2), FadeIn(t2), run_time=0.3); setn(2)

        # ===== 5. Two solutions, near x = +-0.739 =====
        self.until(S[5])
        ans = VGroup(B("Answer", 40, GREY_P, SEMIBOLD), H("2", 170, OR), B("solutions", 44, INK, SEMIBOLD)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 1340)
        xv = M(r"x\approx\pm0.739", 52, OR); cx(xv, 1510)
        self.ev("stamp"); self.play(FadeOut(cnt), GrowFromCenter(a_), run_time=0.45, rate_func=rate_functions.ease_out_back)
        self.until(wt(5, 3, 0.1)); self.play(FadeIn(xv, shift=UP * 0.15), run_time=0.3)

        # ===== 6. End =====
        self.until(S[6])
        self.to(INK, e2, ax, cs, cl, b1, bl, vv, vl, shL, shR, v1, v2, vlb, nz, d1, t1, mlab, d2, t2, a_, xv, lb); self.remove(self.hdr_d)
        self.end_card(6, "Bound it first, then count.")


class Pow(MathReel):
    EVENTS = "pow"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        # ===== 0. Which is bigger: 2^100 or 3^63? =====
        self.add(self.hdr); lb = self.label("JEE Main", False); self.add(lb)
        q1 = at(H("Which is bigger?", 100, INK), 320)
        a1 = M(r"2^{100}", 200); a2 = M(r"3^{63}", 200, OR); vs = B("vs", 48, GREY_P, SEMIBOLD)
        row = VGroup(a1, vs, a2).arrange(RIGHT, buff=0.8); cx(row, 700)
        self.add(q1, row)

        # ===== 1. Comment your pick. No calculator. =====
        bub = VGroup(RoundedRectangle(width=px(888), height=px(120), corner_radius=0.2, fill_color=INK, fill_opacity=1, stroke_width=0))
        bub.add(B("Comment your pick before you scroll", 38, WHITE_, SEMIBOLD).move_to(bub[0])); cx(bub, 1060)
        tail = Polygon([X(180), Y(1120), 0], [X(230), Y(1120), 0], [X(170), Y(1160), 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        self.until(wt(1, 0, 0.1)); self.ev("tick"); self.play(FadeIn(bub, shift=UP * 0.2), FadeIn(tail, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        nc = self.chip("No calculator", size=36); cx(nc, 1260)
        self.until(wt(1, 3, 0.1)); self.ev("tick"); self.play(GrowFromCenter(nc), run_time=0.3)

        # ===== 2. Take log base 10: 100 log 2 vs 63 log 3 =====
        self.until(S[2])
        tl = self.chip("take log base 10", size=38); cx(tl, 520)
        l1 = M(r"100\log 2", 120); l2 = M(r"63\log 3", 120, OR); vs2 = B("vs", 48, GREY_P, SEMIBOLD)
        lrow = VGroup(l1, vs2, l2).arrange(RIGHT, buff=0.7); fitw(lrow, 900); cx(lrow, 720)
        self.ev("tick")
        self.play(FadeOut(VGroup(q1, bub, tail, nc), shift=UP * 0.2), FadeIn(tl, shift=DOWN * 0.1), ReplacementTransform(a1, l1), ReplacementTransform(a2, l2), ReplacementTransform(vs, vs2), run_time=0.55, rate_func=EXPO)
        g2 = M(r"\log 2=0.3010", 80); cx(g2, 980)
        g3 = M(r"\log 3=0.4771", 80, OR); cx(g3, 1130)
        self.until(wt(2, 4, 0.1)); self.ev("tick"); self.play(FadeIn(g2, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        self.until(wt(2, 8, 0.1)); self.ev("tick"); self.play(FadeIn(g3, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)

        # ===== 3. So the logs are 30.10 and 30.06 (zoomed number line) =====
        self.until(S[3])
        m1 = M(r"100\times0.3010=30.10", 72); cx(m1, 620)
        m2 = M(r"63\times0.4771=30.06", 72, OR); cx(m2, 760)
        self.play(FadeOut(VGroup(tl, lrow, g2, g3), shift=UP * 0.2), run_time=0.3)
        self.until(wt(3, 4, 0.1)); self.ev("tick"); self.play(FadeIn(m1, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        self.until(wt(3, 6, 0.1)); self.ev("tick"); self.play(FadeIn(m2, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        nl = NumberLine(x_range=[30.0, 30.15, 0.05], length=px(860), color=INK, stroke_width=4, include_numbers=False, include_tip=False)
        cx(nl, 1000)
        nlab = VGroup(*[B(f"{v:.2f}", 36, GREY_P).next_to(nl.n2p(v), DOWN, buff=0.15) for v in (30.0, 30.05, 30.10, 30.15)])
        p1 = Dot(nl.n2p(30.103), radius=px(16), color=INK).set_z_index(5); p2 = Dot(nl.n2p(30.0586), radius=px(16), color=OR).set_z_index(5)
        pl1 = M(r"2^{100}", 68).next_to(p1, UP, buff=0.22); pl2 = M(r"3^{63}", 68, OR).next_to(p2, UP, buff=0.22)
        zt = B("zoomed in", 32, OR, SEMIBOLD).next_to(nl, UP, buff=1.1).align_to(nl, LEFT)
        self.play(Create(nl), FadeIn(nlab), FadeIn(zt), GrowFromCenter(p1), GrowFromCenter(p2), FadeIn(pl1), FadeIn(pl2), run_time=0.5)

        # ===== 4. Bigger log, bigger number. 2^100 wins. =====
        self.until(S[4])
        ans = M(r"2^{100}>3^{63}", 130); ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 1290)
        self.until(wt(4, 4, 0.12)); self.ev("stamp"); self.play(GrowFromCenter(a_), run_time=0.45, rate_func=rate_functions.ease_out_back)

        # ===== 5. Both have 31 digits. That's why it feels so close. =====
        self.until(S[5])
        self.play(FadeOut(VGroup(m1, m2, nl, nlab, zt, p1, p2, pl1, pl2), shift=UP * 0.2), a_.animate.scale(0.7).move_to([0, Y(420), 0]), run_time=0.4, rate_func=EXPO)
        n1 = str(2 ** 100); n2 = str(3 ** 63)
        s1 = " ".join([n1[:1]] + [n1[i:i + 3] for i in range(1, len(n1), 3)])
        s2 = " ".join([n2[:1]] + [n2[i:i + 3] for i in range(1, len(n2), 3)])
        r1 = VGroup(M(r"2^{100}=", 54), B(s1, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=0.2)
        r2 = VGroup(M(r"3^{63}=", 54, OR), B(s2, 34, OR, SEMIBOLD)).arrange(RIGHT, buff=0.2)
        for r in (r1, r2): fitw(r, 900)
        cx(r1, 760); cx(r2, 900)
        d31 = self.chip("31 digits each", size=38); cx(d31, 1080)
        self.ev("tick"); self.play(FadeIn(r1, shift=UP * 0.2), FadeIn(r2, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.until(wt(5, 2, 0.1)); self.ev("tick"); self.play(GrowFromCenter(d31), run_time=0.3)
        cl = at(SER("Logs settle it in two lines.", 84, OR), 1300); fitw(cl, 888)
        self.until(wt(5, 7, 0.1)); self.play(FadeIn(cl, shift=UP * 0.2), run_time=0.35)

        # ===== 6. End =====
        self.until(S[6])
        self.to(INK, a_, r1, r2, d31, cl, lb); self.remove(self.hdr_d)
        self.end_card(6, "Compare the logs, not the numbers.")


class Motiv(MathReel):
    EVENTS = "motiv"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        RD = "#E5484D"
        # ===== 0. Bad mock score today? (visible on frame 0) =====
        self.add(self.hdr); lb = self.label("For JEE aspirants", False); self.add(lb)
        h1 = at(H("Bad mock score", 104, INK), 330); h2 = at(H("today?", 104, INK), 450)
        sc = [132, 141, 138, 150, 156, 121]
        cd = RoundedRectangle(width=px(860), height=px(470), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3); cx(cd, 870)
        ma = Axes(x_range=[0, 5.4, 1], y_range=[100, 170, 20], x_length=px(700), y_length=px(300), tips=False, axis_config={"color": RULE, "stroke_width": 3})
        ma.move_to(cd.get_center() + DOWN * px(20))
        pts = [ma.c2p(i, v) for i, v in enumerate(sc)]
        ml = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts[:-1])
        md = VMobject(stroke_color=RD, stroke_width=6).set_points_as_corners(pts[-2:])
        dots = VGroup(*[Dot(p, radius=px(10), color=INK) for p in pts[:-1]], Dot(pts[-1], radius=px(13), color=RD))
        tl = B("today", 32, RD, SEMIBOLD).next_to(pts[-1], DOWN, buff=0.18)
        ct = B("Your mock scores", 30, GREY_P, SEMIBOLD).next_to(cd.get_corner(UL), DR, buff=0.3)
        self.add(h1, h2, cd, ma, ml, md, dots, tl, ct)

        # ===== 1. Here's the maths that should calm you down. =====
        self.until(S[1])
        hm = at(SER("Here's the maths.", 110, OR), 1290); fitw(hm, 900)
        self.ev("tick"); self.play(FadeIn(hm, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)

        # ===== 2. 1% better every day: 1.01^365 ~ 37.8 =====
        self.until(S[2])
        ax = Axes(x_range=[0, 365, 73], y_range=[0, 40, 10], x_length=px(860), y_length=px(700), tips=False, axis_config={"color": INK, "stroke_width": 3})
        ax.move_to([X(560), Y(940), 0])
        xl = VGroup(B("day 0", 30, GREY_P).next_to(ax.c2p(0, 0), DOWN, buff=0.15), B("day 365", 30, GREY_P).next_to(ax.c2p(365, 0), DOWN, buff=0.15))
        e1 = M(r"1.01^{365}\approx 37.8", 84); cx(e1, 330)
        self.ev("tick")
        self.play(FadeOut(VGroup(h1, h2, cd, ma, ml, md, dots, tl, ct, hm), shift=UP * 0.2), Create(ax), FadeIn(xl), run_time=0.45, rate_func=EXPO)
        g1 = ax.plot(lambda x: 1.01 ** x, x_range=[0, 365], color=OR, stroke_width=8)
        cnt = DecimalNumber(1.0, num_decimal_places=1, font_size=96, color=OR).move_to([X(330), Y(560), 0])
        cx_ = M(r"\times", 80, OR).next_to(cnt, LEFT, buff=0.15)
        trk = ValueTracker(0)
        cnt.add_updater(lambda m: m.set_value(1.01 ** trk.get_value()))
        self.until(wt(2, 0, 0.05)); self.add(cnt, cx_)
        self.play(Create(g1), trk.animate.set_value(365), run_time=2.4, rate_func=rate_functions.ease_in_quad)
        cnt.clear_updaters()
        self.until(wt(2, 7, 0.1)); self.ev("tick"); self.play(FadeIn(e1, shift=DOWN * 0.2), run_time=0.35, rate_func=EXPO)
        big = VGroup(M(r"\times", 70, OR), H("37.8", 110, OR)).arrange(RIGHT, buff=0.12).next_to(ax.c2p(365, 37.8), LEFT, buff=0.35)
        self.until(wt(2, 10, 0.1)); self.ev("stamp")
        self.play(ReplacementTransform(VGroup(cnt, cx_), big), run_time=0.45, rate_func=rate_functions.ease_out_back)

        # ===== 3. 1% worse every day: 0.99^365 ~ 0.03 =====
        self.until(S[3])
        g2 = ax.plot(lambda x: 0.99 ** x, x_range=[0, 365], color=RD, stroke_width=8)
        e2 = M(r"0.99^{365}\approx 0.03", 84, RD); cx(e2, 450)
        self.ev("tick"); self.play(Create(g2), run_time=1.0, rate_func=rate_functions.ease_in_out_sine)
        self.until(wt(3, 4, 0.1)); self.play(FadeIn(e2, shift=DOWN * 0.2), run_time=0.35, rate_func=EXPO)
        sm = VGroup(M(r"\times", 56, RD), H("0.03", 70, RD)).arrange(RIGHT, buff=0.1).next_to(ax.c2p(365, 0), UP, buff=0.3).align_to(big, RIGHT)
        self.until(wt(3, 5, 0.1)); self.ev("tick"); self.play(FadeIn(sm, shift=UP * 0.15), run_time=0.3)

        # ===== 4. The gap isn't talent. It's 1%, every single day. =====
        self.until(S[4])
        br = DoubleArrow(ax.c2p(250, 0.3), ax.c2p(250, 1.01 ** 250 - 0.7), color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.08)
        gl = B("the gap", 40, INK, SEMIBOLD).next_to(ax.c2p(250, 6.5), RIGHT, buff=0.25)
        gp = at(SER("Not talent. 1% a day.", 92, INK), 1420); fitw(gp, 900)
        self.ev("tick"); self.play(GrowArrow(br), FadeIn(gl, shift=LEFT * 0.1), run_time=0.45)
        self.until(wt(4, 4, 0.1)); self.play(FadeIn(gp, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)

        # ===== 5. One mock is a single point. Your preparation is the whole curve. =====
        self.until(S[5])
        ms = [96, 104, 99, 112, 118, 109, 121, 130, 124, 137, 141, 122, 146, 151, 144, 158, 163, 155, 169, 174]
        ax2 = Axes(x_range=[0, 21, 5], y_range=[80, 190, 20], x_length=px(860), y_length=px(640), tips=False, axis_config={"color": INK, "stroke_width": 3})
        ax2.move_to([X(560), Y(900), 0])
        t2 = B("Mock tests (illustration)", 30, GREY_P, SEMIBOLD).next_to(ax2.c2p(0, 190), RIGHT, buff=0.2)
        p2 = [ax2.c2p(i + 1, v) for i, v in enumerate(ms)]
        ln2 = VMobject(stroke_color=GREY_P, stroke_width=4).set_points_as_corners(p2)
        d2 = VGroup(*[Dot(p, radius=px(9), color=INK) for p in p2])
        self.play(FadeOut(VGroup(ax, xl, g1, g2, e1, e2, big, sm, br, gl, gp), shift=UP * 0.2), Create(ax2), FadeIn(t2), run_time=0.4, rate_func=EXPO)
        self.ev("tick"); self.play(Create(ln2), LaggedStart(*[GrowFromCenter(d) for d in d2], lag_ratio=0.05), run_time=0.9)
        ring = Circle(radius=px(34), color=RD, stroke_width=6).move_to(p2[11])
        rl = B("one bad day", 32, RD, SEMIBOLD).next_to(ring, DOWN, buff=0.15)
        self.until(wt(5, 4, 0.1)); self.ev("tick"); self.play(Create(ring), FadeIn(rl), d2[11].animate.set_color(RD), run_time=0.4)
        k, b0 = np.polyfit(np.arange(1, 21), ms, 1)
        tr = Line(ax2.c2p(0.5, k * 0.5 + b0), ax2.c2p(20.5, k * 20.5 + b0), color=OR, stroke_width=10)
        trl = B("your curve", 36, OR, SEMIBOLD).next_to(ax2.c2p(16, k * 16 + b0), UP, buff=0.55).shift(LEFT * 0.6)
        self.until(wt(5, 9, 0.1)); self.ev("chime"); self.play(Create(tr), FadeIn(trl), run_time=0.6, rate_func=EXPO)

        # ===== 6. End =====
        self.until(S[6])
        self.to(INK, ax2, t2, ln2, d2, ring, rl, tr, trl, lb); self.remove(self.hdr_d)
        self.end_card(6, "Keep showing up.")


# ---------------- Short format (from the sin x insights, 20 Oct): moving hook on frame 0, on-screen comment prompt,
# series tag, answer near the end, 1 s brand flash instead of an end card. ----------------
class ShortReel(MathReel):
    SERIES = "JEE in 20s"
    def options_row(self, vals, y, tex=True):
        row = VGroup()
        for L, v in zip("ABCD", vals):
            c_ = RoundedRectangle(width=px(200), height=px(104), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            t_ = VGroup(B(L, 34, OR, SEMIBOLD), (M(v, 52) if tex else H(v, 40, INK))).arrange(RIGHT, buff=0.22)
            if t_.width > px(184): t_.scale_to_fit_width(px(184))
            t_.move_to(c_)
            row.add(VGroup(c_, t_))
        row.arrange(RIGHT, buff=px(22)); cx(row, y); return row
    def comment_chip(self, s="Comment A, B, C or D"):
        g = VGroup(RoundedRectangle(width=px(560), height=px(76), corner_radius=0.18, fill_color=INK, fill_opacity=1, stroke_width=0))
        g.add(B(s, 32, WHITE_, SEMIBOLD).move_to(g[0])); cx(g, 1410); return g
    def brand_flash(self, *gone):
        C = K.C
        self.until(K.DUR - 0.95); self.to(INK, *gone); self.remove(self.hdr_d)
        wm = wordmark(px(640), dark=True).move_to([0, Y(820), 0]); url = H("tutorda.org", 84, OR).move_to([0, Y(1000), 0])
        self.ev("wordmark"); self.play(FadeIn(wm, shift=UP * 0.2), FadeIn(url, shift=UP * 0.2), run_time=0.2, rate_func=EXPO)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class Cubic(ShortReel):
    EVENTS = "cubic"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        RD = "#E5484D"; f = lambda x: x ** 3 - 3 * x + 1
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = at(H("How many real roots?", 88, INK), 290); fitw(q, 900)
        eq = M(r"x^3-3x+1=0", 120); cx(eq, 430)
        opts = self.options_row(["1", "2", "3", "0"], 575)
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-4, 5, 1], x_length=px(880), y_length=px(640), tips=False, axis_config={"color": INK, "stroke_width": 3})
        ax.move_to([X(540), Y(1010), 0])
        g = ax.plot(f, x_range=[-2.2, 2.05], color=OR, stroke_width=8)
        self.add(q, eq, opts, ax)
        # ===== 0. curve is already drawing on frame 0 =====
        cc = self.comment_chip()
        self.play(Create(g), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. turning points: f'(x) = 3x^2 - 3 = 0 at x = +-1 =====
        self.until(S[1])
        d1 = M(r"f'(x)=3x^2-3=0", 84); cx(d1, 430)
        self.ev("tick"); self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), eq.animate.scale(0.6).move_to([0, Y(300), 0]), run_time=0.35, rate_func=EXPO)
        self.until(wt(1, 4, 0.1)); self.play(FadeIn(d1, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        v1 = DashedLine(ax.c2p(-1, -4), ax.c2p(-1, 5), color=GREY_P, stroke_width=3); v2 = DashedLine(ax.c2p(1, -4), ax.c2p(1, 5), color=GREY_P, stroke_width=3)
        xl = VGroup()
        d1b = M(r"x=\pm1", 84, OR); cx(d1b, 545)
        self.until(wt(1, 10, 0.1)); self.ev("tick"); self.play(Create(v1), Create(v2), FadeIn(d1b, shift=UP * 0.15), run_time=0.4)
        # ===== 2. f(-1) = 3: above the axis =====
        self.until(S[2])
        p1 = Dot(ax.c2p(-1, 3), radius=px(16), color=INK).set_z_index(5)
        l1 = M(r"f(-1)=3", 52).next_to(p1, UP, buff=0.2)
        self.until(wt(2, 4, 0.1)); self.ev("tick"); self.play(GrowFromCenter(p1), FadeIn(l1, shift=DOWN * 0.1), run_time=0.3)
        a1 = B("above", 34, INK, SEMIBOLD).next_to(p1, LEFT, buff=0.3)
        self.until(wt(2, 5, 0.1)); self.play(FadeIn(a1), run_time=0.25)
        # ===== 3. f(1) = -1: below the axis =====
        self.until(S[3])
        p2 = Dot(ax.c2p(1, -1), radius=px(16), color=RD).set_z_index(5)
        l2 = M(r"f(1)=-1", 48, RD).move_to(ax.c2p(1.7, -2.6))
        self.until(wt(3, 4, 0.1)); self.ev("tick"); self.play(GrowFromCenter(p2), FadeIn(l2, shift=UP * 0.1), run_time=0.3)
        a2 = B("below", 34, RD, SEMIBOLD).next_to(l2, DOWN, buff=0.15)
        self.until(wt(3, 5, 0.1)); self.play(FadeIn(a2), run_time=0.25)
        # ===== 4. up, down, up: three crossings =====
        self.until(S[4])
        segs = [ax.plot(f, x_range=r, color=INK, stroke_width=12) for r in ((-2.2, -1), (-1, 1), (1, 2.05))]
        for k in range(3):
            self.until(wt(4, k, 0.05)); self.play(ShowPassingFlash(segs[k].copy().set_color(INK), time_width=0.6), run_time=0.35)
        roots = [-1.8793852415718, 0.3472963553338, 1.5320888862380]
        rd = [Dot(ax.c2p(r, 0), radius=px(14), color=OR).set_z_index(6) for r in roots]
        self.until(wt(4, 6, 0.1)); self.ev("tick"); self.play(FadeOut(cc), LaggedStart(*[GrowFromCenter(d) for d in rd], lag_ratio=0.3), run_time=0.6)
        # ===== 5. Three real roots. Follow for #6 =====
        self.until(S[5])
        ans = VGroup(H("3", 150, OR), B("real roots", 48, INK, SEMIBOLD)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 430)
        self.ev("stamp"); self.play(FadeOut(VGroup(d1, d1b)), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(wt(5, 3, 0.1) if len(K.WT) > 5 else C[5] + 1.0); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(eq, a_, ax, g, v1, v2, xl, p1, l1, a1, p2, l2, a2, *rd, fw, lb)


class Area(ShortReel):
    EVENTS = "area"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = VGroup(H("What fraction of the square", 64, INK), H("is under the curve?", 64, INK)).arrange(DOWN, buff=0.18); fitw(q, 880); cx(q, 300)
        opts = self.options_row([r"\frac12", r"\frac13", r"\frac14", r"\frac23"], 480)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=px(700), y_length=px(700), tips=False, axis_config={"color": INK, "stroke_width": 3})
        ax.move_to([X(540), Y(990), 0])
        sq = Rectangle(width=px(700), height=px(700), stroke_color=INK, stroke_width=3).move_to(ax.c2p(0.5, 0.5))
        g = ax.plot(lambda x: x * x, x_range=[0, 1], color=OR, stroke_width=8)
        area = ax.get_area(g, x_range=[0, 1], color=OR, opacity=0.28)
        tl = VGroup(B("0", 30, GREY_P).next_to(ax.c2p(0, 0), DL, buff=0.1), B("1", 30, GREY_P).next_to(ax.c2p(1, 0), DOWN, buff=0.12), B("1", 30, GREY_P).next_to(ax.c2p(0, 1), LEFT, buff=0.12))
        gl = M(r"y=x^2", 52, OR).move_to(ax.c2p(0.62, 0.72))
        self.add(q, opts, ax, sq, tl)
        # ===== 0. curve + shaded area appear on frame 0 =====
        cc = self.comment_chip()
        self.play(Create(g), FadeIn(gl), run_time=1.1, rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(area), run_time=0.4); self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        rd = M(r"", 10)
        def rects(n):
            return VGroup(*[Rectangle(width=ax.c2p(1 / n, 0)[0] - ax.c2p(0, 0)[0], height=max(1e-4, ax.c2p(0, (k / n) ** 2)[1] - ax.c2p(0, 0)[1]),
                    stroke_color=INK, stroke_width=(3 if n <= 10 else 0.6), fill_color=INK, fill_opacity=0.18).move_to(ax.c2p((k + 0.5) / n, (k / n) ** 2 / 2))
                    for k in range(n)])
        def readout(n, v):
            return VGroup(M(r"n=" + str(n), 64), M(r"\Rightarrow", 64, GREY_P), M(v, 80, OR)).arrange(RIGHT, buff=0.35)
        # ===== 1. Fill it with rectangles. 4 rectangles give 0.22. =====
        self.until(S[1])
        self.ev("tick"); self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), area.animate.set_opacity(0.08), run_time=0.3)
        r4 = rects(4); o4 = readout(4, "0.22"); cx(o4, 400)
        self.until(wt(1, 4, 0.1)); self.ev("tick"); self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in r4], lag_ratio=0.15), FadeIn(o4), run_time=0.5)
        # ===== 2. 10 give 0.285. 100 give 0.328. =====
        self.until(S[2])
        r10 = rects(10); o10 = readout(10, "0.285"); cx(o10, 400)
        self.ev("tick"); self.play(ReplacementTransform(r4, r10), ReplacementTransform(o4, o10), run_time=0.4)
        r100 = rects(100); o100 = readout(100, "0.328"); cx(o100, 400)
        self.until(wt(2, 3, 0.1)); self.ev("tick"); self.play(ReplacementTransform(r10, r100), ReplacementTransform(o10, o100), run_time=0.4)
        # ===== 3. They close in on 1/3: the integral of x^2 from 0 to 1 =====
        self.until(S[3])
        o3 = M(r"\to\ \tfrac13", 96, OR).next_to(o100, DOWN, buff=0.25)
        self.ev("tick"); self.play(FadeIn(o3, shift=LEFT * 0.2), run_time=0.3)
        it = M(r"\int_0^1 x^2\,dx=\tfrac13", 92); cx(it, 400)
        self.until(wt(3, 7, 0.1)); self.play(FadeOut(VGroup(o100, o3), shift=UP * 0.2), FadeOut(r100), area.animate.set_opacity(0.32), FadeIn(it, shift=UP * 0.2), run_time=0.45, rate_func=EXPO)
        # ===== 4. 1/3, not a half. Follow for #7 =====
        self.until(S[4])
        ans = VGroup(M(r"\tfrac13", 150, OR), B("not ½", 48, GREY_P, SEMIBOLD)).arrange(RIGHT, buff=0.4)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)).move_to(ax.c2p(0.32, 0.72))
        self.ev("stamp"); self.play(FadeOut(cc), FadeOut(gl), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.1); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(it, a_, ax, sq, g, area, gl, tl, fw, lb)


def die(n, s=150, color=None):
    sq = RoundedRectangle(width=px(s), height=px(s), corner_radius=px(s) * 0.0028 * 18, fill_color=WHITE_, fill_opacity=1, stroke_color=INK, stroke_width=4)
    P = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)], 4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
         5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)], 6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}
    d = px(s) * 0.27
    pips = VGroup(*[Dot([x * d, y * d, 0], radius=px(s) * 0.085, color=color or INK) for x, y in P[n]])
    return VGroup(sq, pips)


class Dice(ShortReel):
    EVENTS = "dice"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = VGroup(H("Two dice. Which total", 76, INK), H("comes up most?", 76, INK)).arrange(DOWN, buff=0.15); fitw(q, 880); cx(q, 300)
        d1 = die(3).move_to([X(430), Y(560), 0]); d2 = die(5).move_to([X(650), Y(560), 0])
        opts = self.options_row(["6", "7", "8", "12"], 760)
        self.add(q, opts)
        # ===== 0. dice tumble in on frame 0 =====
        cc = self.comment_chip()
        self.play(FadeIn(d1, shift=DOWN * 0.6), FadeIn(d2, shift=DOWN * 0.6), Rotate(d1, PI / 2), Rotate(d2, -PI / 2), run_time=0.8, rate_func=EXPO)
        self.play(Transform(d1, die(6).move_to(d1)), Transform(d2, die(1).move_to(d2)), run_time=0.35)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. 36 equally likely pairs: the grid =====
        self.until(S[1])
        N = 6; cs = px(100); x0, y0 = X(540) - 3 * cs + cs / 2, Y(1010) + 3 * cs - cs / 2
        cells, nums = VGroup(), VGroup()
        for i in range(N):
            for j in range(N):
                c_ = Square(side_length=cs, stroke_color=RULE, stroke_width=2, fill_color=WHITE_, fill_opacity=1).move_to([x0 + j * cs, y0 - i * cs, 0])
                cells.add(c_); nums.add(B(str(i + j + 2), 34, INK, SEMIBOLD).move_to(c_))
        hdr_r = VGroup(*[die(j + 1, 64).move_to([x0 + j * cs, y0 + cs * 0.95, 0]) for j in range(N)])
        hdr_c = VGroup(*[die(i + 1, 64).move_to([x0 - cs * 0.95, y0 - i * cs, 0]) for i in range(N)])
        self.ev("tick"); self.play(FadeOut(VGroup(q, opts, d1, d2), shift=UP * 0.2), FadeIn(hdr_r), FadeIn(hdr_c), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), run_time=0.6)
        n36 = VGroup(H("36", 120, OR), B("equally likely pairs", 40, INK, SEMIBOLD)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN); cx(n36, 420)
        self.until(wt(1, 2, 0.1)); self.ev("tick"); self.play(FadeIn(n36, shift=UP * 0.2), FadeIn(nums), run_time=0.4)
        # ===== 2. colour by total; the sevens are the whole diagonal =====
        self.until(S[2])
        shade = [interpolate_color(ManimColor(WHITE_), ManimColor(OR), 0.12 + 0.13 * (6 - abs(i + j + 2 - 7))) for i in range(N) for j in range(N)]
        self.play(*[c.animate.set_fill(sh) for c, sh in zip(cells, shade)], run_time=0.5)
        diag = [i * N + (5 - i) for i in range(N)]
        self.until(wt(2, 7, 0.1)); self.ev("tick")
        self.play(*[cells[k].animate.set_fill(OR, 1) for k in diag], *[nums[k].animate.set_color(WHITE_) for k in diag], run_time=0.4)
        # ===== 3. six ways to make 7; only five for 6 or 8 (bar chart replaces the 36 line) =====
        self.until(S[3])
        cnt = [6 - abs(s - 7) for s in range(2, 13)]; bw = px(64)
        bars = VGroup(*[Rectangle(width=bw * 0.82, height=px(30) * c, stroke_width=0, fill_color=(OR if s == 7 else GREY_P), fill_opacity=(1 if s == 7 else 0.45)) for s, c in zip(range(2, 13), cnt)])
        for k, b in enumerate(bars): b.move_to([X(540) + (k - 5) * bw, Y(560) - b.height / 2 * 0 + 0, 0]).align_to([0, Y(560), 0], DOWN)
        bl = VGroup(*[B(str(s), 26, GREY_P).next_to(b, DOWN, buff=0.08) for s, b in zip(range(2, 13), bars)])
        six = B("6 ways", 34, OR, SEMIBOLD).next_to(bars[5], UP, buff=0.1)
        self.ev("tick"); self.play(FadeOut(n36, shift=UP * 0.2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), FadeIn(bl), FadeIn(six), run_time=0.6)
        five = VGroup(B("5", 30, INK, SEMIBOLD).next_to(bars[4], UP, buff=0.08), B("5", 30, INK, SEMIBOLD).next_to(bars[6], UP, buff=0.08))
        self.until(wt(3, 6, 0.1)); self.play(FadeIn(five), bars[4].animate.set_fill(opacity=0.8), bars[6].animate.set_fill(opacity=0.8), run_time=0.3)
        # ===== 4. 7, with a 1 in 6 chance. Follow for #8 =====
        self.until(S[4])
        ans = VGroup(H("7", 150, OR), M(r"P=\tfrac{6}{36}=\tfrac16", 64)).arrange(RIGHT, buff=0.45)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 470)
        self.ev("stamp"); self.play(FadeOut(VGroup(bars, bl, six, five)), FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.1); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, cells, nums, hdr_r, hdr_c, fw, lb)


class RectCircle(ShortReel):
    EVENTS = "rect"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = VGroup(H("Biggest rectangle", 80, INK), H("inside a circle?", 80, INK)).arrange(DOWN, buff=0.15); fitw(q, 880); cx(q, 300)
        opts = self.options_row(["r^2", "2r^2", "3r^2", r"\pi r^2"], 480)
        R = px(330); ctr = np.array([X(540), Y(1000), 0])
        circ = Circle(radius=R, color=INK, stroke_width=5).move_to(ctr)
        th = ValueTracker(20 * DEGREES)
        def corner(): return ctr + R * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])
        rect = always_redraw(lambda: Rectangle(width=2 * R * np.cos(th.get_value()), height=2 * R * np.sin(th.get_value()), stroke_color=OR, stroke_width=7, fill_color=OR, fill_opacity=0.15).move_to(ctr))
        self.add(q, opts, circ, rect)
        # ===== 0. rectangle already reshaping on frame 0 =====
        cc = self.comment_chip("Comment A, B, C or D")
        self.play(th.animate.set_value(68 * DEGREES), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.ev("tick"); self.play(th.animate.set_value(30 * DEGREES), FadeIn(cc, shift=UP * 0.15), run_time=0.6)
        # ===== 1. one corner on the circle at angle theta =====
        self.until(S[1])
        dot = always_redraw(lambda: Dot(corner(), radius=px(14), color=INK).set_z_index(5))
        rad = always_redraw(lambda: Line(ctr, corner(), color=INK, stroke_width=4))
        arc = always_redraw(lambda: Arc(radius=px(70), start_angle=0, angle=th.get_value(), arc_center=ctr, color=INK, stroke_width=4))
        thl = always_redraw(lambda: M(r"\theta", 46).move_to(ctr + px(110) * np.array([np.cos(th.get_value() / 2), np.sin(th.get_value() / 2), 0])))
        rl = M(r"r", 46).move_to(ctr + R * 0.55 * np.array([np.cos(30 * DEGREES), np.sin(30 * DEGREES), 0]) + UP * 0.35)
        self.ev("tick"); self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), FadeIn(dot), Create(rad), FadeIn(rl), run_time=0.4)
        self.until(wt(1, 6, 0.1)); self.play(Create(arc), FadeIn(thl), run_time=0.35)
        # ===== 2. width 2r cos theta, height 2r sin theta =====
        self.until(S[2])
        wl = always_redraw(lambda: M(r"2r\cos\theta", 50, OR).next_to(ctr + DOWN * R * np.sin(th.get_value()), DOWN, buff=0.15))
        hl = always_redraw(lambda: M(r"2r\sin\theta", 50, OR).rotate(PI / 2).next_to(ctr + LEFT * R * np.cos(th.get_value()), RIGHT, buff=0.15))
        self.ev("tick"); self.play(FadeIn(wl), run_time=0.3)
        self.until(wt(2, 4, 0.1)); self.ev("tick"); self.play(FadeIn(hl), FadeOut(rl), run_time=0.3)
        # ===== 3. area = 2r^2 sin 2theta, peaks at 45 degrees =====
        self.until(S[3])
        af = M(r"A=2r^2\sin2\theta", 84); cx(af, 400)
        rd = always_redraw(lambda: VGroup(M(r"\sin2\theta=", 56, GREY_P), DecimalNumber(np.sin(2 * th.get_value()), num_decimal_places=2, font_size=64, color=OR)).arrange(RIGHT, buff=0.2).move_to([X(540), Y(530), 0]))
        self.ev("tick"); self.play(FadeIn(af, shift=UP * 0.2), FadeIn(rd), run_time=0.35)
        self.play(th.animate.set_value(66 * DEGREES), run_time=0.9, rate_func=rate_functions.ease_in_out_sine)
        self.until(wt(3, 8, 0.15)); self.play(th.animate.set_value(45 * DEGREES), run_time=0.6, rate_func=EXPO)
        thl.clear_updaters(); d45 = B("45°", 40, OR, SEMIBOLD).move_to(thl).shift(RIGHT * 0.15)
        self.ev("tick"); self.play(ReplacementTransform(thl, d45), run_time=0.3)
        # ===== 4. A square, area 2r^2. Follow for #9 =====
        self.until(S[4])
        ans = VGroup(B("Square", 56, INK, SEMIBOLD), M(r"A=2r^2", 96, OR)).arrange(RIGHT, buff=0.45)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 470)
        self.ev("stamp"); self.play(FadeOut(VGroup(af, rd)), FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.2); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        for m in (rect, dot, rad, arc, wl, hl): m.clear_updaters()
        self.brand_flash(a_, circ, rect, dot, rad, arc, wl, hl, d45, fw, lb)


class SinLim(ShortReel):
    EVENTS = "sinlim"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = M(r"\lim_{x\to0}\frac{\sin x}{x}=\,?", 120); cx(q, 330)
        opts = self.options_row(["0", "1", r"\infty", r"\text{none}"], 540)
        R = px(380); O = np.array([X(380), Y(1180), 0])
        xv = ValueTracker(0.95)
        def P(): return O + R * np.array([np.cos(xv.get_value()), np.sin(xv.get_value()), 0])
        def Tp(): return O + R * np.array([1, np.tan(xv.get_value()), 0])
        A = O + R * RIGHT
        arc = Arc(radius=R, start_angle=-0.1, angle=PI / 2 + 0.1, arc_center=O, color=INK, stroke_width=4)
        axl = VGroup(Line(O + LEFT * px(40), O + RIGHT * (R + px(60)), color=INK, stroke_width=3), Line(O + DOWN * px(40), O + UP * (R + px(60)), color=INK, stroke_width=3))
        rad = always_redraw(lambda: Line(O, Tp(), color=INK, stroke_width=4))
        self.add(q, opts, axl, arc, rad)
        cc = self.comment_chip()
        # ===== 0. the angle is already moving on frame 0 =====
        self.play(xv.animate.set_value(0.7), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. three areas, one inside the next =====
        self.until(S[1])
        t1 = always_redraw(lambda: Polygon(O, A, P(), stroke_color="#14B8A6", stroke_width=4, fill_color="#14B8A6", fill_opacity=0.45))
        sec = always_redraw(lambda: Sector(radius=R, angle=xv.get_value(), arc_center=O, stroke_color=OR, stroke_width=4, fill_color=OR, fill_opacity=0.25))
        t2 = always_redraw(lambda: Polygon(O, A, Tp(), stroke_color=GREY_P, stroke_width=3, fill_color=GREY_P, fill_opacity=0.12))
        tline = always_redraw(lambda: Line(A, Tp(), color=GREY_P, stroke_width=4))
        self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), run_time=0.3)
        self.until(wt(1, 4, 0.1)); self.ev("tick"); self.play(LaggedStart(FadeIn(t2), FadeIn(sec), FadeIn(t1), lag_ratio=0.35), Create(tline), run_time=0.7)
        # ===== 2. sin x, then x, then tan x =====
        self.until(S[2])
        iq = [M(r"\sin x", 96, "#14B8A6"), M(r"<", 96, GREY_P), M(r"x", 96, OR), M(r"<", 96, GREY_P), M(r"\tan x", 96, GREY_P)]
        row = VGroup(*iq).arrange(RIGHT, buff=0.3); cx(row, 420)
        for k, (w_, items) in enumerate(((0, [0]), (3, [1, 2]), (5, [3, 4]))):
            self.until(wt(2, w_, 0.08)); self.ev("tick")
            self.play(*[FadeIn(iq[i], shift=UP * 0.15) for i in items], Indicate([t1, sec, t2][k], color=None, scale_factor=1.03), run_time=0.3)
        # ===== 3. cos x < sin x / x < 1 =====
        self.until(S[3])
        sq = M(r"\cos x<\frac{\sin x}{x}<1", 100); cx(sq, 420)
        self.ev("tick"); self.play(ReplacementTransform(row, sq), run_time=0.5, rate_func=EXPO)
        # ===== 4. as x shrinks, cos x climbs to 1 (live values) =====
        self.until(S[4])
        live = always_redraw(lambda: VGroup(
            VGroup(M(r"\cos x", 44, GREY_P), DecimalNumber(np.cos(xv.get_value()), num_decimal_places=3, font_size=60, color=INK)).arrange(DOWN, buff=0.12),
            VGroup(M(r"\tfrac{\sin x}{x}", 44, GREY_P), DecimalNumber(np.sin(xv.get_value()) / xv.get_value(), num_decimal_places=3, font_size=60, color=OR)).arrange(DOWN, buff=0.12),
            VGroup(M(r"1", 44, GREY_P), DecimalNumber(1.0, num_decimal_places=3, font_size=60, color=INK)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=0.9).move_to([X(540), Y(680), 0]))
        self.add(live); self.ev("tick")
        self.play(xv.animate.set_value(0.05), run_time=max(0.8, C[5] - self.Tm() - 0.15), rate_func=rate_functions.ease_in_out_sine)
        # ===== 5. squeezed to 1. Follow for #10 =====
        self.until(S[5])
        ans = M(r"\lim_{x\to0}\frac{\sin x}{x}=1", 96)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 420)
        self.ev("stamp"); self.play(FadeOut(sq), FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[5] + 0.9); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        for m in (rad, t1, sec, t2, tline, live): m.clear_updaters()
        self.brand_flash(a_, axl, arc, rad, t1, sec, t2, tline, live, fw, lb)


class Groups4(ShortReel):
    EVENTS = "groups"; SERIES = "CSIR-NET in 20s"
    def table(self, labels, prod, title, cs=px(84)):
        col = {"e": WHITE_, "a": "#FFC83D", "b": "#2DD4BF", "c": "#E5484D", "0": WHITE_, "1": "#FFC83D", "2": "#2DD4BF", "3": "#E5484D"}
        g = VGroup(); cells = {}
        for i in range(5):
            for j in range(5):
                if i == 0 and j == 0: t = M(r"\ast", 40, GREY_P); c_ = Square(side_length=cs, stroke_width=0)
                elif i == 0 or j == 0:
                    s = labels[(j if i == 0 else i) - 1]; t = M(s, 44, INK); c_ = Square(side_length=cs, stroke_width=0)
                else:
                    s = prod(labels[i - 1], labels[j - 1]); t = M(s, 44, INK)
                    c_ = Square(side_length=cs, stroke_color=RULE, stroke_width=2, fill_color=col[s], fill_opacity=0.6 if s not in ("e", "0") else 1)
                    cells[(i, j)] = c_
                c_.move_to([j * cs, -i * cs, 0]); t.move_to(c_); g.add(VGroup(c_, t))
        tt = M(title, 64, INK).next_to(g, UP, buff=0.3)
        return VGroup(tt, g), cells
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = VGroup(H("How many groups", 84, INK), H("of order 4?", 84, INK)).arrange(DOWN, buff=0.15); fitw(q, 880); cx(q, 320)
        opts = self.options_row(["1", "2", "3", "4"], 560)
        toks = VGroup(*[VGroup(Circle(radius=px(56), stroke_width=0, fill_color=c, fill_opacity=0.8 if c != WHITE_ else 1).set_stroke(RULE, 3), M(s, 60, INK))
                        for s, c in (("e", WHITE_), ("a", "#FFC83D"), ("b", "#2DD4BF"), ("c", "#E5484D"))]).arrange(RIGHT, buff=px(60)); cx(toks, 950)
        self.add(q, opts)
        cc = self.comment_chip()
        # ===== 0. four elements drop in on frame 0 =====
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.8) for t in toks], lag_ratio=0.2), run_time=0.9, rate_func=EXPO)
        self.play(Rotate(toks, PI / 8, about_point=toks.get_center()), run_time=0.3); self.play(Rotate(toks, -PI / 8, about_point=toks.get_center()), run_time=0.25)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. an element of order 4 -> cyclic Z4 =====
        self.until(S[1])
        Z, zc = self.table(["0", "1", "2", "3"], lambda a, b: str((int(a) + int(b)) % 4), r"\mathbb{Z}_4")
        Z.scale_to_fit_width(px(430)).move_to([X(310), Y(930), 0])
        self.ev("tick"); self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), FadeOut(toks), run_time=0.3)
        self.until(wt(1, 8, 0.1)); self.ev("tick"); self.play(FadeIn(Z, shift=UP * 0.2), run_time=0.45, rate_func=EXPO)
        # ===== 2. every element squares to e -> Klein V4 =====
        self.until(S[2])
        def kp(a, b):
            if a == "e": return b
            if b == "e": return a
            if a == b: return "e"
            return ({"a", "b", "c"} - {a, b}).pop()
        V, vc = self.table(["e", "a", "b", "c"], kp, r"V_4")
        V.scale_to_fit_width(px(430)).move_to([X(770), Y(930), 0])
        self.ev("tick"); self.play(FadeIn(V, shift=UP * 0.2), run_time=0.45, rate_func=EXPO)
        dg = VGroup(*[SurroundingRectangle(vc[(k, k)], color=INK, buff=0, stroke_width=6) for k in range(1, 5)])
        self.until(wt(2, 3, 0.1)); self.play(Create(dg), run_time=0.35)
        kl = B("a² = b² = c² = e", 36, INK, SEMIBOLD).next_to(V, DOWN, buff=0.3)
        self.play(FadeIn(kl), run_time=0.25)
        # ===== 3. both tables symmetric across the diagonal =====
        self.until(S[3])
        self.play(FadeOut(dg), run_time=0.2)
        ds = VGroup(*[DashedLine(t[(1, 1)].get_corner(UL), t[(4, 4)].get_corner(DR), color=INK, stroke_width=5) for t in (zc, vc)])
        self.until(wt(3, 6, 0.15)); self.ev("tick"); self.play(Create(ds), run_time=0.4)
        pairs = [(1, 2), (1, 3), (2, 4)]
        self.play(*[Indicate(t[(i, j)], color=OR, scale_factor=1.12) for t in (zc, vc) for i, j in pairs],
                  *[Indicate(t[(j, i)], color=OR, scale_factor=1.12) for t in (zc, vc) for i, j in pairs], run_time=0.6)
        sym = B("ab = ba everywhere", 38, OR, SEMIBOLD); cx(sym, 1290)
        self.play(FadeIn(sym), run_time=0.25)
        # ===== 4. two groups, both abelian. Follow for #2 =====
        self.until(S[4])
        ans = VGroup(H("2", 140, OR), B("groups · both abelian", 48, INK, SEMIBOLD)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 440)
        self.ev("stamp"); self.play(FadeOut(cc), FadeOut(sym), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.2); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, Z, V, kl, ds, fw, lb)


class OddSq(ShortReel):
    EVENTS = "oddsq"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = M(r"1+3+5+\cdots+(2n-1)=\,?", 92); fitw(q, 900); cx(q, 330)
        opts = self.options_row(["n", "2n", "n^2", "n(n+1)"], 520)
        self.add(q, opts)
        cols = [OR, "#14B8A6", "#FFC83D", "#E5484D"]
        toks = VGroup(*[M(s, 120, c) for s, c in zip(["1", "3", "5", "7"], cols)]).arrange(RIGHT, buff=0.9); cx(toks, 900)
        cc = self.comment_chip()
        # ===== 0. 1, 3, 5, 7 pop in on the words =====
        for k in range(4):
            self.until(wt(0, 4 + k, 0.05) if k else 0.0); self.play(FadeIn(toks[k], scale=0.6), run_time=0.22)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1-2. L shapes build squares =====
        cs = px(96); g0 = np.array([X(100), Y(1240), 0])
        def cell(i, j, c):
            sq_ = Square(side_length=cs * 0.9, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to(g0 + np.array([(j + 0.5) * cs, (i + 0.5) * cs, 0]))
            return sq_
        Ls = [VGroup(*[cell(i, j, cols[k]) for i in range(k + 1) for j in range(k + 1) if max(i, j) == k]) for k in range(4)]
        side = lambda k: B(f"{k + 1}×{k + 1}", 44, INK, SEMIBOLD).move_to(g0 + np.array([(k + 1) * cs / 2, (k + 1) * cs + px(55), 0]))
        sums = [M(s, 60) for s in (r"1=1^2", r"1+3=2^2", r"1+3+5=3^2", r"1+3+5+7=4^2")]
        for k, sm in enumerate(sums): sm.scale(0.84).move_to([0, Y(820 + k * 120), 0]).align_to([X(510), 0, 0], LEFT)
        self.until(S[1]); self.ev("tick")
        self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), toks.animate.scale(0.5).move_to([X(540), Y(380), 0]), run_time=0.3)
        lab = side(0)
        self.until(wt(1, 0, 0.05)); self.play(GrowFromCenter(Ls[0]), FadeIn(sums[0]), run_time=0.3)
        self.until(wt(1, 2, 0.05)); self.ev("tick"); self.play(LaggedStart(*[GrowFromCenter(c) for c in Ls[1]], lag_ratio=0.15), run_time=0.4)
        lab2 = side(1)
        self.until(wt(1, 8, 0.1)); self.play(FadeIn(lab2), FadeIn(sums[1]), run_time=0.3); cur = lab2
        for k, w_ in ((2, 0), (3, 5)):
            self.until(wt(2, w_, 0.05)); self.ev("tick")
            nl = side(k)
            self.play(LaggedStart(*[GrowFromCenter(c) for c in Ls[k]], lag_ratio=0.08), ReplacementTransform(cur, nl), FadeIn(sums[k]), run_time=0.5); cur = nl
        # ===== 3. each odd number wraps one more L =====
        self.until(S[3])
        outl = VGroup(*[SurroundingRectangle(L, color=INK, buff=0.02, stroke_width=0) for L in Ls])
        self.until(wt(3, 3, 0.1)); self.ev("tick")
        self.play(*[Indicate(L, color=None, scale_factor=1.06) for L in Ls], run_time=0.7, lag_ratio=0.2)
        # ===== 4. the first n odd numbers make n^2 =====
        self.until(S[4])
        ans = M(r"1+3+\cdots+(2n-1)=n^2", 84)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); fitw(a_, 940); cx(a_, 470)
        self.ev("stamp"); self.play(FadeOut(toks), FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.6); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, *Ls, cur, *sums, fw, lb)


class Eigen(ShortReel):
    EVENTS = "eigen"; SERIES = "CSIR-NET in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = VGroup(H("Which real vector stays on", 64, INK), H("its own line after a 90° turn?", 64, INK)).arrange(DOWN, buff=0.15); fitw(q, 900); cx(q, 300)
        opts = self.options_row(["x-axis", "y = x", "every", "none"], 480, tex=False)
        O = np.array([X(540), Y(1010), 0]); L = px(330)
        axes = VGroup(Line(O + LEFT * px(400), O + RIGHT * px(400), color=RULE, stroke_width=3), Line(O + DOWN * px(400), O + UP * px(400), color=RULE, stroke_width=3))
        ang = ValueTracker(20 * DEGREES)
        def vec(a, c, w=8): return Arrow(O, O + L * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=c, stroke_width=w, max_tip_length_to_length_ratio=0.12)
        v = always_redraw(lambda: vec(ang.get_value(), INK))
        rv = always_redraw(lambda: vec(ang.get_value() + PI / 2, OR))
        line = always_redraw(lambda: DashedLine(O - px(420) * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]), O + px(420) * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]), color=GREY_P, stroke_width=3))
        self.add(q, opts, axes, line, v, rv)
        cc = self.comment_chip()
        # ===== 0. the vector and its 90 degree turn already moving =====
        self.play(ang.animate.set_value(70 * DEGREES), run_time=1.4, rate_func=rate_functions.ease_in_out_sine)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. any arrow turns off its own line =====
        self.until(S[1])
        lg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.6, color=INK, stroke_width=9), B("v", 42, INK, SEMIBOLD)).arrange(RIGHT, buff=0.18),
                    VGroup(Line(ORIGIN, RIGHT * 0.6, color=OR, stroke_width=9), B("Av (turned 90°)", 42, OR, SEMIBOLD)).arrange(RIGHT, buff=0.18)).arrange(RIGHT, buff=0.7); cx(lg, 440)
        self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), FadeIn(lg), run_time=0.3)
        self.until(wt(1, 5, 0.05)); self.ev("tick")
        self.play(ang.animate.set_value(200 * DEGREES), run_time=max(0.8, C[2] - self.Tm() - 0.2), rate_func=rate_functions.ease_in_out_sine)
        # ===== 2. no real eigenvector =====
        self.until(S[2])
        nr = self.chip("no real eigenvector", size=44); cx(nr, 580)
        self.until(wt(2, 3, 0.1)); self.ev("tick"); self.play(GrowFromCenter(nr), run_time=0.3)
        # ===== 3. characteristic equation =====
        self.until(S[3])
        mat = M(r"A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}", 72); cx(mat, 560)
        ce = M(r"\det(A-\lambda I)=\lambda^2+1=0", 72); fitw(ce, 880); cx(ce, 740)
        for m in (v, rv, line): m.clear_updaters()
        self.play(FadeOut(VGroup(axes, line, v, rv, lg), shift=DOWN * 0.2), nr.animate.move_to([0, Y(1180), 0]), FadeIn(mat, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.until(wt(3, 4, 0.1)); self.ev("tick"); self.play(FadeIn(ce, shift=UP * 0.2), run_time=0.35)
        # ===== 4. eigenvalues +-i =====
        self.until(S[4])
        ans = M(r"\lambda=\pm i", 130)
        ap = RoundedRectangle(width=ans.width + px(100), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 940)
        self.ev("stamp"); self.play(FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.0); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, mat, ce, nr, fw, lb)


class KingInt(ShortReel):
    EVENTS = "kint"; SERIES = "JEE in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        I0 = M(r"\int_0^1 x(1-x)^{99}\,dx=\,?", 100); fitw(I0, 900); cx(I0, 340)
        opts = self.options_row([r"\frac{1}{100}", r"\frac{1}{101}", r"\frac{1}{10100}", r"\frac{1}{9900}"], 560)
        nl = NumberLine(x_range=[0, 1, 0.5], length=px(800), color=INK, stroke_width=4, include_tip=False); cx(nl, 980)
        nlab = VGroup(M("0", 44).next_to(nl.n2p(0), DOWN, buff=0.2), M("1", 44).next_to(nl.n2p(1), DOWN, buff=0.2))
        xv = ValueTracker(0.15)
        d1 = always_redraw(lambda: Dot(nl.n2p(xv.get_value()), radius=px(16), color=INK))
        d2 = always_redraw(lambda: Dot(nl.n2p(1 - xv.get_value()), radius=px(16), color=OR))
        l1 = always_redraw(lambda: M("x", 48).next_to(nl.n2p(xv.get_value()), UP, buff=0.25))
        l2 = always_redraw(lambda: M("1-x", 48, OR).next_to(nl.n2p(1 - xv.get_value()), UP, buff=0.25))
        self.add(I0, opts, nl, nlab, d1, d2, l1, l2)
        cc = self.comment_chip()
        # ===== 0. x and 1-x already mirroring on frame 0 =====
        self.play(xv.animate.set_value(0.38), run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        self.ev("tick"); self.play(xv.animate.set_value(0.2), FadeIn(cc, shift=UP * 0.15), run_time=0.6)
        # ===== 1. swap x for 1-x: same value =====
        self.until(S[1])
        pr = M(r"\int_0^1 f(x)\,dx=\int_0^1 f(1-x)\,dx", 70); fitw(pr, 880); cx(pr, 700)
        self.play(FadeOut(opts, shift=UP * 0.2), I0.animate.scale(0.7).move_to([0, Y(320), 0]), run_time=0.3)
        self.until(wt(1, 0, 0.05)); self.ev("tick"); self.play(xv.animate.set_value(0.8), FadeIn(pr, shift=UP * 0.2), run_time=0.6)
        # ===== 2-4. the three lines =====
        for m in (d1, d2, l1, l2): m.clear_updaters()
        steps = [M(r"=\int_0^1 (1-x)\,x^{99}\,dx", 84), M(r"=\int_0^1 \left(x^{99}-x^{100}\right)dx", 84), M(r"=\tfrac{1}{100}-\tfrac{1}{101}", 96)]
        for k, st in enumerate(steps): st.scale(0.78); fitw(st, 880); cx(st, 520 + k * 225)
        self.until(S[2]); self.ev("tick")
        self.play(FadeOut(VGroup(nl, nlab, d1, d2, l1, l2, pr), shift=DOWN * 0.2), FadeIn(steps[0], shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.until(S[3]); self.ev("tick"); self.play(FadeIn(steps[1], shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        self.until(S[4]); self.ev("tick"); self.play(FadeIn(steps[2], shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        # ===== 5. 1/10100 =====
        self.until(S[5])
        ans = M(r"=\frac{1}{10100}", 130)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)).scale(0.66); cx(a_, 1190)
        self.ev("stamp"); self.play(FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[5] + 0.9); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, I0, *steps, fw, lb)


class Monty(ShortReel):
    EVENTS = "monty"; SERIES = "JEE in 20s"
    def door(self, n):
        r = RoundedRectangle(width=px(230), height=px(340), corner_radius=0.12, fill_color=WHITE_, fill_opacity=1, stroke_color=INK, stroke_width=5)
        knob = Dot(r.get_right() + LEFT * px(36), radius=px(9), color=INK)
        return VGroup(r, knob, H(str(n), 90, INK).move_to(r))
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = VGroup(H("3 doors, 1 car.", 84, INK), H("Should you switch?", 84, INK)).arrange(DOWN, buff=0.15); fitw(q, 880); cx(q, 300)
        opts = self.options_row(["Stay", "Switch", "50-50", "Depends"], 500, tex=False)
        doors = VGroup(*[self.door(n) for n in (1, 2, 3)]).arrange(RIGHT, buff=px(60)); cx(doors, 860)
        self.add(q, opts)
        cc = self.comment_chip()
        # ===== 0. doors drop in, you pick door 1 =====
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.6) for d in doors], lag_ratio=0.2), run_time=0.8, rate_func=EXPO)
        yp = B("your pick", 34, OR, SEMIBOLD).next_to(doors[0], UP, buff=0.2)
        self.play(doors[0][0].animate.set_stroke(OR, width=8), FadeIn(yp), run_time=0.3)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. first pick right 1 time in 3 =====
        self.until(S[1])
        self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), run_time=0.3)
        p1 = M(r"\tfrac13", 110, OR).next_to(doors[0], DOWN, buff=0.35)
        self.until(wt(1, 5, 0.1)); self.ev("tick"); self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.3)
        # ===== 2. 2 times in 3 behind the other two =====
        self.until(S[2])
        br = Brace(VGroup(doors[1], doors[2]), DOWN, color=INK)
        p2 = M(r"\tfrac23", 110, INK).next_to(br, DOWN, buff=0.15)
        self.until(wt(2, 1, 0.1)); self.ev("tick"); self.play(GrowFromCenter(br), FadeIn(p2), run_time=0.35)
        # ===== 3. host opens a goat door; the 2/3 moves to the last door =====
        self.until(S[3])
        op = RoundedRectangle(width=px(230), height=px(340), corner_radius=0.12, fill_color=GREY_P, fill_opacity=0.25, stroke_color=GREY_P, stroke_width=4).move_to(doors[2])
        goat = B("goat", 44, GREY_P, SEMIBOLD).move_to(doors[2])
        self.until(wt(3, 2, 0.1)); self.ev("tick"); self.play(ReplacementTransform(doors[2], VGroup(op, goat)), run_time=0.35)
        p2b = M(r"\tfrac23", 110, OR).next_to(doors[1], DOWN, buff=0.35)
        self.until(wt(3, 10, 0.1)); self.ev("tick"); self.play(FadeOut(br), ReplacementTransform(p2, p2b), doors[1][0].animate.set_stroke(OR, width=8), run_time=0.5, rate_func=EXPO)
        # ===== 4. switch: win 2/3 =====
        self.until(S[4])
        ans = VGroup(B("Switch", 64, INK, SEMIBOLD), M(r"\Rightarrow\ \text{win }\tfrac23", 84, OR)).arrange(RIGHT, buff=0.4)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 470)
        self.ev("stamp"); self.play(FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.6); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, doors[0], doors[1], op, goat, yp, p1, p2b, fw, lb)


class Harmonic(ShortReel):
    EVENTS = "harm"; SERIES = "CSIR-NET in 20s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = M(r"1+\tfrac12+\tfrac13+\tfrac14+\cdots", 100); fitw(q, 900); cx(q, 320)
        opts = self.options_row([r"\to2", r"\to e", r"\to\tfrac{\pi^2}{6}", r"\infty"], 500)
        N = 16; bw = px(52); base = np.array([X(540) - N * bw / 2, Y(1300), 0]); hU = px(560)
        bars = VGroup(*[Rectangle(width=bw * 0.86, height=hU / n, stroke_width=0, fill_color=GREY_P, fill_opacity=0.55).move_to(base + np.array([(n - 0.5) * bw, hU / n / 2, 0])) for n in range(1, N + 1)])
        bl = VGroup(*[M(r"\tfrac1{%d}" % n, 40, GREY_P).next_to(bars[n - 1], DOWN, buff=0.1) for n in (1, 2, 3, 4)])
        self.add(q, opts)
        cc = self.comment_chip()
        # ===== 0. terms appear as bars on the words (frame 0 already moving) =====
        self.play(GrowFromEdge(bars[0], DOWN), FadeIn(bl[0]), run_time=0.3)
        for k, w_ in ((1, 3), (2, 6), (3, 9)):
            self.until(wt(0, w_, 0.05)); self.play(GrowFromEdge(bars[k], DOWN), FadeIn(bl[k]), run_time=0.25)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[4:]], lag_ratio=0.08), run_time=0.8)
        self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # groups: [1/2], [1/3,1/4], [1/5..1/8], [1/9..1/16]
        grp = [(1, 2), (2, 4), (4, 8), (8, 16)]; cols = [OR, "#14B8A6", "#FFC83D", "#E5484D"]
        def mark(k):
            a, b = grp[k]; g = VGroup(*bars[a:b])
            br = Brace(g, UP, color=cols[k], buff=0.12) if k else Brace(g, UP, color=cols[k], buff=0.12)
            lab = M(r">\tfrac12" if k else r"=\tfrac12", 56, INK)
            if k == 0: lab.next_to(br, UR, buff=0.05).shift(RIGHT * 0.15 + UP * 0.35)
            elif k == 1: lab.next_to(br, UP, buff=0.1).shift(UP * 0.1)
            else: lab.next_to(br, UP, buff=0.1)
            return g, br, lab
        # ===== 1. group the terms: 1/3 + 1/4 > 1/2 =====
        self.until(S[1]); self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), run_time=0.3)
        ms = []
        for k, (ci, w_) in enumerate(((1, 0), (1, 3), (2, 4), (3, 4))):
            self.until(wt(ci, w_, 0.1) if k < 3 else S[3] + 0.1); self.ev("tick")
            g, br, lab = mark(k); ms += [br, lab]
            self.play(*[b.animate.set_fill(cols[k], 0.85) for b in g], GrowFromCenter(br), FadeIn(lab), run_time=0.35)
        # ===== 3. every group adds at least a half =====
        ps = M(r"S>1+\tfrac12+\tfrac12+\tfrac12+\cdots", 84); fitw(ps, 900); cx(ps, 430)
        self.until(wt(3, 6, 0.1)); self.play(FadeIn(ps, shift=UP * 0.2), run_time=0.35)
        # ===== 4. diverges =====
        self.until(S[4])
        ans = VGroup(M(r"\sum\frac1n", 96), B("diverges", 64, OR, SEMIBOLD)).arrange(RIGHT, buff=0.4)
        ap = RoundedRectangle(width=ans.width + px(80), height=ans.height + px(50), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
        a_ = VGroup(ap, ans.move_to(ap)); cx(a_, 430)
        self.ev("stamp"); self.play(FadeOut(ps), FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[4] + 1.6); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(a_, bars, bl, *ms, fw, lb)


class Quiz(ShortReel):
    EVENTS = "quiz"; SERIES = "Week recap"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        t1 = at(H("3 questions.", 110, INK), 420); t2 = at(H("Can you get 3/3?", 84, OR), 560)
        dots = VGroup(*[Circle(radius=px(34), stroke_color=INK, stroke_width=5) for _ in range(3)]).arrange(RIGHT, buff=px(40)); cx(dots, 1290)
        self.add(t1)
        self.play(FadeIn(t2, shift=UP * 0.2), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25), run_time=0.8, rate_func=EXPO)
        def ring(t0, dur):
            tr = ValueTracker(0); cxy = np.array([X(540), Y(1150), 0])
            arc = always_redraw(lambda: Arc(radius=px(70), start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()), arc_center=cxy, color=OR, stroke_width=12))
            num = always_redraw(lambda: H(str(max(1, int(np.ceil(3 * (1 - tr.get_value()))))), 80, INK).move_to(cxy))
            return tr, arc, num
        def question(i, qm, vis, ans_m, k):
            self.until(S[i]); self.ev("tick")
            tag = B(f"Question {k}", 40, OR, SEMIBOLD); cx(tag, 300)
            qq = qm; fitw(qq, 900); cx(qq, 450 if len(qm) > 1 and isinstance(qm, VGroup) else 430)
            self.play(FadeIn(tag), FadeIn(qq, shift=UP * 0.2), FadeIn(vis, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
            # thinking time: countdown ring over the silence before the answer
            t0 = C[i + 1]; tr, arc, num = ring(t0, 1.6)
            self.until(t0); self.add(arc, num); self.play(tr.animate.set_value(1), run_time=1.5, rate_func=linear)
            arc.clear_updaters(); num.clear_updaters(); self.remove(arc, num)
            a_ = ans_m; ap = RoundedRectangle(width=a_.width + px(80), height=a_.height + px(40), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=6)
            box = VGroup(ap, a_.move_to(ap)).move_to([0, Y(1150), 0])
            self.ev("stamp"); self.play(GrowFromCenter(box), dots[k - 1].animate.set_fill(OR, 1).set_stroke(OR), run_time=0.35, rate_func=rate_functions.ease_out_back)
            return VGroup(tag, qq, vis, box)
        # ===== Q1 =====
        self.until(S[1]); self.play(FadeOut(VGroup(t1, t2), shift=UP * 0.2), run_time=0.3)
        ax = Axes(x_range=[-4, 4, 1], y_range=[-1.3, 2.3, 1], x_length=px(700), y_length=px(300), tips=False, axis_config={"color": RULE, "stroke_width": 3})
        cx(ax, 800)
        v1 = VGroup(ax, ax.plot(np.cos, x_range=[-4, 4], color=INK, stroke_width=5), ax.plot(lambda x: abs(x), x_range=[-2.3, 2.3], color=OR, stroke_width=6, use_smoothing=False))
        g1 = question(1, VGroup(H("How many solutions?", 72, INK), M(r"|x|=\cos x", 96)).arrange(DOWN, buff=0.25), v1, VGroup(H("2", 110, OR), B("solutions", 44, INK, SEMIBOLD)).arrange(RIGHT, buff=0.25, aligned_edge=DOWN), 1)
        # ===== Q2 =====
        self.until(S[3] - 0.25); self.play(FadeOut(g1), run_time=0.25)
        v2 = VGroup(M(r"2^{100}", 130), B("vs", 44, GREY_P, SEMIBOLD), M(r"3^{63}", 130, OR)).arrange(RIGHT, buff=0.6); cx(v2, 760)
        g2 = question(3, H("Which is bigger?", 72, INK), v2, M(r"2^{100}>3^{63}", 96), 2)
        # ===== Q3 =====
        self.until(S[5] - 0.25); self.play(FadeOut(g2), run_time=0.25)
        v3 = VGroup(die(2, 170), die(5, 170)).arrange(RIGHT, buff=px(60)); cx(v3, 760)
        g3 = question(5, H("Most likely total?", 72, INK), v3, VGroup(H("7", 110, OR), M(r"P=\tfrac16", 64)).arrange(RIGHT, buff=0.35), 3)
        # ===== score + follow =====
        sc = self.comment_chip("Comment your score: 0, 1, 2 or 3"); sc[0].stretch_to_fit_width(px(720)); cx(sc, 1410)
        self.until(C[6] + 1.6 + 0.6); self.play(FadeIn(sc, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(g3, dots, sc, lb)


# ---------------- Promo remake (Aro's "all in one place" overview, 23 Oct) in the house style ----------------
def _atom(c=OR, w=190):
    g = VGroup(*[Ellipse(width=px(w), height=px(w * 0.36), stroke_color=c, stroke_width=6).rotate(a) for a in (0, PI / 3, -PI / 3)])
    return g.add(Dot(radius=px(13), color=INK))
def _clip(c=INK):
    b = RoundedRectangle(width=px(124), height=px(156), corner_radius=0.1, stroke_color=c, stroke_width=6)
    ls = VGroup(*[Line([-px(38), 0, 0], [px(30), 0, 0], stroke_color=c, stroke_width=5).shift(UP * px(40 - 26 * i) + RIGHT * px(8)) for i in range(3)])
    tk = VMobject(stroke_color=OR, stroke_width=9).set_points_as_corners([[-px(30), -px(40), 0], [-px(10), -px(58), 0], [px(32), -px(16), 0]])
    cl = RoundedRectangle(width=px(52), height=px(20), corner_radius=0.05, fill_color=c, fill_opacity=1, stroke_width=0).move_to(UP * px(78))
    return VGroup(b, ls, tk, cl)
def _school(c=WHITE_):
    body = Rectangle(width=px(170), height=px(105), stroke_color=c, stroke_width=6).shift(DOWN * px(20))
    roof = Polygon([-px(105), px(33), 0], [px(105), px(33), 0], [0, px(100), 0], stroke_color=c, stroke_width=6)
    door = Rectangle(width=px(36), height=px(54), fill_color=OR, fill_opacity=1, stroke_width=0).shift(DOWN * px(46))
    return VGroup(body, roof, door)
def _college(c=WHITE_):
    top = Polygon([0, px(62), 0], [px(115), px(16), 0], [0, -px(28), 0], [-px(115), px(16), 0], fill_color=c, fill_opacity=1, stroke_width=0)
    cap = Arc(radius=px(64), start_angle=PI + 0.3, angle=PI - 0.6, stroke_color=c, stroke_width=6).shift(DOWN * px(8))
    ts = Line([px(78), px(8), 0], [px(78), -px(64), 0], stroke_color=OR, stroke_width=6)
    return VGroup(cap, top, ts)
def _coaching(c=WHITE_):
    bd = RoundedRectangle(width=px(184), height=px(120), corner_radius=0.08, fill_color=OR, fill_opacity=1, stroke_width=0)
    sy = B("+ − × ÷", 32, WHITE_, SEMIBOLD).move_to(bd)
    lg = VGroup(Line([-px(56), -px(60), 0], [-px(76), -px(106), 0]), Line([px(56), -px(60), 0], [px(76), -px(106), 0])).set_stroke(c, 6)
    return VGroup(bd, sy, lg)


class Promo(ShortReel):
    EVENTS = "promo"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        LBL = "Learn · Practise · Test"
        def lab(dark=False):
            g = self.label(LBL, dark); self.add(g); return g
        def title(s, y=250, color=INK, size=88):
            return fitw(at(H(s, size, color), y), 888)
        def pill(s, w, h=96, size=40, fill=WHITE_, fg=INK, stroke=RULE):
            r = RoundedRectangle(width=px(w), height=px(h), corner_radius=0.16, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3)
            t = B(s, size, fg, SEMIBOLD); fitw(t, w - 30); return VGroup(r, t.move_to(r))

        # ===== A. Maths, science, exams and English. All in one place. (tiles already popping on frame 0) =====
        self.add(self.hdr); lb = lab()
        h1 = at(H("Maths, science,", 96, INK), 250); h2 = at(H("exams & English.", 96, INK), 360)
        def tile(icon, name, x, y):
            c_ = RoundedRectangle(width=px(430), height=px(350), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            c_.move_to([X(x), Y(y), 0])
            if icon.height > px(170): icon.scale_to_fit_height(px(170))
            icon.move_to(c_.get_center() + UP * px(40))
            return VGroup(c_, icon, B(name, 42, INK, SEMIBOLD).move_to(c_.get_center() + DOWN * px(118)))
        im = M(r"\int\!\pi", 130); en = H("Aa", 130, INK); en[1].set_color(OR)
        tl = [tile(im, "Maths", 315, 650), tile(_atom(), "Science", 765, 650), tile(_clip(), "Exams", 315, 1035), tile(en, "English", 765, 1035)]
        self.add(h1, h2, tl[0])
        self.play(Indicate(tl[0][1], color=OR, scale_factor=1.12), run_time=0.5)
        for k, w in ((1, 1), (2, 2), (3, 4)):
            self.until(wt(0, w, 0.08)); self.ev("tick"); self.play(GrowFromCenter(tl[k]), run_time=0.3, rate_func=EXPO)
        op = VGroup(SER("All in", 110, INK), SER("one place.", 110, OR)).arrange(RIGHT, buff=0.3); cx(op, 1360)
        ul = Line(op[1].get_corner(DL) + DOWN * 0.08, op[1].get_corner(DR) + DOWN * 0.08, color=OR, stroke_width=8)
        self.until(wt(0, 5, 0.1)); self.play(FadeIn(op, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        self.until(wt(0, 7, 0.0)); self.play(Create(ul), run_time=0.35)

        # ===== B. Interactive courses for Class 10, 11 and 12, with live labs and worked solutions. =====
        self.until(S[1]); self.to(PAPER); lb = lab()
        t1 = title("Interactive courses")
        tabs = VGroup(*[pill(f"Class {n}", 260, 90, 38) for n in (10, 11, 12)]).arrange(RIGHT, buff=px(24)); cx(tabs, 375)
        subs = VGroup(*[tag(s, 36) for s in ("Maths", "Physics", "Chemistry")]).arrange(RIGHT, buff=px(20)); cx(subs, 475)
        self.ev("tick"); self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        on = None
        for k, w in enumerate((4, 5, 7)):
            self.until(wt(1, w, 0.08))
            hi = tabs[k][0].copy().set_fill(OR).set_stroke(OR); tx = tabs[k][1].copy().set_color(WHITE_)
            anims = [FadeIn(tabs[k], scale=0.9), FadeIn(hi), FadeIn(tx)]
            if on is not None: anims.append(FadeOut(on))
            if k == 0: anims.append(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in subs], lag_ratio=0.2))
            self.play(*anims, run_time=0.25); on = VGroup(hi, tx)
        lc = card(888, 360, WHITE_, RULE); cx(lc, 735)
        ltag = tag("Live lab", 30, WHITE_, INK).next_to(lc.get_corner(UL), DR, buff=0.22)
        lf = M(r"y=a\sin x", 48).next_to(lc.get_corner(UR), DL, buff=0.25)
        la = Axes(x_range=[0, 2 * PI, PI], y_range=[-1.6, 1.6, 1], x_length=px(600), y_length=px(170), tips=False, axis_config={"color": RULE, "stroke_width": 3})
        la.move_to(lc.get_center() + UP * px(10))
        amp = ValueTracker(0.5)
        wave = always_redraw(lambda: la.plot(lambda x: amp.get_value() * math.sin(x), x_range=[0, 2 * PI], color=OR, stroke_width=7))
        sl = Line([X(260), Y(870), 0], [X(820), Y(870), 0], color=RULE, stroke_width=6)
        knob = always_redraw(lambda: Dot(sl.point_from_proportion((amp.get_value() - 0.3) / 1.2), radius=px(17), color=INK))
        sla = B("a", 34, GREY_P, SEMIBOLD).next_to(sl, LEFT, buff=0.2)
        self.until(wt(1, 9, 0.1)); self.ev("tick")
        self.play(FadeIn(VGroup(lc, ltag, lf, la, sl, sla), shift=UP * 0.15), run_time=0.3, rate_func=EXPO); self.add(wave, knob)
        self.play(amp.animate.set_value(1.4), run_time=0.9, rate_func=rate_functions.ease_in_out_sine)
        sc = card(888, 520, WHITE_, RULE); cx(sc, 1240)
        stag = tag("Worked solution", 30, WHITE_, INK).next_to(sc.get_corner(UL), DR, buff=0.22)
        s1 = M(r"x^2-5x+6=0", 66); s2 = M(r"(x-2)(x-3)=0", 66); s3 = M(r"x=2,\ 3", 66, OR)
        for m, y in ((s1, 1120), (s2, 1240), (s3, 1360)): cx(m, y)
        tk3 = tick(0.26).next_to(s3, RIGHT, buff=0.3)
        self.until(wt(1, 12, 0.25)); self.ev("tick")
        self.play(FadeIn(VGroup(sc, stag), shift=UP * 0.15), FadeIn(s1), run_time=0.25, rate_func=EXPO)
        self.play(LaggedStart(FadeIn(s2, shift=DOWN * 0.1), AnimationGroup(FadeIn(s3, shift=DOWN * 0.1), GrowFromCenter(tk3)), lag_ratio=0.6), run_time=0.5)

        # ===== C. Practice that adapts to you, with step-by-step answers. =====
        self.until(S[2]); self.to(PAPER); lb = lab()
        t2 = title("Practice that adapts")
        lv = VGroup(*[pill(s, 260, 90, 38) for s in ("Easy", "Medium", "Hard")]).arrange(RIGHT, buff=px(24)); cx(lv, 390)
        hl = lv[0][0].copy().set_fill(OR).set_stroke(OR).set_z_index(1)
        lvt = VGroup(*[p[1].copy().set_z_index(2) for p in lv]); lvt[0].set_color(WHITE_)
        qc = card(888, 220, WHITE_, RULE); cx(qc, 610)
        q = M(r"\text{Solve } 2x+3=11", 78).move_to(qc)
        self.ev("tick"); self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(lv), FadeIn(hl), FadeIn(lvt), FadeIn(qc), FadeIn(q), run_time=0.3, rate_func=EXPO)
        self.until(wt(2, 2, 0.1)); self.ev("tick")
        self.play(hl.animate.move_to(lv[1][0]), lvt[0].animate.set_color(INK), lvt[1].animate.set_color(WHITE_), run_time=0.35, rate_func=EXPO)
        st = [M(r"2x=11-3", 76), M(r"2x=8", 76), M(r"x=4", 96, OR)]
        for m, y in zip(st, (830, 960, 1110)): cx(m, y)
        bx = self.answer_box(st[2]); tk = tick(0.3).next_to(bx, RIGHT, buff=0.3)
        self.until(wt(2, 6, 0.15))
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.12) for m in st], lag_ratio=0.45), run_time=0.8)
        self.ev("stamp"); self.play(Create(bx), GrowFromCenter(tk), run_time=0.3)

        # ===== D. Mock tests for JEE, NEET, IELTS, PTE and more. The first mock is free. =====
        self.until(S[3]); self.to(PAPER); lb = lab()
        t3 = title("Mock tests")
        big = [pill(s, 430, 120, 52) for s in ("JEE Main", "NEET-UG", "IELTS", "PTE")]
        for p, (x, y) in zip(big, ((315, 420), (765, 420), (315, 565), (765, 565))): p.move_to([X(x), Y(y), 0])
        sm = VGroup(*[tag(s, 34) for s in ("GATE", "CSIR-NET", "SAT", "TOEFL")]).arrange(RIGHT, buff=px(18))
        sm2 = VGroup(*[tag(s, 34) for s in ("GRE", "GMAT", "TNPSC", "Duolingo")]).arrange(RIGHT, buff=px(18))
        cx(sm, 715); cx(sm2, 795)
        self.play(FadeIn(t3, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        for k, w in enumerate((3, 4, 5, 6)):
            self.until(wt(3, w, 0.08)); self.ev("tick"); self.play(GrowFromCenter(big[k]), run_time=0.22, rate_func=EXPO)
        self.until(wt(3, 8, 0.1)); self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in [*sm, *sm2]], lag_ratio=0.08), run_time=0.5)
        sp = VGroup(H("First mock", 70, OR), H("FREE", 150, OR)).arrange(DOWN, buff=0.1)
        sr = RoundedRectangle(width=sp.width + px(90), height=sp.height + px(60), corner_radius=0.2, stroke_color=OR, stroke_width=10, fill_color=WHITE_, fill_opacity=1)
        stamp = VGroup(sr, sp.move_to(sr)).rotate(-8 * DEGREES); cx(stamp, 1140)
        self.until(wt(3, 13, 0.12)); self.ev("stamp")
        self.play(FadeIn(stamp, scale=1.6), run_time=0.4, rate_func=rate_functions.ease_out_back)

        # ===== E. Maths games and free tools, from times tables to graph plotters. =====
        self.until(S[4]); self.to(PAPER); lb = lab()
        t4 = title("Maths games")
        gm = [pill(s, 430, 96, 40) for s in ("Math Sprint", "Algebra Escape", "Times Table Blitz", "Sudoku")]
        for p, (x, y) in zip(gm, ((315, 390), (765, 390), (315, 506), (765, 506))): p.move_to([X(x), Y(y), 0])
        self.ev("tick"); self.play(FadeIn(t4, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        self.until(wt(4, 1, 0.1)); self.play(LaggedStart(*[GrowFromCenter(p) for p in gm], lag_ratio=0.15), run_time=0.5, rate_func=EXPO)
        pc = card(888, 840, WHITE_, RULE); cx(pc, 1060)
        ptag = tag("Free tool · Graph plotter", 30, WHITE_, INK).next_to(pc.get_corner(UL), DR, buff=0.22)
        pa = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=px(640), y_length=px(560), tips=False, axis_config={"color": INK, "stroke_width": 3})
        pa.move_to(pc.get_center() + DOWN * px(40))
        pg = pa.plot(lambda x: x * x, x_range=[-3, 3], color=OR, stroke_width=8)
        pl = M(r"y=x^2", 60, OR).next_to(pa.c2p(0.25, 8.2), RIGHT, buff=0.1)
        self.until(wt(4, 3, 0.1)); self.ev("tick"); self.play(FadeIn(VGroup(pc, ptag, pa), shift=UP * 0.15), run_time=0.3, rate_func=EXPO)
        self.until(wt(4, 9, 0.3)); self.play(Create(pg), FadeIn(pl), run_time=0.9, rate_func=rate_functions.ease_in_out_sine)

        # ===== F. Schools, colleges and coaching centres can partner with us too. (ink) =====
        self.until(S[5]); self.to(INK); lb = lab(True)
        t5 = title("For institutions", color=WHITE_)
        ic = [(_school(), "Schools"), (_college(), "Colleges"), (_coaching(), "Coaching")]
        cols = []
        for (g, n), x in zip(ic, (230, 540, 850)):
            g.move_to([X(x), Y(600), 0]); cols.append(VGroup(g, B(n, 38, WHITE_, SEMIBOLD).move_to([X(x), Y(760), 0])))
        self.play(FadeIn(t5, shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        for k, w in enumerate((0, 1, 3)):
            self.until(wt(5, w, 0.05)); self.ev("tick"); self.play(FadeIn(cols[k], shift=UP * 0.2), run_time=0.3, rate_func=EXPO)
        pw = SER("Partner with", 110, WHITE_); cx(pw, 1040)
        wm2 = wordmark(px(560), dark=True); cx(wm2, 1200)
        self.until(wt(5, 6, 0.1)); self.ev("chime"); self.rise(pw, wm2)

        # ===== G. Start free today at tutorda.org. =====
        self.until(S[6]); self.to(PAPER); lb = lab()
        g1 = at(H("Start free", 140, INK), 600); g2 = at(SER("today.", 150, OR), 770)
        bt = RoundedRectangle(width=px(700), height=px(150), corner_radius=0.3, fill_color=OR, fill_opacity=1, stroke_width=0)
        btn = VGroup(bt, H("tutorda.org  →", 66, WHITE_).move_to(bt)); cx(btn, 1010)
        self.rise(g1, g2, btn)
        self.until(C[6] + 0.85); self.play(btn.animate.scale(0.94), run_time=0.12); self.play(btn.animate.scale(1 / 0.94), run_time=0.15)
        self.brand_flash(g1, g2, btn, lb)


# ---------------- Hook reel (27 Oct): is 0.999... = 1? (Yes: 10x - x = 9.) ----------------
class Nines(ShortReel):
    EVENTS = "nines"; SERIES = "Maths in 15s"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        def MT(*p, size=104, color=INK): return MathTex(*p, font_size=size, color=color)
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        # ===== 0. nines already typing on frame 0, YES / NO on screen =====
        q = fitw(at(H("Is this equal to 1?", 88, INK), 290), 888)
        digs = H("0.99999999…", 150, INK); fitw(digs, 888); cx(digs, 500)
        def pill(s, fill, fg):
            r = RoundedRectangle(width=px(400), height=px(150), corner_radius=0.22, fill_color=fill, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            return VGroup(r, H(s, 72, fg).move_to(r))
        yes, no = pill("YES", WHITE_, INK), pill("NO", WHITE_, INK)
        opts = VGroup(yes, no).arrange(RIGHT, buff=px(48)); cx(opts, 790)
        self.add(q, opts, digs[:3])
        for k in range(3, len(digs)):
            self.add(digs[k]); self.wait(0.09)
        cc = self.comment_chip("Comment YES or NO")
        self.until(1.4); self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. Call it x =====
        self.until(S[1])
        l1 = MT("x", "=", "0", r".999\ldots", size=96); l1.move_to([X(560), Y(600), 0])
        l2 = MT("10x", "=", "9", r".999\ldots", size=96); l2.move_to([0, Y(450), 0]); l2.shift(RIGHT * (l1[3].get_left()[0] - l2[3].get_left()[0]))
        dx = -VGroup(l1, l2).get_center()[0] + px(30); l1.shift(RIGHT * dx); l2.shift(RIGHT * dx)
        self.ev("tick")
        self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), ReplacementTransform(digs, l1), run_time=0.4, rate_func=EXPO)
        # ===== 2. 10x = 9.999... (written above, decimals aligned) =====
        self.until(S[2])
        t10 = tag("× 10", 36, WHITE_, OR).next_to(l2, UP, buff=0.25).align_to(l2, LEFT)
        self.until(wt(2, 0, 0.1)); self.ev("tick"); self.play(FadeIn(l2, shift=DOWN * 0.2), FadeIn(t10), run_time=0.35, rate_func=EXPO)
        # ===== 3. Subtract: the endless nines cancel =====
        self.until(S[3])
        mn = MT("-", color=OR).next_to(l1, LEFT, buff=0.35)
        rule = Line([X(150), Y(700), 0], [X(930), Y(700), 0], color=INK, stroke_width=5)
        self.ev("tick"); self.play(FadeOut(t10), FadeIn(mn), Create(rule), run_time=0.3)
        self.until(wt(3, 3, 0.1)); self.play(l1[3].animate.set_color(OR), l2[3].animate.set_color(OR), run_time=0.25)
        st = [Line(m.get_left() + LEFT * 0.08, m.get_right() + RIGHT * 0.08, color=OR, stroke_width=9) for m in (l1[3], l2[3])]
        self.until(wt(3, 5, 0.1)); self.ev("tick")
        self.play(*[Create(s) for s in st], l1[3].animate.set_opacity(0.35), l2[3].animate.set_opacity(0.35), run_time=0.3)
        # ===== 4. 9x = 9, x = 1 exactly =====
        self.until(S[4])
        l3 = MT("9x", "=", "9"); l3.move_to([0, Y(800), 0]).align_to(l1, RIGHT).shift(LEFT * (l1[3].width))
        self.until(wt(4, 1, 0.1)); self.ev("tick"); self.play(FadeIn(l3, shift=DOWN * 0.15), run_time=0.3, rate_func=EXPO)
        ans = MT("x", "=", "1", size=124, color=OR)
        ap = RoundedRectangle(width=ans.width + px(110), height=ans.height + px(70), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=7)
        a_ = VGroup(ap, ans.move_to(ap)).move_to([X(360), Y(1030), 0])
        ys = VGroup(RoundedRectangle(width=px(300), height=px(130), corner_radius=0.22, fill_color=OR, fill_opacity=1, stroke_width=0))
        ys.add(H("YES", 64, WHITE_).move_to(ys[0])); ys.move_to([X(810), Y(1030), 0])
        self.until(wt(4, 7, 0.12)); self.ev("stamp")
        self.play(FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(ys, scale=1.3), run_time=0.25, rate_func=EXPO)
        # ===== 5. Same number, two names. Follow for more =====
        self.until(S[5])
        tn = VGroup(H("0.999…", 96, INK), H("=", 96, GREY_P), H("1", 96, OR)).arrange(RIGHT, buff=0.35); cx(tn, 1240)
        self.ev("tick"); self.play(FadeIn(tn, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        fw = self.comment_chip("Follow for more"); fw[0].set_fill(OR)
        self.until(C[5] + 1.1); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(l1, l2, mn, rule, *st, l3, a_, ys, tn, fw, lb)
