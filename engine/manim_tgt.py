"""Two targeted 30 s reels in the brand-film system: Jee (JEE Main aspirants) and Csir (CSIR-NET Mathematical Sciences).
Structure: the student's real problem -> what other mock tests stop at -> Dynamic Assessment (the difference) -> what it
does for you -> the exam's own mocks (verified pattern, Mock 1 free) -> support (worked solutions, AI tutor 24/7, live) -> end.
Render: FILM_AUDIO=aud_jee tools/manim_build.sh engine/manim_tgt.py Jee aud_jee out/jee.mp4 [draft]
        FILM_AUDIO=aud_csir tools/manim_build.sh engine/manim_tgt.py Csir aud_csir out/csir.mp4 [draft]"""
import os, sys, json, math
ENGINE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENGINE)
from manim_film2 import *
import manim_film2 as F


class Tgt(F.Film2):
    EVENTS = "tgt"

    def setup_common(self):
        self.Tm = lambda: self.renderer.time
        self._ground = Rectangle(width=9.2, height=16.4, fill_color=PAPER, fill_opacity=1, stroke_width=0).set_z_index(-20); self.add(self._ground)
        self.captions()
        self.hdr = wordmark(px(250)); left(self.hdr.move_to([0, Y(118), 0])); self.hdr.set_z_index(12)
        self.hdr_d = wordmark(px(250), dark=True); left(self.hdr_d.move_to([0, Y(118), 0])); self.hdr_d.set_z_index(12)
        self.S = [c - 0.25 for c in K.C]

    def to(self, color, *gone):
        """Wipe to a new ground and put the right header back."""
        self.ground(color, UP, 0.38)
        self.remove(*gone)
        self.add(self.hdr_d if color == INK else self.hdr)

    def label(self, s, dark):
        g = B(s, 40, OR, SEMIBOLD); g.move_to([0, Y(118), 0]).align_to([X(984), 0, 0], RIGHT); g.set_z_index(12)
        return g

    # ---------- Dynamic Assessment (ink): question card + accuracy / time / confidence tiles ----------
    def da(self, i, qlabel, qmath, ans, w_title, w_acc, w_time, w_conf, secs):
        wt = K.wt
        dy = Text("Dynamic", font="Poppins", weight=ULTRABOLD, color=WHITE_, font_size=110 * 0.6); dy[0].set_color(OR)
        asm = Text("Assessment", font="Poppins", weight=ULTRABOLD, color=WHITE_, font_size=110 * 0.6); asm[0].set_color(OR)
        at(dy, 300); at(asm, 430)
        qc = card(888, 270, WHITE_); left(qc.move_to([0, Y(700), 0]))
        ql = B(qlabel, 30, GREY_P, SEMIBOLD); left(ql.move_to([0, Y(615), 0]), 140)
        qm = qmath; left(qm.move_to([0, Y(720), 0]), 140)
        tiles = VGroup(*[card(280, 210, INK2) for _ in range(3)]).arrange(RIGHT, buff=px(24)); left(tiles.move_to([0, Y(985), 0]))
        tl = [B(s, 28, GREY_I, SEMIBOLD) for s in ("Accuracy", "Time", "Confidence")]
        for t_, c_ in zip(tl, tiles): t_.move_to(c_.get_top() + DOWN * px(44)).align_to(c_.get_left() + RIGHT * px(30), LEFT)
        acc = VGroup(ans, tick(0.17)).arrange(RIGHT, buff=0.2)
        acc.move_to(tiles[0].get_center() + DOWN * px(25)).align_to(tiles[0].get_left() + RIGHT * px(30), LEFT)
        tv = ValueTracker(0); tm = H("0:00", 72, WHITE_)
        def _tm(m):
            m.become(H(f"0:{int(tv.get_value()):02d}", 72, WHITE_)); m.move_to(tiles[1].get_center() + DOWN * px(28)).align_to(tiles[1].get_left() + RIGHT * px(30), LEFT)
        tm.add_updater(_tm); _tm(tm)
        cbg = RoundedRectangle(width=px(220), height=px(14), corner_radius=px(7), fill_color=INK3, fill_opacity=1, stroke_width=0)
        cbg.move_to(tiles[2].get_center() + DOWN * px(30)).align_to(tiles[2].get_left() + RIGHT * px(30), LEFT).set_z_index(2)
        cf = cbg.copy().set_fill(OR, 1).set_z_index(3); cf.stretch_to_fit_width(px(6)); cf.align_to(cbg, LEFT)
        if w_title == 0:
            self.play(FadeIn(Group(qc, ql, qm), shift=UP * 0.3), FadeIn(dy, shift=UP * 0.3), FadeIn(asm, shift=UP * 0.3), run_time=0.35, rate_func=EXPO)
        else:
            self.play(FadeIn(Group(qc, ql, qm), shift=UP * 0.3), run_time=0.3, rate_func=EXPO)
            self.until(wt(i, w_title, 0.1)); self.rise(dy, asm, rt=0.4, lag=0.15)
        self.until(wt(i, w_acc, 0.1)); self.ev("tick"); self.play(*[FadeIn(m, shift=UP * 0.3) for m in (tiles[0], tl[0], acc)], run_time=0.28, rate_func=EXPO)
        self.until(wt(i, w_time, 0.1)); self.ev("tick"); self.play(FadeIn(tiles[1], shift=UP * 0.3), FadeIn(tl[1], shift=UP * 0.3), run_time=0.2, rate_func=EXPO)
        self.add(tm); self.play(tv.animate.set_value(secs), run_time=0.3)
        self.until(wt(i, w_conf, 0.1)); self.ev("tick"); self.play(FadeIn(tiles[2], shift=UP * 0.3), FadeIn(tl[2], shift=UP * 0.3), run_time=0.2, rate_func=EXPO)
        self.add(cbg, cf); self.play(cf.animate.stretch_to_fit_width(px(176)).align_to(cbg, LEFT), run_time=0.3)
        tm.clear_updaters()
        return [dy, asm, qc, ql, qm, tiles, *tl, acc, tm, cbg, cf]

    # ---------- topic map (paper): bars, one flagged ----------
    def topic_map(self, i, title, topics, w_show, w_flag, flag_text, next_text=None, w_next=None, strong_text=None, w_strong=None, next_label=None):
        wt = K.wt
        tt = at(H(title, 84, INK), 330)
        rows, flag = [], None
        for k, (sub, name, v, weak) in enumerate(topics):
            y = 540 + k * 205
            s_ = B(sub, 28, GREY_P, SEMIBOLD); left(s_.move_to([0, Y(y - 40), 0]))
            n_ = H(name, 46, INK, BOLD); left(n_.move_to([0, Y(y + 8), 0]))
            bb = RoundedRectangle(width=px(888), height=px(18), corner_radius=px(9), fill_color=PAPER2, fill_opacity=1, stroke_width=0); left(bb.move_to([0, Y(y + 62), 0]))
            bf = RoundedRectangle(width=px(888) * v, height=px(18), corner_radius=px(9), fill_color=OR if weak else INK, fill_opacity=1, stroke_width=0); left(bf.move_to([0, Y(y + 62), 0]))
            pc = B(f"{int(v * 100)}%", 30, OR if weak else GREY_P, SEMIBOLD); pc.move_to([0, Y(y + 8), 0]).align_to([X(984), 0, 0], RIGHT)
            rows.append(VGroup(s_, n_, bb, bf, pc))
            if weak: flag = (k, y)
        self.play(FadeIn(tt, shift=UP * 0.3), LaggedStart(*[AnimationGroup(FadeIn(r[0]), FadeIn(r[1]), FadeIn(r[2]), GrowFromEdge(r[3], LEFT), FadeIn(r[4])) for r in rows], lag_ratio=0.15), run_time=0.6, rate_func=EXPO)
        if strong_text:
            sts = []
            for k2, (sub, name, v, weak) in enumerate(topics):
                if weak: continue
                t2 = tag(strong_text, 30, WHITE_, INK); t2.move_to([0, Y(540 + k2 * 205 + 8), 0]).align_to([X(860), 0, 0], RIGHT); sts.append(t2)
            self.until(wt(i, w_strong, 0.1)); self.ev("tick"); self.play(LaggedStart(*[FadeIn(t2, shift=LEFT * 0.2) for t2 in sts], lag_ratio=0.2), run_time=0.35, rate_func=EXPO)
        else: sts = []
        k, y = flag
        tg = tag(flag_text, 30, WHITE_, OR); tg.move_to([0, Y(y + 8), 0]).align_to([X(860), 0, 0], RIGHT)
        self.until(wt(i, w_flag, 0.1)); self.ev("tick"); self.play(FadeIn(tg, shift=LEFT * 0.2), rows[k][1].animate.set_color(OR), run_time=0.3, rate_func=EXPO)
        extra = [tt, *rows, tg, *sts]
        if next_text:
            nx = VGroup(card(888, 150, INK), VGroup(B(next_label or ("Next question" if "Rotational" in next_text else "Practise next"), 30, GREY_I, SEMIBOLD), H(next_text, 46, WHITE_)).arrange(DOWN, buff=0.08, aligned_edge=LEFT))
            nx[1].move_to(nx[0]).align_to(nx[0].get_left() + RIGHT * px(40), LEFT); left(nx.move_to([0, Y(1340), 0]))
            arr = Text("→", font="Poppins", color=OR, font_size=60).move_to(nx[0].get_right() + LEFT * px(70))
            self.until(wt(i, w_next, 0.1)); self.play(FadeIn(nx, shift=UP * 0.3), FadeIn(arr, shift=RIGHT * 0.2), run_time=0.35, rate_func=EXPO)
            extra += [nx, arr]
        return extra

    # ---------- mock (ink): exam phone + facts column + Mock 1 free stamp ----------
    def mock(self, i, exam, pattern_lines, facts, w_free):
        wt = K.wt; T = self.Tm
        ex = Phone([X(300), Y(880), 0], 0.78, screen="#121A2E")
        L_, T0 = ex.screen.get_left()[0] + ex.p(36), ex.top() - ex.p(110)
        et = VGroup(B(exam, 38, WHITE_, SEMIBOLD), B("Mock 1", 38, OR, SEMIBOLD)).arrange(RIGHT, buff=0.12).move_to([0, T0, 0]).align_to([L_, 0, 0], LEFT)
        if et.width > ex.screen.width - ex.p(72): et.scale_to_fit_width(ex.screen.width - ex.p(72)).align_to([L_, 0, 0], LEFT)
        t_ex = self.renderer.time
        tmr = always_redraw(lambda: B("Time left  {:02d}:{:02d}:{:02d}".format(*(lambda s: (s // 3600, s % 3600 // 60, s % 60))(max(0, int(10800 - max(0, T() - t_ex) * 41)))), 30, GREY_I).move_to([0, T0 - ex.p(56), 0]).align_to([L_, 0, 0], LEFT))
        info = VGroup(*[B(s, 28, "#C9CFDD") for s in pattern_lines]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        info.next_to(tmr, DOWN, buff=0.3).align_to([L_, 0, 0], LEFT)
        pal = VGroup(*[RoundedRectangle(width=ex.p(66), height=ex.p(66), corner_radius=ex.p(12), fill_color="#222C45", fill_opacity=1, stroke_width=0) for _ in range(36)])
        pal.arrange_in_grid(rows=6, cols=6, buff=ex.p(16)).move_to([ex.screen.get_center()[0], ex.screen.get_center()[1] - ex.p(170), 0])
        mk = VGroup(RoundedRectangle(width=ex.p(200), height=ex.p(64), corner_radius=ex.p(14), fill_color="#7C3AED", fill_opacity=1, stroke_width=0), B("Review", 24, WHITE_, SEMIBOLD))
        mk[1].move_to(mk[0]); mk.move_to([ex.screen.get_center()[0], ex.screen.get_bottom()[1] + ex.p(90), 0])
        rng = np.random.default_rng(5)
        fills = [OR if rng.random() < 0.8 else "#7C3AED" for k in range(18)]
        col = []
        for k, (big, small, wi) in enumerate(facts):
            y = 470 + k * 190
            b_ = H(big, 50, WHITE_); b_.move_to([0, Y(y), 0]).align_to([X(590), 0, 0], LEFT)
            s_ = B(small, 28, GREY_I); s_.move_to([0, Y(y + 58), 0]).align_to([X(590), 0, 0], LEFT)
            if b_.width > px(394): b_.scale_to_fit_width(px(394)).align_to([X(590), 0, 0], LEFT)
            if s_.width > px(394): s_.scale_to_fit_width(px(394)).align_to([X(590), 0, 0], LEFT)
            rl = Line([X(590), Y(y + 110), 0], [X(984), Y(y + 110), 0], stroke_color=INK3, stroke_width=3)
            col.append((wi, VGroup(b_, s_, rl)))
        self.ev("tick")
        self.play(FadeIn(Group(ex, et, info, pal, mk), shift=UP * 0.5), FadeIn(col[0][1], shift=LEFT * 0.3), run_time=0.4, rate_func=EXPO)
        self.add(tmr)
        for n_, (wi, g) in enumerate(col[1:]):
            self.until(wt(i, wi, 0.1)); self.ev("tick")
            part = list(range(n_ * 9, min(18, n_ * 9 + 9)))
            anims = [FadeIn(g, shift=LEFT * 0.3)] + ([LaggedStart(*[pal[k].animate.set_fill(fills[k]) for k in part], lag_ratio=0.1)] if part else [])
            self.play(*anims, run_time=0.45, rate_func=EXPO)
        if w_free is None:
            return [ex, et, tmr, info, pal, mk, *[g for _, g in col]]
        stamp = VGroup(RoundedRectangle(width=px(400), height=px(150), corner_radius=0.2, fill_color=OR, fill_opacity=1, stroke_width=0), H("Mock 1 free", 56, WHITE_))
        stamp[1].move_to(stamp[0]); stamp.rotate(-4 * DEGREES).move_to([X(784), Y(1360), 0])
        self.until(wt(i, w_free, 0.12)); self.ev("stamp")
        self.play(GrowFromCenter(stamp), run_time=0.45, rate_func=rate_functions.ease_out_back)
        return [ex, et, tmr, info, pal, mk, stamp, *[g for _, g in col]]

    # ---------- support (paper): photo strip + three rows ----------
    def support(self, i, photo_name, fy, w_rows):
        wt = K.wt
        ph = photo(photo_name, "ed", 1080, 640, fy).move_to([0, Y(200 + 320), 0]).set_z_index(-5)
        items = (("Worked solutions", "for every question"), ("AI tutor", "doubts cleared 24/7"), ("Live classes", "with expert teachers"))
        rows = []
        for k, ((a, b), wi) in enumerate(zip(items, w_rows)):
            y = 960 + k * 190
            ta = H(a, 70, INK); left(ta.move_to([0, Y(y), 0]))
            tb = B(b, 34, GREY_P); left(tb.move_to([0, Y(y + 62), 0]))
            rl = Line([X(96), Y(y + 110), 0], [X(984), Y(y + 110), 0], stroke_color=RULE, stroke_width=3)
            rows.append((wi, VGroup(ta, tb, rl)))
        self.ev("tick")
        self.play(FadeIn(ph, shift=UP * 0.3), FadeIn(rows[0][1], shift=UP * 0.3), run_time=0.35, rate_func=EXPO)
        self.kb(ph, self.Tm(), self.S[i + 1], 1.0, 1.04)
        for wi, g in rows[1:]:
            self.until(wt(i, wi, 0.1)); self.ev("tick"); self.play(FadeIn(g, shift=UP * 0.3), run_time=0.3, rate_func=EXPO)
        return [ph, *[g for _, g in rows]]

    # ---------- AI tutor chat at midnight, then live class (ink -> photo) ----------
    def chat_live(self, i, q, steps, w_ans, w_live, live_word):
        wt = K.wt; T = self.Tm
        clock = at(H("11:58 pm", 110, WHITE_), 300)
        cc = card(888, 900, INK2); left(cc.move_to([0, Y(470 + 450), 0]))
        av = Circle(radius=px(30), fill_color=OR, fill_opacity=1, stroke_width=0).move_to([X(96 + 70), Y(540), 0])
        avt = B("AI", 26, WHITE_, SEMIBOLD).move_to(av)
        nm = VGroup(B("AI tutor", 34, WHITE_, SEMIBOLD), B("online", 24, "#4ADE80")).arrange(DOWN, buff=0.04, aligned_edge=LEFT).next_to(av, RIGHT, buff=0.18)
        qb_r = RoundedRectangle(width=q.width + px(60), height=q.height + px(44), corner_radius=px(28), fill_color=OR, fill_opacity=1, stroke_width=0)
        qb = VGroup(qb_r, q.move_to(qb_r)); qb.move_to([X(984) - qb_r.width / 2 - px(30), Y(680), 0])
        ans = VGroup(*steps).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        ab_r = RoundedRectangle(width=min(px(800), ans.width + px(60)), height=ans.height + px(50), corner_radius=px(28), fill_color="#222C45", fill_opacity=1, stroke_width=0)
        if ans.width > px(740): ans.scale_to_fit_width(px(740))
        ab = VGroup(ab_r, ans.move_to(ab_r)); ab.move_to([X(126) + ab_r.width / 2, qb.get_bottom()[1] - px(30) - ab_r.height / 2, 0])
        self.ev("tick")
        self.play(FadeIn(clock, shift=UP * 0.3), FadeIn(VGroup(cc, av, avt, nm), shift=UP * 0.4), FadeIn(qb, shift=UP * 0.2), run_time=0.4, rate_func=EXPO)
        self.until(wt(i, w_ans, 0.1)); self.ev("tick")
        self.play(FadeIn(ab_r), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ans], lag_ratio=0.2), run_time=0.7)
        tp = photo("teacher", "ed", 1080, BAND_TOP, 0.42).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        shade = Rectangle(width=9.2, height=px(560), fill_color=INK, fill_opacity=0.6, stroke_width=0).set_z_index(-4).move_to([0, Y(BAND_TOP) + px(280), 0])
        top_sh = Rectangle(width=9.2, height=px(230), fill_color=INK, fill_opacity=0.55, stroke_width=0).set_z_index(-4).move_to([0, Y(115), 0])
        rd = Dot(radius=px(12), color="#FF3B3B")
        live = VGroup(RoundedRectangle(width=px(176), height=px(60), corner_radius=0.12, fill_color=INK, fill_opacity=0.9, stroke_width=0), VGroup(rd, B("Live", 32, WHITE_, SEMIBOLD)).arrange(RIGHT, buff=0.14))
        live[1].move_to(live[0]); left(live.move_to([0, Y(270), 0]))
        g1 = at(H("Want a teacher?", 84, WHITE_), 1250); g2 = at(SER("Go live.", 150, "#FFB27A"), 1400)
        self.until(wt(i, w_live, 0.12)); self.ev("tick")
        self.play(FadeOut(VGroup(clock, cc, av, avt, nm, qb, ab), shift=UP * 0.3), FadeIn(tp), FadeIn(shade), FadeIn(top_sh), FadeIn(g1, shift=UP * 0.3), run_time=0.4, rate_func=EXPO)
        self.kb(tp, T(), self.S[i + 1], 1.0, 1.04)
        rd.add_updater(lambda d: d.set_opacity(0.35 + 0.65 * (0.5 + 0.5 * math.cos(T() * 7))))
        self.until(wt(i, live_word, 0.1)); self.rise(live, g2, rt=0.35, lag=0.1)
        return [tp, shade, top_sh, live, g1, g2, rd]

    # ---------- end card (ink) ----------
    def end(self, i, line):
        C = K.C
        wm2 = wordmark(px(860), dark=True).move_to([0, Y(600), 0])
        ln = B(line, 54, WHITE_, SEMIBOLD).move_to([0, Y(810), 0])
        self.ev("wordmark"); self.play(LaggedStart(FadeIn(wm2[:5], shift=UP * 0.4), FadeIn(wm2[5:], shift=DOWN * 0.4), FadeIn(ln, shift=UP * 0.3), lag_ratio=0.25), run_time=0.6, rate_func=EXPO)
        sf_ = B("Start free at", 46, GREY_I).move_to([0, Y(960), 0])
        url = H("tutorda.org", 120, OR).move_to([0, Y(1095), 0])
        ul = Line(url.get_corner(DL) + DOWN * 0.12, url.get_corner(DR) + DOWN * 0.12, stroke_color=OR, stroke_width=6)
        self.until(C[i] + 0.9); self.rise(sf_, rt=0.3)
        self.until(C[i] + 1.4); self.play(FadeIn(url, shift=UP * 0.3), Create(ul), run_time=0.4, rate_func=EXPO)
        self.until(K.DUR)
        json.dump(getattr(self, "_events", []), open(os.path.join(KIT, "out", f"{self.EVENTS}_events.json"), "w"))


class Jee(Tgt):
    EVENTS = "jee"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        # ===== 0. Two JEE aspirants. Same mock score. Different mistakes. (ink) — visible on frame 0 =====
        self._ground.set_fill(INK, 1); self.add(self.hdr_d)
        lb = self.label("JEE Main", True); self.add(lb)
        pa = photo("p1", "ed", 432, 700, 0.36).move_to([X(96 + 216), Y(250 + 350), 0])
        pb = photo("p2", "ed", 432, 700, 0.36).move_to([X(552 + 216), Y(250 + 350), 0])
        chips = []
        for x0 in (96, 552):
            c_ = VGroup(RoundedRectangle(width=px(432), height=px(110), corner_radius=0.14, fill_color=INK2, fill_opacity=1, stroke_width=0))
            l1 = B("Mock score", 28, GREY_I, SEMIBOLD); v1 = H("186 / 300", 50, WHITE_)
            g = VGroup(l1, v1).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to(c_).align_to(c_.get_left() + RIGHT * px(30), LEFT)
            chips.append(VGroup(c_, g).move_to([X(x0 + 216), Y(1030), 0]))
        self.add(pa, pb, chips[0], chips[1])
        self.kb(pa, 0, S[1], 1.0, 1.035); self.kb(pb, 0, S[1], 1.0, 1.035)
        tags = [tag("Rushed the numericals", 28, WHITE_, OR), tag("Unsure, so skipped", 28, WHITE_, OR)]
        for t_, x0 in zip(tags, (96, 552)): t_.move_to([0, Y(1150), 0]).align_to([X(x0), 0, 0], LEFT)
        dm = at(SER("different mistakes.", 120, OR), 1330)
        self.until(wt(0, 3, 0.1)); self.ev("tick"); self.play(*[Indicate(c[1][1], color=OR, scale_factor=1.06) for c in chips], run_time=0.4)
        self.until(wt(0, 6, 0.1)); self.ev("tick"); self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.2) for t_ in tags], lag_ratio=0.2), FadeIn(dm, shift=UP * 0.3), run_time=0.5, rate_func=EXPO)

        # ===== 1. Most mock tests stop at the score. (paper) =====
        self.until(S[1]); pa.clear_updaters(); pb.clear_updaters(); self.to(PAPER, pa, pb, *chips, *tags, dm, lb)
        mt = at(B("Most mock tests", 50, GREY_P, SEMIBOLD), 330)
        sc = card(888, 640, WHITE_); left(sc.move_to([0, Y(800), 0]))
        r1 = B("Result", 30, GREY_P, SEMIBOLD); left(r1.move_to([0, Y(560), 0]), 150)
        r2 = H("186 / 300", 130, INK); left(r2.move_to([0, Y(680), 0]), 150)
        sk = VGroup()
        for k, s_ in enumerate(("Why you lost marks", "What to practise next", "How you think")):
            y = 860 + k * 90
            t_ = B(s_, 32, "#B9B2A6"); left(t_.move_to([0, Y(y), 0]), 150)
            d_ = B("—", 32, "#B9B2A6"); d_.move_to([0, Y(y), 0]).align_to([X(930), 0, 0], RIGHT)
            sk.add(VGroup(t_, d_))
        self.rise(mt, rt=0.3); self.play(FadeIn(Group(sc, r1, r2), shift=UP * 0.3), run_time=0.35, rate_func=EXPO)
        stop = at(SER("stop at the score.", 128, OR), 1330)
        self.until(wt(1, 3, 0.1)); self.ev("stamp"); self.play(FadeIn(sk, shift=UP * 0.2), FadeIn(stop, shift=UP * 0.3), run_time=0.4, rate_func=EXPO)

        # ===== 2. Dynamic Assessment: how accurate, how fast, how sure (ink) =====
        self.until(S[2]); self.to(INK, mt, sc, r1, r2, sk, stop)
        da = self.da(2, "Question 12 · Mathematics", MathTex(r"\int_0^{\pi/2}\sin x\,dx", color=INK, font_size=64 * 0.8),
                     MathTex(r"=1", color=WHITE_, font_size=48 * 0.8), 1, 8, 10, 12, 38)

        # ===== 3. Your next question targets your weak topics (paper) =====
        self.until(S[3]); self.to(PAPER, *da)
        tm_ = self.topic_map(3, "Your topic map", (("Mathematics", "Definite integration", 0.82, False), ("Chemistry", "Chemical equilibrium", 0.64, False),
                                                    ("Physics", "Rotational motion", 0.31, True)), 0, 4, "Weak", "Rotational motion", 6)

        # ===== 4. Ten full JEE Main mocks, real interface, NTA marking. Mock 1 is free. (ink) =====
        self.until(S[4]); self.to(INK, *tm_)
        mk = self.mock(4, "JEE Main", ("75 questions · 3 h", "300 marks"),
                       (("Unlimited mocks", "JEE Main pattern", 0), ("Real exam interface", "palette, mark for review", 8), ("NTA marking", "+4 / −1, numericals too", 11)), 15)

        # ===== 5. Worked solutions, AI tutor 24/7, live classes (paper) =====
        self.until(S[5]); self.gone(mk[2]); self.to(PAPER, *mk)
        sp = self.support(5, "teacher", 0.42, (0, 3, 7))

        # ===== 6. End =====
        self.until(S[6]); self.to(INK, *sp); self.remove(self.hdr_d)
        self.end(6, "JEE Main mocks · Mock 1 free")


class Csir(Tgt):
    EVENTS = "csir"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        # ===== 0. CSIR-NET Maths. Attempt 60 out of 120. (paper) — headline on frame 0 =====
        self.add(self.hdr)
        lb = self.label("CSIR-NET", False); self.add(lb)
        h1 = at(H("CSIR-NET", 120, INK), 330); h2 = at(SER("Mathematical Sciences", 84, INK), 470)
        self.add(h1, h2)
        cols = []
        for k, (p, a, n) in enumerate((("Part A", 15, 20), ("Part B", 25, 40), ("Part C", 20, 60))):
            x0 = 96 + k * 304
            c_ = card(280, 380, WHITE_); c_.move_to([X(x0 + 140), Y(800), 0])
            pt = B(p, 32, GREY_P, SEMIBOLD); pt.move_to([0, Y(660), 0]).align_to([X(x0 + 30), 0, 0], LEFT)
            big = H(str(a), 120, INK); big.move_to([0, Y(800), 0]).align_to([X(x0 + 30), 0, 0], LEFT)
            of = B(f"attempt of {n}", 30, GREY_P); of.move_to([0, Y(920), 0]).align_to([X(x0 + 30), 0, 0], LEFT)
            cols.append(VGroup(c_, pt, big, of))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cols], lag_ratio=0.15), run_time=0.7, rate_func=EXPO)
        tot = VGroup(H("Attempt", 84, INK), H("60", 84, OR), H("of 120.", 84, INK)).arrange(RIGHT, buff=0.3); left(tot.move_to([0, Y(1120), 0]))
        self.until(wt(0, 2, 0.1)); self.ev("tick"); self.rise(tot, rt=0.4)
        self.play(*[c[2].animate.set_color(OR) for c in cols], run_time=0.3)

        # ===== 1. Choosing which ones is a skill. (photo) =====
        self.until(S[1]); self.to(INK, h1, h2, *cols, tot, lb)
        p3 = photo("p3", "ed", 1080, BAND_TOP, 0.4).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        shade = Rectangle(width=9.2, height=px(560), fill_color=INK, fill_opacity=0.62, stroke_width=0).set_z_index(-4).move_to([0, Y(BAND_TOP) + px(280), 0])
        top_sh = Rectangle(width=9.2, height=px(230), fill_color=INK, fill_opacity=0.55, stroke_width=0).set_z_index(-4).move_to([0, Y(115), 0])
        g1 = at(H("Choosing which ones", 84, WHITE_), 1230); g2 = at(SER("is a skill.", 140, "#FFB27A"), 1380)
        self.play(FadeIn(p3), FadeIn(shade), FadeIn(top_sh), FadeIn(g1, shift=UP * 0.3), run_time=0.35, rate_func=EXPO)
        self.kb(p3, T(), S[2], 1.0, 1.05)
        self.until(wt(1, 3, 0.1)); self.rise(g2, rt=0.4)

        # ===== 2. Dynamic Assessment tracks every answer: accuracy, time and confidence (ink) =====
        self.until(S[2]); p3.clear_updaters(); self.to(INK, p3, shade, top_sh, g1, g2)
        qm = VGroup(MathTex(r"f_n(x)=x^n \text{ on } [0,1]", color=INK, font_size=52 * 0.8), B("Uniformly convergent?", 32, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        da = self.da(2, "Part C · Real Analysis", qm, B("No", 44, WHITE_, SEMIBOLD), 1, 6, 7, 9, 51)

        # ===== 3. So you see where you're strong, and what to fix. (paper) =====
        self.until(S[3]); self.to(PAPER, *da)
        tm_ = self.topic_map(3, "Where you stand", (("Part C", "Linear Algebra", 0.84, False), ("Part C", "Complex Analysis", 0.71, False),
                                                     ("Part C", "Real Analysis", 0.38, True)), 3, 7, "Fix next", "Real Analysis · Part C", 9)

        # ===== 4. Ten full mocks. Parts A, B and C, official attempt limits. Mock 1 is free. (ink) =====
        self.until(S[4]); self.to(INK, *tm_)
        mk = self.mock(4, "CSIR-NET Maths", ("120 Q · attempt 60", "3 h · 200 marks"),
                       (("Unlimited mocks", "Mathematical Sciences", 0), ("Parts A · B · C", "in the real order", 3), ("Official limits", "attempt rules and marking", 11)), 16)

        # ===== 5. Worked solutions, AI tutor 24/7, live classes (paper) =====
        self.until(S[5]); self.gone(mk[2]); self.to(PAPER, *mk)
        sp = self.support(5, "pg", 0.34, (0, 3, 7))

        # ===== 6. End =====
        self.until(S[6]); self.to(INK, *sp); self.remove(self.hdr_d)
        self.end(6, "CSIR-NET Maths mocks · Mock 1 free")


class Jee2(Tgt):
    EVENTS = "jee2"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        # ===== 0. Unlimited mocks elsewhere. Same score. Every single time. (ink) =====
        self._ground.set_fill(INK, 1); self.add(self.hdr_d)
        lb = self.label("JEE Main", True); self.add(lb)
        hd = at(B("Unlimited mocks elsewhere.", 46, GREY_I, SEMIBOLD), 250)
        scores = [151, 149, 152, 150, 153, 151, 148, 152, 150, 151, 149, 152, 150, 151, 152, 150, 149, 151]
        cards = []
        for k, sc in enumerate(scores):
            r_, c_ = divmod(k, 3)
            g = VGroup(card(280, 150, INK2), B(f"Mock {k + 1:02d}", 26, GREY_I, SEMIBOLD), H(f"{sc}", 64, WHITE_), B("/ 300", 26, GREY_I))
            g[1].move_to(g[0].get_top() + DOWN * px(34)).align_to(g[0].get_left() + RIGHT * px(26), LEFT)
            g[2].move_to(g[0].get_center() + DOWN * px(18)).align_to(g[0].get_left() + RIGHT * px(26), LEFT)
            g[3].next_to(g[2], RIGHT, buff=0.12, aligned_edge=DOWN)
            g.move_to([X(96 + 140 + c_ * 304), Y(400 + r_ * 170), 0]); cards.append(g)
        self.add(hd, *cards[:3])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[3:]], lag_ratio=0.12), run_time=1.3, rate_func=EXPO)
        ss = at(H("Same score.", 120, WHITE_), 1440)
        self.until(wt(0, 3, 0.1)); self.ev("stamp"); self.play(FadeIn(ss, shift=UP * 0.3), *[c[2].animate.set_color(OR) for c in cards], run_time=0.35, rate_func=EXPO)

        # ===== 1. Your mock tells you what you scored. Never why. (paper) =====
        self.until(S[1]); self.to(PAPER, hd, *cards, ss, lb)
        sc = card(888, 640, WHITE_); left(sc.move_to([0, Y(700), 0]))
        r1 = B("Mock result", 30, GREY_P, SEMIBOLD); left(r1.move_to([0, Y(460), 0]), 150)
        r2 = H("152 / 300", 130, INK); left(r2.move_to([0, Y(580), 0]), 150)
        why = VGroup(RoundedRectangle(width=px(780), height=px(260), corner_radius=0.18, fill_color=PAPER, fill_opacity=1, stroke_color="#B9B2A6", stroke_width=3), B("Why?", 40, "#B9B2A6", SEMIBOLD))
        why[1].move_to(why[0]); why.move_to([X(540), Y(860), 0])
        self.play(FadeIn(Group(sc, r1, r2), shift=UP * 0.3), FadeIn(why, shift=UP * 0.2), run_time=0.35, rate_func=EXPO)
        nw = at(SER("Never why.", 150, OR), 1300)
        self.until(wt(1, 7, 0.1)); self.ev("stamp"); self.play(FadeIn(nw, shift=UP * 0.3), why[0].animate.set_stroke(OR), why[1].animate.set_color(OR), run_time=0.35, rate_func=EXPO)

        # ===== 2. TutorDA reads how you solve. Right or wrong. How fast. How sure. (ink) =====
        self.until(S[2]); self.to(INK, sc, r1, r2, why, nw)
        da = self.da(2, "Question 12 · Mathematics", MathTex(r"\int_0^{\pi/2}\sin x\,dx", color=INK, font_size=64 * 0.8),
                     MathTex(r"=1", color=WHITE_, font_size=48 * 0.8), 0, 5, 9, 11, 38)

        # ===== 3. Then your next question targets your weak spot. Yours, not everyone's. (paper) =====
        self.until(S[3]); self.to(PAPER, *da)
        tm_ = self.topic_map(3, "Your topic map", (("Mathematics", "Definite integration", 0.82, False), ("Chemistry", "Chemical equilibrium", 0.64, False),
                                                    ("Physics", "Rotational motion", 0.31, True)), 0, 4, "Weak spot", "Rotational motion", 8, next_label="Your next question")

        # ===== 4. Unlimited JEE Main mocks. Real NTA pattern. A worked solution for every question. (ink) =====
        self.until(S[4]); self.to(INK, *tm_)
        mk = self.mock(4, "JEE Main", ("75 questions · 3 h", "300 marks"),
                       (("Unlimited mocks", "JEE Main pattern", 0), ("Real NTA pattern", "+4 / −1, numericals too", 4), ("Worked solutions", "for every question", 8)), None)

        # ===== 5. Stuck at midnight? Ask the AI tutor. Want a teacher? Go live. =====
        self.until(S[5]); self.gone(mk[2]); self.to(INK, *mk)
        q = VGroup(B("Why is", 34, WHITE_), MathTex(r"\int_0^{\pi/2}\sin x\,dx=1\,?", color=WHITE_, font_size=46 * 0.8)).arrange(RIGHT, buff=0.12)
        steps = [B("Step 1  Antiderivative of sin x", 30, "#C9CFDD"), MathTex(r"\int \sin x\,dx=-\cos x", color=WHITE_, font_size=46 * 0.8),
                 B("Step 2  Put in the limits", 30, "#C9CFDD"), MathTex(r"-\cos\tfrac{\pi}{2}+\cos 0=0+1", color=WHITE_, font_size=46 * 0.8),
                 MathTex(r"=1", color=OR, font_size=52 * 0.8)]
        cl = self.chat_live(5, q, steps, 3, 7, 10)

        # ===== 6. Your first mock is free. tutorda.org =====
        self.until(S[6]); self.gone(cl[-1]); [m.clear_updaters() for m in cl]; self.to(INK, *cl); self.remove(self.hdr_d)
        self.end(6, "Your first mock is free.")


class Csir2(Tgt):
    EVENTS = "csir2"
    def construct(self):
        self.setup_common(); C, wt, S, T = K.C, K.wt, self.S, self.Tm
        # ===== 0. 120 questions. You answer only 60. Which 60? (paper) — grid visible on frame 0 =====
        self.add(self.hdr)
        lb = self.label("CSIR-NET Maths", False); self.add(lb)
        h1 = at(H("120 questions.", 110, INK), 300)
        sq = VGroup(*[RoundedRectangle(width=px(58), height=px(58), corner_radius=px(10), fill_color=PAPER2, fill_opacity=1, stroke_width=0) for _ in range(120)])
        sq.arrange_in_grid(rows=10, cols=12, buff=px(16)); left(sq.move_to([0, Y(420 + 365), 0]))
        self.add(h1, sq)
        rng = np.random.default_rng(3); pick = rng.choice(120, 60, replace=False)
        h2 = at(H("You answer 60.", 110, OR), 300)
        self.until(wt(0, 6, 0.1)); self.ev("tick")
        self.play(FadeOut(h1, shift=UP * 0.3), FadeIn(h2, shift=UP * 0.3), LaggedStart(*[sq[int(k)].animate.set_fill(OR) for k in pick], lag_ratio=0.02), run_time=0.9, rate_func=EXPO)
        ws = at(SER("Which sixty?", 150, INK), 1320)
        pick2 = rng.choice(120, 60, replace=False)
        self.until(wt(0, 9, 0.1)); self.ev("stamp")
        self.play(FadeIn(ws, shift=UP * 0.3), *[sq[k].animate.set_fill(OR if k in set(pick2.tolist()) else PAPER2) for k in range(120)], run_time=0.5)

        # ===== 1. In CSIR-NET Maths, that choice is a skill. And you can train it. (photo) =====
        self.until(S[1]); self.to(INK, h2, sq, ws, lb)
        p3 = photo("p3", "ed", 1080, BAND_TOP, 0.4).move_to([0, Y(BAND_TOP / 2), 0]).set_z_index(-5)
        shade = Rectangle(width=9.2, height=px(560), fill_color=INK, fill_opacity=0.62, stroke_width=0).set_z_index(-4).move_to([0, Y(BAND_TOP) + px(280), 0])
        top_sh = Rectangle(width=9.2, height=px(230), fill_color=INK, fill_opacity=0.55, stroke_width=0).set_z_index(-4).move_to([0, Y(115), 0])
        g1 = at(H("That choice is a skill.", 84, WHITE_), 1230); g2 = at(SER("You can train it.", 140, "#FFB27A"), 1380)
        if g1.width > px(888): g1.scale_to_fit_width(px(888)); left(g1)
        self.play(FadeIn(p3), FadeIn(shade), FadeIn(top_sh), run_time=0.3)
        self.kb(p3, T(), S[2], 1.0, 1.05)
        self.until(wt(1, 3, 0.1)); self.rise(g1, rt=0.35)
        self.until(wt(1, 8, 0.1)); self.rise(g2, rt=0.4)

        # ===== 2. TutorDA tracks every answer: accuracy, time and confidence. (ink) =====
        self.until(S[2]); p3.clear_updaters(); self.to(INK, p3, shade, top_sh, g1, g2)
        qm = VGroup(MathTex(r"a_n=(-1)^n", color=INK, font_size=52 * 0.8), B("Bounded. Convergent?", 32, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        da = self.da(2, "Part C · Real Analysis", qm, B("No", 44, WHITE_, SEMIBOLD), 0, 4, 5, 7, 51)

        # ===== 3. So you learn which topics to attempt, and which to fix first. (paper) =====
        self.until(S[3]); self.to(PAPER, *da)
        tm_ = self.topic_map(3, "Where you stand", (("Part C", "Linear Algebra", 0.84, False), ("Part C", "Complex Analysis", 0.71, False),
                                                     ("Part C", "Real Analysis", 0.38, True)), 0, 10, "Fix first", strong_text="Attempt", w_strong=6)

        # ===== 4. Unlimited mocks. Parts A, B and C. Official attempt limits. Worked solutions. (ink) =====
        self.until(S[4]); self.to(INK, *tm_)
        mk = self.mock(4, "CSIR-NET Maths", ("120 Q · attempt 60", "3 h · 200 marks"),
                       (("Unlimited mocks", "Mathematical Sciences", 0), ("Parts A · B · C", "in the real order", 2), ("Official limits", "attempt rules and marking", 7), ("Worked solutions", "for every question", 10)), None)

        # ===== 5. Doubt at midnight? The AI tutor explains. Want a teacher? Go live. =====
        self.until(S[5]); self.gone(mk[2]); self.to(INK, *mk)
        q = VGroup(B("Is every bounded", 34, WHITE_), B("sequence convergent?", 34, WHITE_)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        steps = [B("Not always. Take", 30, "#C9CFDD"), MathTex(r"a_n=(-1)^n", color=WHITE_, font_size=48 * 0.8),
                 B("Bounded, but it keeps jumping", 30, "#C9CFDD"), B("between −1 and 1, so no limit.", 30, "#C9CFDD"),
                 B("Bolzano–Weierstrass: it still has", 30, OR), B("a convergent subsequence.", 30, OR)]
        cl = self.chat_live(5, q, steps, 3, 7, 10)

        # ===== 6. Your first mock is free. tutorda.org =====
        self.until(S[6]); self.gone(cl[-1]); [m.clear_updaters() for m in cl]; self.to(INK, *cl); self.remove(self.hdr_d)
        self.end(6, "Your first mock is free.")
