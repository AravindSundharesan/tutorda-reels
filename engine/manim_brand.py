"""TutorDA brand reel v2: dark brand look (navy + orange/gold, Orbitron display, Poppins body),
generated photo plates (Z-Image-Turbo, assets/gen), vector product UI (chat, exam, maths card), footer captions.
Render: tools/manim_build.sh engine/manim_brand.py Brand intro2 out/brand.mp4 [draft]"""
import os, sys, math
import numpy as np
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
from manim_common import *          # config, CRF patch, px/X/Y, baseline, ReelScene
import intro2 as K
import manimpango

GEN, SITE = os.path.join(KIT, "assets", "gen"), os.path.join(KIT, "assets", "site")
LOGO_PNG = os.path.join(SITE, "tutorda_logomoodle.png")      # the brand mark (the only brand asset used)
manimpango.register_font(os.path.join(KIT, "assets", "fonts", "Orbitron.ttf"))
config.background_color = "#0D0D1A"
BG, SURF, SURF2, LINE_C = "#0D0D1A", "#161630", "#1F1F3D", "#2E2E55"
TXT, MUTED = "#E8E8FF", "#A3A8CC"
OR, GOLD, INKD = "#FF8C00", "#FFD700", "#1A1000"
GREEN = "#22C55E"
GRAD = ("#FFFFFF", OR, GOLD)        # the brand's heading gradient

def D(s, size, grad=True, color=TXT):
    t = Text(s, font="Orbitron", weight=ULTRABOLD, font_size=size * 0.6, color=color)
    return t.set_color_by_gradient(*GRAD) if grad else t
def P(s, size, color=TXT, weight=BOLD):
    return Text(s, font="Poppins", weight=weight, color=color, font_size=size * 0.6)
def plate(name):
    return ImageMobject(os.path.join(GEN, name + "_plate.jpg")).set_height(16).move_to(ORIGIN)
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
def glow(r, y, op=0.10, c=OR):
    """Soft radial light (a smooth gradient image, not stacked circles)."""
    g = ImageMobject(os.path.join(SITE, "glow_blue.png" if c != OR else "glow_or.png")).set_height(2 * r).move_to([0, Y(y), 0])
    return g

class Phone(Group):
    """Phone frame (assets/site/phone_frame.png, drawn by us) around a vector screen."""
    SW, SH = 556, 1176
    def __init__(self, center, scale=1.0):
        self.screen = RoundedRectangle(width=px(self.SW), height=px(self.SH), corner_radius=px(56), fill_color="#10102A", fill_opacity=1, stroke_width=0)
        self.frame = ImageMobject(os.path.join(SITE, "phone_frame.png")).set_height(px(1220)).set_z_index(3)
        super().__init__(self.screen, self.frame); self.scale(scale).move_to(center); self.k = scale
    def top(self): return self.screen.get_top()[1]
    def p(self, v): return px(v) * self.k        # screen pixels -> scene units

class Brand(ReelScene):
    K = K
    def kb(self, m, t0, t1, s0=1.0, s1=1.07, drift=(0, 0)):
        base_h, c0 = m.height, m.get_center().copy()
        def upd(mm):
            u = min(1, max(0, (self.renderer.time - t0) / (t1 - t0)))
            mm.set_height(base_h * (s0 + (s1 - s0) * u)); mm.move_to(c0 + np.array([drift[0] * u, drift[1] * u, 0]))
        m.add_updater(upd); return m

    def captions(self):
        """Footer captions: white Poppins Bold over the bottom scrim, the current word in gold."""
        now = lambda: self.renderer.time; caps = []
        for i in range(len(K.CLIPS) - 1):
            cap = K.CLIPS[i][2]; lines = [l.split() for l in cap.split("|")]
            words = [w for l in lines for w in l]; line_txt = [" ".join(l) for l in lines]; spans = []
            for li, l in enumerate(lines):
                c = 0
                for w_ in l: spans.append((li, c, c + len(w_))); c += len(w_) + 1
            def make(k, lines=lines, line_txt=line_txt, spans=spans):
                rows = VGroup(*[Text(line_txt[li], font="Poppins", weight=BOLD, color=WHITE, font_size=46 * 0.6,
                                     t2c=({f"[{spans[k][1]}:{spans[k][2]}]": GOLD} if k >= 0 and spans[k][0] == li else {}))
                                for li in range(len(lines))])
                for li, r in enumerate(rows): r.shift(UP * (-li * px(62) - baseline(r)))
                return rows.move_to([0, Y(1772) + rows.height / 2, 0])
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
        C, wt, S = K.C, K.wt, [c - 0.25 for c in K.C]
        scrim = ImageMobject(os.path.join(SITE, "scrim.png")).set_height(16).set_z_index(5)
        logo = ImageMobject(LOGO_PNG).set_height(px(66)).move_to([0, Y(120), 0]).set_z_index(10)
        prog = always_redraw(lambda: Line([-4.5, 7.97, 0], [-4.5 + 9 * min(1, max(0.001, self.renderer.time / K.DUR)), 7.97, 0],
                                          stroke_width=8, color=OR).set_z_index(10))
        self.add(scrim, logo, prog); self.captions()

        # ===== 1. HOOK: Boards. JEE. NEET. IELTS. Still juggling five apps? =====
        bg = self.kb(plate("hook"), 0, S[1], 1.0, 1.09, drift=(0, 0.15)).set_z_index(-10); self.add(bg)
        words = [D(w, 128) for w in ("BOARDS", "JEE", "NEET", "IELTS")]
        for w, y in zip(words, (560, 720, 880, 1040)): w.move_to([0, Y(y), 0])
        self.add(words[0])                                   # frame 0 already reads
        for k in (1, 2, 3):
            self.until(wt(0, k, 0.06)); self.play(FadeIn(words[k], scale=1.35), run_time=0.16, rate_func=rush_from)
        apps = D("5 APPS?", 104, grad=False, color=GOLD).move_to([0, Y(1250), 0])
        self.until(wt(0, 5, 0.1))
        self.play(*[w.animate(rate_func=there_and_back).shift(UP * 0.18 * (1 if j % 2 else -1)).rotate(0.06 * (1 if j % 2 else -1))
                    for j, w in enumerate(words)], run_time=0.45)
        self.until(wt(0, 6, 0.08)); self.play(FadeIn(apps, scale=1.3), run_time=0.2, rate_func=rush_from)

        # ===== 2. TutorDA puts it all in one place (brand moment on the dark ground) =====
        self.until(S[1])
        big = ImageMobject(LOGO_PNG).set_width(px(780)).move_to([0, Y(760), 0])
        g1 = glow(4.6, 760, 0.16)
        self.play(*[w.animate.scale(0.12).move_to([0, Y(760), 0]).set_opacity(0) for w in words], FadeOut(apps, scale=0.5),
                  FadeOut(bg), run_time=0.35, rate_func=rush_into)
        bg.clear_updaters(); self.remove(bg)
        self.play(FadeIn(g1, scale=0.6), FadeIn(big, scale=0.7), run_time=0.35, rate_func=rush_from)
        pills = VGroup(*[chip(s, 40, TXT, SURF2, stroke=LINE_C) for s in ("Maths", "Science", "Exams", "English")]).arrange(RIGHT, buff=0.16).move_to([0, Y(930), 0])
        self.until(wt(1, 3, 0.1)); self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in pills], lag_ratio=0.15), run_time=0.45)

        # ===== 3. Live classes and interactive courses for Class 10 to 12 =====
        self.until(S[2])
        bg = self.kb(plate("teacher"), S[2], S[3], 1.0, 1.06, drift=(-0.2, 0)).set_z_index(-10)
        self.play(FadeOut(Group(big, pills, g1)), FadeIn(bg), run_time=0.3)
        dot = Dot(radius=px(13), color="#FF3B3B")
        live = VGroup(RoundedRectangle(width=px(190), height=px(64), corner_radius=px(32), fill_color=BG, fill_opacity=0.85, stroke_width=0),
                      VGroup(dot, P("LIVE", 34, WHITE)).arrange(RIGHT, buff=0.14)).move_to([X(150), Y(290), 0])
        live[1].move_to(live[0])
        self.until(wt(2, 0, 0.05)); self.play(FadeIn(live, shift=RIGHT * 0.2), run_time=0.25)
        dot.add_updater(lambda d: d.set_opacity(0.35 + 0.65 * (0.5 + 0.5 * math.cos(self.renderer.time * 7))))
        cc = RoundedRectangle(width=px(840), height=px(300), corner_radius=0.3, fill_color=BG, fill_opacity=0.88, stroke_color=LINE_C, stroke_width=2).move_to([0, Y(1230), 0])
        ct = D("INTERACTIVE COURSES", 44).move_to(cc.get_top() + DOWN * px(62))
        subj = VGroup(*[chip(s, 36, TXT, SURF2) for s in ("Maths", "Physics", "Chemistry")]).arrange(RIGHT, buff=0.16).move_to(cc.get_center() + DOWN * px(5))
        bar_bg = RoundedRectangle(width=px(720), height=px(16), corner_radius=px(8), fill_color=SURF2, fill_opacity=1, stroke_width=0).move_to(cc.get_bottom() + UP * px(55))
        prog_v = ValueTracker(0.03)
        bar = always_redraw(lambda: RoundedRectangle(width=px(720) * prog_v.get_value(), height=px(16), corner_radius=px(8), fill_opacity=1, stroke_width=0)
                            .set_fill(color=[OR, GOLD]).move_to(bar_bg.get_left(), aligned_edge=LEFT))
        self.until(wt(2, 3, 0.12)); self.play(FadeIn(VGroup(cc, ct, subj, bar_bg), shift=UP * 0.4), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.add(bar); self.play(prog_v.animate.set_value(0.64), run_time=0.8, rate_func=smooth)
        cls = VGroup(*[chip(f"Class {n}", 42, INKD, GOLD) for n in (10, 11, 12)]).arrange(RIGHT, buff=0.2).move_to([0, Y(1000), 0])
        self.until(wt(2, 7, 0.1)); self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cls], lag_ratio=0.35), run_time=0.5, rate_func=rate_functions.ease_out_back)

        # ===== 4. Practice that adapts to your level, with step-by-step solutions =====
        self.until(S[3])
        dot.clear_updaters(); bar.clear_updaters()
        self.play(FadeOut(Group(cc, ct, subj, bar_bg, bar, cls, live), shift=LEFT * 0.4), FadeOut(bg), run_time=0.3)
        bg.clear_updaters(); self.remove(bg)
        g2 = glow(4.4, 560, 0.12)
        card = RoundedRectangle(width=px(900), height=px(840), corner_radius=0.35, fill_color=SURF, fill_opacity=1,
                                stroke_color=LINE_C, stroke_width=2.5).move_to([0, Y(860), 0])
        head = Text("ADAPTIVE PRACTICE", font="Orbitron", weight=ULTRABOLD, font_size=34 * 0.6, color=OR).move_to([X(310), Y(500), 0])
        q = VGroup(P("Solve", 48, MUTED, MEDIUM), MathTex(r"2x+3=11", color=WHITE, font_size=72 * 0.8)).arrange(RIGHT, buff=0.3).move_to([0, Y(610), 0])
        segs = VGroup(*[RoundedRectangle(width=px(250), height=px(58), corner_radius=px(29), fill_color=SURF2, fill_opacity=1, stroke_width=0) for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to([0, Y(740), 0])
        segl = VGroup(*[P(s, 32, MUTED).move_to(g) for s, g in zip(("Easy", "Medium", "Hard"), segs)]).set_z_index(2)
        for l in segl: l.align_to(segl[1], UP)
        hi = segs[0].copy().set_fill(OR, 1).set_z_index(1); segl[0].set_color(INKD)
        self.play(FadeIn(g2), FadeIn(card, shift=UP * 0.3), FadeIn(head), FadeIn(q), FadeIn(segs), FadeIn(hi), FadeIn(segl), run_time=0.4)
        self.until(wt(3, 2, 0.1))
        self.play(hi.animate.move_to(segs[1]), segl[0].animate.set_color(MUTED), segl[1].animate.set_color(INKD), run_time=0.4, rate_func=smooth)
        sol = VGroup(*[MathTex(a, "=", b, color=c, font_size=f * 0.8) for a, b, c, f in
                       (("2x", "11-3", TXT, 70), ("2x", "8", TXT, 70), ("x", "4", GOLD, 84))]).arrange(DOWN, buff=0.42)
        for e in sol: e.shift(RIGHT * (X(560) - e[1].get_center()[0]))
        sol.shift(UP * (Y(1010) - sol.get_center()[1]))
        nums = VGroup(*[P(f"Step {i + 1}", 34, OR) for i in range(3)])
        for n, e in zip(nums, sol): n.move_to([0, e[1].get_center()[1], 0]).align_to([X(170), 0, 0], LEFT)
        self.until(wt(3, 7, 0.15))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(n), Write(s)) for n, s in zip(nums, sol)], lag_ratio=0.4), run_time=0.9)
        ok = VGroup(Circle(radius=0.3, fill_color=GREEN, fill_opacity=1, stroke_width=0),
                    VMobject(stroke_color=WHITE, stroke_width=8).set_points_as_corners([[-0.12, 0, 0], [-0.03, -0.1, 0], [0.14, 0.11, 0]])).next_to(sol[2], RIGHT, buff=0.35)
        self.play(FadeIn(ok, scale=0.5), run_time=0.25, rate_func=rate_functions.ease_out_back)

        # ===== 5. Stuck at midnight? Ask the AI tutor. It clears your doubts, 24/7 (our own chat UI) =====
        self.until(S[4])
        self.play(FadeOut(Group(card, head, q, segs, segl, hi, sol, nums, ok, g2), shift=UP * 0.3), run_time=0.3)
        night = glow(5.0, 700, 0.16, "#3B4CCA")
        moon = Difference(Circle(radius=0.42), Circle(radius=0.38).shift(RIGHT * 0.22 + UP * 0.12),
                          fill_color="#F4F1DE", fill_opacity=1, stroke_width=0).move_to([X(900), Y(330), 0])
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
        qtxt = VGroup(P("How do I solve", 40, INKD), MathTex(r"x^2-5x+6=0\,?", color=INKD, font_size=48 * 0.8)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        b1 = bubble(qtxt, True, sep.get_y() - ph.p(40))
        ans = VGroup(P("Factorise it:", 38, TXT, MEDIUM), MathTex(r"(x-2)(x-3)=0", color=TXT, font_size=48 * 0.8),
                     VGroup(P("So", 38, TXT, MEDIUM), MathTex(r"x=2 \text{ or } 3", color=GOLD, font_size=48 * 0.8)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        b2 = bubble(ans, False, b1.get_bottom()[1] - ph.p(30))
        typing = bubble(VGroup(*[Dot(radius=ph.p(9), color=MUTED) for _ in range(3)]).arrange(RIGHT, buff=ph.p(12)), False, b1.get_bottom()[1] - ph.p(30))
        for k, d_ in enumerate(typing[1]): d_.add_updater(lambda m, k=k: m.set_opacity(0.3 + 0.7 * max(0, math.sin(self.renderer.time * 8 - k))))
        inp = RoundedRectangle(width=ph.screen.width - ph.p(70), height=ph.p(84), corner_radius=ph.p(42), fill_color=SURF2, fill_opacity=1, stroke_width=0).move_to([0, ph.screen.get_bottom()[1] + ph.p(90), 0])
        inpt = P("Ask a doubt…", 32, MUTED, MEDIUM).move_to(inp).align_to(inp.get_left() + RIGHT * ph.p(36), LEFT)
        snd = Circle(radius=ph.p(30), fill_color=OR, fill_opacity=1, stroke_width=0).move_to(inp.get_right() + LEFT * ph.p(50))
        self.play(FadeIn(night), FadeIn(moon), FadeIn(clock, shift=DOWN * 0.2), FadeIn(ph, shift=UP * 0.8), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.add(av, avf, name, sep, inp, inpt, snd)
        self.until(wt(4, 3, 0.1)); self.play(FadeIn(b1, shift=UP * 0.25), run_time=0.25)
        self.add(typing)
        self.until(wt(4, 8, 0.15)); self.remove(typing)
        for d_ in typing[1]: d_.clear_updaters()
        self.play(FadeIn(b2, shift=UP * 0.25), run_time=0.3)
        tf = D("24/7", 200).move_to([0, Y(330), 0])
        self.until(wt(4, 11, 0.12)); self.play(FadeOut(clock, scale=0.7), FadeIn(tf, scale=1.3), run_time=0.3, rate_func=rush_from)

        # ===== 6. Real exam-pattern mock tests for JEE, NEET, GATE and IELTS. Your first mock is free (our own exam UI) =====
        self.until(S[5])
        chat = Group(ph, av, avf, name, sep, b1, b2, inp, inpt, snd)
        self.play(FadeOut(Group(night, moon, tf)), chat.animate.shift(LEFT * 9.5), run_time=0.35, rate_func=rush_into)
        self.remove(chat)
        g3 = glow(4.6, 900, 0.12)
        ex = Phone([0, Y(960), 0], 1.0)
        L, R_, T0 = ex.screen.get_left()[0] + ex.p(36), ex.screen.get_right()[0] - ex.p(36), ex.top() - ex.p(110)
        title = VGroup(P("JEE Main", 40, TXT), P("· Mock 1", 40, OR)).arrange(RIGHT, buff=0.12).move_to([0, T0, 0]).align_to([L, 0, 0], LEFT)
        def clock_txt():
            s = max(0, int(3 * 3600 - max(0, self.renderer.time - C[5]) * 37))
            return P(f"Time left  {s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}", 30, GOLD, MEDIUM).move_to([0, T0 - ex.p(58), 0]).align_to([L, 0, 0], LEFT)
        timer = always_redraw(clock_txt)
        qcard = RoundedRectangle(width=R_ - L, height=ex.p(520), corner_radius=ex.p(28), fill_color=SURF, fill_opacity=1, stroke_width=0).move_to([0, T0 - ex.p(390), 0])
        qh = VGroup(P("Question 12", 30, MUTED, MEDIUM), P("+4  /  −1", 28, GREEN, MEDIUM)).arrange(RIGHT, buff=0.5).move_to(qcard.get_top() + DOWN * ex.p(50))
        qq = VGroup(P("If", 34, TXT, MEDIUM), MathTex(r"f(x)=x^3,", color=TXT, font_size=42 * 0.8), P("find", 34, TXT, MEDIUM), MathTex(r"f'(2)", color=TXT, font_size=42 * 0.8)).arrange(RIGHT, buff=0.12).move_to(qcard.get_top() + DOWN * ex.p(130))
        opts = VGroup()
        for k, v in enumerate(("6", "8", "12", "16")):
            r = RoundedRectangle(width=(R_ - L - ex.p(70)) / 2, height=ex.p(84), corner_radius=ex.p(20), fill_color=SURF2, fill_opacity=1, stroke_color=LINE_C, stroke_width=2)
            opts.add(VGroup(r, VGroup(P("ABCD"[k], 30, MUTED), MathTex(v, color=TXT, font_size=40 * 0.8)).arrange(RIGHT, buff=0.22).move_to(r)))
        opts.arrange_in_grid(rows=2, cols=2, buff=(ex.p(22), ex.p(22))).move_to(qcard.get_center() + DOWN * ex.p(70))
        pal = VGroup(*[RoundedRectangle(width=ex.p(66), height=ex.p(66), corner_radius=ex.p(14), fill_color=SURF2, fill_opacity=1, stroke_width=0) for _ in range(30)])
        pal.arrange_in_grid(rows=5, cols=6, buff=ex.p(16)).next_to(qcard, DOWN, buff=ex.p(40))
        pn = VGroup(*[P(str(i + 1), 24, MUTED, MEDIUM).move_to(b) for i, b in enumerate(pal)]).set_z_index(2)
        self.play(FadeIn(g3), FadeIn(ex, shift=UP * 1.0), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.add(title, timer); self.play(FadeIn(VGroup(qcard, qh, qq, opts, pal, pn)), run_time=0.3)
        rng = np.random.default_rng(3); state = [GREEN if rng.random() < 0.75 else OR for _ in range(11)]
        self.play(LaggedStart(*[pal[i].animate.set_fill(state[i]) for i in range(11)], lag_ratio=0.25), run_time=1.0)
        self.play(opts[2][0].animate.set_fill(OR, 0.25).set_stroke(OR, 3), pal[11].animate.set_fill(GREEN), run_time=0.3)   # f'(2) = 3*2^2 = 12 -> C
        ex_c = [chip(s, 44, INKD, GOLD) for s in ("JEE", "NEET", "GATE", "IELTS")]
        for c_, (x, y) in zip(ex_c, ((150, 420), (930, 560), (150, 1300), (930, 1420))): c_.move_to([X(x), Y(y), 0]).set_z_index(6)
        for c_, wi in zip(ex_c, (5, 6, 7, 9)):
            self.until(wt(5, wi, 0.1)); self.play(FadeIn(c_, scale=0.6), run_time=0.22, rate_func=rate_functions.ease_out_back)
        free = glow_pill("MOCK 1  ·  FREE", 66).rotate(0.06).move_to([0, Y(1500), 0]).set_z_index(8)
        self.until(wt(5, 14, 0.1)); self.play(FadeIn(free, scale=1.6), run_time=0.3, rate_func=rush_from)

        # ===== 7. And free maths games and tools, free forever =====
        self.until(S[6])
        timer.clear_updaters()
        self.play(FadeOut(Group(ex, title, timer, qcard, qh, qq, opts, pal, pn, *ex_c, free, g3), shift=UP * 0.4), run_time=0.3)
        g4 = glow(4.6, 760, 0.12)
        g1n = ("Math Sprint", "Algebra Escape", "Times Table Blitz", "Prime Hunter", "Fraction Duel", "Sudoku", "Chess", "Number Quest")
        g2n = ("Graph Plotter", "Matrix Calculator", "Unit Converter", "Statistics Calculator", "Worksheet Generator")
        row1 = VGroup(*[chip(s, 42, TXT, SURF2, stroke=LINE_C) for s in g1n * 2]).arrange(RIGHT, buff=0.22).move_to([2.0, Y(640), 0])
        row2 = VGroup(*[chip(s, 42, INKD, GOLD) for s in g2n * 2]).arrange(RIGHT, buff=0.22).move_to([-2.0, Y(900), 0])
        lab1 = D("GAMES", 64).move_to([X(250), Y(530), 0]); lab2 = D("TOOLS", 64).move_to([X(250), Y(790), 0])
        row1.add_updater(lambda m, dt: m.shift(LEFT * 1.6 * dt)); row2.add_updater(lambda m, dt: m.shift(RIGHT * 1.6 * dt))
        self.add(g4)
        self.until(wt(6, 2, 0.1)); self.play(FadeIn(lab1), FadeIn(row1), run_time=0.3)
        self.until(wt(6, 4, 0.1)); self.play(FadeIn(lab2), FadeIn(row2), run_time=0.3)
        ff = D("FREE FOREVER", 92).move_to([0, Y(1180), 0])
        self.until(wt(6, 6, 0.1)); self.play(FadeIn(ff, scale=1.3), run_time=0.3, rate_func=rush_from)

        # ===== 8. Start free today at tutorda.org =====
        self.until(S[7])
        bg = self.kb(plate("calm"), S[7], S[8], 1.0, 1.06).set_z_index(-10)
        self.play(FadeOut(Group(row1, row2, lab1, lab2, ff, g4)), FadeIn(bg), run_time=0.3); row1.clear_updaters(); row2.clear_updaters()
        s1 = D("START FREE", 120).move_to([0, Y(1110), 0]); s2 = D("TODAY", 120).move_to([0, Y(1255), 0])
        site = glow_pill("tutorda.org", 86).move_to([0, Y(1440), 0])
        self.play(FadeIn(s1, shift=UP * 0.3), run_time=0.3)
        self.until(wt(7, 2, 0.1)); self.play(FadeIn(s2, shift=UP * 0.3), run_time=0.25)
        self.until(wt(7, 4, 0.2)); self.play(FadeIn(site, scale=0.7), run_time=0.3, rate_func=rate_functions.ease_out_back)
        self.play(ShowPassingFlash(site[0].copy().set_fill(opacity=0).set_stroke(WHITE, 8), time_width=0.5), run_time=0.6)

        # ===== END CARD =====
        self.until(S[8])
        self.play(FadeOut(Group(s1, s2, site)), FadeOut(bg), FadeOut(logo), run_time=0.3); bg.clear_updaters()
        big = ImageMobject(LOGO_PNG).set_width(px(820)).move_to([0, Y(800), 0])
        g5 = glow(4.6, 800, 0.14)
        f1 = D("FOLLOW TUTORDA", 64).move_to([0, Y(1010), 0])
        f2 = glow_pill("tutorda.org", 60).move_to([0, Y(1150), 0])
        self.play(FadeIn(g5), FadeIn(big, scale=0.85), run_time=0.4, rate_func=rush_from)
        self.play(LaggedStart(FadeIn(f1, shift=UP * 0.15), FadeIn(f2, scale=0.9), lag_ratio=0.3), run_time=0.5)
        self.until(K.DUR)
