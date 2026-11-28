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
        rows = [B(l.strip(), 40 if s == self.CTA else 32, WHITE_, SEMIBOLD) for l in s.split("|")]   # "|" = line break; CTA larger
        t = VGroup(*rows).arrange(DOWN, buff=px(10))
        g = VGroup(RoundedRectangle(width=max(px(560), t.width + px(64)), height=t.height + px(44), corner_radius=0.18, fill_color=INK, fill_opacity=1, stroke_width=0))
        g.add(t.move_to(g[0])); g.move_to([px(getattr(self, "CX", 540)) - 4.5, Y(getattr(self, "CHIP_Y", 1410)), 0]); return g
    CTA = "Follow TutorDA | and comment TRICKS | to get the PDF"   # keyword lead magnet (Aro, 28 Oct)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
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
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
        self.until(C[5] + 1.1); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(l1, l2, mn, rule, *st, l3, a_, ys, tn, fw, lb)


# ---------------- Template v2 (28 Oct audit fixes): everything inside Instagram's safe zone (y 230-1440, right 200 px clear
# for the action rail), header below the Reels top bar, floating caption pill instead of the bottom band (which the
# Instagram caption overlay covers), hook inside the profile-grid crop, 22-25 s with a trap beat and motion to the end. ----------------
class ShortReel2(ShortReel):
    HDR_Y = 262; HDR_R = 870; CAP_PILL = False; BAND_TOP = 1460; CAP_Y = 1545; CAP_X = 0; CHIP_Y = 1250; CX = 490   # captions in the footer band (Aro, 28 Oct)
    def c2(self, m, y):           # centre on the safe-zone axis (x = 490)
        return m.move_to([X(490), Y(y), 0])


class Nines2(ShortReel2):
    EVENTS = "nines2"; SERIES = "Daily maths trick"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        RD = "#E5484D"
        def MT(*p, size=96, color=INK): return MathTex(*p, font_size=size, color=color)
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        # ===== 0. Is this equal to 1? (nines typing on frame 0) =====
        q = self.c2(fitw(H("Is this equal to 1?", 80, INK), 760), 380)
        digs = fitw(H("0.99999999…", 132, INK), 760); self.c2(digs, 540)
        def pill(s, w=330):
            r = RoundedRectangle(width=px(w), height=px(130), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            return VGroup(r, H(s, 64, INK).move_to(r))
        opts = VGroup(pill("YES"), pill("NO")).arrange(RIGHT, buff=px(40)); self.c2(opts, 740)
        self.add(q, opts, digs[:3])
        for k in range(3, len(digs)):
            self.add(digs[k]); self.wait(0.08)
        cc = self.comment_chip("Pause and guess")
        self.until(1.3); self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== 1. Most people say no. It's always a tiny bit less. (number line zoom toward 1) =====
        self.until(S[1])
        d2 = self.c2(H("0.999…", 110, INK), 420)
        nl = NumberLine(x_range=[0.9, 1.0, 0.1], length=px(720), color=INK, stroke_width=5, include_numbers=False, tick_size=0.12)
        self.c2(nl, 760)
        l9 = B("0.9", 34, GREY_P, SEMIBOLD).next_to(nl.n2p(0.9), DOWN, buff=0.25); l1 = B("1", 40, INK, SEMIBOLD).next_to(nl.n2p(1.0), DOWN, buff=0.25)
        self.ev("tick")
        self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), ReplacementTransform(digs, d2), Create(nl), FadeIn(l9), FadeIn(l1), run_time=0.45, rate_func=EXPO)
        no = self.c2(H("NO?", 90, RD), 590)
        self.until(wt(1, 3, 0.1)); self.play(FadeIn(no, scale=1.3), run_time=0.25, rate_func=EXPO)
        val = ValueTracker(0.9)
        dot = always_redraw(lambda: Dot(nl.n2p(val.get_value()), radius=px(16), color=OR))
        gap = always_redraw(lambda: BraceBetweenPoints(nl.n2p(val.get_value()) + UP * 0.35, nl.n2p(1.0) + UP * 0.35, direction=UP, color=RD) if 1 - val.get_value() > 0.004 else VGroup())
        self.add(dot)
        self.play(val.animate.set_value(0.99), run_time=0.6, rate_func=EXPO)
        self.add(gap)
        tb = self.c2(SER("a tiny bit less?", 78, RD), 980)
        self.until(wt(1, 7, 0.1)); self.play(FadeIn(tb, shift=UP * 0.15), val.animate.set_value(0.999), run_time=0.6, rate_func=EXPO)
        self.play(val.animate.set_value(0.99999), run_time=0.8, rate_func=rate_functions.ease_in_out_sine)
        # ===== 2. Call it x. Then 10x is 9.999... =====
        self.until(S[2])
        l1x = MT("x", "=", "0", r".999\ldots"); l1x.move_to([X(500), Y(640), 0])
        l2x = MT("10x", "=", "9", r".999\ldots"); l2x.move_to([0, Y(490), 0]); l2x.shift(RIGHT * (l1x[3].get_left()[0] - l2x[3].get_left()[0]))
        dx = X(490) - VGroup(l1x, l2x).get_center()[0]; l1x.shift(RIGHT * dx); l2x.shift(RIGHT * dx)
        self.ev("tick")
        self.play(FadeOut(VGroup(no, nl, l9, l1, dot, gap, tb), shift=UP * 0.2), ReplacementTransform(d2, l1x), run_time=0.45, rate_func=EXPO)
        self.remove(dot, gap)
        t10 = tag("× 10", 36, WHITE_, OR).next_to(l2x, UP, buff=0.25).align_to(l2x, LEFT)
        self.until(wt(2, 4, 0.1)); self.ev("tick"); self.play(FadeIn(l2x, shift=DOWN * 0.2), FadeIn(t10), run_time=0.35, rate_func=EXPO)
        self.play(Indicate(l2x[3], color=OR, scale_factor=1.06), Indicate(l1x[3], color=OR, scale_factor=1.06), run_time=0.7)
        # ===== 3. Subtract x, and the endless nines cancel. =====
        self.until(S[3])
        mn = MT("-", color=OR).next_to(l1x, LEFT, buff=0.35)
        rule = Line([X(130), Y(735), 0], [X(860), Y(735), 0], color=INK, stroke_width=5)
        self.ev("tick"); self.play(FadeOut(t10), FadeIn(mn), Create(rule), run_time=0.3)
        self.until(wt(3, 4, 0.1)); self.play(l1x[3].animate.set_color(OR), l2x[3].animate.set_color(OR), run_time=0.25)
        st = [Line(m.get_left() + LEFT * 0.08, m.get_right() + RIGHT * 0.08, color=OR, stroke_width=9) for m in (l1x[3], l2x[3])]
        self.until(wt(3, 6, 0.1)); self.ev("tick")
        self.play(*[Create(s) for s in st], l1x[3].animate.set_opacity(0.35), l2x[3].animate.set_opacity(0.35), run_time=0.35)
        # ===== 4. 9x = 9, so x is exactly 1. =====
        self.until(S[4])
        l3 = MT("9x", "=", "9"); l3.move_to([0, Y(835), 0]); l3.shift(RIGHT * (l1x[1].get_center()[0] - l3[1].get_center()[0]))
        self.until(wt(4, 0, 0.05)); self.ev("tick"); self.play(FadeIn(l3, shift=DOWN * 0.15), run_time=0.3, rate_func=EXPO)
        ans = MT("x", "=", "1", size=116, color=OR)
        ap = RoundedRectangle(width=ans.width + px(100), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=7)
        a_ = VGroup(ap, ans.move_to(ap)).move_to([X(340), Y(1020), 0])
        ys = VGroup(RoundedRectangle(width=px(240), height=px(120), corner_radius=0.22, fill_color=OR, fill_opacity=1, stroke_width=0))
        ys.add(H("YES", 58, WHITE_).move_to(ys[0])); ys.next_to(a_, RIGHT, buff=px(36))
        self.until(wt(4, 6, 0.12)); self.ev("stamp")
        self.play(FadeOut(cc), GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(ys, scale=1.3), run_time=0.25, rate_func=EXPO)
        # ===== 5. Still not sure? 1/3 = 0.333..., times 3 = 0.999... = 1 =====
        self.until(S[5])
        s1 = MT(r"\tfrac{1}{3}", "=", r"0.333\ldots"); self.c2(s1, 470)
        s2 = MT(r"\tfrac{3}{3}", "=", r"0.999\ldots"); self.c2(s2, 680)
        s2.shift(RIGHT * (s1[1].get_center()[0] - s2[1].get_center()[0]))
        t3 = tag("× 3", 40, WHITE_, OR).move_to([X(490), Y(575), 0])
        s3 = MT("1", "=", r"0.999\ldots", size=110, color=OR); self.c2(s3, 900)
        bx = SurroundingRectangle(s3, color=OR, buff=0.3, corner_radius=0.18, stroke_width=7)
        sn = self.c2(B("Still not sure?", 44, GREY_P, SEMIBOLD), 360)
        self.ev("tick"); self.play(FadeOut(VGroup(l1x, l2x, mn, rule, *st, l3, a_, ys), shift=UP * 0.25), FadeIn(sn), run_time=0.4, rate_func=EXPO)
        self.until(wt(5, 3, 0.1)); self.play(FadeIn(s1, shift=DOWN * 0.15), run_time=0.35, rate_func=EXPO)
        self.until(wt(5, 6, 0.1)); self.ev("tick"); self.play(FadeIn(t3, scale=1.2), run_time=0.25)
        self.until(wt(5, 9, 0.15)); self.play(TransformFromCopy(s1, s2), run_time=0.5, rate_func=EXPO)
        self.until(wt(5, 11, 0.1)); self.ev("stamp")
        self.play(TransformFromCopy(s2, s3), Create(bx), run_time=0.5, rate_func=rate_functions.ease_out_back)
        # ===== 6. Same number, two names. Comment TRICKS for the free sheet. =====
        self.until(S[6])
        tn = VGroup(H("0.999…", 96, INK), H("=", 96, GREY_P), H("1", 96, OR)).arrange(RIGHT, buff=0.35); self.c2(tn, 640)
        two = self.c2(SER("same number, two names", 64, OR), 800)
        self.ev("tick"); self.play(FadeOut(VGroup(sn, s1, s2, t3, s3, bx), shift=UP * 0.2), FadeIn(tn, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.play(FadeIn(two, shift=UP * 0.1), run_time=0.3)
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
        self.until(C[6] + 1.0); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(tn, two, fw, lb)


def _opts2(self, vals, y, w=176):
    row = VGroup()
    for L, v in zip("ABCD", vals):
        c_ = RoundedRectangle(width=px(w), height=px(104), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
        t_ = VGroup(B(L, 32, OR, SEMIBOLD), M(v, 50)).arrange(RIGHT, buff=0.18)
        if t_.width > px(w - 18): t_.scale_to_fit_width(px(w - 18))
        row.add(VGroup(c_, t_.move_to(c_)))
    row.arrange(RIGHT, buff=px(18)); return self.c2(row, y)
ShortReel2.opts2 = _opts2
ShortReel2.SAVE = "Save this for your exam"


class Telescope(ShortReel2):
    EVENTS = "tele"; SERIES = "Daily maths trick"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        RD = "#E5484D"
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        # ===== A. Can you add all 99 of these in 10 seconds? (terms writing on frame 0) =====
        q = self.c2(fitw(H("Add all 99 in 10 seconds?", 70, INK), 760), 360)
        parts = [r"\frac{1}{1\cdot2}", "+", r"\frac{1}{2\cdot3}", "+", r"\frac{1}{3\cdot4}", r"+\cdots+", r"\frac{1}{99\cdot100}"]
        sm = MathTex(*parts, font_size=72, color=INK); fitw(sm, 760); self.c2(sm, 530)
        opts = self.opts2([r"1", r"\tfrac{99}{100}", r"\tfrac{100}{99}", r"\tfrac{1}{100}"], 700)
        self.add(q, sm[0], opts)
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.15) for p in sm[1:]], lag_ratio=0.35), run_time=1.1, rate_func=EXPO)
        cc = self.comment_chip(self.SAVE)
        self.until(1.3); self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.3)
        # ===== B. Most students hunt for a common denominator. Don't. =====
        self.until(S[1])
        self.ev("tick"); self.play(FadeOut(VGroup(q, opts), shift=UP * 0.2), sm.animate.scale(0.85).move_to([X(490), Y(400), 0]), run_time=0.4, rate_func=EXPO)
        cd = self.c2(B("common denominator?", 44, GREY_P, SEMIBOLD), 560)
        big = self.c2(M(r"1\cdot2\cdot3\cdot4\cdots99\cdot100", 64), 660)
        self.until(wt(1, 5, 0.1)); self.play(FadeIn(cd), FadeIn(big, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        x1 = Line(big.get_corner(UL) + LEFT * 0.1, big.get_corner(DR) + RIGHT * 0.1, color=RD, stroke_width=10)
        x2 = Line(big.get_corner(DL) + LEFT * 0.1, big.get_corner(UR) + RIGHT * 0.1, color=RD, stroke_width=10)
        self.until(wt(1, 7, 0.05)); self.ev("tick"); self.play(Create(x1), Create(x2), run_time=0.3)
        # ===== C. Split every term: 1/k - 1/(k+1) =====
        self.until(S[2])
        idn = MathTex(r"\frac{1}{k(k+1)}", "=", r"\frac{1}{k}", "-", r"\frac{1}{k+1}", font_size=84, color=INK); self.c2(idn, 600)
        self.ev("tick"); self.play(FadeOut(VGroup(cd, big, x1, x2), shift=UP * 0.2), FadeIn(idn[0], shift=UP * 0.15), run_time=0.35, rate_func=EXPO)
        self.until(wt(2, 3, 0.1)); self.play(FadeIn(idn[1:3], shift=LEFT * 0.15), run_time=0.3)
        self.until(wt(2, 5, 0.15)); self.play(FadeIn(idn[3:], shift=LEFT * 0.15), idn[2].animate.set_color(OR), run_time=0.3)
        self.play(idn[4].animate.set_color(OR), run_time=0.2)
        # ===== D. Write them out, and the middle terms cancel in pairs. =====
        self.until(S[3])
        tk1 = ["1", "-", r"\tfrac12", "+", r"\tfrac12", "-", r"\tfrac13", "+", r"\tfrac13", "-", r"\tfrac14"]
        tk2 = ["+", r"\cdots", "+", r"\tfrac{1}{99}", "-", r"\tfrac{1}{100}"]
        e1 = MathTex(*tk1, font_size=84, color=INK); fitw(e1, 780); self.c2(e1, 770)
        e2 = MathTex(*tk2, font_size=84, color=INK); e2.scale(e1[2].height / MathTex(r"\tfrac12", font_size=84).height); self.c2(e2, 900)
        ex = VGroup(e1, e2)
        self.ev("tick"); self.play(idn.animate.scale(0.75).move_to([X(490), Y(590), 0]), Write(e1), run_time=0.8)
        self.play(Write(e2), run_time=0.4)
        def sl(m0, m1): return Line(m0.get_left() + LEFT * 0.05, m1.get_right() + RIGHT * 0.05, color=OR, stroke_width=8)
        st = [sl(e1[1], e1[4]), sl(e1[5], e1[8]), sl(e1[9], e1[10]), sl(e2[0], e2[3])]
        dim = [VGroup(*e1[1:5]), VGroup(*e1[5:9]), VGroup(*e1[9:11]), VGroup(*e2[0:4])]
        self.until(wt(3, 7, 0.15)); self.ev("tick")
        self.play(LaggedStart(*[AnimationGroup(Create(s_), d_.animate.set_opacity(0.3)) for s_, d_ in zip(st, dim)], lag_ratio=0.4), run_time=1.1)
        # ===== E. Only the first and the last survive: 1 - 1/100 =====
        self.until(S[4])
        self.play(e1[0].animate.set_color(OR).scale(1.2), run_time=0.25)
        self.until(wt(4, 5, 0.1)); self.play(e2[4:6].animate.set_color(OR).scale(1.2), run_time=0.25)
        rs = MathTex("=", "1", "-", r"\frac{1}{100}", font_size=84, color=INK); self.c2(rs, 1040); rs[1].set_color(OR); rs[3].set_color(OR)
        self.until(wt(4, 7, 0.1)); self.ev("tick"); self.play(TransformFromCopy(VGroup(e1[0], e2[4], e2[5]), rs[1:]), FadeIn(rs[0]), run_time=0.5, rate_func=EXPO)
        # ===== F. So the sum is 99/100. Option B. =====
        self.until(S[5])
        self.play(FadeOut(VGroup(idn, ex, *st), shift=UP * 0.2), rs.animate.move_to([X(490), Y(560), 0]), run_time=0.35, rate_func=EXPO)
        ans = MathTex(r"\frac{99}{100}", font_size=120, color=OR)
        ap = RoundedRectangle(width=ans.width + px(110), height=ans.height + px(60), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=7)
        a_ = VGroup(ap, ans.move_to(ap)).move_to([X(400), Y(880), 0])
        ob = VGroup(RoundedRectangle(width=px(230), height=px(110), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0)); ob.add(H("B", 64, WHITE_).move_to(ob[0])); ob.next_to(a_, RIGHT, buff=px(30))
        self.play(FadeOut(cc), run_time=0.2)
        self.until(wt(5, 4, 0.12)); self.ev("stamp"); self.play(GrowFromCenter(a_), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(wt(5, 6, 0.1)); self.play(FadeIn(ob, scale=1.3), run_time=0.25, rate_func=EXPO)
        # ===== G. Save this. Follow TutorDA and comment TRICKS to get the PDF. =====
        self.until(S[6])
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
        self.until(C[6] + 1.2); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(sm, rs, a_, ob, fw, lb)


class Pow2(ShortReel2):
    EVENTS = "pw2"; SERIES = "Daily maths trick"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        RD = "#E5484D"
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        q = self.c2(H("Which is bigger?", 84, INK), 360)
        ang = ValueTracker(6 * DEGREES); piv = [X(490), Y(700), 0]; L = px(560); drop = 0
        lt, rt = MathTex(r"31^{11}", font_size=84, color=INK), MathTex(r"17^{14}", font_size=84, color=INK)
        la, ra = B("A", 34, OR, SEMIBOLD), B("B", 34, OR, SEMIBOLD)
        def card(num, lab):
            r = RoundedRectangle(width=num.width + px(70), height=px(150), corner_radius=0.16, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            num.move_to(r); return VGroup(r, num)
        cl, cr = card(lt, la), card(rt, ra)
        def bal():
            a = ang.get_value(); d = np.array([np.cos(a), np.sin(a), 0]) * L / 2
            pl, pr = np.array(piv) - d, np.array(piv) + d
            cl.move_to(pl + UP * (cl.height / 2 + 0.05)); cr.move_to(pr + UP * (cr.height / 2 + 0.05))
            return Line(pl, pr, color=INK, stroke_width=10)
        stand = VGroup(Polygon([X(490), Y(700), 0], [X(440), Y(810), 0], [X(540), Y(810), 0], fill_color=INK, fill_opacity=1, stroke_width=0))
        scale_ = always_redraw(bal)
        self.add(q, stand, scale_, cl, cr)
        self.play(ang.animate.set_value(-6 * DEGREES), run_time=0.9, rate_func=rate_functions.ease_in_out_sine)
        self.play(ang.animate.set_value(4 * DEGREES), run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        cc = self.comment_chip(self.SAVE); self.ev("tick"); self.play(FadeIn(cc, shift=UP * 0.15), ang.animate.set_value(0), run_time=0.5)
        # ===== B. Most people pick 31^11 (base is bigger) =====
        self.until(S[1])
        bb = self.c2(SER("bigger base?", 72, RD), 960)
        self.until(wt(1, 3, 0.1)); self.ev("tick")
        self.play(ang.animate.set_value(10 * DEGREES), lt.animate.set_color(RD), run_time=0.5, rate_func=EXPO)
        self.until(wt(1, 6, 0.1)); self.play(FadeIn(bb, shift=UP * 0.15), run_time=0.3)
        # ===== C. Compare both with powers of 2 =====
        self.until(S[2])
        pw = VGroup(*[tag(s, 40, INK, PAPER2) for s in ("2", "4", "8", "16", "32", "64")]).arrange(RIGHT, buff=px(14)); self.c2(pw, 960)
        self.ev("tick"); self.play(FadeOut(bb), lt.animate.set_color(INK), ang.animate.set_value(0), run_time=0.35)
        self.until(wt(2, 6, 0.15)); self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pw], lag_ratio=0.15), run_time=0.7)
        self.play(Indicate(pw[3], color=OR), Indicate(pw[4], color=OR), run_time=0.6)
        # ===== D. 31 < 32 so 31^11 < 2^55 =====
        self.until(S[3])
        sc = VGroup(stand, lt, rt, la, ra)
        self.remove(scale_); frozen = bal(); self.add(frozen)
        allsc = VGroup(frozen, stand, cl, cr)
        self.ev("tick"); self.play(FadeOut(VGroup(q, pw), shift=UP * 0.2), allsc.animate.scale(0.62).move_to([X(490), Y(450), 0]), run_time=0.45, rate_func=EXPO)
        r1 = MathTex("31", "<", "32", "=", "2^5", font_size=76, color=INK); self.c2(r1, 680)
        r2 = MathTex(r"31^{11}", "<", r"32^{11}", "=", r"2^{55}", font_size=76, color=INK); self.c2(r2, 790)
        self.until(wt(3, 4, 0.15)); self.play(FadeIn(r1, shift=UP * 0.12), run_time=0.35, rate_func=EXPO)
        self.until(wt(3, 6, 0.15)); self.play(FadeIn(r2, shift=UP * 0.12), run_time=0.35, rate_func=EXPO)
        self.until(wt(3, 10, 0.15)); self.play(r2[4].animate.set_color(OR), run_time=0.25)
        # ===== E. 17 > 16 so 17^14 > 2^56 =====
        self.until(S[4])
        r3 = MathTex("17", ">", "16", "=", "2^4", font_size=76, color=INK); self.c2(r3, 930)
        r4 = MathTex(r"17^{14}", ">", r"16^{14}", "=", r"2^{56}", font_size=76, color=INK); self.c2(r4, 1040)
        self.until(wt(4, 4, 0.15)); self.ev("tick"); self.play(FadeIn(r3, shift=UP * 0.12), run_time=0.35, rate_func=EXPO)
        self.until(wt(4, 6, 0.15)); self.play(FadeIn(r4, shift=UP * 0.12), run_time=0.35, rate_func=EXPO)
        self.until(wt(4, 10, 0.15)); self.play(r4[4].animate.set_color(OR), run_time=0.25)
        # ===== F. 2^56 beats 2^55: 17^14 wins (by more than 6 times) =====
        self.until(S[5])
        ch = MathTex(r"31^{11}", "<", r"2^{55}", "<", r"2^{56}", "<", r"17^{14}", font_size=80, color=INK); fitw(ch, 760); self.c2(ch, 1010)
        ch[2].set_color(OR); ch[4].set_color(OR)
        self.play(FadeOut(VGroup(r1, r3), shift=UP * 0.15), r2.animate.move_to([X(490), Y(700), 0]), r4.animate.move_to([X(490), Y(840), 0]), run_time=0.35, rate_func=EXPO)
        self.play(FadeOut(cc), run_time=0.2)
        self.until(wt(5, 1, 0.1)); self.ev("tick"); self.play(FadeIn(ch[:6], shift=UP * 0.12), run_time=0.4, rate_func=EXPO)
        self.until(wt(5, 3, 0.1)); self.play(FadeIn(ch[6], shift=UP * 0.12), ch[6].animate.set_color(OR), run_time=0.3)
        # tip the (small) balance to B and box 17^14
        piv2 = stand.get_top(); self.remove(frozen)
        ang.set_value(0); L = L * 0.62; drop = drop * 0.62; piv = piv2
        scale2 = always_redraw(bal); self.add(scale2)
        cr[0].set_stroke(OR, 6)
        self.until(wt(5, 4, 0.1)); self.ev("stamp")
        self.play(ang.animate.set_value(-12 * DEGREES), rt.animate.set_color(OR), run_time=0.5, rate_func=rate_functions.ease_out_back)
        x6 = tag("× 6.6", 40, WHITE_, OR).next_to(cr, UP, buff=0.12)
        self.until(wt(5, 8, 0.15)); self.play(FadeIn(x6, scale=1.2), run_time=0.3)
        # ===== G. CTA =====
        self.until(S[6])
        fw = self.comment_chip(self.CTA); fw[0].set_fill(OR)
        self.until(C[6] + 1.2); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(scale2, stand, cl, cr, x6, r2, r4, ch, fw, lb)


class AvgSpeed(ShortReel2):
    """Average speed trap (15 Nov). 60 km/h there, 40 back, same distance: average = 2ab/(a+b) = 48, not 50.
    Checked in Python with fractions for d = 1, 7, 120, 300 km: always 48. Rope-reel format: guessable question on frame 0,
    assumption said out loud ("same distance both ways"), the middle step spoken, a save-worthy rule card, send line echoes the hook."""
    EVENTS = "avgspeed"; SERIES = "JEE Main · Maths"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)     # subtitles in the footer space (Aro, 14 Nov)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        q1 = self.c2(H("60 there, 40 back.", 66, INK), 410)
        q2 = self.c2(H("Average speed?", 58, OR), 482)
        # ---- the road: home -> college ----
        xa, xb, ry = 190, 770, 650
        road = Line(P(xa, ry), P(xb, ry), color=INK, stroke_width=6)
        da, db = Dot(P(xa, ry), radius=px(13), color=INK), Dot(P(xb, ry), radius=px(13), color=INK)
        la, lbb = B("Home", 32, GREY_P, SEMIBOLD).move_to(P(xa, ry + 44)), B("College", 32, GREY_P, SEMIBOLD).move_to(P(xb, ry + 44))
        s60 = H("60 km/h  →", 36, BLUE).move_to(P(480, ry - 50))
        s40 = H("←  40 km/h", 36, OR).move_to(P(480, ry + 92))
        car = Dot(P(xa, ry), radius=px(20), color=OR).set_z_index(5)
        # the car shuttles for the whole reel: out in 1.0 s (60), back in 1.5 s (40), so the screen never stands still
        t0 = self.renderer.time
        def drive(m):
            u = (self.renderer.time - t0) % 2.5
            f = u / 1.0 if u < 1.0 else 1 - (u - 1.0) / 1.5
            m.move_to(P(xa + (xb - xa) * f, ry))
        car.add_updater(drive)
        self.add(road, da, db, la, lbb, s60, car, q1, q2)
        self.until(wt(0, 6, 0.08)); self.ev("tick"); self.play(FadeIn(s40, shift=LEFT * 0.1), run_time=0.3, rate_func=EXPO)
        self.until(C[1] - 0.05)
        # ===== B. options; "50" crossed on "Nope" =====
        def pill(s):
            r = RoundedRectangle(width=px(200), height=px(74), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            return VGroup(r, H(s, 44, INK).move_to(r))
        ops = [pill("50"), pill("48"), pill("45")]
        for o, x in zip(ops, (270, 490, 710)): o.move_to(P(x, 840))
        self.ev("tick"); self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.08) for o in ops], lag_ratio=0.12), run_time=0.4, rate_func=EXPO)
        self.until(wt(1, 4, 0.08)); self.play(Indicate(ops[0], color=OR, scale_factor=1.1), run_time=0.4)
        x50 = Line(ops[0][0].get_corner(DL) + UR * px(10), ops[0][0].get_corner(UR) + DL * px(10), color=RD, stroke_width=8)
        self.until(wt(1, 5, 0.06)); self.ev("stamp"); self.play(Create(x50), ops[0][1].animate.set_color(GREY_P), run_time=0.25)
        # ===== C. 120 km: 2 h going, 3 h back (time bars, 120 px per hour) =====
        km = tag("120 km", 30, WHITE_, INK).move_to(P(480, ry))
        self.until(wt(2, 1, 0.08)); self.ev("tick"); self.play(FadeIn(km, scale=1.15), run_time=0.3, rate_func=EXPO)
        bx, by, hh = 190, 975, 64
        def bar(x0, hours, col, txt):
            r = Rectangle(width=px(120 * hours), height=px(hh), fill_color=col, fill_opacity=1, stroke_width=0)
            r.move_to(P(x0 + 60 * hours, by)); t = H(txt, 36, WHITE_).move_to(r); return VGroup(r, t)
        g = bar(bx, 2, BLUE, "2 h"); b3 = bar(bx + 240, 3, OR, "3 h")
        tl = B("time", 28, GREY_P, SEMIBOLD).move_to(P(bx - 10, by - 58)).align_to(g, LEFT)
        self.until(wt(2, 3, 0.08)); self.play(FadeIn(tl), GrowFromEdge(g, LEFT), run_time=0.6, rate_func=rate_functions.linear)
        self.until(wt(2, 6, 0.08)); self.play(GrowFromEdge(b3, LEFT), run_time=0.9, rate_func=rate_functions.linear)
        # ===== D. 240 km / 5 h = 48 (the one spring moment) =====
        eq = M(r"\frac{240\ \text{km}}{5\ \text{h}} = 48\ \text{km/h}", 54, INK).move_to(P(490, 1105))
        self.until(C[3] - 0.05); self.ev("wipe"); self.play(FadeIn(eq, shift=UP * 0.08), run_time=0.4, rate_func=EXPO)
        ans = ops[1]
        tick = VGroup(Circle(radius=px(18), fill_color=WHITE_, fill_opacity=1, stroke_width=0), B("✓", 24, OR, SEMIBOLD)); tick[1].move_to(tick[0])
        tick.move_to(ans[0].get_left() + RIGHT * px(32))
        self.until(wt(3, 5, 0.12)); self.ev("stamp")
        self.play(ans[0].animate.set_fill(OR, 1).set_stroke(OR, 6), ans[1].animate.set_color(WHITE_).shift(RIGHT * px(16)), FadeIn(tick, scale=1.4),
                  ops[2].animate.set_opacity(0.4), eq.animate.set_color(OR_D),
                  run_time=0.45, rate_func=rate_functions.ease_out_back)
        # ===== E. the rule: same distance both ways -> 2ab/(a+b) =====
        rt = B("Same distance both ways", 30, GREY_P, SEMIBOLD)
        rf = M(r"\bar v = \frac{2ab}{a+b}", 60, INK)
        rule = VGroup(rt, rf).arrange(DOWN, buff=px(14))
        rbox = RoundedRectangle(width=rule.width + px(90), height=rule.height + px(48), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=5)
        card = VGroup(rbox, rule.move_to(rbox)); self.c2(card, 1298)
        self.until(wt(4, 3, 0.1)); self.ev("tick"); self.play(FadeIn(rbox), FadeIn(rt, shift=UP * 0.06), run_time=0.35, rate_func=EXPO)
        self.until(wt(4, 9, 0.1)); self.play(Write(rf), run_time=0.6)
        # ===== F. send line, held to the last frame =====
        self.until(C[-1] - 0.02)
        ft = VGroup(H("Send this to", 44, WHITE_), H("a 50 guesser", 44, WHITE_)).arrange(DOWN, buff=px(6))
        fw = VGroup(RoundedRectangle(width=ft.width + px(80), height=ft.height + px(40), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0)); fw.add(ft.move_to(fw[0]))
        self.c2(fw, 1560); fw.set_z_index(22); self.ev("tick"); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.4, rate_func=EXPO)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class SdShift(ShortReel2):
    """Statistics (16 Nov): add 10 to every mark, the standard deviation does not change; double every mark and it doubles.
    Checked in Python: marks 40, 55, 60, 70, 85 -> sigma 15.03; +10 -> 15.03; x2 -> 30.07 (population SD).
    Fixes from the avg-speed review: 16-17 s, the rule card arrives with the answer (not at the end), one moving picture,
    a less familiar surprise than the classic trick question."""
    EVENTS = "sdshift"; SERIES = "JEE Main · Statistics"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        q1 = self.c2(H("+10 to every mark.", 66, INK), 418)
        q2 = self.c2(H("Standard deviation?", 56, OR), 490)
        sig = tag("σ = 15", 36, WHITE_, INK).move_to(P(490, 575))
        marks = [40, 55, 60, 70, 85]
        mx = lambda m: 130 + (m - 30) * 10
        def axis(y, alpha=1.0):
            ln = Line(P(120, y), P(840, y), color=INK, stroke_width=4)
            tk = VGroup(*[Line(P(mx(v), y - 8), P(mx(v), y + 8), color=INK, stroke_width=3) for v in range(30, 101, 10)])
            tl = VGroup(*[B(str(v), 26, GREY_P, SEMIBOLD).move_to(P(mx(v), y + 32)) for v in range(30, 101, 10)])
            return VGroup(ln, tk, tl).set_opacity(alpha)
        ya, yb = 730, 960
        ax1 = axis(ya); t0 = self.renderer.time
        def row(vals, y, col):
            g = VGroup()
            for i, v in enumerate(vals):
                d = Dot(P(mx(v), y - 36), radius=px(20), color=col); t = B(str(v), 30, INK, SEMIBOLD).move_to(P(mx(v), y - 80))
                g.add(VGroup(d, t))
            return g
        r1 = row(marks, ya, BLUE)
        # frame 0 already moving: the marks bob gently
        for i, m in enumerate(r1):
            base = m.get_center().copy()
            m.add_updater(lambda mob, b=base, ph=i * 1.1: mob.move_to(b + UP * px(5) * math.sin(2 * math.pi * (self.renderer.time - t0) / 1.4 + ph)))
        self.add(ax1, r1, q1, q2, sig)
        # ===== B. options; +10 crossed on "Nope" =====
        def pill(s):
            r = RoundedRectangle(width=px(200), height=px(74), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            return VGroup(r, H(s, 42, INK).move_to(r))
        ops = [pill("+10"), pill("Same"), pill("−10")]
        for o, x in zip(ops, (270, 490, 710)): o.move_to(P(x, 1100))
        self.until(C[1] - 0.05); self.ev("tick")
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.08) for o in ops], lag_ratio=0.12), run_time=0.4, rate_func=EXPO)
        self.until(wt(1, 4, 0.08)); self.play(Indicate(ops[0], color=OR, scale_factor=1.1), run_time=0.4)
        x10 = Line(ops[0][0].get_corner(DL) + UR * px(10), ops[0][0].get_corner(UR) + DL * px(10), color=RD, stroke_width=8)
        self.until(wt(1, 6, 0.06)); self.ev("stamp"); self.play(Create(x10), ops[0][1].animate.set_color(GREY_P), run_time=0.25)
        # ===== C. every mark moves 10 right: copy slides to a second line; same gaps on both =====
        ax2 = axis(yb); r2 = row([m + 10 for m in marks], yb, OR)
        lbA = B("before", 28, GREY_P, SEMIBOLD).move_to(P(130, ya - 128)).align_to(ax1[0], LEFT)
        lbB = B("after +10", 28, OR, SEMIBOLD).move_to(P(130, yb - 128)).align_to(ax1[0], LEFT)
        self.until(wt(2, 2, 0.1)); self.ev("wipe")
        for m in r1: m.clear_updaters()
        ghost = r1.copy()
        self.add(ghost)
        self.play(FadeIn(ax2), FadeIn(lbA), FadeIn(lbB), Transform(ghost, r2), run_time=0.9, rate_func=rate_functions.ease_in_out_cubic)
        def gaps(r, y):
            g = VGroup()
            for a, b in zip(r[:-1], r[1:]):
                xa, xb = a[0].get_center()[0], b[0].get_center()[0]
                ar = DoubleArrow([xa, Y(y), 0], [xb, Y(y), 0], buff=px(20), color=TEAL, stroke_width=4, tip_length=0.09, max_tip_length_to_length_ratio=0.35)
                g.add(ar)
            return g
        gA, gB = gaps(r1, ya - 36), gaps(ghost, yb - 36)
        self.until(wt(2, 9, 0.1)); self.ev("tick")
        self.play(LaggedStart(*[GrowFromCenter(a) for a in gA], lag_ratio=0.1), LaggedStart(*[GrowFromCenter(a) for a in gB], lag_ratio=0.1), run_time=0.7)
        # ===== D. still 15 (the one spring moment) + first rule line =====
        ans = ops[1]
        tick = VGroup(Circle(radius=px(18), fill_color=WHITE_, fill_opacity=1, stroke_width=0), B("✓", 24, OR, SEMIBOLD)); tick[1].move_to(tick[0])
        tick.move_to(ans[0].get_left() + RIGHT * px(32))
        sig2 = tag("σ = 15", 34, WHITE_, OR).move_to(P(730, yb - 128))
        rr1 = M(r"x + c:\ \ \sigma\ \text{same}", 56, INK)
        rr2 = M(r"k\,x:\ \ \sigma \times |k|", 56, INK)
        rule = VGroup(rr1, rr2).arrange(DOWN, buff=px(18), aligned_edge=LEFT)
        rbox = RoundedRectangle(width=rule.width + px(100), height=rule.height + px(52), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=5)
        card = VGroup(rbox, rule.move_to(rbox)); self.c2(card, 1285)
        self.until(wt(3, 1, 0.12)); self.ev("stamp")
        self.play(ans[0].animate.set_fill(OR, 1).set_stroke(OR, 6), ans[1].animate.set_color(WHITE_).shift(RIGHT * px(16)), FadeIn(tick, scale=1.4),
                  ops[2].animate.set_opacity(0.4), FadeIn(sig2, scale=1.3), FadeIn(rbox), FadeIn(rr1, shift=UP * 0.06),
                  run_time=0.45, rate_func=rate_functions.ease_out_back)
        # ===== E. double every mark: sigma doubles =====
        self.until(wt(4, 0, 0.08)); self.ev("tick"); self.play(FadeIn(rr2, shift=UP * 0.06), run_time=0.35, rate_func=EXPO)
        self.until(wt(4, 6, 0.08)); self.play(Indicate(rr2, color=OR, scale_factor=1.08), run_time=0.5)
        # ===== F. send line in the footer, held to the last frame; marks bob again =====
        for i, m in enumerate(ghost):
            base = m.get_center().copy()
            m.add_updater(lambda mob, b=base, ph=i * 1.1: mob.move_to(b + UP * px(5) * math.sin(2 * math.pi * (self.renderer.time - t0) / 1.4 + ph)))
        self.until(C[-1] - 0.02)
        ft = VGroup(H("Follow TutorDA", 44, WHITE_), H("Comment PDF", 44, WHITE_)).arrange(DOWN, buff=px(6))   # Aro, 16 Nov: follow + PDF ask
        fw = VGroup(RoundedRectangle(width=ft.width + px(80), height=ft.height + px(40), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0)); fw.add(ft.move_to(fw[0]))
        self.c2(fw, 1560); fw.set_z_index(22); self.ev("tick"); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.4, rate_func=EXPO)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PhyFall(ShortReel2):
    """JEE physics (19 Nov): drop one ball, throw one sideways from the same height; both land together.
    Checked in Python: h = 20 m, g = 10 m/s^2 -> t = sqrt(2h/g) = 2 s for both; thrown at 15 m/s lands 30 m out.
    Rope format: everyday guess on frame 0, 3 options, assumption said aloud ("ignore air"), rule card with the answer.
    Ending per Aro (19 Nov): Follow TutorDA only."""
    EVENTS = "phyfall"; SERIES = "JEE Main · Physics"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        q1 = self.c2(H("Which lands first?", 66, INK), 400)
        top, gy, x0 = 600, 1130, 300
        PXM_Y, PXM_X, v = 26.5, 14.0, 15.0
        cliff = Rectangle(width=px(160), height=px(gy - top), fill_color="#D9D3C7", fill_opacity=1, stroke_width=0).move_to(P(200, (top + gy) / 2))
        h20 = B("20 m", 34, INK, SEMIBOLD).rotate(PI / 2).move_to(P(200, (top + gy) / 2))
        ground = Line(P(110, gy), P(835, gy), color=INK, stroke_width=5)
        tau = ValueTracker(0.0)
        def pos(which, t):
            y = top - 22 + PXM_Y * 5 * t * t
            x = x0 + 22 if which == 0 else x0 + 76 + PXM_X * v * t
            return P(x, y)
        ballA = Dot(pos(0, 0), radius=px(22), color=BLUE).set_z_index(6)
        ballB = Dot(pos(1, 0), radius=px(22), color=OR).set_z_index(6)
        t0 = self.renderer.time
        ballA.add_updater(lambda m: m.move_to(pos(0, tau.get_value())))
        ballB.add_updater(lambda m: m.move_to(pos(1, tau.get_value())))
        la = B("dropped", 30, BLUE, SEMIBOLD).move_to(P(x0 - 20, top - 72))
        lbb = B("thrown", 30, OR, SEMIBOLD).move_to(P(x0 + 167, top - 72))
        arr = Arrow(P(x0 + 112, top - 22), P(x0 + 222, top - 22), buff=0, color=OR, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        arr.add_updater(lambda m: m.set_opacity(0 if tau.get_value() > 0.02 else 0.55 + 0.45 * math.sin(2 * math.pi * (self.renderer.time - t0) / 0.9)))
        self.add(cliff, h20, ground, ballA, ballB, la, lbb, arr, q1)
        # ===== B. options =====
        def pill(s):
            r = RoundedRectangle(width=px(230), height=px(74), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            return VGroup(r, H(s, 34, INK).move_to(r))
        ops = [pill("Dropped"), pill("Thrown"), pill("Same time")]
        for o, x in zip(ops, (240, 478, 716)): o.move_to(P(x, 1240))
        self.until(C[1] - 0.05); self.ev("tick")
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.08) for o in ops], lag_ratio=0.12), run_time=0.4, rate_func=EXPO)
        self.until(wt(1, 8, 0.08)); self.play(Indicate(ops[0], color=OR, scale_factor=1.1), run_time=0.45)
        # ===== C. the fall: ghost pairs and level lines every 0.5 s =====
        self.until(wt(2, 2, 0.05)); self.ev("wipe")
        self.play(FadeOut(la), FadeOut(lbb), run_time=0.2)
        T_end = wt(3, 0, 0.06); seg = max(0.3, (T_end - self.renderer.time) / 4)
        for k in range(1, 5):
            self.play(tau.animate.set_value(0.5 * k), run_time=seg, rate_func=rate_functions.linear)
            if k < 4:
                ga, gb = Dot(pos(0, 0.5 * k), radius=px(14), color=BLUE).set_opacity(0.35), Dot(pos(1, 0.5 * k), radius=px(14), color=OR).set_opacity(0.35)
                ln = DashedLine(pos(0, 0.5 * k), pos(1, 0.5 * k), color=TEAL, stroke_width=4, dash_length=0.08)
                self.add(ln, ga, gb)
        # ===== D. same time (the one spring moment) =====
        ans = ops[2]
        tick = VGroup(Circle(radius=px(18), fill_color=WHITE_, fill_opacity=1, stroke_width=0), B("✓", 24, OR, SEMIBOLD)); tick[1].move_to(tick[0])
        tick.move_to(ans[0].get_left() + RIGHT * px(26))
        ta = tag("2 s", 30, WHITE_, BLUE).move_to(P(x0 + 22, gy + 42)); tb = tag("2 s", 30, WHITE_, OR).move_to(P(x0 + 76 + PXM_X * v * 2, gy + 42))
        self.ev("stamp")
        self.play(ans[0].animate.set_fill(OR, 1).set_stroke(OR, 6), ans[1].animate.set_color(WHITE_).shift(RIGHT * px(22)), FadeIn(tick, scale=1.4),
                  ops[0].animate.set_opacity(0.4), ops[1].animate.set_opacity(0.4), FadeIn(ta, scale=1.3), FadeIn(tb, scale=1.3),
                  run_time=0.45, rate_func=rate_functions.ease_out_back)
        # ===== E. rule card =====
        rf = M(r"t = \sqrt{2h/g} = \sqrt{2\cdot 20/10} = 2\ \text{s}", 38, INK)
        rt = B("Sideways speed doesn't change the fall", 28, GREY_P, SEMIBOLD)
        rule = VGroup(rf, rt).arrange(DOWN, buff=px(12))
        rbox = RoundedRectangle(width=rule.width + px(70), height=rule.height + px(40), corner_radius=0.2, fill_color=WHITE_, fill_opacity=1, stroke_color=OR, stroke_width=5)
        card = VGroup(rbox, rule.move_to(rbox)); self.c2(card, 1358)
        self.until(C[4] - 0.05); self.ev("tick"); self.play(FadeIn(rbox), FadeIn(rf, shift=UP * 0.06), run_time=0.4, rate_func=EXPO)
        self.until(wt(4, 5, 0.08)); self.play(FadeIn(rt, shift=UP * 0.06), run_time=0.35, rate_func=EXPO)
        # ===== F. follow card in the footer; the 'same time' pill keeps breathing =====
        base_s = ans.get_center().copy()
        ans[0].add_updater(lambda m: m.set_stroke(OR, 6 + 4 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 1.1))))
        self.until(C[-1] - 0.02)
        ft = VGroup(H("Follow TutorDA", 44, WHITE_), H("for JEE physics", 40, WHITE_)).arrange(DOWN, buff=px(6))
        fw = VGroup(RoundedRectangle(width=ft.width + px(80), height=ft.height + px(40), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0)); fw.add(ft.move_to(fw[0]))
        self.c2(fw, 1560); fw.set_z_index(22); self.ev("tick"); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.4, rate_func=EXPO)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoA(ShortReel2):
    """JEE course promo, script A '5-mark trap' (20 Nov). Value first (the sqrt(x^2) = |x| trap, +4/-1 marking),
    then the personalised scorecard, the 300/300 challenge, free trial -> Rs 99/month, 'Comment LINK'.
    The scorecard is a SAMPLE illustration (223 = 68 + 74 + 81), labelled as such on screen."""
    EVENTS = "promoa"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        q1 = self.c2(H("Spot the mistake.", 60, INK), 430)
        eq = M(r"\sqrt{x^2} = x", 130, INK).move_to(P(490, 640))
        mk = tag("JEE Main:  +4 right,  −1 wrong", 30, WHITE_, INK).move_to(P(490, 820))
        eq.add_updater(lambda m: m.set_opacity(1).scale_to_fit_height(m.height))  # keep reference
        pulse = always_redraw(lambda: SurroundingRectangle(eq, buff=px(26), corner_radius=0.18, color=OR,
                              stroke_width=4 + 3 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 1.0))))
        self.add(q1, eq, mk, pulse)
        # ===== B. not x, it's |x| =====
        rx = eq[0][-1]
        strike = Line(rx.get_corner(DL) + DL * px(8), rx.get_corner(UR) + UR * px(8), color=RD, stroke_width=10)
        self.until(wt(1, 4, 0.06)); self.ev("stamp"); self.play(Create(strike), run_time=0.25)
        eq2 = M(r"\sqrt{x^2} = |x|", 120, INK).move_to(P(490, 640)); eq2[0][-3:].set_color(TEAL)
        self.until(wt(1, 7, 0.08)); self.ev("tick"); eq.clear_updaters()
        self.play(FadeOut(strike), TransformMatchingShapes(eq, eq2), run_time=0.5, rate_func=EXPO); eq = eq2
        # ===== C. x = -3 check =====
        c1 = M(r"x = -3:", 64, INK); c2 = M(r"\sqrt{9} = 3", 64, INK); c3 = M(r"\neq -3", 64, RD)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=px(26)); fitw(row, 700); row.move_to(P(490, 950))
        self.until(C[2] - 0.05); self.play(FadeIn(c1, shift=UP * 0.08), run_time=0.3, rate_func=EXPO)
        self.until(wt(2, 3, 0.08)); self.play(FadeIn(c2, shift=UP * 0.08), run_time=0.3, rate_func=EXPO)
        self.until(wt(2, 7, 0.08)); self.ev("tick"); self.play(FadeIn(c3, scale=1.2), run_time=0.3, rate_func=EXPO)
        # ===== D. +4 missed, -1 taken: 5 marks =====
        p4 = tag("+4  missed", 40, WHITE_, GREY_P); m1 = tag("−1  taken", 40, WHITE_, RD); tot = H("= 5 marks gone", 52, RD)
        drow = VGroup(p4, m1).arrange(RIGHT, buff=px(30)).move_to(P(490, 1080)); tot.move_to(P(490, 1185))
        self.until(C[3] - 0.05); self.play(FadeIn(p4, shift=UP * 0.08), run_time=0.3, rate_func=EXPO)
        self.until(wt(3, 3, 0.08)); self.play(FadeIn(m1, shift=UP * 0.08), run_time=0.3, rate_func=EXPO)
        self.until(wt(3, 6, 0.0)); self.ev("stamp"); self.play(FadeIn(tot, scale=1.15), run_time=0.35, rate_func=rate_functions.ease_out_back)
        part1 = VGroup(q1, eq, mk, row, drow, tot)
        # ===== E. the scorecard (sample) =====
        cw, ch, cy = 700, 800, 860
        card = RoundedRectangle(width=px(cw), height=px(ch), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, cy))
        top = cy - ch / 2
        ttl = H("Your TutorDA scorecard", 42, INK).move_to(P(490, top + 52)).align_to(card, LEFT).shift(RIGHT * px(36))
        smp = tag("SAMPLE", 22, WHITE_, GREY_P).move_to(P(490 + cw / 2 - 72, top + 96))
        sub = B("Mock test 7 · JEE Main pattern", 28, GREY_P, SEMIBOLD).next_to(ttl, DOWN, buff=px(8)).align_to(ttl, LEFT)
        # row 1: marks + subject bars
        r1y = top + 205
        mlab = B("Marks", 30, GREY_P, SEMIBOLD).move_to(P(160, r1y - 40)).align_to(ttl, LEFT)
        score = H("223 / 300", 60, INK).move_to(P(250, r1y + 12)).align_to(ttl, LEFT)
        subs = [("Maths", 68, BLUE), ("Physics", 74, TEAL), ("Chemistry", 81, OR)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(subs):
            yy = r1y - 42 + i * 46
            nmt = B(nm, 26, INK, SEMIBOLD).move_to(P(560, yy)).align_to(P(462, yy), LEFT)
            bg = Rectangle(width=px(110), height=px(18), fill_color="#ECE7DE", fill_opacity=1, stroke_width=0).move_to(P(695, yy))
            fg = Rectangle(width=px(110 * v / 100), height=px(18), fill_color=col, fill_opacity=1, stroke_width=0).set_z_index(3).move_to(bg.get_left() + RIGHT * px(110 * v / 200))
            val = B(str(v), 26, INK, SEMIBOLD).next_to(bg, RIGHT, buff=px(8))
            bars.add(VGroup(nmt, bg, fg, val))
        # row 2: lagging in
        r2y = top + 400
        llab = B("Lagging in", 30, GREY_P, SEMIBOLD).move_to(P(160, r2y - 40)).align_to(ttl, LEFT)
        lag1 = VGroup(Dot(radius=px(9), color=RD), B("Algebra: modulus  (−5 marks)", 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(12))
        lag2 = VGroup(Dot(radius=px(9), color=OR), B("Rotational motion", 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(12))
        lags = VGroup(lag1, lag2).arrange(DOWN, buff=px(12), aligned_edge=LEFT).move_to(P(490, r2y + 16)).align_to(ttl, LEFT)
        # row 3: fix next
        r3y = top + 610
        flab = B("Fix next", 30, GREY_P, SEMIBOLD).move_to(P(160, r3y - 40)).align_to(ttl, LEFT)
        fixt = VGroup(M(r"\sqrt{x^2} = |x|", 46, TEAL), B("revise modulus rules", 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(16)).move_to(P(490, r3y + 10)).align_to(ttl, LEFT)
        seps = VGroup(*[Line(P(490 - cw / 2 + 30, top + yy), P(490 + cw / 2 - 30, top + yy), color=RULE, stroke_width=2) for yy in (118, 312, 525)])
        sc = VGroup(card, seps, ttl, smp, sub, mlab, score, bars, llab, lags, flab, fixt)
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(FadeOut(part1, shift=UP * 0.3), FadeOut(pulse), run_time=0.35)
        self.play(FadeIn(card, shift=UP * 0.2), FadeIn(seps), FadeIn(ttl), FadeIn(smp), FadeIn(sub), FadeIn(mlab), FadeIn(score),
                  LaggedStart(*[GrowFromEdge(b[2], LEFT) for b in bars], lag_ratio=0.15), *[FadeIn(VGroup(b[0], b[1], b[3])) for b in bars],
                  FadeIn(llab), FadeIn(lags), FadeIn(flab), FadeIn(fixt), run_time=0.7, rate_func=EXPO)
        self.until(wt(4, 4, 0.08)); self.ev("tick"); self.play(Indicate(lag1, color=RD, scale_factor=1.06), run_time=0.5)
        # ===== F. marks / lagging / fix next light up in turn =====
        def hl(mob):
            return SurroundingRectangle(mob, buff=px(14), corner_radius=0.12, color=OR, stroke_width=5)
        h1 = hl(VGroup(mlab, score, bars)); h2 = hl(VGroup(llab, lags)); h3 = hl(VGroup(flab, fixt))
        self.until(wt(5, 4, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(5, 7, 0.08)); self.play(ReplacementTransform(h1, h2), run_time=0.3)
        self.until(wt(5, 11, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        # ===== G. not like other institutes: aim for 300/300 (the one spring moment) =====
        nl = tag("Not like other institutes", 40, WHITE_, INK).move_to(P(490, 560))
        aim = H("Aim for", 64, INK).move_to(P(490, 720))
        nv = ValueTracker(223)
        cnt = always_redraw(lambda: VGroup(H(f"{int(round(nv.get_value()))}", 150, OR), H("/ 300", 110, INK)).arrange(RIGHT, buff=px(20), aligned_edge=DOWN).move_to(P(490, 860)))
        self.until(C[6] - 0.05); self.ev("wipe")
        self.play(FadeOut(sc), FadeOut(h3), FadeIn(nl, shift=UP * 0.08), run_time=0.4, rate_func=EXPO)
        self.until(wt(6, 5, 0.1)); self.play(FadeIn(aim, shift=UP * 0.1), FadeIn(cnt, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(6, 10, 0.1)); self.ev("stamp")
        self.play(nv.animate.set_value(300), run_time=max(0.5, wt(6, 13, 0.0) - self.renderer.time), rate_func=rate_functions.ease_out_cubic)
        # ===== H. price + Comment LINK =====
        price = VGroup(H("Free trial", 56, INK), H("→", 56, GREY_P), H("₹99/month", 64, OR)).arrange(RIGHT, buff=px(20)).move_to(P(490, 1090)); fitw(price, 720); price.move_to(P(490, 1090))
        self.until(C[-1] - 0.02); self.ev("tick"); self.play(FadeIn(price, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        bub = RoundedRectangle(width=px(64), height=px(46), corner_radius=0.12, fill_color=WHITE_, fill_opacity=1, stroke_width=0)
        tail = Triangle(fill_color=WHITE_, fill_opacity=1, stroke_width=0).scale(px(12)).rotate(PI).next_to(bub, DOWN, buff=-px(4)).shift(LEFT * px(14))
        icon = VGroup(bub, tail)
        ct = VGroup(icon, VGroup(H("Comment LINK", 50, WHITE_), B("we'll DM you the link", 28, WHITE_, SEMIBOLD)).arrange(DOWN, buff=px(4))).arrange(RIGHT, buff=px(22))
        fw = VGroup(RoundedRectangle(width=ct.width + px(80), height=ct.height + px(44), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0)); fw.add(ct.move_to(fw[0]))
        self.c2(fw, 1560); fw.set_z_index(22)
        self.until(C[-1] + 2.45); self.ev("tick"); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.4, rate_func=EXPO)
        fw.add_updater(lambda m: m.set_opacity(1))
        cbase = fw.get_center().copy()
        fw.add_updater(lambda m: m.move_to(cbase + UP * px(4) * math.sin(2 * math.pi * (self.renderer.time - t0) / 1.2)))
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


def promo_scorecard(P, title, total, subs, lags, fix_tex, fix_txt, cy=860, cw=700, ch=800):
    """SAMPLE scorecard used in the JEE course promos (20 Nov). Returns (group, parts)."""
    card = RoundedRectangle(width=px(cw), height=px(ch), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, cy))
    top = cy - ch / 2
    ttl = H(title, 42, INK).move_to(P(490, top + 52)).align_to(card, LEFT).shift(RIGHT * px(36))
    smp = tag("SAMPLE", 22, WHITE_, GREY_P).move_to(P(490 + cw / 2 - 72, top + 96))
    sub = B("Mock test 7 · JEE Main pattern", 28, GREY_P, SEMIBOLD).next_to(ttl, DOWN, buff=px(8)).align_to(ttl, LEFT)
    r1y = top + 205
    mlab = B("Marks", 30, GREY_P, SEMIBOLD).move_to(P(160, r1y - 40)).align_to(ttl, LEFT)
    score = H(f"{total} / 300", 60, INK).move_to(P(250, r1y + 12)).align_to(ttl, LEFT)
    bars = VGroup()
    for i, (nm, v, col) in enumerate(subs):
        yy = r1y - 42 + i * 46
        nmt = B(nm, 26, INK, SEMIBOLD).move_to(P(560, yy)).align_to(P(462, yy), LEFT)
        bg = Rectangle(width=px(110), height=px(18), fill_color="#ECE7DE", fill_opacity=1, stroke_width=0).move_to(P(695, yy))
        fg = Rectangle(width=px(110 * v / 100), height=px(18), fill_color=col, fill_opacity=1, stroke_width=0).set_z_index(3).move_to(bg.get_left() + RIGHT * px(110 * v / 200))
        val = B(str(v), 26, INK, SEMIBOLD).next_to(bg, RIGHT, buff=px(8))
        bars.add(VGroup(nmt, bg, fg, val))
    r2y = top + 400
    llab = B("Lagging in", 30, GREY_P, SEMIBOLD).move_to(P(160, r2y - 40)).align_to(ttl, LEFT)
    cols = ["#E5484D", OR]
    lagv = VGroup(*[VGroup(Dot(radius=px(9), color=cols[i % 2]), B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(12)) for i, t in enumerate(lags)])
    lagv.arrange(DOWN, buff=px(12), aligned_edge=LEFT).move_to(P(490, r2y + 16)).align_to(ttl, LEFT)
    r3y = top + 610
    flab = B("Fix next", 30, GREY_P, SEMIBOLD).move_to(P(160, r3y - 40)).align_to(ttl, LEFT)
    fixt = VGroup(M(fix_tex, 46, TEAL), B(fix_txt, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(16)).move_to(P(490, r3y + 10)).align_to(ttl, LEFT)
    seps = VGroup(*[Line(P(490 - cw / 2 + 30, top + yy), P(490 + cw / 2 - 30, top + yy), color=RULE, stroke_width=2) for yy in (118, 312, 525)])
    parts = dict(card=card, seps=seps, ttl=ttl, smp=smp, sub=sub, mlab=mlab, score=score, bars=bars, llab=llab, lags=lagv, flab=flab, fixt=fixt)
    return VGroup(card, seps, ttl, smp, sub, mlab, score, bars, llab, lagv, flab, fixt), parts


def promo_card_in(scene, p, extra=()):
    scene.play(FadeIn(p["card"], shift=UP * 0.2), FadeIn(p["seps"]), FadeIn(p["ttl"]), FadeIn(p["smp"]), FadeIn(p["sub"]), FadeIn(p["mlab"]), FadeIn(p["score"]),
               LaggedStart(*[GrowFromEdge(b[2], LEFT) for b in p["bars"]], lag_ratio=0.15), *[FadeIn(VGroup(b[0], b[1], b[3])) for b in p["bars"]],
               FadeIn(p["llab"]), FadeIn(p["lags"]), FadeIn(p["flab"]), FadeIn(p["fixt"]), *extra, run_time=0.7, rate_func=EXPO)


def promo_aim(scene, P, start, wt_from, wt_to, y=860):
    aim = H("Aim for", 64, INK).move_to(P(490, y - 140))
    nv = ValueTracker(start)
    cnt = always_redraw(lambda: VGroup(H(f"{int(round(nv.get_value()))}", 150, OR), H("/ 300", 110, INK)).arrange(RIGHT, buff=px(20), aligned_edge=DOWN).move_to(P(490, y)))
    return aim, nv, cnt


def promo_cta(scene, P, t0):
    bub = RoundedRectangle(width=px(64), height=px(46), corner_radius=0.12, fill_color=WHITE_, fill_opacity=1, stroke_width=0)
    tail = Triangle(fill_color=WHITE_, fill_opacity=1, stroke_width=0).scale(px(12)).rotate(PI).next_to(bub, DOWN, buff=-px(4)).shift(LEFT * px(14))
    ct = VGroup(VGroup(bub, tail), VGroup(H("Comment LINK", 50, WHITE_), B("we'll DM you the link", 28, WHITE_, SEMIBOLD)).arrange(DOWN, buff=px(4))).arrange(RIGHT, buff=px(22))
    fw = VGroup(RoundedRectangle(width=ct.width + px(80), height=ct.height + px(44), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0)); fw.add(ct.move_to(fw[0]))
    scene.c2(fw, 1560); fw.set_z_index(22)
    scene.ev("tick"); scene.play(FadeIn(fw, shift=UP * 0.15), run_time=0.4, rate_func=EXPO)
    base = fw.get_center().copy()
    fw.add_updater(lambda m: m.move_to(base + UP * px(4) * math.sin(2 * math.pi * (scene.renderer.time - t0) / 1.2)))
    return fw


class PromoB(ShortReel2):
    """JEE course promo, script B '2 months left' (20 Nov). SAMPLE scorecard 186 = 58 + 61 + 67."""
    EVENTS = "promob"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. 9 Sundays: calendar pages flip in from frame 0, then the JEE Main stamp lands =====
        head = H("9 Sundays", 132, OR).move_to(P(490, 455))
        subh = H("left before JEE Main", 50, INK).move_to(P(490, 565))
        days = [("22", "NOV"), ("29", "NOV"), ("6", "DEC"), ("13", "DEC"), ("20", "DEC"), ("27", "DEC"), ("3", "JAN"), ("10", "JAN"), ("17", "JAN")]
        def page(dn, mo):
            body = RoundedRectangle(width=px(180), height=px(150), corner_radius=0.12, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            band = Rectangle(width=px(180), height=px(40), fill_color=RD, fill_opacity=1, stroke_width=0).align_to(body, UP)
            band = RoundedRectangle(width=px(180), height=px(44), corner_radius=0.12, fill_color=RD, fill_opacity=1, stroke_width=0).align_to(body, UP)
            sun = B("SUN", 24, WHITE_, SEMIBOLD).move_to(band)
            num = H(dn, 60, INK).move_to(body.get_center() + DOWN * px(14))
            mon = B(mo, 22, GREY_P, SEMIBOLD).next_to(num, RIGHT, buff=px(8)).align_to(num, DOWN)
            return VGroup(body, band, sun, num, mon)
        pages = VGroup(*[page(d, m) for d, m in days]).arrange_in_grid(3, 3, buff=(px(24), px(22))).move_to(P(490, 880))
        stamp = tag("JEE MAIN · 20 JAN", 40, WHITE_, RD).rotate(-0.06).move_to(P(490, 1192))
        for pg in pages: pg.set_opacity(0.18)
        self.add(head, subh, pages)
        self.play(LaggedStart(*[pg.animate(rate_func=EXPO).set_opacity(1).scale(1.0) for pg in pages], lag_ratio=0.2), run_time=1.5)
        self.until(wt(0, 6, 0.1)); self.ev("stamp")
        self.play(FadeIn(stamp, scale=1.6), run_time=0.3, rate_func=rate_functions.ease_out_back)
        sbase = stamp.get_center().copy()
        stamp.add_updater(lambda m: m.set_opacity(1))
        head.add_updater(lambda m: m.set_opacity(0.8 + 0.2 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 0.9))))
        # ===== B. each Sunday becomes a full mock, not a new chapter =====
        def mock(pg):
            c = Circle(radius=px(30), fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to(pg[0].get_corner(DR) + UL * px(8))
            return VGroup(c, B("MOCK", 18, WHITE_, SEMIBOLD).move_to(c)).rotate(-0.2)
        mocks = VGroup(*[mock(pg) for pg in pages])
        q75 = tag("75 Qs · 3 hours each", 30, WHITE_, TEAL).move_to(P(490, 1275))
        self.until(wt(1, 4, 0.1)); self.ev("tick")
        self.play(LaggedStart(*[FadeIn(m, scale=1.8) for m in mocks], lag_ratio=0.12), FadeIn(q75, shift=UP * 0.08), run_time=1.0, rate_func=EXPO)
        part1 = VGroup(head, subh, pages, stamp, mocks, q75)
        # ===== C. a bare score: now what? =====
        bare = H("186 / 300", 120, INK).move_to(P(490, 700)); nw = H("Now what?", 60, GREY_P).move_to(P(490, 840))
        self.until(C[2] - 0.05); self.ev("wipe"); head.clear_updaters(); stamp.clear_updaters()
        self.play(FadeOut(part1, shift=UP * 0.3), FadeIn(bare, scale=0.9), run_time=0.45, rate_func=EXPO)
        self.until(wt(2, 6, 0.08)); self.play(FadeIn(nw, shift=UP * 0.08), run_time=0.3, rate_func=EXPO)
        # ===== D. the scorecard builds around the score =====
        sc, p = promo_scorecard(P, "Your TutorDA scorecard", 186, [("Maths", 58, BLUE), ("Physics", 61, TEAL), ("Chemistry", 67, OR)],
                                ["Calculus: limits  (−12 marks)", "Electrostatics"], r"\tfrac{\sin x}{x}\to 1", "revise limits")
        self.until(wt(3, 7, 0.1)); self.ev("wipe")
        self.play(FadeOut(nw), ReplacementTransform(bare, p["score"].copy().set_opacity(0)), run_time=0.3)
        promo_card_in(self, p)
        # ===== E. marks / lagging / improve light up =====
        hl = lambda mob: SurroundingRectangle(mob, buff=px(14), corner_radius=0.12, color=OR, stroke_width=5)
        h1, h2, h3 = hl(VGroup(p["mlab"], p["score"], p["bars"])), hl(VGroup(p["llab"], p["lags"])), hl(VGroup(p["flab"], p["fixt"]))
        self.until(wt(4, 1, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(4, 5, 0.08)); self.play(ReplacementTransform(h1, h2), run_time=0.3)
        self.until(wt(4, 11, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        # ===== F. personalised, not one plan for everybody =====
        ps = tag("Your plan. Not everybody's.", 38, WHITE_, INK).move_to(P(490, 395))
        self.until(C[5] - 0.05); self.ev("tick"); self.play(FadeIn(ps, shift=DOWN * 0.08), Indicate(p["fixt"], color=TEAL, scale_factor=1.06), run_time=0.5)
        # ===== G. aim for 300 =====
        aim, nv, cnt = promo_aim(self, P, 186, 0, 0)
        self.until(C[6] - 0.05); self.ev("wipe")
        self.play(FadeOut(sc), FadeOut(h3), FadeOut(ps), FadeIn(aim, shift=UP * 0.1), FadeIn(cnt, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(6, 6, 0.1)); self.ev("stamp")
        self.play(nv.animate.set_value(300), run_time=max(0.5, wt(6, 9, 0.0) - self.renderer.time), rate_func=rate_functions.ease_out_cubic)
        # ===== H. all these features, just Rs 99/month + Comment LINK =====
        feats = ["Full JEE Main mock tests", "Scorecard after every test", "Chapters you're lagging in", "What to fix next", "Doubt support"]
        def frow(t):
            ck = VGroup(Circle(radius=px(20), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 24, WHITE_, SEMIBOLD))
            ck[1].move_to(ck[0]); return VGroup(ck, B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(18))
        rows = VGroup(*[frow(t) for t in feats]).arrange(DOWN, buff=px(22), aligned_edge=LEFT)
        fbox = RoundedRectangle(width=px(700), height=rows.height + px(70), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, 760))
        rows.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * px(44))
        fhd = H("All these features", 46, INK).next_to(fbox, UP, buff=px(22))
        price = VGroup(H("Just", 60, INK), H("₹99", 110, OR), H("/month", 60, INK)).arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(P(490, 1130))
        self.until(C[-1] - 0.05); self.ev("wipe")
        self.play(FadeOut(aim), FadeOut(cnt), FadeIn(fhd, shift=DOWN * 0.08), FadeIn(fbox), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.8, rate_func=EXPO)
        self.until(C[-1] + 0.95); self.ev("stamp"); self.play(FadeIn(price, scale=1.25), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(C[-1] + 2.75); promo_cta(self, P, t0)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoC(ShortReel2):
    """JEE course promo, script C 'Where did the marks go?' for parents (20 Nov). SAMPLE scorecard 260 = 84 + 86 + 90 (40 lost)."""
    EVENTS = "promoc"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. -40 marks. Where? =====
        sc0 = H("260 / 300", 110, INK).move_to(P(490, 560))
        lost = H("−40 marks", 96, RD).move_to(P(490, 720))
        lost.add_updater(lambda m: m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 1.0))))
        wh = H("Where?", 72, INK).move_to(P(490, 860))
        self.add(sc0, lost, wh)
        # ===== B. a rank tells where, not why =====
        rk = tag("Rank: where they stand", 38, WHITE_, INK); why = tag("Why: ?", 38, WHITE_, RD)
        rr = VGroup(rk, why).arrange(DOWN, buff=px(22)).move_to(P(490, 1080))
        tk = B("✓", 40, TEAL, SEMIBOLD).next_to(rk, RIGHT, buff=px(16)); xx = B("✗", 40, RD, SEMIBOLD).next_to(why, RIGHT, buff=px(16))
        self.until(C[1] - 0.05); self.ev("tick"); self.play(FadeIn(rk, shift=UP * 0.08), FadeIn(tk), run_time=0.35, rate_func=EXPO)
        self.until(wt(1, 7, 0.08)); self.ev("stamp"); self.play(FadeIn(why, shift=UP * 0.08), FadeIn(xx), run_time=0.3, rate_func=EXPO)
        # ===== C. the parent sees the scorecard =====
        sc, p = promo_scorecard(P, "Your child's scorecard", 260, [("Maths", 84, BLUE), ("Physics", 86, TEAL), ("Chemistry", 90, OR)],
                                ["Coordinate geometry  (−16)", "Thermodynamics"], r"y=mx+c", "revise lines")
        self.until(C[2] - 0.05); self.ev("wipe"); lost.clear_updaters()
        self.play(FadeOut(VGroup(sc0, lost, wh, rr, tk, xx), shift=UP * 0.3), run_time=0.35)
        promo_card_in(self, p)
        hl = lambda mob: SurroundingRectangle(mob, buff=px(14), corner_radius=0.12, color=OR, stroke_width=5)
        h1, h2, h3 = hl(VGroup(p["mlab"], p["score"], p["bars"])), hl(VGroup(p["llab"], p["lags"])), hl(VGroup(p["flab"], p["fixt"]))
        self.until(wt(3, 6, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(3, 10, 0.08)); self.play(ReplacementTransform(h1, h2), run_time=0.3)
        self.until(wt(3, 15, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        # ===== D. regular updates to 20 Jan: a timeline =====
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(FadeOut(sc), FadeOut(h3), run_time=0.35)
        ln = Line(P(150, 760), P(830, 760), color=INK, stroke_width=5)
        dots = VGroup(*[Dot(P(150 + i * 85, 760), radius=px(14), color=TEAL) for i in range(8)])
        dl = B("an update after every test", 32, GREY_P, SEMIBOLD).move_to(P(490, 690))
        goal = tag("JEE Main · 20 Jan", 34, WHITE_, OR).move_to(P(650, 850))
        flag = Dot(P(830, 760), radius=px(18), color=OR)
        self.play(Create(ln), FadeIn(dl), run_time=0.35)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.18), run_time=max(0.6, wt(4, 6, 0.1) - self.renderer.time - 0.05))
        self.ev("tick"); self.play(FadeIn(flag, scale=1.4), FadeIn(goal, shift=UP * 0.08), run_time=0.35, rate_func=EXPO)
        # ===== E. not like other institutes; aim for 300 =====
        nl = tag("Not like other institutes", 40, WHITE_, INK).move_to(P(490, 560))
        aim, nv, cnt = promo_aim(self, P, 260, 0, 0)
        self.until(C[5] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(ln, dots, dl, goal, flag)), FadeIn(nl, shift=UP * 0.08), run_time=0.4, rate_func=EXPO)
        self.until(wt(5, 6, 0.1)); self.play(FadeIn(aim, shift=UP * 0.1), FadeIn(cnt, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(5, 12, 0.1)); self.ev("stamp")
        self.play(nv.animate.set_value(300), run_time=max(0.5, wt(5, 15, 0.0) - self.renderer.time), rate_func=rate_functions.ease_out_cubic)
        # ===== F. price; G. Comment LINK =====
        price = VGroup(H("Free trial", 56, INK), H("→", 56, GREY_P), H("₹99/month", 64, OR)).arrange(RIGHT, buff=px(20)); fitw(price, 720); price.move_to(P(490, 1090))
        self.until(C[6] - 0.05); self.ev("tick"); self.play(FadeIn(price, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(C[-1] + 1.1); promo_cta(self, P, t0)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


def promo_scorecard2(P, cy=850, title="Your child's scorecard"):
    """Richer SAMPLE scorecard (21 Nov, Aro: 'looks simple'). 260/300: Maths 21c 0w 4s = 84, Physics 22c 2w 1s = 86,
    Chemistry 23c 2w 0s = 90 -> 66 correct, 4 wrong, 5 skipped. Returns (group, parts, score tracker)."""
    RD = "#E5484D"; NAVY = "#0E142A"; cw, ch = 700, 840; top = cy - ch / 2; L = 490 - cw / 2 + 40
    shadow = RoundedRectangle(width=px(cw), height=px(ch), corner_radius=0.26, fill_color=NAVY, fill_opacity=0.10, stroke_width=0).move_to(P(490, cy + 12))
    card = RoundedRectangle(width=px(cw), height=px(ch), corner_radius=0.26, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, cy))
    hb = RoundedRectangle(width=px(cw), height=px(128), corner_radius=0.26, fill_color=NAVY, fill_opacity=1, stroke_width=0).move_to(P(490, top + 64))
    hsq = Rectangle(width=px(cw), height=px(40), fill_color=NAVY, fill_opacity=1, stroke_width=0).move_to(P(490, top + 108))
    ttl = H(title, 40, WHITE_).move_to(P(490, top + 46)); ttl.align_to(P(L, 0), LEFT)
    sub = B("Mock test 7 · JEE Main pattern", 26, "#AEB8CC", SEMIBOLD).next_to(ttl, DOWN, buff=px(8)).align_to(ttl, LEFT)
    smp = tag("SAMPLE", 22, NAVY, "#FFC83D").move_to(P(490 + cw / 2 - 80, top + 46))
    head = VGroup(hb, hsq, ttl, sub, smp)
    # score ring
    rc = P(255, top + 255); R = px(84)
    ring_bg = Circle(radius=R, stroke_color="#ECE7DE", stroke_width=20).move_to(rc)
    st = ValueTracker(0)
    arc = always_redraw(lambda: Arc(radius=R, start_angle=PI / 2, angle=-TAU * max(0.001, st.get_value()) / 300, stroke_color=OR, stroke_width=20).move_arc_center_to(rc))
    num = always_redraw(lambda: H(str(int(round(st.get_value()))), 58, INK).move_to(rc + UP * px(10)))
    of = B("of 300", 24, GREY_P, SEMIBOLD).move_to(rc + DOWN * px(36))
    # subject bars with marks lost
    subs = [("Maths", 84, 16, BLUE), ("Physics", 86, 14, TEAL), ("Chemistry", 90, 10, OR)]
    bars = VGroup()
    for i, (nm, v, lost, col) in enumerate(subs):
        yy = top + 192 + i * 62
        nmt = B(nm, 26, INK, SEMIBOLD).move_to(P(450, yy)).align_to(P(392, yy), LEFT)
        bg = RoundedRectangle(width=px(150), height=px(16), corner_radius=0.04, fill_color="#ECE7DE", fill_opacity=1, stroke_width=0).move_to(P(632, yy))
        fg = RoundedRectangle(width=px(150 * v / 100), height=px(16), corner_radius=0.04, fill_color=col, fill_opacity=1, stroke_width=0).set_z_index(3)
        fg.move_to(bg.get_left() + RIGHT * px(150 * v / 200))
        val = B(str(v), 26, INK, SEMIBOLD).next_to(bg, RIGHT, buff=px(10))
        dl = B(f"−{lost}", 24, RD, SEMIBOLD).move_to(P(800, yy))
        bars.add(VGroup(nmt, bg, fg, val, dl))
    stats = VGroup(tag("66 correct", 28, WHITE_, TEAL), tag("4 wrong", 28, WHITE_, RD), tag("5 skipped", 28, WHITE_, GREY_P)).arrange(RIGHT, buff=px(14)).move_to(P(490, top + 395))
    sep = Line(P(L, top + 450), P(490 + cw / 2 - 40, top + 450), color=RULE, stroke_width=2)
    # lagging in
    llab = B("Lagging in", 28, GREY_P, SEMIBOLD).move_to(P(300, top + 488)).align_to(P(L, 0), LEFT)
    def lrow(t, why, d, y):
        row = VGroup(Dot(radius=px(9), color=RD), B(t, 32, INK, SEMIBOLD), B(why, 24, GREY_P, SEMIBOLD)).arrange(RIGHT, buff=px(12))
        row.move_to(P(400, y)).align_to(P(L, 0), LEFT); ch_ = tag(d, 26, WHITE_, RD).move_to(P(490 + cw / 2 - 70, y))
        return VGroup(row, ch_)
    lags = VGroup(lrow("Coordinate geometry", "4 skipped", "−16", top + 540), lrow("Thermodynamics", "2 wrong", "−10", top + 596))
    # fix next
    fb = RoundedRectangle(width=px(cw - 60), height=px(150), corner_radius=0.18, fill_color="#E3F4F1", fill_opacity=1, stroke_width=0).move_to(P(490, top + 725))
    flab = B("Fix next", 28, TEAL, SEMIBOLD).move_to(fb.get_corner(UL) + RIGHT * px(90) + DOWN * px(34)).align_to(fb, LEFT).shift(RIGHT * px(26))
    fixt = VGroup(B("Revise straight lines", 34, INK, SEMIBOLD), M(r"y=mx+c", 38, TEAL)).arrange(RIGHT, buff=px(16))
    fixt.next_to(flab, DOWN, buff=px(12)).align_to(flab, LEFT)
    fsub = B("before mock test 8", 24, GREY_P, SEMIBOLD).next_to(fixt, DOWN, buff=px(8)).align_to(flab, LEFT)
    parts = dict(shadow=shadow, card=card, head=head, ring_bg=ring_bg, arc=arc, num=num, of=of, bars=bars, stats=stats, sep=sep,
                 llab=llab, lags=lags, fb=fb, flab=flab, fixt=fixt, fsub=fsub,
                 scorebox=VGroup(ring_bg, of, bars, stats), lagbox=VGroup(llab, lags), fixbox=fb)
    grp = VGroup(shadow, card, head, ring_bg, arc, num, of, bars, stats, sep, llab, lags, fb, flab, fixt, fsub)
    return grp, parts, st


def promo_card2_in(scene, p, st, total=260):
    scene.play(FadeIn(VGroup(p["shadow"], p["card"]), shift=UP * 0.2), FadeIn(p["head"], shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
    scene.add(p["ring_bg"], p["arc"], p["num"])
    scene.play(FadeIn(p["ring_bg"]), FadeIn(p["of"]), st.animate.set_value(total),
               LaggedStart(*[GrowFromEdge(b[2], LEFT) for b in p["bars"]], lag_ratio=0.15), *[FadeIn(VGroup(b[0], b[1], b[3], b[4])) for b in p["bars"]],
               run_time=0.9, rate_func=rate_functions.ease_out_cubic)
    scene.play(LaggedStart(*[FadeIn(c, scale=1.2) for c in p["stats"]], lag_ratio=0.2), FadeIn(p["sep"]), FadeIn(p["llab"]),
               LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in p["lags"]], lag_ratio=0.25),
               FadeIn(p["fb"]), FadeIn(p["flab"]), FadeIn(p["fixt"]), FadeIn(p["fsub"]), run_time=0.7, rate_func=EXPO)


class PromoC2(ShortReel2):
    """JEE course promo C v2 for parents (21 Nov): guessable hook 'which subject cost the most?', answer held to ~4.3 s,
    then the scorecard by ~10 s. SAMPLE: 260 = 84 + 86 + 90, lost 16 + 14 + 10 = 40."""
    EVENTS = "promoc2"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. hook on frame 0: lost 40 marks, which subject? (3 guessable options, draining guess bar) =====
        l1 = H("Your child lost", 56, INK).move_to(P(490, 410))
        big = H("40 marks", 130, RD).move_to(P(490, 520))
        l2 = B("in a mock test", 38, GREY_P, SEMIBOLD).move_to(P(490, 612))
        qq = H("Which subject cost the most?", 54, INK); fitw(qq, 700); qq.move_to(P(490, 705))
        def card(nm, col):
            body = RoundedRectangle(width=px(206), height=px(280), corner_radius=0.18, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            band = RoundedRectangle(width=px(206), height=px(62), corner_radius=0.18, fill_color=col, fill_opacity=1, stroke_width=0).align_to(body, UP)
            name = B(nm, 30, WHITE_, SEMIBOLD).move_to(band)
            q = H("?", 110, INK).move_to(body.get_center() + DOWN * px(8))
            lab = B("marks lost", 24, GREY_P, SEMIBOLD).move_to(body.get_bottom() + UP * px(34))
            return VGroup(body, band, name, q, lab)
        cards = VGroup(card("Maths", BLUE), card("Physics", TEAL), card("Chemistry", OR)).arrange(RIGHT, buff=px(20)).move_to(P(480, 920))
        glab = B("Guess before the answer", 30, GREY_P, SEMIBOLD).move_to(P(490, 1112))
        gbg = RoundedRectangle(width=px(600), height=px(16), corner_radius=0.05, fill_color="#ECE7DE", fill_opacity=1, stroke_width=0).move_to(P(490, 1160))
        T1 = C[1] - 0.05
        gbar = always_redraw(lambda: RoundedRectangle(width=max(0.001, px(600) * max(0.0, 1 - (self.renderer.time - t0) / (T1 - t0))), height=px(16),
                                                      corner_radius=0.05, fill_color=OR, fill_opacity=1, stroke_width=0).align_to(gbg, LEFT).set_y(gbg.get_y()))
        big.add_updater(lambda m: m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 0.9))))
        self.add(l1, big, l2, qq, cards, glab, gbg, gbar)
        self.until(wt(0, 9, 0.1)); self.ev("tick")
        self.play(LaggedStart(*[Indicate(c, color=c[1].get_fill_color(), scale_factor=1.07) for c in cards], lag_ratio=0.25), run_time=1.0)
        # ===== B. Maths: 16 marks, all from one chapter =====
        self.until(T1); self.ev("stamp"); big.clear_updaters(); big.set_opacity(1)
        vals = [H("−16", 84, RD), H("−14", 84, INK), H("−10", 84, INK)]
        for v, c in zip(vals, cards): v.move_to(c[3])
        self.remove(gbar)
        self.play(*[ReplacementTransform(c[3], v) for c, v in zip(cards, vals)], cards[0][0].animate.set_stroke(RD, width=7),
                  cards[1].animate.set_opacity(0.4), cards[2].animate.set_opacity(0.4), vals[1].animate.set_opacity(0.4), vals[2].animate.set_opacity(0.4),
                  FadeOut(glab), FadeOut(gbg), run_time=0.4, rate_func=EXPO)
        self.play(VGroup(cards[0], vals[0]).animate.scale(1.08), run_time=0.25, rate_func=rate_functions.ease_out_back)
        chap = tag("All 16: Coordinate geometry", 38, WHITE_, RD); fitw(chap, 720); chap.move_to(P(490, 1150))
        self.until(wt(1, 5, 0.1)); self.ev("tick"); self.play(FadeIn(chap, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        part1 = VGroup(l1, big, l2, qq, cards, *vals, chap)
        # ===== C. a rank won't tell you that; not like other institutes =====
        rk = VGroup(tag("Rank", 44, WHITE_, INK), B("tells you where they stand", 34, INK, SEMIBOLD)).arrange(DOWN, buff=px(14)).move_to(P(490, 560))
        nt = VGroup(tag("Why they lost marks?", 44, WHITE_, RD), B("a rank won't tell you", 34, RD, SEMIBOLD)).arrange(DOWN, buff=px(14)).move_to(P(490, 820))
        nl = tag("We're not like other institutes", 40, WHITE_, TEAL); fitw(nl, 720); nl.move_to(P(490, 1100))
        self.until(C[2] - 0.05); self.ev("wipe")
        self.play(FadeOut(part1, shift=UP * 0.3), FadeIn(rk, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(2, 2, 0.1)); self.ev("stamp"); self.play(FadeIn(nt, scale=1.15), run_time=0.3, rate_func=EXPO)
        self.until(wt(2, 6, 0.1)); self.ev("tick"); self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        # ===== D. the scorecard =====
        sc, p, st = promo_scorecard2(P)
        self.until(C[3] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(rk, nt, nl), shift=UP * 0.3), run_time=0.3)
        promo_card2_in(self, p, st)
        # ===== E. marks / lagging / fix next light up =====
        hl = lambda mob: SurroundingRectangle(mob, buff=px(12), corner_radius=0.14, color=OR, stroke_width=5)
        h1 = hl(VGroup(p["ring_bg"], p["bars"], p["stats"])); h2 = hl(p["lagbox"]); h3 = hl(p["fb"])
        self.until(wt(4, 1, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(4, 3, 0.08)); self.play(ReplacementTransform(h1, h2), Indicate(p["lags"][0][1], color=RD, scale_factor=1.12), run_time=0.35)
        self.until(wt(4, 9, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        # ===== F. updated after every test, to JEE Main on 20 Jan =====
        self.until(C[5] - 0.05); self.ev("wipe")
        p["arc"].clear_updaters(); p["num"].clear_updaters()
        self.play(FadeOut(sc), FadeOut(h3), run_time=0.3)
        hd = H("Updated after every test", 54, INK); fitw(hd, 740); hd.move_to(P(490, 600))
        ln = Line(P(150, 800), P(830, 800), color=INK, stroke_width=5)
        dots = VGroup(*[Dot(P(150 + i * 85, 800), radius=px(14), color=TEAL) for i in range(8)])
        goal = tag("JEE Main · 20 Jan", 40, WHITE_, OR).move_to(P(640, 905))
        flag = Dot(P(830, 800), radius=px(20), color=OR)
        self.play(FadeIn(hd, shift=UP * 0.08), Create(ln), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.18), run_time=max(0.6, wt(5, 8, 0.1) - self.renderer.time - 0.05))
        self.ev("stamp"); self.play(FadeIn(flag, scale=1.5), FadeIn(goal, shift=UP * 0.08), run_time=0.35, rate_func=EXPO)
        # ===== G. aim for 300 =====
        aim, nv, cnt = promo_aim(self, P, 260, 0, 0)
        self.until(C[6] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(hd, ln, dots, goal, flag)), FadeIn(aim, shift=UP * 0.1), FadeIn(cnt, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(6, 7, 0.1)); self.ev("stamp")
        self.play(nv.animate.set_value(300), run_time=max(0.5, wt(6, 10, 0.0) - self.renderer.time), rate_func=rate_functions.ease_out_cubic)
        # ===== H. all these features, just Rs 99/month + Comment LINK =====
        feats = ["Full JEE Main mock tests", "Scorecard after every test", "Chapters they're lagging in", "What to fix next", "Doubt support"]
        def frow(t):
            ck = VGroup(Circle(radius=px(20), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 24, WHITE_, SEMIBOLD))
            ck[1].move_to(ck[0]); return VGroup(ck, B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(18))
        rows = VGroup(*[frow(t) for t in feats]).arrange(DOWN, buff=px(22), aligned_edge=LEFT)
        fbox = RoundedRectangle(width=px(700), height=rows.height + px(70), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, 760))
        rows.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * px(44))
        fhd = H("All these features", 46, INK).next_to(fbox, UP, buff=px(22))
        price = VGroup(H("Just", 60, INK), H("₹99", 110, OR), H("/month", 60, INK)).arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(P(490, 1130))
        self.until(C[-1] - 0.05); self.ev("wipe")
        self.play(FadeOut(aim), FadeOut(cnt), FadeIn(fhd, shift=DOWN * 0.08), FadeIn(fbox), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.7, rate_func=EXPO)
        self.until(C[-1] + 1.05); self.ev("stamp"); self.play(FadeIn(price, scale=1.25), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(C[-1] + 2.6); promo_cta(self, P, t0)
        fol = VGroup(tag("+ Follow", 36, WHITE_, BLUE), B("TutorDA for more updates", 36, INK, SEMIBOLD)).arrange(RIGHT, buff=px(16))
        fitw(fol, 680); fol.move_to(P(490, 1300))
        self.until(C[-1] + 4.25); self.ev("tick"); self.play(FadeIn(fol, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.play(Indicate(fol[0], color=BLUE, scale_factor=1.12), run_time=0.5)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoD(ShortReel2):
    """JEE course promo D (22 Nov), students: 'skip 5, get 4 wrong, how many marks lost?' 24 / 36 / 40 -> 40
    (5x4 + 4x5). Rule card with the answer. 300 - 40 = 260 -> where did they go? -> scorecard (66c 4w 5s) -> Rs 99 + LINK."""
    EVENTS = "promod"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. frame 0: the question, 3 options, draining guess bar =====
        sch = tag("JEE Main marking:  +4 right  ·  −1 wrong", 30, WHITE_, INK); fitw(sch, 700); sch.move_to(P(490, 405))
        q1 = VGroup(H("Skip 5.", 92, INK), H("Get 4 wrong.", 92, RD)).arrange(DOWN, buff=px(6)).move_to(P(490, 560))
        q2 = H("How many marks did you lose?", 50, INK); fitw(q2, 700); q2.move_to(P(490, 725))
        def opt(letter, val, col):
            body = RoundedRectangle(width=px(206), height=px(190), corner_radius=0.18, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            chip = tag(letter, 28, WHITE_, col).move_to(body.get_top() + DOWN * px(36))
            num = H(val, 92, INK).move_to(body.get_center() + DOWN * px(22))
            return VGroup(body, chip, num)
        opts = VGroup(opt("A", "24", BLUE), opt("B", "36", OR), opt("C", "40", TEAL)).arrange(RIGHT, buff=px(20)).move_to(P(480, 905))
        glab = B("Guess before the answer", 30, GREY_P, SEMIBOLD).move_to(P(490, 1068))
        gbg = RoundedRectangle(width=px(600), height=px(16), corner_radius=0.05, fill_color="#ECE7DE", fill_opacity=1, stroke_width=0).move_to(P(490, 1112))
        T1 = C[1] - 0.05
        gbar = always_redraw(lambda: RoundedRectangle(width=max(0.001, px(600) * max(0.0, 1 - (self.renderer.time - t0) / (T1 - t0))), height=px(16),
                                                      corner_radius=0.05, fill_color=OR, fill_opacity=1, stroke_width=0).align_to(gbg, LEFT).set_y(gbg.get_y()))
        q1[1].add_updater(lambda m: m.set_opacity(0.72 + 0.28 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 0.9))))
        self.add(sch, q1, q2, opts, glab, gbg, gbar)
        self.until(wt(0, 9, 0.1)); self.ev("tick")
        self.play(LaggedStart(*[o.animate(rate_func=there_and_back).scale(1.08) for o in opts], lag_ratio=0.25), run_time=1.0)
        # ===== B. 40. skip costs 4 =====
        self.until(T1); self.ev("stamp"); q1[1].clear_updaters(); q1[1].set_opacity(1); self.remove(gbar)
        tick = VGroup(Circle(radius=px(26), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 30, WHITE_, SEMIBOLD))
        tick[1].move_to(tick[0]); tick.move_to(opts[2][0].get_corner(UR) + LEFT * px(10) + DOWN * px(10))
        self.play(opts[2][0].animate.set_stroke(TEAL, width=7), opts[0].animate.set_opacity(0.35), opts[1].animate.set_opacity(0.35),
                  FadeOut(glab), FadeOut(gbg), FadeIn(tick, scale=1.5), run_time=0.35, rate_func=EXPO)
        self.play(VGroup(opts[2], tick).animate.scale(1.08), run_time=0.25, rate_func=rate_functions.ease_out_back)
        # working board
        r1 = VGroup(tag("Skip", 34, WHITE_, GREY_P), M(r"5 \times 4 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        r2 = VGroup(tag("Wrong", 34, WHITE_, RD), M(r"4 \times 5 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        board = VGroup(r1, r2).arrange(DOWN, buff=px(40), aligned_edge=LEFT).move_to(P(490, 610))
        why = B("4 missed  +  1 taken away", 30, GREY_P, SEMIBOLD).next_to(r2, DOWN, buff=px(14)).align_to(r2[1], LEFT)
        tl = Line(P(250, 0), P(730, 0), color=INK, stroke_width=4).set_y(Y(800))
        tot = VGroup(B("Marks lost", 40, INK, SEMIBOLD), H("40", 96, RD)).arrange(RIGHT, buff=px(24)).move_to(P(490, 875))
        rule = VGroup(B("Rule", 26, OR, SEMIBOLD), H("Wrong answer = −5", 46, WHITE_), B("A skip only costs 4", 30, "#D5DCE8", SEMIBOLD)).arrange(DOWN, buff=px(8))
        rbox = RoundedRectangle(width=px(640), height=rule.height + px(56), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1110))
        rule.move_to(rbox)
        self.until(wt(1, 2, 0.1)); self.ev("wipe")
        self.play(FadeOut(VGroup(sch, q1, q2, opts, tick), shift=UP * 0.3), run_time=0.3)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        # ===== C. wrong costs 5 =====
        self.until(C[2] - 0.05); self.ev("tick"); self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(2, 7, 0.1)); self.play(FadeIn(why, shift=UP * 0.06), run_time=0.3)
        self.until(wt(2, 11, 0.1)); self.ev("stamp")
        self.play(Create(tl), FadeIn(tot, scale=1.15), FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        # ===== D. 300 - 40 = 260, where did the 40 go? =====
        eq = VGroup(H("300", 96, INK), H("−", 96, INK), H("40", 96, RD), H("=", 96, INK), H("260", 96, OR)).arrange(RIGHT, buff=px(18)).move_to(P(490, 560))
        wq = H("Where did the 40 go?", 58, INK); fitw(wq, 700); wq.move_to(P(490, 730))
        qs = VGroup(*[VGroup(tag(n, 32, WHITE_, c), H("?", 80, c)).arrange(DOWN, buff=px(10)) for n, c in [("Maths", BLUE), ("Physics", TEAL), ("Chemistry", OR)]]).arrange(RIGHT, buff=px(44)).move_to(P(490, 920))
        self.until(C[3] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(board, why, tl, tot, rbox, rule), shift=UP * 0.3), FadeIn(eq, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(3, 6, 0.1)); self.ev("tick")
        self.play(FadeIn(wq, shift=UP * 0.08), LaggedStart(*[FadeIn(x, scale=1.2) for x in qs], lag_ratio=0.2), run_time=0.6, rate_func=EXPO)
        self.play(LaggedStart(*[Wiggle(x[1], scale_value=1.15) for x in qs], lag_ratio=0.15), run_time=0.8)
        # ===== E. the scorecard =====
        sc, p, st = promo_scorecard2(P, title="Your scorecard")
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(eq, wq, qs), shift=UP * 0.3), run_time=0.3)
        promo_card2_in(self, p, st)
        # ===== F. marks / lagging / fix next =====
        hl = lambda mob: SurroundingRectangle(mob, buff=px(12), corner_radius=0.14, color=OR, stroke_width=5)
        h1 = hl(VGroup(p["ring_bg"], p["bars"], p["stats"])); h2 = hl(p["lagbox"]); h3 = hl(p["fb"])
        self.until(wt(5, 1, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(5, 3, 0.08)); self.play(ReplacementTransform(h1, h2), Indicate(p["lags"][0][1], color=RD, scale_factor=1.12), run_time=0.35)
        self.until(wt(5, 9, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        # ===== G. aim for 300 =====
        aim, nv, cnt = promo_aim(self, P, 260, 0, 0)
        self.until(C[6] - 0.05); self.ev("wipe")
        p["arc"].clear_updaters(); p["num"].clear_updaters()
        self.play(FadeOut(sc), FadeOut(h3), FadeIn(aim, shift=UP * 0.1), FadeIn(cnt, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(6, 6, 0.1)); self.ev("stamp")
        self.play(nv.animate.set_value(300), run_time=max(0.5, wt(6, 9, 0.0) - self.renderer.time), rate_func=rate_functions.ease_out_cubic)
        # ===== H. all these features, Rs 99/month, Comment LINK =====
        feats = ["Full JEE Main mock tests", "Scorecard after every test", "Chapters you're lagging in", "What to fix next", "Doubt support"]
        def frow(t):
            ck = VGroup(Circle(radius=px(20), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 24, WHITE_, SEMIBOLD))
            ck[1].move_to(ck[0]); return VGroup(ck, B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(18))
        rows = VGroup(*[frow(t) for t in feats]).arrange(DOWN, buff=px(22), aligned_edge=LEFT)
        fbox = RoundedRectangle(width=px(700), height=rows.height + px(70), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, 760))
        rows.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * px(44))
        fhd = H("All these features", 46, INK).next_to(fbox, UP, buff=px(22))
        price = VGroup(H("Just", 60, INK), H("₹99", 110, OR), H("/month", 60, INK)).arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(P(490, 1150))
        self.until(C[-1] - 0.05); self.ev("wipe")
        self.play(FadeOut(aim), FadeOut(cnt), FadeIn(fhd, shift=DOWN * 0.08), FadeIn(fbox), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.7, rate_func=EXPO)
        self.until(C[-1] + 1.05); self.ev("stamp"); self.play(FadeIn(price, scale=1.25), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(C[-1] + 2.6); promo_cta(self, P, t0)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoD2(ShortReel2):
    """Promo D v2 (22 Nov): hook 'Only 4 wrong. Still lost 40 marks. You're losing marks you don't even see.' over a
    75-box answer sheet (66 right, 4 wrong, 5 blank skips that light up on 'see'). Then 5x4 + 4x5 = 40, rule card, scorecard."""
    EVENTS = "promod2"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. frame 0: only 4 wrong, still lost 40, over the answer sheet =====
        sch = tag("Your JEE Main mock  ·  75 questions", 30, WHITE_, INK); fitw(sch, 700); sch.move_to(P(490, 470))
        h1 = H("Only 4 wrong.", 92, INK).move_to(P(490, 585))
        h2 = VGroup(B("Still lost", 48, INK, SEMIBOLD), H("40 marks", 100, RD)).arrange(RIGHT, buff=px(20), aligned_edge=DOWN).move_to(P(490, 702))
        WRONG = {7, 23, 41, 60}; SKIP = {12, 29, 33, 52, 70}
        grid = VGroup(); wrong = VGroup(); skip = VGroup()
        for k in range(75):
            r, c = divmod(k, 15); xy = P(156 + 19 + c * 45, 850 + r * 45)
            if k in WRONG:
                cell = VGroup(RoundedRectangle(width=px(38), height=px(38), corner_radius=0.06, fill_color=RD, fill_opacity=1, stroke_width=0),
                              B("✗", 24, WHITE_, SEMIBOLD)).move_to(xy); cell[1].move_to(cell[0]); wrong.add(cell)
            elif k in SKIP:
                cell = RoundedRectangle(width=px(38), height=px(38), corner_radius=0.06, fill_color="#F7F3EC", fill_opacity=1, stroke_color="#E2DBCF", stroke_width=2).move_to(xy); skip.add(cell)
            else:
                cell = RoundedRectangle(width=px(38), height=px(38), corner_radius=0.06, fill_color="#BFE9E1", fill_opacity=1, stroke_width=0).move_to(xy)
            grid.add(cell)
        sq = lambda col, st=0: RoundedRectangle(width=px(26), height=px(26), corner_radius=0.05, fill_color=col, fill_opacity=1, stroke_width=st, stroke_color=OR)
        leg = VGroup(VGroup(sq("#BFE9E1"), B("66 right", 30, INK, SEMIBOLD)).arrange(RIGHT, buff=px(10)),
                     VGroup(sq(RD), B("4 wrong", 30, INK, SEMIBOLD)).arrange(RIGHT, buff=px(10))).arrange(RIGHT, buff=px(40)).move_to(P(490, 1118))
        for w in wrong: w.add_updater(lambda m, w=w: m.set_opacity(0.65 + 0.35 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 0.8))))
        self.add(sch, h1, h2, grid, leg)
        self.until(wt(0, 5, 0.1)); self.ev("tick"); self.play(Indicate(h2[1], color=RD, scale_factor=1.04), run_time=0.5)
        # ===== B. you don't even see: the 5 blanks were skips =====
        sk = VGroup(sq(OR), B("5 skipped", 30, OR, SEMIBOLD)).arrange(RIGHT, buff=px(10))
        self.until(wt(1, 3, 0.05)); self.ev("stamp")
        for w in wrong: w.clear_updaters(); w.set_opacity(1)
        self.play(*[c.animate.set_fill(OR, 1).set_stroke(OR, 3) for c in skip], leg.animate.shift(LEFT * px(130)), run_time=0.35, rate_func=EXPO)
        sk.next_to(leg, RIGHT, buff=px(40))
        self.play(FadeIn(sk, shift=LEFT * 0.1), *[c.animate(rate_func=there_and_back).scale(1.35) for c in skip], run_time=0.6)
        leg.add(sk)
        # working board
        r1 = VGroup(tag("Skip", 34, WHITE_, GREY_P), M(r"5 \times 4 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        r2 = VGroup(tag("Wrong", 34, WHITE_, RD), M(r"4 \times 5 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        board = VGroup(r1, r2).arrange(DOWN, buff=px(40), aligned_edge=LEFT).move_to(P(490, 610))
        why = B("4 missed  +  1 taken away", 30, GREY_P, SEMIBOLD).next_to(r2, DOWN, buff=px(14)).align_to(r2[1], LEFT)
        tl = Line(P(250, 0), P(730, 0), color=INK, stroke_width=4).set_y(Y(800))
        tot = VGroup(B("Marks lost", 40, INK, SEMIBOLD), H("40", 96, RD)).arrange(RIGHT, buff=px(24)).move_to(P(490, 875))
        rule = VGroup(B("Rule", 26, OR, SEMIBOLD), H("Wrong answer = −5", 46, WHITE_), B("A skip only costs 4", 30, "#D5DCE8", SEMIBOLD)).arrange(DOWN, buff=px(8))
        rbox = RoundedRectangle(width=px(640), height=rule.height + px(56), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1110))
        rule.move_to(rbox)
        self.until(C[2] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(sch, h1, h2, grid, leg), shift=UP * 0.3), run_time=0.3)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        # ===== C. wrong costs 5 =====
        self.until(C[3] - 0.05); self.ev("tick"); self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(3, 7, 0.1)); self.play(FadeIn(why, shift=UP * 0.06), run_time=0.3)
        self.until(wt(3, 11, 0.1)); self.ev("stamp")
        self.play(Create(tl), FadeIn(tot, scale=1.15), FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        # ===== D. 300 - 40 = 260, where did the 40 go? =====
        eq = VGroup(H("300", 96, INK), H("−", 96, INK), H("40", 96, RD), H("=", 96, INK), H("260", 96, OR)).arrange(RIGHT, buff=px(18)).move_to(P(490, 560))
        wq = H("Which chapters?", 64, INK); fitw(wq, 700); wq.move_to(P(490, 730))
        qs = VGroup(*[VGroup(tag(n, 32, WHITE_, c), H("?", 80, c)).arrange(DOWN, buff=px(10)) for n, c in [("Maths", BLUE), ("Physics", TEAL), ("Chemistry", OR)]]).arrange(RIGHT, buff=px(44)).move_to(P(490, 920))
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(board, why, tl, tot, rbox, rule), shift=UP * 0.3), FadeIn(eq, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(4, 2, 0.1)); self.ev("tick")
        self.play(FadeIn(wq, shift=UP * 0.08), LaggedStart(*[FadeIn(x, scale=1.2) for x in qs], lag_ratio=0.2), run_time=0.6, rate_func=EXPO)
        self.play(LaggedStart(*[Wiggle(x[1], scale_value=1.15) for x in qs], lag_ratio=0.15), run_time=0.8)
        # ===== E. the scorecard =====
        sc, p, st = promo_scorecard2(P, title="Your scorecard")
        self.until(C[5] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(eq, wq, qs), shift=UP * 0.3), run_time=0.3)
        promo_card2_in(self, p, st)
        # ===== F. marks / lagging / fix next =====
        hl = lambda mob: SurroundingRectangle(mob, buff=px(12), corner_radius=0.14, color=OR, stroke_width=5)
        h1 = hl(VGroup(p["ring_bg"], p["bars"], p["stats"])); h2 = hl(p["lagbox"]); h3 = hl(p["fb"])
        self.until(wt(6, 1, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(6, 3, 0.08)); self.play(ReplacementTransform(h1, h2), Indicate(p["lags"][0][1], color=RD, scale_factor=1.12), run_time=0.35)
        self.until(wt(6, 9, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        # ===== G. aim for 300 =====
        aim, nv, cnt = promo_aim(self, P, 260, 0, 0)
        self.until(C[7] - 0.05); self.ev("wipe")
        p["arc"].clear_updaters(); p["num"].clear_updaters()
        self.play(FadeOut(sc), FadeOut(h3), FadeIn(aim, shift=UP * 0.1), FadeIn(cnt, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(7, 6, 0.1)); self.ev("stamp")
        self.play(nv.animate.set_value(300), run_time=max(0.5, wt(7, 9, 0.0) - self.renderer.time), rate_func=rate_functions.ease_out_cubic)
        # ===== H. all these features, Rs 99/month, Comment LINK =====
        feats = ["Full JEE Main mock tests", "Scorecard after every test", "Chapters you're lagging in", "What to fix next", "Doubt support"]
        def frow(t):
            ck = VGroup(Circle(radius=px(20), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 24, WHITE_, SEMIBOLD))
            ck[1].move_to(ck[0]); return VGroup(ck, B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(18))
        rows = VGroup(*[frow(t) for t in feats]).arrange(DOWN, buff=px(22), aligned_edge=LEFT)
        fbox = RoundedRectangle(width=px(700), height=rows.height + px(70), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, 760))
        rows.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * px(44))
        fhd = H("All these features", 46, INK).next_to(fbox, UP, buff=px(22))
        price = VGroup(H("Just", 60, INK), H("₹99", 110, OR), H("/month", 60, INK)).arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(P(490, 1150))
        self.until(C[-1] - 0.05); self.ev("wipe")
        self.play(FadeOut(aim), FadeOut(cnt), FadeIn(fhd, shift=DOWN * 0.08), FadeIn(fbox), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.7, rate_func=EXPO)
        self.until(C[-1] + 1.05); self.ev("stamp"); self.play(FadeIn(price, scale=1.25), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(C[-1] + 2.6); promo_cta(self, P, t0)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoD3(ShortReel2):
    """Promo D v2 (22 Nov): hook 'Only 4 wrong. Still lost 40 marks. You're losing marks you don't even see.' over a
    75-box answer sheet (66 right, 4 wrong, 5 blank skips that light up on 'see'). Then 5x4 + 4x5 = 40, rule card, scorecard."""
    EVENTS = "promod3"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. frame 0: only 4 wrong, still lost 40, over the answer sheet =====
        sch = tag("Your JEE Main mock  ·  75 questions", 30, WHITE_, INK); fitw(sch, 700); sch.move_to(P(490, 470))
        h1 = H("Only 4 wrong.", 92, INK).move_to(P(490, 585))
        h2 = VGroup(B("Still lost", 48, INK, SEMIBOLD), H("40 marks", 100, RD)).arrange(RIGHT, buff=px(20), aligned_edge=DOWN).move_to(P(490, 702))
        WRONG = {7, 23, 41, 60}; SKIP = {12, 29, 33, 52, 70}
        grid = VGroup(); wrong = VGroup(); skip = VGroup()
        for k in range(75):
            r, c = divmod(k, 15); xy = P(156 + 19 + c * 45, 850 + r * 45)
            if k in WRONG:
                cell = VGroup(RoundedRectangle(width=px(38), height=px(38), corner_radius=0.06, fill_color=RD, fill_opacity=1, stroke_width=0),
                              B("✗", 24, WHITE_, SEMIBOLD)).move_to(xy); cell[1].move_to(cell[0]); wrong.add(cell)
            elif k in SKIP:
                cell = RoundedRectangle(width=px(38), height=px(38), corner_radius=0.06, fill_color="#F7F3EC", fill_opacity=1, stroke_color="#E2DBCF", stroke_width=2).move_to(xy); skip.add(cell)
            else:
                cell = RoundedRectangle(width=px(38), height=px(38), corner_radius=0.06, fill_color="#BFE9E1", fill_opacity=1, stroke_width=0).move_to(xy)
            grid.add(cell)
        sq = lambda col, st=0: RoundedRectangle(width=px(26), height=px(26), corner_radius=0.05, fill_color=col, fill_opacity=1, stroke_width=st, stroke_color=OR)
        leg = VGroup(VGroup(sq("#BFE9E1"), B("66 right", 30, INK, SEMIBOLD)).arrange(RIGHT, buff=px(10)),
                     VGroup(sq(RD), B("4 wrong", 30, INK, SEMIBOLD)).arrange(RIGHT, buff=px(10))).arrange(RIGHT, buff=px(40)).move_to(P(490, 1118))
        for w in wrong: w.add_updater(lambda m, w=w: m.set_opacity(0.65 + 0.35 * (0.5 + 0.5 * math.sin(2 * math.pi * (self.renderer.time - t0) / 0.8))))
        self.add(sch, h1, h2, grid, leg)
        self.until(wt(0, 8, 0.1)); self.ev("tick"); self.play(Indicate(h2[1], color=RD, scale_factor=1.04), run_time=0.5)
        # ===== B. you don't even see: the 5 blanks were skips =====
        sk = VGroup(sq(OR), B("5 skipped", 30, OR, SEMIBOLD)).arrange(RIGHT, buff=px(10))
        self.until(wt(1, 3, 0.05)); self.ev("stamp")
        for w in wrong: w.clear_updaters(); w.set_opacity(1)
        self.play(*[c.animate.set_fill(OR, 1).set_stroke(OR, 3) for c in skip], leg.animate.shift(LEFT * px(130)), run_time=0.35, rate_func=EXPO)
        sk.next_to(leg, RIGHT, buff=px(40))
        self.play(FadeIn(sk, shift=LEFT * 0.1), *[c.animate(rate_func=there_and_back).scale(1.35) for c in skip], run_time=0.6)
        leg.add(sk)
        # working board
        r1 = VGroup(tag("Skip", 34, WHITE_, GREY_P), M(r"5 \times 4 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        r2 = VGroup(tag("Wrong", 34, WHITE_, RD), M(r"4 \times 5 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        board = VGroup(r1, r2).arrange(DOWN, buff=px(40), aligned_edge=LEFT).move_to(P(490, 610))
        why = B("4 missed  +  1 negative", 30, GREY_P, SEMIBOLD).next_to(r2, DOWN, buff=px(14)).align_to(r2[1], LEFT)
        tl = Line(P(250, 0), P(730, 0), color=INK, stroke_width=4).set_y(Y(800))
        tot = VGroup(B("Marks lost", 40, INK, SEMIBOLD), H("40", 96, RD)).arrange(RIGHT, buff=px(24)).move_to(P(490, 875))
        rule = VGroup(B("Rule", 26, OR, SEMIBOLD), H("Wrong answer = −5", 46, WHITE_), B("A skip only costs 4", 30, "#D5DCE8", SEMIBOLD)).arrange(DOWN, buff=px(8))
        rbox = RoundedRectangle(width=px(640), height=rule.height + px(56), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1110))
        rule.move_to(rbox)
        self.until(C[2] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(sch, h1, h2, grid, leg), shift=UP * 0.3), run_time=0.3)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        # ===== C. wrong costs 5 =====
        self.until(C[3] - 0.05); self.ev("tick"); self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(3, 8, 0.1)); self.play(FadeIn(why, shift=UP * 0.06), run_time=0.3)
        self.until(wt(3, 12, 0.1)); self.ev("stamp")
        self.play(Create(tl), FadeIn(tot, scale=1.15), FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        # ===== D. 300 - 40 = 260, where did the 40 go? =====
        eq = VGroup(H("300", 96, INK), H("−", 96, INK), H("40", 96, RD), H("=", 96, INK), H("260", 96, OR)).arrange(RIGHT, buff=px(18)).move_to(P(490, 560))
        wq = H("Which chapters?", 64, INK); fitw(wq, 700); wq.move_to(P(490, 730))
        qs = VGroup(*[VGroup(tag(n, 32, WHITE_, c), H("?", 80, c)).arrange(DOWN, buff=px(10)) for n, c in [("Maths", BLUE), ("Physics", TEAL), ("Chemistry", OR)]]).arrange(RIGHT, buff=px(44)).move_to(P(490, 920))
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(board, why, tl, tot, rbox, rule), shift=UP * 0.3), FadeIn(eq, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(4, 8, 0.1)); self.ev("tick")
        self.play(FadeIn(wq, shift=UP * 0.08), LaggedStart(*[FadeIn(x, scale=1.2) for x in qs], lag_ratio=0.2), run_time=0.6, rate_func=EXPO)
        self.play(LaggedStart(*[Wiggle(x[1], scale_value=1.15) for x in qs], lag_ratio=0.15), run_time=0.8)
        # ===== E. the scorecard =====
        sc, p, st = promo_scorecard2(P, title="Your scorecard")
        self.until(C[5] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(eq, wq, qs), shift=UP * 0.3), run_time=0.3)
        promo_card2_in(self, p, st)
        # ===== F. marks / lagging / fix next =====
        hl = lambda mob: SurroundingRectangle(mob, buff=px(12), corner_radius=0.14, color=OR, stroke_width=5)
        h1 = hl(VGroup(p["ring_bg"], p["bars"], p["stats"])); h2 = hl(p["lagbox"]); h3 = hl(p["fb"])
        self.until(wt(6, 3, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(6, 5, 0.08)); self.play(ReplacementTransform(h1, h2), Indicate(p["lags"][0][1], color=RD, scale_factor=1.12), run_time=0.35)
        self.until(wt(6, 9, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        p["arc"].clear_updaters(); p["num"].clear_updaters()
        # ===== H. all these features, Rs 99/month, Comment LINK =====
        feats = ["Full JEE Main mock tests", "Scorecard after every test", "Chapters you're lagging in", "What to fix next", "Doubt support"]
        def frow(t):
            ck = VGroup(Circle(radius=px(20), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 24, WHITE_, SEMIBOLD))
            ck[1].move_to(ck[0]); return VGroup(ck, B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(18))
        rows = VGroup(*[frow(t) for t in feats]).arrange(DOWN, buff=px(22), aligned_edge=LEFT)
        fbox = RoundedRectangle(width=px(700), height=rows.height + px(70), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, 760))
        rows.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * px(44))
        fhd = H("All of this", 50, INK).next_to(fbox, UP, buff=px(22))
        price = VGroup(H("Just", 60, INK), H("₹99", 110, OR), H("/month", 60, INK)).arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(P(490, 1150))
        self.until(C[-1] - 0.05); self.ev("wipe")
        self.play(FadeOut(sc), FadeOut(h3), FadeIn(fhd, shift=DOWN * 0.08), FadeIn(fbox), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.7, rate_func=EXPO)
        self.until(C[-1] + 0.6); self.ev("stamp"); self.play(FadeIn(price, scale=1.25), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(C[-1] + 2.25); promo_cta(self, P, t0)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoD4(ShortReel2):
    """Promo D v4 (22 Nov, Aro: answer-sheet intro 'boring'). Live countdown hook: 300 drops hit by hit
    (-5 wrong x4, -4 skip x5, synced to 'two ninety-five / two ninety-one') to 260; twist 'only 4 wrong'."""
    EVENTS = "promod4"; SERIES = "JEE Main 2027"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        O = json.load(open(os.path.join(KIT, "topics/jee_promo_d4/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        t0 = self.renderer.time
        # ===== A. live countdown: 300 -> 260, a chip per hit =====
        HITS = [-5, -4, -4, -5, -4, -5, -4, -4, -5]
        sch = tag("Your JEE Main mock score", 30, WHITE_, INK).move_to(P(490, 470))
        q = H("Watch it fall.", 60, INK).move_to(P(490, 560))
        val = ValueTracker(300)
        def numcol():
            f = (300 - val.get_value()) / 40.0
            return interpolate_color(ManimColor(INK), ManimColor(RD), max(0, min(1, f)))
        num = always_redraw(lambda: H(str(int(round(val.get_value()))), 250, numcol()).move_to(P(490, 740)))
        of = B("out of 300", 40, GREY_P, SEMIBOLD).move_to(P(490, 880))
        slots = [P(200 + (j % 5) * 145, 1010 + (j // 5) * 74) for j in range(9)]
        chips = VGroup()
        def chip(h):
            return tag("✗ −5" if h == -5 else "skip −4", 23, WHITE_, RD if h == -5 else OR)
        self.add(sch, q, num, of)
        times = [C[0] + O[0][1], C[0] + O[0][2]]
        a, b = C[0] + O[0][3], C[1] - 0.2
        times += [a + (b - a) * j / 6 for j in range(7)]
        for j, (h, tt) in enumerate(zip(HITS, times)):
            self.until(tt - 0.02); self.ev("tick")
            c = chip(h).move_to(P(490, 740)).scale(0.6); chips.add(c)
            rt = 0.3 if j < 2 else 0.18
            self.play(val.animate.increment_value(h), c.animate.scale(1 / 0.6).move_to(slots[j]), run_time=rt, rate_func=EXPO)
        num.clear_updaters(); num.become(H("260", 250, RD).move_to(P(490, 740)))
        # ===== B. 40 marks gone, and only 4 wrong =====
        gone = H("40 marks, gone.", 64, RD).move_to(P(490, 560))
        self.until(C[1] - 0.05); self.ev("stamp")
        self.play(FadeOut(q, shift=UP * 0.1), FadeIn(gone, scale=1.15), Indicate(num, color=RD, scale_factor=1.04), run_time=0.4, rate_func=EXPO)
        wr = [c for c, h in zip(chips, HITS) if h == -5]; sk = [c for c, h in zip(chips, HITS) if h == -4]
        lw = B("4 wrong", 30, RD, SEMIBOLD).move_to(P(490, 975)); ls = B("5 skipped", 30, OR, SEMIBOLD).move_to(P(490, 1100))
        self.until(wt(1, 7, 0.1)); self.ev("tick")
        self.play(*[c.animate.move_to(P(490 + (k - 1.5) * 150, 1025)) for k, c in enumerate(wr)],
                  *[c.animate.move_to(P(490 + (k - 2) * 145, 1150)) for k, c in enumerate(sk)], FadeIn(lw), FadeIn(ls), run_time=0.45, rate_func=EXPO)
        self.play(*[c.animate(rate_func=there_and_back).scale(1.12) for c in wr], run_time=0.4)
        # ===== C. the catch: a wrong answer costs 5 =====
        r2 = VGroup(tag("Wrong", 34, WHITE_, RD), M(r"4 \times 5 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        r1 = VGroup(tag("Skip", 34, WHITE_, OR), M(r"5 \times 4 = 20", 66, INK)).arrange(RIGHT, buff=px(26))
        board = VGroup(r2, r1).arrange(DOWN, buff=px(70), aligned_edge=LEFT).move_to(P(490, 640))
        why = B("4 missed  +  1 negative", 30, GREY_P, SEMIBOLD).next_to(r2, DOWN, buff=px(12)).align_to(r2[1], LEFT)
        tl = Line(P(250, 0), P(730, 0), color=INK, stroke_width=4).set_y(Y(830))
        tot = VGroup(B("Marks lost", 40, INK, SEMIBOLD), H("40", 96, RD)).arrange(RIGHT, buff=px(24)).move_to(P(490, 905))
        rule = VGroup(B("Rule", 26, OR, SEMIBOLD), H("Wrong answer = −5", 46, WHITE_), B("A skip costs 4", 30, "#D5DCE8", SEMIBOLD)).arrange(DOWN, buff=px(8))
        rbox = RoundedRectangle(width=px(640), height=rule.height + px(56), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1130))
        rule.move_to(rbox)
        catch = H("Here's the catch.", 64, INK).move_to(P(490, 640))
        self.until(C[2] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(sch, gone, num, of, chips, lw, ls), shift=UP * 0.3), FadeIn(catch, scale=1.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(2, 3, 0.1)); self.ev("tick")
        self.play(FadeOut(catch, shift=UP * 0.2), FadeIn(r2, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(2, 11, 0.1)); self.play(FadeIn(why, shift=UP * 0.06), run_time=0.3)
        # ===== D. the other 20: skips =====
        self.until(wt(3, 4, 0.1)); self.ev("tick"); self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.until(wt(3, 8, 0.1)); self.ev("stamp")
        self.play(Create(tl), FadeIn(tot, scale=1.15), FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        # ===== E. 300 - 40 = 260, where did the 40 go? =====
        eq = VGroup(H("300", 96, INK), H("−", 96, INK), H("40", 96, RD), H("=", 96, INK), H("260", 96, OR)).arrange(RIGHT, buff=px(18)).move_to(P(490, 560))
        wq = H("Which chapters?", 64, INK); fitw(wq, 700); wq.move_to(P(490, 730))
        qs = VGroup(*[VGroup(tag(n, 32, WHITE_, c), H("?", 80, c)).arrange(DOWN, buff=px(10)) for n, c in [("Maths", BLUE), ("Physics", TEAL), ("Chemistry", OR)]]).arrange(RIGHT, buff=px(44)).move_to(P(490, 920))
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(board, why, tl, tot, rbox, rule), shift=UP * 0.3), FadeIn(eq, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(4, 8, 0.1)); self.ev("tick")
        self.play(FadeIn(wq, shift=UP * 0.08), LaggedStart(*[FadeIn(x, scale=1.2) for x in qs], lag_ratio=0.2), run_time=0.6, rate_func=EXPO)
        self.play(LaggedStart(*[Wiggle(x[1], scale_value=1.15) for x in qs], lag_ratio=0.15), run_time=0.8)
        # ===== E. the scorecard =====
        sc, p, st = promo_scorecard2(P, title="Your scorecard")
        self.until(C[5] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(eq, wq, qs), shift=UP * 0.3), run_time=0.3)
        promo_card2_in(self, p, st)
        # ===== F. marks / lagging / fix next =====
        hl = lambda mob: SurroundingRectangle(mob, buff=px(12), corner_radius=0.14, color=OR, stroke_width=5)
        h1 = hl(VGroup(p["ring_bg"], p["bars"], p["stats"])); h2 = hl(p["lagbox"]); h3 = hl(p["fb"])
        self.until(wt(6, 3, 0.08)); self.play(Create(h1), run_time=0.3)
        self.until(wt(6, 5, 0.08)); self.play(ReplacementTransform(h1, h2), Indicate(p["lags"][0][1], color=RD, scale_factor=1.12), run_time=0.35)
        self.until(wt(6, 9, 0.08)); self.play(ReplacementTransform(h2, h3), run_time=0.3)
        p["arc"].clear_updaters(); p["num"].clear_updaters()
        # ===== H. all these features, Rs 99/month, Comment LINK =====
        feats = ["Full JEE Main mock tests", "Scorecard after every test", "Chapters you're lagging in", "What to fix next", "Doubt support"]
        def frow(t):
            ck = VGroup(Circle(radius=px(20), fill_color=TEAL, fill_opacity=1, stroke_width=0), B("✓", 24, WHITE_, SEMIBOLD))
            ck[1].move_to(ck[0]); return VGroup(ck, B(t, 34, INK, SEMIBOLD)).arrange(RIGHT, buff=px(18))
        rows = VGroup(*[frow(t) for t in feats]).arrange(DOWN, buff=px(22), aligned_edge=LEFT)
        fbox = RoundedRectangle(width=px(700), height=rows.height + px(70), corner_radius=0.22, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3).move_to(P(490, 760))
        rows.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * px(44))
        fhd = H("All of this", 50, INK).next_to(fbox, UP, buff=px(22))
        price = VGroup(H("Just", 60, INK), H("₹99", 110, OR), H("/month", 60, INK)).arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(P(490, 1150))
        self.until(C[-1] - 0.05); self.ev("wipe")
        self.play(FadeOut(sc), FadeOut(h3), FadeIn(fhd, shift=DOWN * 0.08), FadeIn(fbox), run_time=0.35, rate_func=EXPO)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.7, rate_func=EXPO)
        self.until(C[-1] + 0.6); self.ev("stamp"); self.play(FadeIn(price, scale=1.25), run_time=0.4, rate_func=rate_functions.ease_out_back)
        self.until(C[-1] + 2.25); promo_cta(self, P, t0)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller1(ShortReel2):
    """Method Killer #1 (23 Nov): partial fractions by cover-up vs comparing coefficients.
    (2x^2-7x+3)/((x-1)(x+1)(x-2)) = 1/(x-1) + 2/(x+1) - 1/(x-2). Viewer tries C in a 3-2-1 countdown; answer last."""
    EVENTS = "mk1"; SERIES = "Method Killer #1"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        # ---------- frame 0: title + the fraction + the school method ----------
        t1 = H("STOP COMPARING", 82, INK); t2 = H("COEFFICIENTS", 82, RD)
        title = VGroup(t1, t2).arrange(DOWN, buff=px(4)); fitw(title, 700); title.move_to(P(490, 445))
        num = M(r"2x^2-7x+3", 74)
        f1, f2, f3 = M(r"(x-1)", 74), M(r"(x+1)", 74), M(r"(x-2)", 74)
        den = VGroup(f1, f2, f3).arrange(RIGHT, buff=px(4))
        bar = Line(LEFT, RIGHT, color=INK, stroke_width=4).set_width(den.width + px(10))
        frac = VGroup(num, bar, den).arrange(DOWN, buff=px(12)); fitw(frac, 640); frac.move_to(P(490, 660))
        fa, fb, fc = M(r"\frac{A}{x-1}", 66), M(r"\frac{B}{x+1}", 66), M(r"\frac{C}{x-2}", 66)
        rhs = VGroup(M(r"=", 66), fa, M(r"+", 66), fb, M(r"+", 66), fc).arrange(RIGHT, buff=px(14)); fitw(rhs, 630); rhs.next_to(frac, DOWN, buff=px(40)).set_x(X(490))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(rhs, DOWN, buff=px(44)).set_x(X(490))
        eqs = VGroup(M(r"A+B+C=2", 50), M(r"-A-3B=-7", 50), M(r"-2A+2B-C=3", 50)).arrange(DOWN, buff=px(18)).next_to(st, DOWN, buff=px(22)).set_x(X(490))
        note = B("3 equations · 3 unknowns", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(20))
        self.add(title, frac, rhs, st, eqs[0])
        self.play(LaggedStart(FadeIn(eqs[1], shift=DOWN * 0.08), FadeIn(eqs[2], shift=DOWN * 0.08), lag_ratio=0.5), run_time=0.9)
        self.play(FadeIn(note), run_time=0.3)
        school = VGroup(st, eqs, note)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 6, 0.1)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.45, rate_func=EXPO)
        # ---------- cover-up for A ----------
        SH = px(150); ct = tag("Cover-up trick", 34, WHITE_, TEAL).move_to([X(490), rhs.get_bottom()[1] + SH - px(48), 0])
        def cover(f):
            return RoundedRectangle(width=f.width + px(14), height=f.height + px(14), corner_radius=0.08, fill_color=OR, fill_opacity=0.92, stroke_width=0).move_to(f).set_z_index(5)
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2), VGroup(frac, rhs).animate.shift(UP * SH), FadeIn(ct, scale=1.1), run_time=0.45, rate_func=EXPO)
        cv = cover(f1)
        xv = tag("x = 1", 38, WHITE_, OR).move_to(ct.get_center() + DOWN * px(78))
        self.until(wt(1, 6, 0.08)); self.ev("tick"); self.play(FadeIn(cv, scale=1.2), run_time=0.3, rate_func=EXPO)
        self.until(wt(1, 10, 0.08)); self.play(FadeIn(xv, shift=UP * 0.08), run_time=0.3)
        EY = Y(1110); evA = M(r"\frac{2-7+3}{(1+1)(1-2)}", 66).move_to([X(490), EY, 0])
        self.play(Write(evA), run_time=0.6)
        # ---------- A = 1 ----------
        full = MathTex(r"\frac{2-7+3}{(1+1)(1-2)}", r"=\frac{-2}{-2}=1", font_size=66, color=INK); full[1].set_color(TEAL)
        fitw(full, 700); full.move_to([X(490), EY, 0]); evA2 = full[1]
        self.until(C[2] - 0.05)
        self.play(ReplacementTransform(evA, full[0]), FadeIn(evA2, shift=LEFT * 0.1), run_time=0.45, rate_func=EXPO)
        evA = full[0]
        self.until(wt(2, 8, 0.05)); self.ev("stamp")
        na = M(r"\frac{1}{x-1}", 66, TEAL).match_height(fa).move_to(fa)
        self.play(Transform(fa, na), Indicate(evA2, color=TEAL, scale_factor=1.06), run_time=0.4)
        # ---------- B = 2 ----------
        xvb = tag("x = −1", 38, WHITE_, OR).move_to(xv)
        evB = M(r"\frac{2+7+3}{(-1-1)(-1-2)}=\frac{12}{6}=2", 58).move_to(P(490, 1080))
        fitw(evB, 700); evB.move_to([X(490), EY, 0])
        self.until(C[3] - 0.05); self.ev("tick")
        self.play(cv.animate.move_to(f2), FadeOut(evA), FadeOut(evA2), Transform(xv, xvb), run_time=0.35, rate_func=EXPO)
        self.until(wt(3, 11, 0.08)); self.play(Write(evB), run_time=0.7)
        self.until(wt(3, 16, 0.05)); self.ev("stamp")
        nb = M(r"\frac{2}{x+1}", 66, TEAL).match_height(fb).move_to(fb)
        self.play(Transform(fb, nb), run_time=0.35)
        # ---------- your turn: C, 3-2-1 ----------
        xvc = tag("x = 2", 38, WHITE_, OR).move_to(xv)
        yt = H("Your turn", 60, INK).move_to([X(490), EY, 0])
        self.until(C[4] - 0.05); self.ev("wipe")
        self.play(cv.animate.move_to(f3), FadeOut(evB), Transform(xv, xvc), FadeIn(yt, scale=1.1), Indicate(fc, color=OR, scale_factor=1.15), run_time=0.4, rate_func=EXPO)
        T0 = wt(4, 11, 0.0) + 0.35; T1 = C[5] - 0.1
        ring_bg = Circle(radius=px(78), stroke_color="#ECE7DE", stroke_width=14).move_to(P(490, 1270))
        ring = always_redraw(lambda: Arc(radius=px(78), start_angle=PI / 2, angle=-TAU * max(0.001, min(1, (self.renderer.time - T0) / (T1 - T0))), stroke_color=OR, stroke_width=14).move_arc_center_to(ring_bg.get_center()))
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 80, INK).move_to(ring_bg))
        self.until(T0); self.ev("tick"); self.add(ring_bg, ring, cnt)
        # ---------- reveal C = -1 (answer last) ----------
        evC = M(r"\frac{8-14+3}{(2-1)(2+1)}=\frac{-3}{3}=-1", 58); fitw(evC, 700); evC.move_to([X(490), EY, 0])
        self.until(T1); self.ev("stamp"); ring.clear_updaters(); cnt.clear_updaters()
        self.play(FadeOut(VGroup(ring_bg, ring, cnt, yt)), Write(evC), run_time=0.6)
        self.until(wt(5, 7, 0.05))
        nc = M(r"\frac{-1}{x-2}", 66, RD).match_height(fc).move_to(fc)
        self.play(Transform(fc, nc), FadeOut(cv), run_time=0.35)
        box = SurroundingRectangle(rhs, buff=px(16), corner_radius=0.14, color=TEAL, stroke_width=6)
        rule = VGroup(B("Rule", 26, OR, SEMIBOLD), H("Linear factor? Cover it,", 40, WHITE_), H("put its root in.", 40, WHITE_)).arrange(DOWN, buff=px(6))
        rbox = RoundedRectangle(width=px(640), height=rule.height + px(50), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1300))
        rule.move_to(rbox)
        zero = tag("0 equations", 34, WHITE_, TEAL).move_to(xv)
        self.until(wt(5, 9, 0.05)); self.ev("stamp")
        self.play(Create(box), FadeOut(ct), Transform(xv, zero), FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.45, rate_func=EXPO)
        # ---------- tomorrow: #2 ----------
        nxt = VGroup(tag("Method Killer #2 · tomorrow", 32, WHITE_, OR), B("Repeated factors", 40, INK, SEMIBOLD)).arrange(DOWN, buff=px(12))
        self.until(C[6] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(evC, rbox, rule), shift=DOWN * 0.1), FadeIn(nxt.move_to(P(490, 1130)), shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        OF = json.load(open(os.path.join(KIT, "topics/jee_mk1/vo/offsets.json")))[6][1]
        fol = VGroup(tag("+ Follow", 38, WHITE_, BLUE), H("TutorDA", 46, INK)).arrange(RIGHT, buff=px(16)); fitw(fol, 640); fol.move_to(P(490, 1290))
        self.until(C[6] + OF - 0.05); self.ev("tick")
        self.play(FadeIn(fol, shift=UP * 0.1), run_time=0.35, rate_func=EXPO)
        self.play(Indicate(fol[0], color=BLUE, scale_factor=1.12), run_time=0.5)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller2(ShortReel2):
    """Method Killer #2 (23 Nov): repeated factor. (5x+1)/((x-1)^2(x+2)) = 1/(x-1) + 2/(x-1)^2 - 1/(x+2).
    Cover-up gives B (cover the whole square) and C; A from the x^2 terms: A + C = 0. Viewer guesses A; answer last."""
    EVENTS = "mk2"; SERIES = "Method Killer #2"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk2/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        # ---------- frame 0 ----------
        t1 = H("STOP SOLVING", 84, INK); t2 = H("3 EQUATIONS", 84, RD)
        title = VGroup(t1, t2).arrange(DOWN, buff=px(4)); fitw(title, 700); title.move_to(P(490, 445))
        num = M(r"5x+1", 74)
        f1, f2 = M(r"(x-1)^2", 74), M(r"(x+2)", 74)
        den = VGroup(f1, f2).arrange(RIGHT, buff=px(4))
        bar = Line(LEFT, RIGHT, color=INK, stroke_width=4).set_width(den.width + px(10))
        frac = VGroup(num, bar, den).arrange(DOWN, buff=px(12)); fitw(frac, 640); frac.move_to(P(490, 660))
        fa, fb, fc = M(r"\frac{A}{x-1}", 66), M(r"\frac{B}{(x-1)^2}", 66), M(r"\frac{C}{x+2}", 66)
        rhs = VGroup(M(r"=", 66), fa, M(r"+", 66), fb, M(r"+", 66), fc).arrange(RIGHT, buff=px(14)); fitw(rhs, 630)
        rhs.next_to(frac, DOWN, buff=px(40)).set_x(X(490))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(rhs, DOWN, buff=px(44)).set_x(X(490))
        eqs = VGroup(M(r"A+C=0", 50), M(r"A+B-2C=5", 50), M(r"-2A+2B+C=1", 50)).arrange(DOWN, buff=px(18)).next_to(st, DOWN, buff=px(22)).set_x(X(490))
        note = B("3 equations · 3 unknowns", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(20))
        self.add(title, frac, rhs, st, eqs[0])
        self.play(LaggedStart(FadeIn(eqs[1], shift=DOWN * 0.08), FadeIn(eqs[2], shift=DOWN * 0.08), lag_ratio=0.5), run_time=0.9)
        self.play(FadeIn(note), run_time=0.3)
        school = VGroup(st, eqs, note)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 3, 0.1)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.45, rate_func=EXPO)
        rf = tag("Every JEE student does this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 4, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- B: cover the whole square ----------
        SH = px(150); ct = tag("Cover-up trick", 34, WHITE_, TEAL).move_to([X(490), rhs.get_bottom()[1] + SH - px(48), 0])
        def cover(f):
            return RoundedRectangle(width=f.width + px(14), height=f.height + px(14), corner_radius=0.08, fill_color=OR, fill_opacity=0.92, stroke_width=0).move_to(f).set_z_index(5)
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2), VGroup(frac, rhs).animate.shift(UP * SH), FadeIn(ct, scale=1.1), run_time=0.45, rate_func=EXPO)
        cv = cover(f1); self.play(FadeIn(cv, scale=1.2), Indicate(fb, color=OR, scale_factor=1.1), run_time=0.35, rate_func=EXPO)
        xv = tag("x = 1", 38, WHITE_, OR).move_to(ct.get_center() + DOWN * px(78))
        EY = Y(1110)
        evB = MathTex(r"\frac{5(1)+1}{1+2}", r"=\frac{6}{3}=2", font_size=66, color=INK); evB[1].set_color(TEAL); fitw(evB, 700); evB.move_to([X(490), EY, 0])
        self.until(wt(1, 7, 0.08)); self.play(FadeIn(xv, shift=UP * 0.08), Write(evB[0]), run_time=0.5)
        self.until(wt(1, 11, 0.08)); self.play(FadeIn(evB[1], shift=LEFT * 0.1), run_time=0.35)
        self.until(wt(1, 16, 0.05)); self.ev("stamp")
        nb = M(r"\frac{2}{(x-1)^2}", 66, TEAL).match_height(fb).move_to(fb); self.play(Transform(fb, nb), run_time=0.35)
        # ---------- C ----------
        xvc = tag("x = −2", 38, WHITE_, OR).move_to(xv)
        evC = MathTex(r"\frac{5(-2)+1}{(-2-1)^2}", r"=\frac{-9}{9}=-1", font_size=62, color=INK); evC[1].set_color(RD); fitw(evC, 700); evC.move_to([X(490), EY, 0])
        self.until(C[2] - 0.05); self.ev("tick")
        cv2 = cover(f2); self.play(FadeOut(cv), FadeIn(cv2, scale=1.15), FadeOut(evB), Transform(xv, xvc), run_time=0.35, rate_func=EXPO); cv = cv2
        self.until(wt(2, 7, 0.08)); self.play(Write(evC[0]), run_time=0.5)
        self.until(wt(2, 9, 0.08)); self.play(FadeIn(evC[1], shift=LEFT * 0.1), run_time=0.35)
        self.until(wt(2, 16, 0.05)); self.ev("stamp")
        nc = M(r"\frac{-1}{x+2}", 66, RD).match_height(fc).move_to(fc); self.play(Transform(fc, nc), run_time=0.35)
        # ---------- A: no x^2 on top -> A + C = 0 ----------
        self.until(C[3] - 0.05); self.ev("wipe")
        self.play(FadeOut(cv), FadeOut(evC), FadeOut(xv), Indicate(fa, color=OR, scale_factor=1.15), run_time=0.4)
        nx = tag("no x² on top", 32, WHITE_, INK).next_to(num, RIGHT, buff=px(18))
        if nx.get_right()[0] > X(850): nx.next_to(num, LEFT, buff=px(18))
        self.until(wt(3, 8, 0.08)); self.ev("tick")
        self.play(Circumscribe(num, color=OR, buff=px(8)), FadeIn(nx, shift=LEFT * 0.1), run_time=0.6)
        ac = MathTex(r"A+C=0", font_size=78, color=INK).move_to([X(490), Y(1030), 0])
        self.until(wt(3, 14, 0.08)); self.play(Write(ac), run_time=0.5)
        # ---------- your turn: A = ? ----------
        aq = MathTex(r"A=\,?", font_size=78, color=INK).next_to(ac, DOWN, buff=px(26))
        self.until(C[4] - 0.05); self.ev("tick"); self.play(FadeIn(aq, scale=1.15), run_time=0.3)
        T0 = C[4] + OFF[4][0] + 0.9; T1 = C[5] - 0.1
        ring_bg = Circle(radius=px(70), stroke_color="#ECE7DE", stroke_width=14).move_to(P(490, 1320))
        ring = always_redraw(lambda: Arc(radius=px(70), start_angle=PI / 2, angle=-TAU * max(0.001, min(1, (self.renderer.time - T0) / (T1 - T0))), stroke_color=OR, stroke_width=14).move_arc_center_to(ring_bg.get_center()))
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 72, INK).move_to(ring_bg))
        self.until(T0); self.add(ring_bg, ring, cnt)
        # ---------- reveal A = 1 (answer last) ----------
        self.until(T1); self.ev("stamp"); ring.clear_updaters(); cnt.clear_updaters()
        a1 = MathTex(r"A=1", font_size=78, color=TEAL).move_to(aq)
        na = M(r"\frac{1}{x-1}", 66, TEAL).match_height(fa).move_to(fa)
        self.play(FadeOut(VGroup(ring_bg, ring, cnt)), Transform(aq, a1), Transform(fa, na), run_time=0.45, rate_func=EXPO)
        box = SurroundingRectangle(rhs, buff=px(16), corner_radius=0.14, color=TEAL, stroke_width=6)
        rule = VGroup(B("Rule", 26, OR, SEMIBOLD), H("Repeated factor? Cover the", 38, WHITE_), H("full power, then match x² terms.", 38, WHITE_)).arrange(DOWN, buff=px(6))
        rbox = RoundedRectangle(width=px(660), height=rule.height + px(50), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1340))
        fitw(rule, 600); rule.move_to(rbox)
        zero = tag("0 systems of equations", 32, WHITE_, TEAL).move_to(ct)
        self.until(wt(5, 1, 0.05)); self.ev("stamp")
        self.play(Create(box), Transform(ct, zero), FadeOut(nx), FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.45, rate_func=EXPO)
        # ---------- tomorrow + follow ----------
        nxt = VGroup(tag("Method Killer #3 · tomorrow", 32, WHITE_, OR), B("Integration by parts, no pain", 40, INK, SEMIBOLD)).arrange(DOWN, buff=px(12))
        fitw(nxt, 680)
        self.until(C[6] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(ac, aq, rbox, rule), shift=DOWN * 0.1), FadeIn(nxt.move_to(P(490, 1080)), shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(C[6] + OFF[6][1] - 0.1); self.ev("tick")
        follow_card(self, P, 1280)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


def follow_card(scene, P, y, handle="tutorda_", sub="One JEE method killer a day"):
    """Animated 'Follow TutorDA' end beat (23 Nov, Aro: plain chip looked simple). Profile card slides up,
    Follow button glows, a tap ripple, the button flips to 'Following ✓' with a shine sweep. No confetti."""
    NAVY = "#0E142A"; BL = "#2563EB"
    card = RoundedRectangle(width=px(720), height=px(170), corner_radius=0.3, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
    shadow = card.copy().set_fill(NAVY, 0.10).set_stroke(width=0).shift(DOWN * px(8))
    av = Circle(radius=px(54), fill_color=NAVY, fill_opacity=1, stroke_color=OR, stroke_width=6)
    mono = VGroup(H("T", 44, WHITE_), H("DA", 44, OR)).arrange(RIGHT, buff=px(2)).move_to(av)
    name = VGroup(H("Tutor", 48, BL), H("DA", 48, OR)).arrange(RIGHT, buff=px(2))
    hand = B("@" + handle, 30, GREY_P, SEMIBOLD); subl = B(sub, 28, GREY_P, SEMIBOLD)
    txt = VGroup(name, hand, subl).arrange(DOWN, buff=px(4), aligned_edge=LEFT)
    btn = RoundedRectangle(width=px(200), height=px(78), corner_radius=0.18, fill_color=BL, fill_opacity=1, stroke_width=0)
    bt = H("Follow", 38, WHITE_).move_to(btn); button = VGroup(btn, bt)
    row = VGroup(VGroup(av, mono), txt).arrange(RIGHT, buff=px(20))
    grp = VGroup(row, button).arrange(RIGHT, buff=px(30)); fitw(grp, 680)
    card.move_to(P(490, y)); shadow.move_to(card.get_center() + DOWN * px(8)); grp.move_to(card)
    scene.play(FadeIn(shadow, shift=UP * 0.25), FadeIn(card, shift=UP * 0.25), FadeIn(grp, shift=UP * 0.25), run_time=0.45, rate_func=EXPO)
    # glow pulse on the button (two soft rings)
    for k in range(2):
        ring = RoundedRectangle(width=btn.width, height=btn.height, corner_radius=0.18, stroke_color=BL, stroke_width=6, fill_opacity=0).move_to(btn)
        scene.play(ring.animate.scale(1.35).set_stroke(opacity=0), button.animate(rate_func=there_and_back).scale(1.06), run_time=0.45)
        scene.remove(ring)
    # tap: ripple + flip to Following
    rip = Circle(radius=px(10), fill_color=WHITE_, fill_opacity=0.55, stroke_width=0).move_to(btn.get_center() + RIGHT * px(30) + DOWN * px(8)).set_z_index(6)
    btn2 = RoundedRectangle(width=btn.width, height=btn.height, corner_radius=0.18, fill_color="#E8EDF5", fill_opacity=1, stroke_width=0).move_to(btn)
    ftx = H("Following", 30, NAVY)
    chk = VMobject(stroke_color=TEAL, stroke_width=7).set_points_as_corners([[0, 0, 0], [px(9), -px(10), 0], [px(26), px(12), 0]])
    bt2 = VGroup(ftx, chk).arrange(RIGHT, buff=px(8)); fitw(bt2, btn.width / px(1) - 26); bt2.move_to(btn2).set_z_index(9)
    scene.add(rip)
    scene.play(rip.animate.scale(9).set_fill(opacity=0), button.animate.scale(0.94), run_time=0.3)
    scene.remove(rip)
    scene.play(button.animate.scale(1 / 0.94), run_time=0.12)
    btn2.move_to(btn); bt2.move_to(btn)
    scene.play(Transform(btn, btn2), FadeOut(bt, scale=0.8), FadeIn(ftx, scale=1.1), Create(chk), run_time=0.35, rate_func=EXPO)
    grp.add(bt2)
    # shine sweep across the card
    sh = Polygon([0, 0, 0], [px(40), 0, 0], [px(10), -px(150), 0], [-px(30), -px(150), 0], fill_color=WHITE_, fill_opacity=0.55, stroke_width=0)
    sh.move_to(card.get_left() + RIGHT * px(20)).set_z_index(7)
    scene.add(sh); scene.play(sh.animate.move_to(card.get_right() + LEFT * px(20)), run_time=0.5, rate_func=rate_functions.ease_in_out_sine); scene.remove(sh)
    return VGroup(shadow, card, grp)


class MethodKiller3(ShortReel2):
    """Method Killer #3 (25 Nov): integration by parts twice vs the P - P' + P'' rule.
    int x^2 e^x dx = e^x (x^2 - 2x + 2) + C. Frame 0 shows the school method AND the one-line template with blanks
    (Aro's audit 25 Nov: the opening must show the surprise at once). Viewer fills the last blank in a 3-2-1; answer last."""
    EVENTS = "mk3"; SERIES = "Method Killer #3"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk3/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        # ---------- frame 0: title, the integral, school method, one-line template ----------
        t1 = H("STOP DOING", 80, INK); t2 = H("BY PARTS TWICE", 80, RD)
        title = VGroup(t1, t2).arrange(DOWN, buff=px(4)); fitw(title, 700); title.move_to(P(490, 430))
        integ = M(r"\int x^2 e^x\,dx", 84); integ.next_to(title, DOWN, buff=px(30)).set_x(X(490))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(integ, DOWN, buff=px(28)).set_x(X(490))
        eqs = VGroup(M(r"u=x^2,\ \ dv=e^x\,dx", 46), M(r"=x^2e^x-\int 2x\,e^x\,dx", 46), M(r"u=2x,\ \ dv=e^x\,dx\ \ \text{again}", 46))
        eqs.arrange(DOWN, buff=px(14)); fitw(eqs, 640); eqs.next_to(st, DOWN, buff=px(18)).set_x(X(490))
        note = B("2 rounds of parts", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(14))
        line = MathTex(r"e^x", r"\Big(", r"x^2", r"-", r"2x", r"+", r"2", r"\Big)", r"+C", font_size=76, color=INK)
        fitw(line, 600)
        card = RoundedRectangle(width=px(700), height=line.height + px(130), corner_radius=0.28, fill_color=WHITE_, fill_opacity=1, stroke_color=TEAL, stroke_width=4)
        ctag = tag("TutorDA way · one line", 30, WHITE_, TEAL)
        card.next_to(note, DOWN, buff=px(40)).set_x(X(490))
        ctag.move_to(card.get_top()); line.move_to(card.get_center() + DOWN * px(14))
        def blank(m):
            r = RoundedRectangle(width=max(m.width + px(16), px(46)), height=line[2].height + px(22), corner_radius=0.08,
                                 fill_color="#FFF1E0", fill_opacity=1, stroke_width=0).move_to(m).set_y(line[2].get_y() - px(6))
            return VGroup(r, DashedVMobject(r.copy().set_fill(opacity=0).set_stroke(OR, 4), num_dashes=18))
        for k in (4, 6): line[k].set_opacity(0)
        b1, b2 = blank(line[4]), blank(line[6])
        self.add(title, integ, st, eqs, note, card, ctag, line, b1, b2)      # whole contrast visible on frame 0
        self.play(Indicate(VGroup(b1, b2), color=OR, scale_factor=1.12), run_time=0.8)
        school = VGroup(st, eqs, note)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 5, 0.1)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.45, rate_func=EXPO)
        rf = tag("Every JEE student does this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 6, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- clip 1: keep e^x outside, P then -P' ----------
        top = VGroup(card, ctag, line, b1, b2)
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2),
                  integ.animate.scale(0.8).move_to(P(490, 455)), top.animate.move_to(P(490, 690)), run_time=0.45, rate_func=EXPO)
        out = tag("stays outside", 28, WHITE_, INK).next_to(card, DOWN, buff=px(18)).align_to(card, LEFT).shift(RIGHT * px(20))
        self.until(wt(1, 1, 0.08)); self.ev("tick")
        self.play(Circumscribe(line[0], color=OR, buff=px(8)), FadeIn(out, shift=UP * 0.08), run_time=0.6)
        # derivative chain x^2 -> 2x -> 2 -> 0
        CY = 930
        terms = [M(r"x^2", 72), M(r"2x", 72), M(r"2", 72), M(r"0", 72, RD)]
        arrows = [Arrow(LEFT, RIGHT, color=GREY_P, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.3).set_length(px(110)) for _ in range(3)]
        chain = VGroup(terms[0], arrows[0], terms[1], arrows[1], terms[2], arrows[2], terms[3]).arrange(RIGHT, buff=px(22))
        fitw(chain, 620); chain.move_to(P(475, CY))
        dl = [B("d/dx", 24, GREY_P, SEMIBOLD).next_to(a, UP, buff=px(6)) for a in arrows]
        sg = [M(r"+", 54, TEAL), M(r"-", 54, RD), M(r"+", 54, TEAL)]
        for s_, t_ in zip(sg, terms): s_.next_to(t_, DOWN, buff=px(26))
        self.until(wt(1, 6, 0.08)); self.ev("tick")
        self.play(TransformFromCopy(line[2], terms[0]), FadeIn(sg[0], shift=UP * 0.08), FadeOut(out), run_time=0.45, rate_func=EXPO)
        self.until(wt(1, 10, 0.08))
        self.play(GrowArrow(arrows[0]), FadeIn(dl[0]), run_time=0.35)
        self.until(wt(1, 13, 0.08)); self.ev("stamp")
        self.play(FadeIn(terms[1], shift=LEFT * 0.1), FadeIn(sg[1], shift=UP * 0.08), run_time=0.3)
        f1 = line[4].copy().set_opacity(1).set_color(RD)
        self.play(FadeOut(b1, scale=0.9), TransformFromCopy(terms[1], f1), line[3].animate.set_color(RD), run_time=0.45, rate_func=EXPO)
        # ---------- clip 2: + next derivative, your turn ----------
        q = H("?", 72, OR).move_to(terms[2])
        self.until(wt(2, 1, 0.08)); self.ev("tick")
        self.play(GrowArrow(arrows[1]), FadeIn(dl[1]), FadeIn(q, scale=1.2), FadeIn(sg[2], shift=UP * 0.08),
                  Indicate(b2, color=OR, scale_factor=1.15), line[5].animate.set_color(TEAL), run_time=0.45)
        T0 = wt(2, 5, 0.0) + 0.5; T1 = C[3] - 0.1
        ring_bg = Circle(radius=px(70), stroke_color="#ECE7DE", stroke_width=14).move_to(P(490, 1190))
        ring = always_redraw(lambda: Arc(radius=px(70), start_angle=PI / 2, angle=-TAU * max(0.001, min(1, (self.renderer.time - T0) / (T1 - T0))), stroke_color=OR, stroke_width=14).move_arc_center_to(ring_bg.get_center()))
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 72, INK).move_to(ring_bg))
        yt = B("Your turn", 34, INK, SEMIBOLD).next_to(ring_bg, UP, buff=px(18))
        self.until(T0); self.add(ring_bg, ring, cnt); self.play(FadeIn(yt), run_time=0.25)
        # ---------- clip 3: reveal 2 (answer last), stop at 0 ----------
        self.until(T1); self.ev("stamp"); ring.clear_updaters(); cnt.clear_updaters()
        f2 = line[6].copy().set_opacity(1).set_color(TEAL)
        self.play(FadeOut(VGroup(ring_bg, ring, cnt, yt)), ReplacementTransform(q, terms[2]), FadeOut(b2, scale=0.9),
                  TransformFromCopy(terms[2], f2), run_time=0.45, rate_func=EXPO)
        stop = tag("stop", 30, WHITE_, RD).next_to(terms[3], DOWN, buff=px(26))
        self.until(wt(3, 2, 0.08)); self.ev("tick")
        self.play(GrowArrow(arrows[2]), FadeIn(dl[2]), FadeIn(terms[3], shift=LEFT * 0.1), run_time=0.4)
        self.until(wt(3, 7, 0.08)); self.play(FadeIn(stop, scale=1.15), run_time=0.3)
        self.until(wt(3, 8, 0.05)); self.ev("stamp")
        box = SurroundingRectangle(line, buff=px(14), corner_radius=0.14, color=TEAL, stroke_width=6)
        zero = tag("0 rounds of parts", 30, WHITE_, TEAL).move_to(ctag)
        self.play(Create(box), Transform(ctag, zero), line[0:4].animate.set_color(INK), line[5:].animate.set_color(INK),
                  f1.animate.set_color(INK), f2.animate.set_color(INK), run_time=0.45, rate_func=EXPO)
        r1 = VGroup(H("Polynomial times", 40, WHITE_), M(r"e^x", 54, WHITE_)).arrange(RIGHT, buff=px(12), aligned_edge=DOWN)
        r2 = M(r"P-P'+P''-\cdots", 54, WHITE_)
        r3 = B("stop when you hit 0", 34, "#CBD5E1", SEMIBOLD)
        rule = VGroup(B("RULE", 30, OR, SEMIBOLD), r1, r2, r3).arrange(DOWN, buff=px(10))
        if rule.width > px(600): fitw(rule, 600)
        rbox = RoundedRectangle(width=px(660), height=rule.height + px(50), corner_radius=0.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(490, 1260))
        rule.move_to(rbox)
        self.until(wt(3, 13, 0.05)); self.ev("tick")
        self.play(FadeIn(rbox, shift=UP * 0.1), FadeIn(rule, shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        # ---------- clip 4: tomorrow + follow ----------
        nxt = VGroup(tag("Method Killer #4 · tomorrow", 32, WHITE_, OR), B("Definite integrals, King's rule", 40, INK, SEMIBOLD)).arrange(DOWN, buff=px(12))
        fitw(nxt, 680)
        self.until(C[4] - 0.05); self.ev("wipe")
        chainall = VGroup(chain, *dl, *sg, stop)
        self.play(FadeOut(VGroup(chainall, rbox, rule), shift=DOWN * 0.1), FadeIn(nxt.move_to(P(490, 960)), shift=UP * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(C[4] + OFF[4][1] - 0.1); self.ev("tick")
        follow_card(self, P, 1170)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller4(ShortReel2):
    """Method Killer #4 (25 Nov): King's rule. I = int_0^{pi/2} sqrt(sin x)/(sqrt(sin x)+sqrt(cos x)) dx = pi/4.
    Retention fixes from the MK1/MK2 watch graphs (25 Nov): the cross lands on 'Stop' (~0.3 s) so the first second moves;
    one closing line and the follow card right after the answer (~22 s total). Viewer guesses I in a 3-2-1; answer last."""
    EVENTS = "mk4"; SERIES = "Method Killer #4"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk4/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        # ---------- frame 0: title, the integral, the school attempt, the one-swap card ----------
        title = VGroup(H("STOP", 84, INK), H("SUBSTITUTING", 84, RD)).arrange(RIGHT, buff=px(22)); fitw(title, 700); title.move_to(P(490, 385))
        I1 = MathTex(r"I=\int_0^{\pi/2}", r"\frac{\sqrt{\sin x}}{\sqrt{\sin x}+\sqrt{\cos x}}", r"\,dx", font_size=64, color=INK)
        fitw(I1, 700); I1.next_to(title, DOWN, buff=px(34)).set_x(X(490))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(I1, DOWN, buff=px(26)).set_x(X(490))
        eqs = VGroup(M(r"t=\tan x:\ \ \int_0^{\infty}\frac{\sqrt t\,dt}{(\sqrt t+1)(1+t^2)}", 50))
        fitw(eqs, 640); eqs.next_to(st, DOWN, buff=px(16)).set_x(X(490))
        note = B("then partial fractions with √t…", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(12))
        school = VGroup(st, eqs, note)
        ans = MathTex(r"I=", r"\frac{\pi}{4}", font_size=76, color=INK); ans[1].set_opacity(0)
        card = RoundedRectangle(width=px(520), height=ans.height + px(150), corner_radius=0.28, fill_color=WHITE_, fill_opacity=1, stroke_color=TEAL, stroke_width=4)
        ctag = tag("TutorDA way · one swap", 30, WHITE_, TEAL)
        card.next_to(note, DOWN, buff=px(44)).set_x(X(490)); ctag.move_to(card.get_top()); ans.move_to(card.get_center() + DOWN * px(8))
        bl = RoundedRectangle(width=px(70), height=px(96), corner_radius=0.08, fill_color="#FFF1E0", fill_opacity=1, stroke_width=0).move_to(ans[1])
        blank = VGroup(bl, DashedVMobject(bl.copy().set_fill(opacity=0).set_stroke(OR, 4), num_dashes=18))
        cardg = VGroup(card, ctag, ans, blank)
        self.add(title, I1, school, cardg)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 0, -0.12)); self.ev("stamp")                          # lands on "Stop": motion inside the first second
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.4, rate_func=EXPO)
        self.play(Indicate(blank, color=OR, scale_factor=1.12), run_time=0.6)
        rf = tag("Every JEE student tries this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 2, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- clip 1: King's rule swap ----------
        # target stack (measured, no overlaps): I1, chip, I2, sum line, card, ring / follow card
        I1t = I1.copy().move_to(P(490, 425))
        chip = VGroup(tag("King's rule", 30, WHITE_, TEAL), M(r"x\ \to\ \tfrac{\pi}{2}-x", 50)).arrange(RIGHT, buff=px(18))
        chip.next_to(I1t, DOWN, buff=px(16)).set_x(X(490))
        I2 = MathTex(r"I=\int_0^{\pi/2}", r"\frac{\sqrt{\cos x}}{\sqrt{\cos x}+\sqrt{\sin x}}", r"\,dx", font_size=64, color=INK)
        I2.match_height(I1).next_to(chip, DOWN, buff=px(16)).set_x(X(490))
        sm = MathTex(r"2I=\int_0^{\pi/2}", r"\frac{\sqrt{\sin x}+\sqrt{\cos x}}{\sqrt{\sin x}+\sqrt{\cos x}}", r"\,dx", font_size=58, color=INK)
        fitw(sm, 700); sm.next_to(I2, DOWN, buff=px(26)).set_x(X(490))
        s2 = MathTex(r"2I=\int_0^{\pi/2}1\,dx=\frac{\pi}{2}", font_size=56, color=INK); s2.move_to(sm)
        cy = min(sm.get_bottom()[1], s2.get_bottom()[1]) - px(54) - card.height / 2
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2),
                  I1.animate.move_to(I1t), cardg.animate.move_to([X(490), cy, 0]), run_time=0.45, rate_func=EXPO)
        self.until(wt(1, 0, 0.08)); self.ev("tick"); self.play(FadeIn(chip, shift=DOWN * 0.08), run_time=0.35)
        self.until(wt(1, 7, 0.1))
        self.play(TransformFromCopy(I1, I2), run_time=0.55, rate_func=EXPO)
        self.until(wt(1, 8, 0.05)); self.ev("tick")
        self.play(Indicate(I2[1], color=TEAL, scale_factor=1.08), run_time=0.7)
        # ---------- clip 2: add both ----------
        self.until(wt(2, 1, 0.08)); self.ev("tick")
        self.play(TransformFromCopy(VGroup(I1, I2), sm), run_time=0.55, rate_func=EXPO)
        self.until(wt(2, 3, 0.05))
        self.play(Circumscribe(sm[1], color=OR, buff=px(6)), run_time=0.7)
        self.until(wt(2, 7, 0.08)); self.ev("stamp")
        self.play(ReplacementTransform(sm, s2), run_time=0.5, rate_func=EXPO)
        # ---------- clip 3: your turn ----------
        self.until(C[3] - 0.05); self.ev("tick")
        self.play(Indicate(blank, color=OR, scale_factor=1.15), run_time=0.4)
        T0 = C[3] + OFF[3][0] + 0.85; T1 = C[4] - 0.1
        ring_bg = Circle(radius=px(66), stroke_color="#ECE7DE", stroke_width=14).next_to(card, DOWN, buff=px(30))
        ring = always_redraw(lambda: Arc(radius=px(66), start_angle=PI / 2, angle=-TAU * max(0.001, min(1, (self.renderer.time - T0) / (T1 - T0))), stroke_color=OR, stroke_width=14).move_arc_center_to(ring_bg.get_center()))
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 70, INK).move_to(ring_bg))
        self.until(T0); self.add(ring_bg, ring, cnt)
        # ---------- clip 4: reveal pi/4 (answer last), follow straight after ----------
        self.until(T1); self.ev("stamp"); ring.clear_updaters(); cnt.clear_updaters()
        a2 = ans[1].copy().set_opacity(1).set_color(TEAL)
        box = SurroundingRectangle(ans, buff=px(18), corner_radius=0.14, color=TEAL, stroke_width=6)
        zero = tag("0 substitutions", 30, WHITE_, TEAL).move_to(ctag)
        self.play(FadeOut(VGroup(ring_bg, ring, cnt)), FadeOut(blank, scale=0.9), FadeIn(a2, scale=1.25), Create(box), Transform(ctag, zero), run_time=0.45, rate_func=EXPO)
        FY = next(y for y in range(900, 1500, 5) if Y(y) + px(85) < card.get_bottom()[1] - px(40))
        self.until(C[4] + OFF[4][1] - 0.15); self.ev("tick")
        follow_card(self, P, FY)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller5(ShortReel2):
    """Method Killer #5 (27 Nov): Wallis. int_0^{pi/2} sin^6 x dx = (5.3.1)/(6.4.2) * pi/2 = 5pi/32.
    Same retention fixes as MK4: cross lands on 'Stop' (~0.3 s), follow card right after the answer, ~24 s."""
    EVENTS = "mk5"; SERIES = "Method Killer #5"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk5/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        # ---------- frame 0 ----------
        title = VGroup(H("STOP", 84, INK), H("EXPANDING", 84, RD)).arrange(RIGHT, buff=px(22)); fitw(title, 700); title.move_to(P(490, 385))
        I1 = M(r"\int_0^{\pi/2}\sin^6 x\,dx", 84); I1.next_to(title, DOWN, buff=px(34)).set_x(X(490))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(I1, DOWN, buff=px(26)).set_x(X(490))
        eqs = VGroup(M(r"\sin^6x=\left(\frac{1-\cos 2x}{2}\right)^3", 48),
                     M(r"=\tfrac18\left(1-3\cos2x+3\cos^2 2x-\cos^3 2x\right)", 44)).arrange(DOWN, buff=px(12))
        fitw(eqs, 660); eqs.next_to(st, DOWN, buff=px(16)).set_x(X(490))
        note = B("then cos 2x twice more…", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(12))
        school = VGroup(st, eqs, note)
        ans = MathTex(r"=", r"\frac{5\pi}{32}", font_size=70, color=INK); ans[1].set_opacity(0)
        card = RoundedRectangle(width=px(520), height=ans.height + px(110), corner_radius=0.28, fill_color=WHITE_, fill_opacity=1, stroke_color=TEAL, stroke_width=4)
        ctag = tag("TutorDA way · one line", 30, WHITE_, TEAL)
        card.next_to(note, DOWN, buff=px(44)).set_x(X(490)); ctag.move_to(card.get_top()); ans.move_to(card.get_center() + DOWN * px(8))
        bl = RoundedRectangle(width=max(ans[1].width + px(20), px(120)), height=ans[1].height + px(16), corner_radius=0.08, fill_color="#FFF1E0", fill_opacity=1, stroke_width=0).move_to(ans[1])
        blank = VGroup(bl, DashedVMobject(bl.copy().set_fill(opacity=0).set_stroke(OR, 4), num_dashes=22))
        cardg = VGroup(card, ctag, ans, blank)
        self.add(title, I1, school, cardg)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 0, -0.12)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.4, rate_func=EXPO)
        self.play(Indicate(blank, color=OR, scale_factor=1.1), run_time=0.6)
        rf = tag("Every JEE student does this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 7, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- target layout after the wipe (measured) ----------
        I1t = I1.copy().scale(0.72).move_to(P(490, 438))
        chip = tag("Wallis rule", 32, WHITE_, TEAL).next_to(I1t, DOWN, buff=px(16)).set_x(X(490))
        top = MathTex(r"5", r"\cdot", r"3", r"\cdot", r"1", font_size=82, color=INK)
        bot = MathTex(r"6", r"\cdot", r"4", r"\cdot", r"2", font_size=82, color=INK)
        bar = Line(LEFT, RIGHT, color=INK, stroke_width=5).set_width(max(top.width, bot.width) + px(30))
        frac = VGroup(top, bar, bot).arrange(DOWN, buff=px(16))
        times = MathTex(r"\times\ \frac{\pi}{2}", font_size=82, color=INK)
        wal = VGroup(frac, times).arrange(RIGHT, buff=px(26))
        todd = tag("odd numbers below 6", 28, WHITE_, TEAL); tev = tag("even numbers", 28, WHITE_, INK)
        todd.next_to(chip, DOWN, buff=px(20)).set_x(X(490))
        wal.next_to(todd, DOWN, buff=px(18)).set_x(X(490))
        todd.set_x(frac.get_x()); tev.next_to(wal, DOWN, buff=px(18)).set_x(frac.get_x())
        tpow = tag("even power", 28, WHITE_, OR).set_x(times.get_x()).set_y(tev.get_y())
        cy = tev.get_bottom()[1] - px(46) - card.height / 2
        print("MK5 layout: card bottom px", (8 - (cy - card.height / 2)) * 120)
        # ---------- clip 1: wipe, top row ----------
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2),
                  I1.animate.become(I1t), cardg.animate.move_to([X(490), cy, 0]), FadeIn(chip, shift=DOWN * 0.08), run_time=0.45, rate_func=EXPO)
        self.until(wt(1, 5, 0.05)); self.play(FadeIn(todd, shift=DOWN * 0.06), Create(bar), run_time=0.35)
        for k, (i, w_) in enumerate([(0, 9), (2, 10), (4, 11)]):
            self.until(wt(1, w_, 0.05)); self.ev("tick")
            grp = [FadeIn(top[i], shift=DOWN * 0.12, scale=1.2)] + ([FadeIn(top[i - 1])] if i else [])
            self.play(*grp, run_time=0.25)
        # ---------- clip 2: bottom row, x pi/2 ----------
        self.until(wt(2, 4, 0.05)); self.play(FadeIn(tev, shift=UP * 0.06), run_time=0.3)
        for i, w_ in [(0, 6), (2, 7), (4, 8)]:
            self.until(wt(2, w_, 0.05)); self.ev("tick")
            grp = [FadeIn(bot[i], shift=UP * 0.12, scale=1.2)] + ([FadeIn(bot[i - 1])] if i else [])
            self.play(*grp, run_time=0.25)
        self.until(wt(2, 9, 0.05)); self.play(FadeIn(tpow, scale=1.1), run_time=0.3)
        self.until(wt(2, 12, 0.05)); self.ev("stamp")
        self.play(FadeIn(times, shift=LEFT * 0.12), run_time=0.4, rate_func=EXPO)
        # ---------- clip 3: your turn ----------
        self.until(C[3] - 0.05); self.ev("tick")
        self.play(Indicate(blank, color=OR, scale_factor=1.12), run_time=0.4)
        T0 = C[3] + OFF[3][0] + 1.0; T1 = C[4] - 0.1
        ring_bg = Circle(radius=px(66), stroke_color="#ECE7DE", stroke_width=14).next_to(card, DOWN, buff=px(30))
        ring = always_redraw(lambda: Arc(radius=px(66), start_angle=PI / 2, angle=-TAU * max(0.001, min(1, (self.renderer.time - T0) / (T1 - T0))), stroke_color=OR, stroke_width=14).move_arc_center_to(ring_bg.get_center()))
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 70, INK).move_to(ring_bg))
        self.until(T0); self.add(ring_bg, ring, cnt)
        # ---------- clip 4: reveal, follow ----------
        self.until(T1); self.ev("stamp"); ring.clear_updaters(); cnt.clear_updaters()
        a2 = ans[1].copy().set_opacity(1).set_color(TEAL)
        box = SurroundingRectangle(ans, buff=px(18), corner_radius=0.14, color=TEAL, stroke_width=6)
        zero = tag("no expanding", 30, WHITE_, TEAL).move_to(ctag)
        self.play(FadeOut(VGroup(ring_bg, ring, cnt)), FadeOut(blank, scale=0.9), FadeIn(a2, scale=1.25), Create(box), Transform(ctag, zero), run_time=0.45, rate_func=EXPO)
        FY = next(y for y in range(900, 1530, 5) if Y(y) + px(85) < card.get_bottom()[1] - px(40))
        self.until(C[4] + OFF[4][1] - 0.15); self.ev("tick")
        follow_card(self, P, FY)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller6(ShortReel2):
    """Method Killer #6 (28 Nov): int e^x (x-1)/x^2 dx = e^x/x + C via e^x(f + f') = (e^x f)'.
    Playbook: pain hook, contrast frame, word-timed build, one-line why (product rule backwards), the condition,
    predict (3-2-1), answer last, check tag, follow card after the answer."""
    EVENTS = "mk6"; SERIES = "Method Killer #6"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk6/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        # ---------- frame 0 ----------
        title = VGroup(H("STOP", 84, INK), H("BY PARTS HERE", 84, RD)).arrange(RIGHT, buff=px(22)); fitw(title, 700); title.move_to(P(490, 385))
        I1 = M(r"\int e^x\,\frac{x-1}{x^2}\,dx", 76); I1.next_to(title, DOWN, buff=px(30)).set_x(X(490))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(I1, DOWN, buff=px(24)).set_x(X(490))
        eqs = VGroup(M(r"\int\frac{e^x}{x}\,dx-\int\frac{e^x}{x^2}\,dx", 48),
                     M(r"\int\frac{e^x}{x^2}dx=-\frac{e^x}{x}+\int\frac{e^x}{x}dx", 46)).arrange(DOWN, buff=px(12))
        fitw(eqs, 660); eqs.next_to(st, DOWN, buff=px(14)).set_x(X(490))
        note = VGroup(B("and", 30, GREY_P, SEMIBOLD), M(r"\int\frac{e^x}{x}dx", 40, GREY_P), B("has no formula", 30, GREY_P, SEMIBOLD)).arrange(RIGHT, buff=px(10))
        note.next_to(eqs, DOWN, buff=px(10))
        school = VGroup(st, eqs, note)
        ans = MathTex(r"=e^x\cdot", r"\frac{1}{x}", r"+C", font_size=62, color=INK); ans[1].set_opacity(0)
        card = RoundedRectangle(width=px(560), height=ans.height + px(88), corner_radius=0.28, fill_color=WHITE_, fill_opacity=1, stroke_color=TEAL, stroke_width=4)
        ctag = tag("TutorDA way · one line", 30, WHITE_, TEAL)
        card.next_to(note, DOWN, buff=px(40)).set_x(X(490)); ctag.move_to(card.get_top()); ans.move_to(card.get_center() + DOWN * px(8))
        bl = RoundedRectangle(width=max(ans[1].width + px(20), px(90)), height=ans[1].height + px(16), corner_radius=0.08, fill_color="#FFF1E0", fill_opacity=1, stroke_width=0).move_to(ans[1])
        blank = VGroup(bl, DashedVMobject(bl.copy().set_fill(opacity=0).set_stroke(OR, 4), num_dashes=20))
        cardg = VGroup(card, ctag, ans, blank)
        self.add(title, I1, school, cardg)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 0, -0.12)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.4, rate_func=EXPO)
        self.play(Indicate(blank, color=OR, scale_factor=1.1), run_time=0.6)
        rf = tag("Every JEE student does this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 5, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- target layout after the wipe (measured) ----------
        I1t = I1.copy().scale(0.8).move_to(P(490, 438))
        sp = MathTex(r"\frac{x-1}{x^2}", r"=", r"\frac{1}{x}", r"-\frac{1}{x^2}", font_size=58, color=INK)
        sp.next_to(I1t, DOWN, buff=px(66)).set_x(X(490))
        lf = MathTex(r"f", font_size=56, color=TEAL).next_to(sp[2], DOWN, buff=px(14))
        lfd = MathTex(r"f'", font_size=56, color=OR).next_to(sp[3], DOWN, buff=px(14)).set_y(lf.get_y())
        arc = CurvedArrow(sp[2].get_top() + UP * px(10), sp[3].get_top() + UP * px(10) + RIGHT * px(14), angle=-PI / 2.2, color=GREY_P, stroke_width=5)
        ddx = B("d/dx", 26, GREY_P, SEMIBOLD).next_to(arc, UP, buff=px(2))
        rl = MathTex(r"e^x\big(", r"f", r"+", r"f'", r"\big)", r"\;\longrightarrow\;", r"e^x", r"f", font_size=60, color=INK)
        rl[1].set_color(TEAL); rl[3].set_color(OR); rl[7].set_color(TEAL)
        rl.next_to(lf, DOWN, buff=px(30)).set_x(X(490))
        why = tag("product rule, backwards", 28, WHITE_, TEAL).next_to(rl, DOWN, buff=px(16))
        cond = B("works only when the bracket is f + f'", 34, INK, SEMIBOLD).next_to(why, DOWN, buff=px(12))
        cy = cond.get_bottom()[1] - px(40) - card.height / 2
        open(os.path.join(KIT, "out", "mk6_layout.txt"), "w").write(f"I1t {(8-I1t.get_bottom()[1])*120:.0f} sp {(8-sp.get_top()[1])*120:.0f}-{(8-sp.get_bottom()[1])*120:.0f} cond {(8-cond.get_bottom()[1])*120:.0f} card_bottom {(8-(cy-card.height/2))*120:.0f} card_h {card.height*120:.0f}")
        # ---------- clip 1: split, f and f' ----------
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2),
                  I1.animate.become(I1t), cardg.animate.move_to([X(490), cy, 0]), run_time=0.45, rate_func=EXPO)
        self.until(wt(1, 0, 0.05)); self.play(TransformFromCopy(I1[0][3:9] if len(I1[0]) > 9 else I1, sp[0]), FadeIn(sp[1]), run_time=0.45, rate_func=EXPO)
        self.until(wt(1, 3, 0.05)); self.ev("tick"); self.play(FadeIn(sp[2], shift=DOWN * 0.1, scale=1.15), run_time=0.3)
        self.until(wt(1, 6, 0.05)); self.ev("tick"); self.play(FadeIn(sp[3], shift=DOWN * 0.1, scale=1.15), run_time=0.3)
        self.until(wt(1, 11, 0.05)); self.play(FadeIn(lf, shift=UP * 0.06), run_time=0.3)
        self.until(wt(1, 15, 0.05)); self.ev("stamp")
        self.play(Create(arc), FadeIn(ddx), FadeIn(lfd, shift=UP * 0.06), run_time=0.5, rate_func=EXPO)
        # ---------- clip 2: e^x(f + f') -> e^x f, why, condition ----------
        self.until(wt(2, 2, 0.05)); self.ev("tick"); self.play(FadeIn(rl[0:5], shift=UP * 0.08), run_time=0.4)
        self.until(wt(2, 7, 0.05)); self.play(Indicate(rl[1], color=TEAL), run_time=0.35)
        self.until(wt(2, 9, 0.05)); self.play(Indicate(rl[3], color=OR), run_time=0.35)
        self.until(wt(2, 11, 0.05)); self.ev("stamp"); self.play(FadeIn(rl[5:], shift=LEFT * 0.1), run_time=0.4, rate_func=EXPO)
        self.until(wt(2, 13, 0.05)); self.play(FadeIn(why, scale=1.1), run_time=0.3)
        self.until(wt(2, 15, 0.0)); self.play(FadeIn(cond, shift=UP * 0.05), run_time=0.3)
        # ---------- clip 3: your turn ----------
        self.until(C[3] - 0.05); self.ev("tick")
        self.play(Indicate(blank, color=OR, scale_factor=1.12), run_time=0.4)
        T0 = C[3] + OFF[3][0] + 1.0; T1 = C[4] - 0.1
        ring_bg = Circle(radius=px(66), stroke_color="#ECE7DE", stroke_width=14).next_to(card, DOWN, buff=px(30))
        ring = always_redraw(lambda: Arc(radius=px(66), start_angle=PI / 2, angle=-TAU * max(0.001, min(1, (self.renderer.time - T0) / (T1 - T0))), stroke_color=OR, stroke_width=14).move_arc_center_to(ring_bg.get_center()))
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 70, INK).move_to(ring_bg))
        self.until(T0); self.add(ring_bg, ring, cnt)
        # ---------- clip 4: reveal 1/x, check, follow ----------
        self.until(T1); self.ev("stamp"); ring.clear_updaters(); cnt.clear_updaters()
        a2 = ans[1].copy().set_opacity(1).set_color(TEAL)
        box = SurroundingRectangle(ans, buff=px(18), corner_radius=0.14, color=TEAL, stroke_width=6)
        chk_ = tag("differentiate it back: it checks", 28, WHITE_, TEAL).move_to(ctag)
        self.play(FadeOut(VGroup(ring_bg, ring, cnt)), FadeOut(blank, scale=0.9), FadeIn(a2, scale=1.25), Create(box), Transform(ctag, chk_), run_time=0.45, rate_func=EXPO)
        FY = next(y for y in range(900, 1560, 5) if Y(y) + px(85) < card.get_bottom()[1] - px(40))
        self.until(C[4] + OFF[4][1] - 0.15); self.ev("tick")
        follow_card(self, P, FY)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller7(ShortReel2):
    """Method Killer #7 (28 Nov): JEE Main 2026, 23 Jan Shift 1.
    f(x) = int (2 - x^2) e^x / (sqrt(1+x)(1-x)^{3/2}) dx, f(0) = 0 -> f(1/2) = sqrt(3e) - 1 via e^x(f + f').
    The aha beat: f + f' over one denominator has top (1 - x^2) + 1 = 2 - x^2. PYQ tag after the hook, not on frame 0."""
    EVENTS = "mk7"; SERIES = "Method Killer #7"
    RL_WHY = False   # True: show the reason in the rule line, e^x(f + f') = (e^x f)', for viewers who haven't seen MK6
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk7/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        DEN = r"\sqrt{1+x}\,(1-x)^{3/2}"
        # ---------- frame 0 ----------
        title = VGroup(H("STOP", 84, INK), H("PANICKING", 84, RD)).arrange(RIGHT, buff=px(22)); fitw(title, 700); title.move_to(P(490, 380))
        pyq = tag("JEE Main 2026 · 23 Jan, Shift 1", 30, WHITE_, INK).next_to(title, DOWN, buff=px(16)).set_x(X(490))
        prob = M(r"f(x)=\int\frac{(2-x^2)\,e^x}{" + DEN + r"}\,dx", 60); fitw(prob, 720)
        prob.next_to(pyq, DOWN, buff=px(22)).set_x(X(490))
        given = M(r"f(0)=0,\qquad f\!\left(\tfrac12\right)=\ ?", 48).next_to(prob, DOWN, buff=px(14))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(given, DOWN, buff=px(26)).set_x(X(490))
        eqs = M(r"u=\frac{2-x^2}{" + DEN + r"},\quad dv=e^x\,dx", 44); fitw(eqs, 640); eqs.next_to(st, DOWN, buff=px(14)).set_x(X(490))
        note = B("then u' is a monster…", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(10))
        school = VGroup(st, eqs, note)
        ans = MathTex(r"f\!\left(\tfrac12\right)=", r"\sqrt{3e}-1", font_size=64, color=INK); ans[1].set_opacity(0)
        card = RoundedRectangle(width=px(600), height=ans.height + px(96), corner_radius=0.28, fill_color=WHITE_, fill_opacity=1, stroke_color=TEAL, stroke_width=4)
        ctag = tag("TutorDA way · one line", 30, WHITE_, TEAL)
        card.next_to(note, DOWN, buff=px(40)).set_x(X(490)); ctag.move_to(card.get_top()); ans.move_to(card.get_center() + DOWN * px(8))
        bl = RoundedRectangle(width=ans[1].width + px(20), height=ans[1].height + px(18), corner_radius=0.08, fill_color="#FFF1E0", fill_opacity=1, stroke_width=0).move_to(ans[1])
        blank = VGroup(bl, DashedVMobject(bl.copy().set_fill(opacity=0).set_stroke(OR, 4), num_dashes=24))
        cardg = VGroup(card, ctag, ans, blank)
        self.add(title, prob, given, school, cardg)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 0, -0.12)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.4, rate_func=EXPO)
        self.play(Indicate(blank, color=OR, scale_factor=1.08), run_time=0.6)
        self.until(wt(0, 6, 0.05)); self.ev("tick"); self.play(FadeIn(pyq, scale=1.1), run_time=0.3)          # PYQ tag after the hook
        rf = tag("Every JEE student does this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 10, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- target layout after the wipe ----------
        probt = VGroup(prob.copy(), given.copy()); probt[0].scale(0.82); probt[1].scale(0.82)
        probt.arrange(DOWN, buff=px(8)).move_to(P(490, 442))
        pyqt = pyq.copy().scale(0.85).next_to(probt, UP, buff=px(10)).set_x(X(490))
        if self.RL_WHY:
            rl = MathTex(r"e^x\big(", r"f", r"+", r"f'", r"\big)", r"\;=\;", r"\big(e^x", r"f", r"\big)'", font_size=54, color=INK)
        else:
            rl = MathTex(r"e^x\big(", r"f", r"+", r"f'", r"\big)", r"\;\longrightarrow\;", r"e^x", r"f", font_size=54, color=INK)
        rl[1].set_color(TEAL); rl[3].set_color(OR); rl[7].set_color(TEAL)
        rl.next_to(probt, DOWN, buff=px(28)).set_x(X(490))
        fl = MathTex(r"f=\sqrt{\frac{1+x}{1-x}}", font_size=52, color=TEAL)
        fpl = MathTex(r"f'=\frac{1}{" + DEN + r"}", font_size=52, color=OR)
        frow = VGroup(fl, fpl).arrange(RIGHT, buff=px(50)); fitw(frow, 700); frow.next_to(rl, DOWN, buff=px(28)).set_x(X(490))
        sm1 = MathTex(r"f+f'=\frac{(1-x^2)+1}{" + DEN + r"}", font_size=54, color=INK)
        sm2 = MathTex(r"f+f'=\frac{2-x^2}{" + DEN + r"}", font_size=54, color=INK)
        fitw(sm1, 660); sm2.match_height(sm1); fitw(sm2, 660)
        sm1.next_to(frow, DOWN, buff=px(30)).set_x(X(490)); sm2.move_to(sm1)
        sm2t = sm2.copy().move_to(frow.get_center())
        okt = tag("matches the question", 28, WHITE_, TEAL).next_to(sm2t, DOWN, buff=px(10)).set_x(X(490))
        res = MathTex(r"f(x)=e^x\sqrt{\frac{1+x}{1-x}}", r"\;-\;1", font_size=54, color=INK)
        res.next_to(okt, DOWN, buff=px(24)).set_x(X(490))
        cy = res.get_bottom()[1] - px(44) - card.height / 2
        PY = lambda m, e="c": (8 - (m.get_center() if e == "c" else m.get_bottom() if e == "b" else m.get_top())[1]) * 120
        open(os.path.join(KIT, "out", "mk7_layout.txt"), "w").write(f"probt {PY(probt,'t'):.0f}-{PY(probt,'b'):.0f} rl {PY(rl):.0f} frow {PY(frow,'t'):.0f}-{PY(frow,'b'):.0f} sm {PY(sm1,'t'):.0f}-{PY(sm1,'b'):.0f} okt {PY(okt,'b'):.0f} res {PY(res,'t'):.0f}-{PY(res,'b'):.0f} card_h {card.height*120:.0f} card_bottom {(8-(cy-card.height/2))*120:.0f}")
        # ---------- clip 1 ----------
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2),
                  prob.animate.become(probt[0]), given.animate.become(probt[1]), FadeOut(pyq),
                  cardg.animate.move_to([X(490), cy, 0]), run_time=0.45, rate_func=EXPO)
        self.until(wt(1, 1, 0.05)); self.ev("tick"); self.play(FadeIn(rl, shift=UP * 0.08), run_time=0.4)
        self.until(wt(1, 6, 0.05)); self.play(Indicate(rl[1], color=TEAL), run_time=0.3)
        self.until(wt(1, 8, 0.05)); self.play(Indicate(rl[3], color=OR), run_time=0.3)
        self.until(wt(1, 13, 0.05)); self.ev("tick"); self.play(FadeIn(fl, shift=DOWN * 0.08, scale=1.1), run_time=0.4)
        # ---------- clip 2: the aha ----------
        self.until(wt(2, 0, 0.05)); self.ev("tick"); self.play(FadeIn(fpl, shift=DOWN * 0.08, scale=1.1), run_time=0.4)
        self.until(wt(2, 3, 0.05)); self.play(TransformFromCopy(VGroup(fl, fpl), sm1), run_time=0.55, rate_func=EXPO)
        self.until(wt(2, 6, 0.05)); self.play(Circumscribe(sm1, color=OR, buff=px(6)), run_time=0.8)
        self.until(wt(2, 13, 0.05)); self.ev("stamp")
        self.play(ReplacementTransform(sm1, sm2), run_time=0.45, rate_func=EXPO)
        self.play(FadeOut(frow, shift=UP * 0.1), sm2.animate.move_to(sm2t), run_time=0.4, rate_func=EXPO)
        self.play(FadeIn(okt, scale=1.1), Indicate(prob, color=TEAL, scale_factor=1.04), run_time=0.4)
        # ---------- clip 3: constant, then your turn ----------
        self.until(wt(3, 0, 0.05)); self.ev("tick"); self.play(FadeIn(res[0], shift=UP * 0.08), run_time=0.4)
        self.until(wt(3, 6, 0.05)); self.play(FadeIn(res[1], scale=1.2), run_time=0.3)
        opts_tex = [r"\sqrt{2e}-1", r"\sqrt{3e}-1", r"\sqrt{3e}+1", r"\sqrt{2e}+1"]
        chips = VGroup()
        for t_ in opts_tex:
            m = MathTex(t_, font_size=46, color=INK)
            r = RoundedRectangle(width=m.width + px(44), height=m.height + px(26), corner_radius=0.16, fill_color=WHITE_, fill_opacity=1, stroke_color=GREY_P, stroke_width=3)
            chips.add(VGroup(r, m.move_to(r)))
        chips.arrange(RIGHT, buff=px(14)); fitw(chips, 700); chips.next_to(card, DOWN, buff=px(24)).set_x(X(490))
        self.until(wt(3, 8, 0.05)); self.ev("tick")
        self.play(Indicate(blank, color=OR, scale_factor=1.1), LaggedStart(*[FadeIn(c_, shift=UP * 0.06) for c_ in chips], lag_ratio=0.15), run_time=0.6)
        T0 = C[3] + OFF[3][1] + 1.2; T1 = C[4] - 0.1
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 64, OR).move_to(bl))
        self.until(T0); self.add(cnt)
        # ---------- clip 4: reveal, follow ----------
        self.until(T1); self.ev("stamp"); cnt.clear_updaters()
        a2 = ans[1].copy().set_opacity(1).set_color(TEAL)
        box = SurroundingRectangle(ans, buff=px(16), corner_radius=0.14, color=TEAL, stroke_width=6)
        win = chips[1]
        self.play(FadeOut(cnt), FadeOut(blank, scale=0.9), FadeIn(a2, scale=1.2), Create(box),
                  win[0].animate.set_stroke(TEAL, 6).set_fill("#E6F7F5", 1), *[c_.animate.set_opacity(0.25) for i_, c_ in enumerate(chips) if i_ != 1],
                  Transform(ctag, tag("0 rounds of by parts", 30, WHITE_, TEAL).move_to(ctag)), run_time=0.45, rate_func=EXPO)
        FY = next((y for y in range(900, 1560, 5) if Y(y) + px(85) < card.get_bottom()[1] - px(40)), 1560)
        self.until(C[4] + OFF[4][1] - 0.15); self.ev("tick")
        self.play(FadeOut(chips), run_time=0.25)
        follow_card(self, P, FY)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class MethodKiller6PYQ(MethodKiller7):
    """The JEE Main 2026 PYQ reel posted as Method Killer #6 (Aro, 28 Nov): same audio and timing as MK7,
    header says #6, and the rule line shows its reason, e^x(f + f') = (e^x f)', since viewers haven't seen the rule reel."""
    SERIES = "Method Killer #6"; RL_WHY = True


class MethodKiller6P(ShortReel2):
    """Method Killer #7 (28 Nov): JEE Main 2026, 23 Jan Shift 1.
    f(x) = int (2 - x^2) e^x / (sqrt(1+x)(1-x)^{3/2}) dx, f(0) = 0 -> f(1/2) = sqrt(3e) - 1 via e^x(f + f').
    The aha beat: f + f' over one denominator has top (1 - x^2) + 1 = 2 - x^2. PYQ tag after the hook, not on frame 0."""
    EVENTS = "mk6p"; SERIES = "Method Killer #6"
    RL_WHY = True   # True: show the reason in the rule line, e^x(f + f') = (e^x f)', for viewers who haven't seen MK6
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        RD = "#E5484D"; P = lambda x, y: [X(x), Y(y), 0]
        OFF = json.load(open(os.path.join(KIT, "topics/jee_mk6p/vo/offsets.json")))
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        DEN = r"\sqrt{1+x}\,(1-x)^{3/2}"
        # ---------- frame 0 ----------
        title = VGroup(H("STOP", 84, INK), H("PANICKING", 84, RD)).arrange(RIGHT, buff=px(22)); fitw(title, 700); title.move_to(P(490, 380))
        pyq = tag("JEE Main 2026 · 23 Jan, Shift 1", 30, WHITE_, INK).next_to(title, DOWN, buff=px(16)).set_x(X(490))
        prob = M(r"f(x)=\int\frac{(2-x^2)\,e^x}{" + DEN + r"}\,dx", 60); fitw(prob, 720)
        prob.next_to(pyq, DOWN, buff=px(22)).set_x(X(490))
        given = M(r"f(0)=0,\qquad f\!\left(\tfrac12\right)=\ ?", 48).next_to(prob, DOWN, buff=px(14))
        st = tag("School method", 28, WHITE_, GREY_P).next_to(given, DOWN, buff=px(26)).set_x(X(490))
        eqs = M(r"u=\frac{2-x^2}{" + DEN + r"},\quad dv=e^x\,dx", 44); fitw(eqs, 640); eqs.next_to(st, DOWN, buff=px(14)).set_x(X(490))
        note = B("then u' is a monster…", 30, GREY_P, SEMIBOLD).next_to(eqs, DOWN, buff=px(10))
        school = VGroup(st, eqs, note)
        ans = MathTex(r"f\!\left(\tfrac12\right)=", r"\sqrt{3e}-1", font_size=64, color=INK); ans[1].set_opacity(0)
        card = RoundedRectangle(width=px(600), height=ans.height + px(96), corner_radius=0.28, fill_color=WHITE_, fill_opacity=1, stroke_color=TEAL, stroke_width=4)
        ctag = tag("TutorDA way · one line", 30, WHITE_, TEAL)
        card.next_to(note, DOWN, buff=px(40)).set_x(X(490)); ctag.move_to(card.get_top()); ans.move_to(card.get_center() + DOWN * px(8))
        bl = RoundedRectangle(width=ans[1].width + px(20), height=ans[1].height + px(18), corner_radius=0.08, fill_color="#FFF1E0", fill_opacity=1, stroke_width=0).move_to(ans[1])
        blank = VGroup(bl, DashedVMobject(bl.copy().set_fill(opacity=0).set_stroke(OR, 4), num_dashes=24))
        cardg = VGroup(card, ctag, ans, blank)
        self.add(title, prob, given, school, cardg)
        x1 = Line(school.get_corner(UL) + LEFT * px(20), school.get_corner(DR) + RIGHT * px(20), color=RD, stroke_width=10)
        x2 = Line(school.get_corner(DL) + LEFT * px(20), school.get_corner(UR) + RIGHT * px(20), color=RD, stroke_width=10)
        self.until(wt(0, 0, -0.12)); self.ev("stamp")
        self.play(Create(x1), Create(x2), school.animate.set_opacity(0.35), run_time=0.4, rate_func=EXPO)
        self.play(Indicate(blank, color=OR, scale_factor=1.08), run_time=0.6)
        self.until(wt(0, 6, 0.05)); self.ev("tick"); self.play(FadeIn(pyq, scale=1.1), run_time=0.3)          # PYQ tag after the hook
        rf = tag("Every JEE student does this", 30, WHITE_, OR).move_to(st)
        self.until(wt(0, 10, 0.08)); self.play(FadeIn(rf, scale=1.1), run_time=0.3)
        # ---------- target layout after the wipe ----------
        probt = VGroup(prob.copy(), given.copy()); probt[0].scale(0.82); probt[1].scale(0.82)
        probt.arrange(DOWN, buff=px(8)).move_to(P(490, 442))
        pyqt = pyq.copy().scale(0.85).next_to(probt, UP, buff=px(10)).set_x(X(490))
        if self.RL_WHY:
            rl = MathTex(r"e^x\big(", r"f", r"+", r"f'", r"\big)", r"\;=\;", r"\big(e^x", r"f", r"\big)'", font_size=54, color=INK)
        else:
            rl = MathTex(r"e^x\big(", r"f", r"+", r"f'", r"\big)", r"\;\longrightarrow\;", r"e^x", r"f", font_size=54, color=INK)
        rl[1].set_color(TEAL); rl[3].set_color(OR); rl[7].set_color(TEAL)
        rl.next_to(probt, DOWN, buff=px(28)).set_x(X(490))
        fl = MathTex(r"f=\sqrt{\frac{1+x}{1-x}}", font_size=52, color=TEAL)
        fpl = MathTex(r"f'=\frac{1}{" + DEN + r"}", font_size=52, color=OR)
        frow = VGroup(fl, fpl).arrange(RIGHT, buff=px(50)); fitw(frow, 700); frow.next_to(rl, DOWN, buff=px(28)).set_x(X(490))
        sm1 = MathTex(r"f+f'=\frac{(1-x^2)+1}{" + DEN + r"}", font_size=54, color=INK)
        sm2 = MathTex(r"f+f'=\frac{2-x^2}{" + DEN + r"}", font_size=54, color=INK)
        fitw(sm1, 660); sm2.match_height(sm1); fitw(sm2, 660)
        sm1.next_to(frow, DOWN, buff=px(30)).set_x(X(490)); sm2.move_to(sm1)
        sm2t = sm2.copy().move_to(frow.get_center())
        okt = tag("matches the question", 28, WHITE_, TEAL).next_to(sm2t, DOWN, buff=px(10)).set_x(X(490))
        res = MathTex(r"f(x)=e^x\sqrt{\frac{1+x}{1-x}}", r"\;-\;1", font_size=54, color=INK)
        res.next_to(okt, DOWN, buff=px(24)).set_x(X(490))
        cy = res.get_bottom()[1] - px(44) - card.height / 2
        PY = lambda m, e="c": (8 - (m.get_center() if e == "c" else m.get_bottom() if e == "b" else m.get_top())[1]) * 120
        open(os.path.join(KIT, "out", "mk6p_layout.txt"), "w").write(f"probt {PY(probt,'t'):.0f}-{PY(probt,'b'):.0f} rl {PY(rl):.0f} frow {PY(frow,'t'):.0f}-{PY(frow,'b'):.0f} sm {PY(sm1,'t'):.0f}-{PY(sm1,'b'):.0f} okt {PY(okt,'b'):.0f} res {PY(res,'t'):.0f}-{PY(res,'b'):.0f} card_h {card.height*120:.0f} card_bottom {(8-(cy-card.height/2))*120:.0f}")
        # ---------- clip 1 ----------
        self.until(C[1] - 0.05); self.ev("wipe")
        self.play(FadeOut(VGroup(school, x1, x2, rf), shift=DOWN * 0.2), FadeOut(title, shift=UP * 0.2),
                  prob.animate.become(probt[0]), given.animate.become(probt[1]), FadeOut(pyq),
                  cardg.animate.move_to([X(490), cy, 0]), run_time=0.45, rate_func=EXPO)
        cond = B("works only when the bracket is exactly f + f'", 30, INK, SEMIBOLD).move_to(frow); fitw(cond, 700)
        clue = MathTex(r"\frac{d}{dx}", r"\,\frac{1}{\sqrt{1-x}}", r"=\frac{1}{2\,(1-x)^{3/2}}", font_size=52, color=INK)
        clue[1].set_color(OR); fitw(clue, 640); clue.move_to(frow)
        cluetag = tag("the clue", 28, WHITE_, OR).next_to(clue, DOWN, buff=px(12)).set_x(X(490))
        self.until(wt(1, 1, 0.05)); self.ev("tick"); self.play(FadeIn(rl[0:5], shift=UP * 0.08), run_time=0.4)
        self.until(wt(1, 6, 0.05)); self.play(Indicate(rl[1], color=TEAL), run_time=0.3)
        self.until(wt(1, 8, 0.05)); self.play(Indicate(rl[3], color=OR), run_time=0.3)
        self.until(wt(1, 11, 0.05)); self.ev("stamp"); self.play(FadeIn(rl[5:], shift=LEFT * 0.1), FadeIn(cond, shift=UP * 0.05), run_time=0.4)
        # ---------- clip 2: the clue for guessing f ----------
        self.until(wt(2, 1, 0.05)); self.ev("tick")
        self.play(FadeOut(cond), FadeIn(clue, shift=UP * 0.06), FadeIn(cluetag), run_time=0.4)
        self.play(Indicate(clue[2], color=OR, scale_factor=1.06), Indicate(prob, color=OR, scale_factor=1.03), run_time=0.7)
        self.until(wt(2, 11, 0.05)); self.play(Indicate(clue[1], color=OR, scale_factor=1.12), run_time=0.6)
        self.until(wt(2, 17, 0.05)); self.ev("tick"); self.play(FadeOut(VGroup(clue, cluetag), shift=UP * 0.06), FadeIn(fl, shift=DOWN * 0.08, scale=1.1), run_time=0.4)
        # ---------- clip 2: the aha ----------
        self.until(wt(3, 0, 0.05)); self.ev("tick"); self.play(FadeIn(fpl, shift=DOWN * 0.08, scale=1.1), run_time=0.4)
        self.until(wt(3, 3, 0.05)); self.play(TransformFromCopy(VGroup(fl, fpl), sm1), run_time=0.55, rate_func=EXPO)
        self.until(wt(3, 6, 0.05)); self.play(Circumscribe(sm1, color=OR, buff=px(6)), run_time=0.8)
        self.until(wt(3, 13, 0.05)); self.ev("stamp")
        self.play(ReplacementTransform(sm1, sm2), run_time=0.45, rate_func=EXPO)
        self.play(FadeOut(frow, shift=UP * 0.1), sm2.animate.move_to(sm2t), run_time=0.4, rate_func=EXPO)
        self.play(FadeIn(okt, scale=1.1), Indicate(prob, color=TEAL, scale_factor=1.04), run_time=0.4)
        # ---------- clip 3: constant, then your turn ----------
        self.until(wt(4, 0, 0.05)); self.ev("tick"); self.play(FadeIn(res[0], shift=UP * 0.08), run_time=0.4)
        self.until(wt(4, 6, 0.05)); self.play(FadeIn(res[1], scale=1.2), run_time=0.3)
        opts_tex = [r"\sqrt{2e}-1", r"\sqrt{3e}-1", r"\sqrt{3e}+1", r"\sqrt{2e}+1"]
        chips = VGroup()
        for t_ in opts_tex:
            m = MathTex(t_, font_size=46, color=INK)
            r = RoundedRectangle(width=m.width + px(44), height=m.height + px(26), corner_radius=0.16, fill_color=WHITE_, fill_opacity=1, stroke_color=GREY_P, stroke_width=3)
            chips.add(VGroup(r, m.move_to(r)))
        chips.arrange(RIGHT, buff=px(14)); fitw(chips, 700); chips.next_to(card, DOWN, buff=px(24)).set_x(X(490))
        self.until(wt(4, 8, 0.05)); self.ev("tick")
        self.play(Indicate(blank, color=OR, scale_factor=1.1), LaggedStart(*[FadeIn(c_, shift=UP * 0.06) for c_ in chips], lag_ratio=0.15), run_time=0.6)
        T0 = C[4] + OFF[4][1] + 1.2; T1 = C[5] - 0.1
        cnt = always_redraw(lambda: H(str(max(1, 3 - int((self.renderer.time - T0) / ((T1 - T0) / 3)))), 64, OR).move_to(bl))
        self.until(T0); self.add(cnt)
        # ---------- clip 4: reveal, follow ----------
        self.until(T1); self.ev("stamp"); cnt.clear_updaters()
        a2 = ans[1].copy().set_opacity(1).set_color(TEAL)
        box = SurroundingRectangle(ans, buff=px(16), corner_radius=0.14, color=TEAL, stroke_width=6)
        win = chips[1]
        self.play(FadeOut(cnt), FadeOut(blank, scale=0.9), FadeIn(a2, scale=1.2), Create(box),
                  win[0].animate.set_stroke(TEAL, 6).set_fill("#E6F7F5", 1), *[c_.animate.set_opacity(0.25) for i_, c_ in enumerate(chips) if i_ != 1],
                  Transform(ctag, tag("0 rounds of by parts", 30, WHITE_, TEAL).move_to(ctag)), run_time=0.45, rate_func=EXPO)
        FY = next((y for y in range(900, 1560, 5) if Y(y) + px(85) < card.get_bottom()[1] - px(40)), 1560)
        self.until(C[5] + OFF[5][1] - 0.15); self.ev("tick")
        self.play(FadeOut(chips), run_time=0.25)
        follow_card(self, P, FY)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))



class PromoFlipbook(ShortReel2):
    """Promo (28 Nov): 30-s tour of the TutorDA | JEE Main Mathematics flipbook (artifact 6Cp6cWfpe7ypJqDompdfZC).
    Each beat flips to a real brochure page (cropped: no robot mascot, no Rs 999, no draft GST note) and adds big fact chips on the spoken word."""
    EVENTS = "flip"; SERIES = "JEE Main Maths course"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        P = lambda x, y: [X(x), Y(y), 0]
        CR = os.path.join(KIT, "promo_flipbook", "crops")
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        def page(name, maxh=700, width=736, extra=110):
            im = ImageMobject(os.path.join(CR, name + ".png")); im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["lanczos"])
            im.width = px(width)
            if im.height > px(maxh): im.height = px(maxh)
            top = max(350, 880 - (im.height / px(1) + extra) / 2)
            im.move_to([X(470), Y(top) - im.height / 2, 0])
            frame = Rectangle(width=im.width, height=im.height, stroke_color="#CBD5E1", stroke_width=2).move_to(im)
            shadow = Rectangle(width=im.width, height=im.height, fill_color="#0F172A", fill_opacity=0.10, stroke_width=0).move_to(im).shift(RIGHT * px(10) + DOWN * px(10))
            return Group(shadow, im, frame)
        def chips(labels, size=36, colors=None, below=None, buff=20, cols=None):
            g = VGroup()
            for i, t in enumerate(labels):
                fg, bg = (colors[i] if colors else (WHITE_, INK))
                g.add(tag(t, size, fg, bg))
            if cols: g.arrange_in_grid(cols=cols, buff=(px(14), px(14)))
            else: g.arrange(RIGHT, buff=px(14))
            fitw(g, 760); g.next_to(below, DOWN, buff=px(buff)).set_x(X(470))
            return g
        cur = {"pg": None, "chips": []}
        def flip_to(name, maxh=700, extra=110):
            new = page(name, maxh, extra=extra)
            anims = []
            if cur["pg"] is not None:
                old = cur["pg"]
                self.play(old.animate.stretch(0.02, 0, about_edge=LEFT), *[FadeOut(c_) for c_ in cur["chips"]], run_time=0.18, rate_func=rate_functions.ease_in_quad)
                self.remove(old)
            new.stretch(0.02, 0, about_edge=LEFT); self.add(new)
            self.play(new.animate.stretch(50, 0, about_edge=LEFT), run_time=0.28, rate_func=EXPO)
            cur["pg"] = new; cur["chips"] = []
            return new
        def show(m, rt=0.3):
            self.play(FadeIn(m, shift=UP * 0.08, scale=1.08), run_time=rt); cur["chips"].append(m)
        OR_ = (WHITE_, OR); NV = (WHITE_, INK); TL = (WHITE_, TEAL)
        # ---------- 0: cover ----------
        pg = page("c0_cover", extra=120); self.add(pg); cur["pg"] = pg
        c0 = chips(["All 14 units", "Chapter 1 free"], 50, [NV, OR_], below=pg, buff=34)
        self.add(c0[0]); cur["chips"].append(c0[0])
        self.until(wt(0, 8, 0.0)); self.ev("tick"); show(c0[1])
        # ---------- 1: the paper ----------
        self.until(C[1] - 0.25); self.ev("wipe"); pg = flip_to("c1_paper", 600)
        c1 = chips(["25 questions", "100 marks"], 50, [NV, OR_], below=pg, buff=30)
        self.until(wt(1, 3, 0.0)); show(tag("1/3 of JEE Main", 50, WHITE_, TEAL).next_to(pg, DOWN, buff=px(30)).set_x(X(470)))
        self.until(wt(1, 7, 0.0)); self.ev("tick"); self.play(FadeOut(cur["chips"].pop()), run_time=0.15); show(c1[0])
        self.until(wt(1, 10, 0.0)); self.ev("tick"); show(c1[1])
        # ---------- 2: how every section works ----------
        self.until(C[2] - 0.25); self.ev("wipe"); pg = flip_to("c2_steps")
        c2 = chips(["Learn", "Play", "Practise", "Check", "Exam"], 40, [NV, NV, NV, NV, OR_], below=pg, buff=30)
        for i_, w_ in enumerate([2, 3, 7, 8, 10]):
            self.until(wt(2, w_, 0.0)); self.ev("tick"); show(c2[i_], 0.22)
        # ---------- 3: platform ----------
        self.until(C[3] - 0.25); self.ev("wipe"); pg = flip_to("c3_platform", extra=180)
        c3 = chips(["Web", "Android app", "Ask Dayzi · AI mentor"], 40, [NV, NV, TL], below=pg, buff=30, cols=2)
        for i_, w_ in enumerate([2, 4, 7]):
            self.until(wt(3, w_, 0.0)); self.ev("tick"); show(c3[i_], 0.25)
        # ---------- 4: six levels ----------
        self.until(C[4] - 0.25); self.ev("wipe"); pg = flip_to("c4_levels", extra=180)
        c4 = chips(["Prerequisite", "Easy", "Medium", "Hard", "Challenge", "Mock test"], 40, [NV] * 5 + [OR_], below=pg, buff=30, cols=3)
        self.until(wt(4, 0, 0.0)); self.ev("tick")
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.06) for c_ in c4[:5]], lag_ratio=0.15), run_time=0.7); cur["chips"] += list(c4[:5])
        self.until(wt(4, 8, 0.0)); self.ev("stamp"); show(c4[5])
        # ---------- 5: chapters ----------
        self.until(C[5] - 0.25); self.ev("wipe"); pg = flip_to("c5_chapters", 760)
        self.until(wt(5, 1, 0.0)); self.ev("tick"); show(tag("All 14 JEE Main units", 50, WHITE_, INK).next_to(pg, DOWN, buff=px(28)).set_x(X(470)))
        # ---------- 6: plans ----------
        self.until(C[6] - 0.25); self.ev("wipe"); pg = flip_to("c6_plans", 640, extra=120)
        c6 = chips(["Chapter 1: Free", "More from ₹99/month"], 46, [TL, OR_], below=pg, buff=30)
        self.until(wt(6, 3, 0.0)); self.ev("tick"); show(c6[0])
        self.until(wt(6, 6, 0.0)); self.ev("stamp"); show(c6[1])
        # ---------- 7: try it + follow ----------
        self.until(C[7] - 0.25); self.ev("wipe"); pg = flip_to("c7_try", 520, extra=330)
        site = tag("tutorda.org", 60, WHITE_, OR).next_to(pg, DOWN, buff=px(28)).set_x(X(470)); show(site)
        FY = next((y for y in range(900, 1560, 5) if Y(y) + px(85) < site.get_bottom()[1] - px(30)), 1500)
        self.until(C[7] + 1.15); self.ev("tick")
        follow_card(self, P, FY, sub="JEE Main maths, made clear")
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoFlipbook2(ShortReel2):
    """Promo v2 (28 Nov, Aro: 'full brochure, don't crop, add motion'). All 10 flipbook pages shown whole,
    with a page-turn between pages and a camera that eases from the full page into the part being explained.
    The viewport is one ImageMobject whose pixels are recomputed every frame (crop window + squash for the turn)."""
    EVENTS = "flip2"; SERIES = "JEE Main Maths course"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        from PIL import Image as PImage
        import numpy as np
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        P = lambda x, y: [X(x), Y(y), 0]
        PG = os.path.join(KIT, "promo_flipbook", "pages")
        pages = [PImage.open(os.path.join(PG, f"pg-{i:02d}.jpg")).convert("RGB") for i in range(1, 11)]
        PW, PH = pages[0].size; AR = PW / PH
        VW = 640; VH = int(round(VW / AR)); TOPY = 345
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        FULL = (PW / 2, PH / 2, PW)
        def clamp(cx, cy, w):
            w = min(w, PW); h = w / AR
            if h > PH: h = PH; w = h * AR
            cx = min(max(cx, w / 2), PW - w / 2); cy = min(max(cy, h / 2), PH - h / 2)
            return cx, cy, w, h
        # ---- timeline: (flip time, page index, [(t, (cx, cy, w)), ...]) ----
        Z = {0: [(430, 560, 820), (420, 520, 760)], 1: [(430, 640, 860), (430, 640, 800)], 2: [(540, 560, 860), (540, 600, 660)],
             3: [(540, 560, 860), (540, 520, 620)], 4: [(540, 600, 860), (540, 560, 640)], 5: [(540, 620, 860), (540, 520, 620)],
             6: [(540, 780, 940), (540, 700, 780)], 7: [(540, 700, 940), (540, 650, 780)], 8: [(540, 650, 940), (500, 620, 780)],
             9: [(540, 650, 940), (540, 600, 820)]}
        flips = [(-1.0, 0), (wt(0, 6, -0.2), 1)] + [(C[i] - 0.25, i + 1) for i in range(1, 9)]
        beats = []
        for k, (tf, pi) in enumerate(flips):
            tn = flips[k + 1][0] if k + 1 < len(flips) else K.DUR + 1
            t0 = max(tf + 0.45, 0.0)
            kf = [(t0, FULL), (t0 + 0.8, Z[pi][0]), (tn, Z[pi][1])]
            beats.append((tf, pi, kf))
        ease = lambda u: u * u * (3 - 2 * u)
        def win_at(kf, t):
            if t <= kf[0][0]: return kf[0][1]
            for (ta, a), (tb, b) in zip(kf, kf[1:]):
                if t <= tb:
                    u = ease((t - ta) / max(tb - ta, 1e-6)); return tuple(a[j] + (b[j] - a[j]) * u for j in range(3))
            return kf[-1][1]
        def render(pi, win, squash=1.0):
            cx, cy, w, h = clamp(*win)
            im = pages[pi].crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))).resize((VW, VH), PImage.BILINEAR)
            a = np.zeros((VH, VW, 4), dtype=np.uint8)
            if squash >= 0.999:
                a[:, :, :3] = np.asarray(im); a[:, :, 3] = 255
            else:
                sw = max(2, int(VW * squash)); s_ = np.asarray(im.resize((sw, VH), PImage.BILINEAR)).astype(np.float32)
                shade = (1 - 0.35 * (1 - squash)) * np.linspace(1.0, 0.8, sw)[None, :, None]   # page darkens as it turns
                a[:, :sw, :3] = np.clip(s_ * shade, 0, 255).astype(np.uint8); a[:, :sw, 3] = 255
            return a
        def frame_at(t):
            k = max(i for i, b in enumerate(beats) if b[0] <= t)
            tf, pi, kf = beats[k]
            if k > 0 and t < tf + 0.45:
                u = (t - tf) / 0.45
                if u < 0.45:                                   # previous page turns away
                    _, ppi, pkf = beats[k - 1]; return render(ppi, win_at(pkf, tf), squash=1 - ease(u / 0.45) * 0.98)
                return render(pi, FULL, squash=0.02 + 0.98 * ease((u - 0.45) / 0.55))
            return render(pi, win_at(kf, t))
        view = ImageMobject(frame_at(0.0)); view.width = px(VW); view.move_to([X(470), Y(TOPY) - view.height / 2, 0])
        edge = Rectangle(width=view.width, height=view.height, stroke_color="#CBD5E1", stroke_width=2).move_to(view)
        def upd(m):
            m.pixel_array = frame_at(self.renderer.time)
        view.add_updater(upd); self.add(view)
        pagechip = always_redraw(lambda: tag(f"Page {beats[max(i for i, b in enumerate(beats) if b[0] <= self.renderer.time)][1] + 1} of 10", 24, WHITE_, GREY_P).next_to(edge, UP, buff=px(-18)).align_to(edge, RIGHT).shift(LEFT * px(14)))
        self.add(pagechip)
        live = []
        def chips(labels, size=36, colors=None, cols=None):
            g = VGroup()
            for i, t_ in enumerate(labels):
                fg, bg = (colors[i] if colors else (WHITE_, INK)); g.add(tag(t_, size, fg, bg))
            if cols: g.arrange_in_grid(cols=cols, buff=(px(14), px(12)))
            else: g.arrange(RIGHT, buff=px(14))
            fitw(g, 740); g.next_to(edge, DOWN, buff=px(22)).set_x(X(470)); return g
        def show(m, rt=0.28):
            self.play(FadeIn(m, shift=UP * 0.08, scale=1.08), run_time=rt); live.append(m)
        def clear():
            if live: self.play(*[FadeOut(m) for m in live], run_time=0.15); live.clear()
        def turn(i):
            self.until(C[i] - 0.25); self.ev("wipe"); clear()
        OR_ = (WHITE_, OR); NV = (WHITE_, INK); TL = (WHITE_, TEAL)
        c0 = chips(["All 14 units", "Chapter 1 free"], 46, [NV, OR_])
        self.until(0.4); show(c0[0])
        self.until(wt(0, 8, 0.0)); self.ev("tick"); show(c0[1])
        turn(1); c1 = chips(["1/3 of JEE Main", "25 questions", "100 marks"], 40, [TL, NV, OR_])
        for i_, w_ in enumerate([3, 7, 10]): self.until(wt(1, w_, 0.0)); self.ev("tick"); show(c1[i_], 0.22)
        turn(2); c2 = chips(["Learn", "Play", "Practise", "Check", "Exam"], 40, [NV, NV, NV, NV, OR_])
        for i_, w_ in enumerate([2, 3, 7, 8, 10]): self.until(wt(2, w_, 0.0)); self.ev("tick"); show(c2[i_], 0.2)
        turn(3); c3 = chips(["Web", "Android app", "Ask Dayzi · AI mentor"], 38, [NV, NV, TL])
        for i_, w_ in enumerate([2, 4, 7]): self.until(wt(3, w_, 0.0)); self.ev("tick"); show(c3[i_], 0.22)
        turn(4); c4 = chips(["Prerequisite", "Easy", "Medium", "Hard", "Challenge", "Mock test"], 36, [NV] * 5 + [OR_], cols=3)
        self.until(wt(4, 0, 0.0)); self.ev("tick")
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.06) for c_ in c4[:5]], lag_ratio=0.15), run_time=0.7); live.extend(c4[:5])
        self.until(wt(4, 8, 0.0)); self.ev("stamp"); show(c4[5])
        turn(5); self.until(wt(5, 1, 0.0)); self.ev("tick"); show(chips(["All 14 JEE Main units"], 46))
        turn(6); c6 = chips(["Chapter 1: Free", "More from ₹99/month"], 44, [TL, OR_])
        self.until(wt(6, 3, 0.0)); self.ev("tick"); show(c6[0]); self.until(wt(6, 5, 0.0)); self.ev("stamp"); show(c6[1])
        turn(7); c7 = chips(["1 · Open Chapter 1", "2 · Try the lab", "3 · Pick a plan"], 36, [NV, NV, OR_])
        for i_, w_ in enumerate([4, 7, 10]): self.until(wt(7, w_, 0.0)); self.ev("tick"); show(c7[i_], 0.22)
        turn(8); site = chips(["tutorda.org"], 56, [OR_]); show(site)
        FY = next((y for y in range(900, 1560, 5) if Y(y) + px(85) < site.get_bottom()[1] - px(24)), 1500)
        self.until(C[8] + 1.15); self.ev("tick")
        follow_card(self, P, FY, sub="JEE Main maths, made clear")
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class PromoFlipbook3(ShortReel2):
    """Promo v3 (28 Nov): all 10 flipbook pages shown whole. Motion = page turn + slow push-in + a spotlight
    (rest of the page dims, orange box) that glides to the part being explained on the spoken word."""
    EVENTS = "flip2"; SERIES = "JEE Main Maths course"
    CAP_PILL = True; CAP_Y = 1560; CAP_FS = 38; CAP_X = X(490)
    def construct(self):
        from PIL import Image as PImage, ImageDraw
        import numpy as np
        self.setup_common(); C, wt, S = K.C, K.wt, self.S
        P = lambda x, y: [X(x), Y(y), 0]
        PG = os.path.join(KIT, "promo_flipbook", "pages")
        pages = [PImage.open(os.path.join(PG, f"pg-{i:02d}.jpg")).convert("RGB") for i in range(1, 11)]
        PW, PH = pages[0].size; AR = PW / PH
        VW = 640; VH = int(round(VW / AR)); TOPY = 345
        self.add(self.hdr); lb = self.label(self.SERIES, False); self.add(lb)
        self.add(Line(P(96, 318), P(870, 318), color=RULE, stroke_width=3))
        FULLR = (0, 0, PW, PH)
        # spotlight rectangles in page pixels (x0, y0, x1, y1), each fired on a spoken word
        SP = {
            0: [(wt(0, 0, 0.5), (40, 230, 740, 700))],
            1: [(wt(0, 7, 0.0), (60, 380, 880, 1010))],
            2: [(wt(1, 3, -0.1), (70, 360, 1004, 490)), (wt(1, 7, -0.1), (70, 590, 1004, 905))],
            3: [(wt(2, 2, -0.1), (60, 360, 1040, 660))],
            4: [(wt(3, 2, -0.1), (80, 352, 528, 524)), (wt(3, 4, -0.1), (544, 540, 996, 740)), (wt(3, 7, -0.1), (80, 540, 528, 740))],
            5: [(wt(4, 0, -0.1), (78, 356, 998, 680)), (wt(4, 8, -0.1), (682, 546, 974, 664))],
            6: [(wt(5, 1, -0.1), (60, 370, 1040, 1180))],
            7: [(wt(6, 0, -0.1), (80, 392, 372, 918)), (wt(6, 4, -0.1), (390, 392, 682, 918))],
            8: [(wt(7, 4, -0.1), (60, 380, 1040, 545)), (wt(7, 7, -0.1), (60, 605, 1040, 765)), (wt(7, 10, -0.1), (60, 835, 1040, 1015))],
            9: [(C[8] + 0.6, (60, 560, 800, 905))],
        }
        flips = [(-1.0, 0), (wt(0, 6, -0.2), 1)] + [(C[i] - 0.25, i + 1) for i in range(1, 9)]
        ease = lambda u: (lambda v: v * v * (3 - 2 * v))(max(0.0, min(1.0, u)))
        def spot_at(pi, tf, t):
            seq = SP[pi]
            if t < seq[0][0]: return FULLR, 0.0
            prev = seq[0][1]; k = 0
            for i_, (ts, r) in enumerate(seq):
                if t >= ts: k = i_
            ts, r = seq[k]
            a = FULLR if k == 0 else seq[k - 1][1]
            u = ease((t - ts) / 0.35)
            rr = tuple(a[j] + (r[j] - a[j]) * u for j in range(4))
            dim = 0.5 * (u if k == 0 else 1.0)
            return rr, dim
        def render(pi, t, tf, tn, squash=1.0):
            pz = 1.0 + 0.045 * ease((t - tf) / max(tn - tf, 0.5))              # slow push-in
            rr, dim = spot_at(pi, tf, t)
            cx = (rr[0] + rr[2]) / 2 if dim > 0 else PW / 2; cy = (rr[1] + rr[3]) / 2 if dim > 0 else PH / 2
            w = PW / pz; h = w / AR
            cx = (PW / 2) + (cx - PW / 2) * (1 - 1 / pz) * 4; cy = (PH / 2) + (cy - PH / 2) * (1 - 1 / pz) * 4
            cx = min(max(cx, w / 2), PW - w / 2); cy = min(max(cy, h / 2), PH - h / 2)
            box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            arr = np.asarray(pages[pi]).astype(np.float32)
            if dim > 0:
                m = np.full(arr.shape[:2], 1 - dim, np.float32)
                x0, y0, x1, y1 = [int(v) for v in rr]; m[max(y0, 0):y1, max(x0, 0):x1] = 1.0
                arr = arr * m[:, :, None]
            im = PImage.fromarray(arr.clip(0, 255).astype(np.uint8))
            if dim > 0:
                d = ImageDraw.Draw(im); x0, y0, x1, y1 = [int(v) for v in rr]
                d.rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), radius=14, outline=(255, 140, 0), width=int(7 * dim / 0.5) or 1)
            im = im.crop(tuple(int(v) for v in box)).resize((VW, VH), PImage.BILINEAR)
            a = np.zeros((VH, VW, 4), dtype=np.uint8)
            if squash >= 0.999:
                a[:, :, :3] = np.asarray(im); a[:, :, 3] = 255
            else:
                sw = max(2, int(VW * squash)); s_ = np.asarray(im.resize((sw, VH), PImage.BILINEAR)).astype(np.float32)
                shade = (1 - 0.35 * (1 - squash)) * np.linspace(1.0, 0.8, sw)[None, :, None]
                a[:, :sw, :3] = np.clip(s_ * shade, 0, 255).astype(np.uint8); a[:, :sw, 3] = 255
            return a
        def frame_at(t):
            k = max(i for i, b in enumerate(flips) if b[0] <= t)
            tf, pi = flips[k]; tn = flips[k + 1][0] if k + 1 < len(flips) else K.DUR
            if k > 0 and t < tf + 0.45:
                u = (t - tf) / 0.45
                if u < 0.45:
                    ptf, ppi = flips[k - 1]; return render(ppi, tf, max(ptf, 0), tf, squash=1 - ease(u / 0.45) * 0.98)
                return render(pi, tf, tf, tn, squash=0.02 + 0.98 * ease((u - 0.45) / 0.55))
            return render(pi, t, max(tf, 0), tn)
        view = ImageMobject(frame_at(0.0)); view.width = px(VW); view.move_to([X(470), Y(TOPY) - view.height / 2, 0])
        edge = Rectangle(width=view.width, height=view.height, stroke_width=0).move_to(view)
        view.add_updater(lambda m: setattr(m, "pixel_array", frame_at(self.renderer.time))); self.add(view)
        cur_page = lambda: flips[max(i for i, b in enumerate(flips) if b[0] <= self.renderer.time)][1] + 1
        pagechip = always_redraw(lambda: tag(f"Page {cur_page()} of 10", 24, WHITE_, GREY_P).align_to(edge, UR).shift(LEFT * px(12) + DOWN * px(12)))
        self.add(pagechip)
        live = []
        def chips(labels, size=36, colors=None, cols=None):
            g = VGroup()
            for i, t_ in enumerate(labels):
                fg, bg = (colors[i] if colors else (WHITE_, INK)); g.add(tag(t_, size, fg, bg))
            if cols: g.arrange_in_grid(cols=cols, buff=(px(14), px(12)))
            else: g.arrange(RIGHT, buff=px(14))
            fitw(g, 740); g.next_to(edge, DOWN, buff=px(22)).set_x(X(470)); return g
        def show(m, rt=0.28):
            self.play(FadeIn(m, shift=UP * 0.08, scale=1.08), run_time=rt); live.append(m)
        def clear():
            if live: self.play(*[FadeOut(m) for m in live], run_time=0.15); live.clear()
        def turn(i):
            self.until(C[i] - 0.25); self.ev("wipe"); clear()
        OR_ = (WHITE_, OR); NV = (WHITE_, INK); TL = (WHITE_, TEAL)
        c0 = chips(["All 14 units", "Chapter 1 free"], 46, [NV, OR_])
        self.until(0.4); show(c0[0])
        self.until(wt(0, 8, 0.0)); self.ev("tick"); show(c0[1])
        turn(1); c1 = chips(["1/3 of JEE Main", "25 questions", "100 marks"], 40, [TL, NV, OR_])
        for i_, w_ in enumerate([3, 7, 10]): self.until(wt(1, w_, 0.0)); self.ev("tick"); show(c1[i_], 0.22)
        turn(2); c2 = chips(["Learn", "Play", "Practise", "Check", "Exam"], 40, [NV, NV, NV, NV, OR_])
        for i_, w_ in enumerate([2, 3, 7, 8, 10]): self.until(wt(2, w_, 0.0)); self.ev("tick"); show(c2[i_], 0.2)
        turn(3); c3 = chips(["Web", "Android app", "Ask Dayzi · AI mentor"], 38, [NV, NV, TL])
        for i_, w_ in enumerate([2, 4, 7]): self.until(wt(3, w_, 0.0)); self.ev("tick"); show(c3[i_], 0.22)
        turn(4); c4 = chips(["Prerequisite", "Easy", "Medium", "Hard", "Challenge", "Mock test"], 36, [NV] * 5 + [OR_], cols=3)
        self.until(wt(4, 0, 0.0)); self.ev("tick")
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.06) for c_ in c4[:5]], lag_ratio=0.15), run_time=0.7); live.extend(c4[:5])
        self.until(wt(4, 8, 0.0)); self.ev("stamp"); show(c4[5])
        turn(5); self.until(wt(5, 1, 0.0)); self.ev("tick"); show(chips(["All 14 JEE Main units"], 46))
        turn(6); c6 = chips(["Chapter 1: Free", "More from ₹99/month"], 44, [TL, OR_])
        self.until(wt(6, 3, 0.0)); self.ev("tick"); show(c6[0]); self.until(wt(6, 5, 0.0)); self.ev("stamp"); show(c6[1])
        turn(7); c7 = chips(["1 · Open Chapter 1", "2 · Try the lab", "3 · Pick a plan"], 36, [NV, NV, OR_])
        for i_, w_ in enumerate([4, 7, 10]): self.until(wt(7, w_, 0.0)); self.ev("tick"); show(c7[i_], 0.22)
        turn(8); site = chips(["tutorda.org"], 56, [OR_]); show(site)
        FY = next((y for y in range(900, 1560, 5) if Y(y) + px(85) < site.get_bottom()[1] - px(24)), 1500)
        self.until(C[8] + 1.15); self.ev("tick")
        follow_card(self, P, FY, sub="JEE Main maths, made clear")
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))
