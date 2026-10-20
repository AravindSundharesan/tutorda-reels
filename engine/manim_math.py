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
    SERIES = "JEE in 20s · #5"
    def options_row(self, vals, y, tex=True):
        row = VGroup()
        for L, v in zip("ABCD", vals):
            c_ = RoundedRectangle(width=px(200), height=px(104), corner_radius=0.14, fill_color=WHITE_, fill_opacity=1, stroke_color=RULE, stroke_width=3)
            t_ = VGroup(B(L, 34, OR, SEMIBOLD), (M(v, 52) if tex else H(v, 48, INK))).arrange(RIGHT, buff=0.25).move_to(c_)
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
    EVENTS = "cubic"; SERIES = "JEE in 20s · #5"
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
        fw = self.comment_chip("Follow for #6"); fw[0].set_fill(OR)
        self.until(wt(5, 3, 0.1) if len(K.WT) > 5 else C[5] + 1.0); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(eq, a_, ax, g, v1, v2, xl, p1, l1, a1, p2, l2, a2, *rd, fw, lb)


class Area(ShortReel):
    EVENTS = "area"; SERIES = "JEE in 20s · #6"
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
        fw = self.comment_chip("Follow for #7"); fw[0].set_fill(OR)
        self.until(C[4] + 1.1); self.play(FadeIn(fw, shift=UP * 0.15), run_time=0.25)
        self.brand_flash(it, a_, ax, sq, g, area, gl, tl, fw, lb)
