"""TutorDA reel in Manim: Integral calculus - why a circle's area is pi r^2 (pizza sizes).

Render (from the kit folder):
  manim render -r 1080,1920 --fps 30 engine/manim_pizza.py Reel -o pizza_manim_video.mp4      (final)
  manim render -ql engine/manim_pizza.py Reel -o pizza_manim_draft.mp4                           (480p draft)
`./make.sh pizza-m build` does the render + audio mux + QA.

Timing comes from the same voice, word times and cue names as reel6.py (imported), so audio (music, sounds)
and picture stay in sync. Layout uses the kit's platform-safe box (x 85-960 px, y 220-1520 px).
Units: the frame is 9 x 16 units, 1 unit = 120 px; y is up.
"""
import os, sys, math, json
ENGINE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)
import numpy as np
from manim import *
import manimpango
import reel6 as K                      # cue times, clips, word times, brand logo, audio mix
from PIL import Image as PImage

for w in ("Bold", "Medium"): manimpango.register_font(os.path.join(KIT, "assets", "fonts", f"Poppins-{w}.ttf"))
if os.environ.get("MANIM_DRAFT") == "1": config.pixel_width, config.pixel_height, config.frame_rate = 540, 960, 15
else: config.pixel_width, config.pixel_height, config.frame_rate = 1080, 1920, 30
config.frame_width, config.frame_height = 9, 16
config.background_color = "#FFFFFF"

# Manim encodes its pieces at CRF 23, too soft for an upload master: use CRF 14 (the final encode sets the size)
import inspect, manim.scene.scene_file_writer as _sfw
_src = inspect.getsource(_sfw.SceneFileWriter.open_partial_movie_stream).replace('"crf": "23"', '"crf": "14"')
_ns = {}; exec(compile("\n".join(l[4:] for l in _src.splitlines()), _sfw.__file__, "exec"), _sfw.__dict__, _ns)
_sfw.SceneFileWriter.open_partial_movie_stream = _ns["open_partial_movie_stream"]

# ---------------- brand ----------------
INK, INK2, NAVY = "#0F172A", "#475569", "#0E142A"
YEL, AMBER, AMBER_D, TEAL_D = "#FFC83D", "#D97706", "#B45309", "#0D9488"
CRUST, CRUST_D, SAUCE, CHEESE, CHEESE_D = "#EFA35A", "#C27A38", "#D04A34", "#FBEFC8", "#F4D48A"   # sampled from the illustration
PEP, PEP_D, LEAF = "#C4342E", "#96221E", "#409148"
def px(v): return v / 120.0
def Y(py): return 8 - py / 120.0                         # pixel row -> scene y
def X(pxx): return pxx / 120.0 - 4.5                     # pixel column -> scene x

def T(s, size, color=INK, weight=BOLD):
    """Poppins text; size = em size in px (like the PIL kit)."""
    return Text(s, font="Poppins", weight=weight, color=color, font_size=size * 0.6)
def M(s, size, color=INK, **kw):
    return MathTex(s, color=color, font_size=size * 0.8, **kw)
def pill(s, size, fg, bg, padx=0.28, pady=0.14, stroke=None):
    t = T(s, size, fg)
    r = RoundedRectangle(width=t.width + 2 * padx, height=t.height + 2 * pady, corner_radius=(t.height + 2 * pady) / 2,
                         fill_color=bg, fill_opacity=1, stroke_width=3 if stroke else 0, stroke_color=stroke or bg)
    return VGroup(r, t.move_to(r))

# ---------------- clock + cues ----------------
CLIPS, C, E, DUR = K.CLIPS, K.C, K.E, K.DUR
def wt(i, k, lead=0.0): return K.wt(i, k, lead)

PIZZA_PNG = os.path.join(KIT, "assets", "img", "pizza.png")    # Qwen-Image (Apache-2.0) illustration, cut out; see CREDITS
def pizza_img(r, turn=0.0):
    return ImageMobject(PIZZA_PNG).set(width=2 * r).rotate(turn)

def pizza(r, seed=1, toppings=True):
    g = VGroup(Circle(r, fill_color=CRUST, fill_opacity=1, stroke_color=CRUST_D, stroke_width=3),
               Circle(r * 0.86, fill_color=SAUCE, fill_opacity=1, stroke_width=0),
               Circle(r * 0.82, fill_color=CHEESE, fill_opacity=1, stroke_width=0))
    if toppings:
        rng = np.random.default_rng(seed); pts = []; rc = r * 0.82
        for _ in range(4000):                                  # bounded: never loops forever
            if len(pts) >= 9: break
            a, rr = rng.uniform(0, TAU), math.sqrt(rng.uniform(0.02, 1)) * rc * 0.78
            p = np.array([rr * math.cos(a), rr * math.sin(a), 0])
            if all(np.linalg.norm(p - q) > r * 0.31 for q in pts): pts.append(p)
        for p in pts:
            g.add(Circle(r * 0.13, fill_color=PEP, fill_opacity=1, stroke_color=PEP_D, stroke_width=2).move_to(p))
        for _ in range(len(pts)):
            a, rr = rng.uniform(0, TAU), math.sqrt(rng.uniform(0.05, 1)) * rc * 0.8
            leaf = RoundedRectangle(width=r * 0.15, height=r * 0.045, corner_radius=r * 0.02, fill_color=LEAF,
                                    fill_opacity=1, stroke_width=0).rotate(rng.uniform(0, PI))
            g.add(leaf.move_to([rr * math.cos(a), rr * math.sin(a), 0]))
    return g

# ring <-> strip band (the honest unroll: each ring keeps its length 2*pi*x)
def band(cx, cy, xr, dx, ty, u, n=120):
    s = np.linspace(0, 1, n)
    phi = -PI / 2 + TAU * s                                   # cut at the bottom of the ring
    lift = 0.32 * math.sin(PI * u)
    lx = cx - PI * xr + TAU * xr * s
    def edge(rad, ly):
        cxs, cys = cx + rad * np.cos(phi), cy + rad * np.sin(phi)
        return np.stack([cxs * (1 - u) + lx * u, cys * (1 - u) + ly * u + lift, np.zeros(n)], 1)
    outer = edge(xr + dx / 2, ty - dx / 2); inner = edge(xr - dx / 2, ty + dx / 2)
    return np.concatenate([outer, inner[::-1]])

def ring_color(k, n):
    if k == n - 1: return CRUST
    return interpolate_color(ManimColor(CHEESE), ManimColor(CHEESE_D), k / (n - 2))

class Reel(Scene):
    def until(self, t):
        dt = t - self.renderer.time
        if dt > 1 / 60: self.wait(dt)
        elif dt < -0.08: print(f"LATE {-dt:.2f}s for cue at {t:.2f}s", file=sys.stderr)   # cue missed: shorten earlier animations

    def construct(self):
        now = lambda: self.renderer.time          # the scene clock itself (a dt-driven tracker drifted)

        # ---------- persistent UI: header, progress, captions, website ----------
        logo_png = os.path.join(KIT, "out", "_logo.png"); os.makedirs(os.path.dirname(logo_png), exist_ok=True)
        K.logo_light(2.0).save(logo_png)
        logo = ImageMobject(logo_png).scale_to_fit_height(px(76)).move_to([0, Y(118), 0])
        subj = T("CLASS 12 MATHS  ·  INTEGRAL CALCULUS", 36, INK2).move_to([0, Y(205), 0])
        site = T("www.tutorda.org", 40, INK2).move_to([0, Y(1560), 0])
        track = Line([-4.5, 7.97, 0], [4.5, 7.97, 0], stroke_width=9, color="#E7E9EF")
        prog = always_redraw(lambda: Line([-4.5, 7.97, 0], [-4.5 + 9 * min(1, max(0.001, now() / DUR)), 7.97, 0],
                                          stroke_width=9, color=YEL))
        header = Group(logo, subj, site)
        self.add(track, prog, header)

        caps = []
        for i in range(len(CLIPS) - 1):
            words = CLIPS[i][2].split(); probe = [T(w_, 48, WHITE).width for w_ in words]; sp = px(14)
            def width(a, b): return sum(probe[a:b]) + sp * (b - a - 1)
            if width(0, len(words)) <= px(760): lines = [words]
            else:
                k = min(range(1, len(words)), key=lambda k: max(width(0, k), width(k, len(words))) + (0 if words[k - 1][-1] in ",.:;!?" else px(120)))
                lines = [words[:k], words[k:]]
            line_txt = [" ".join(l) for l in lines]
            spans = []                                             # (row, char start, char end) per word, spaces included
            for li, l in enumerate(lines):
                c = 0
                for w_ in l: spans.append((li, c, c + len(w_))); c += len(w_) + 1
            def make(k):                                           # k = highlighted word (-1: none); Manim maps chars -> glyphs
                rows = VGroup(*[Text(line_txt[li], font="Poppins", weight=BOLD, color=WHITE, font_size=48 * 0.6,
                                     t2c=({f"[{spans[k][1]}:{spans[k][2]}]": YEL} if k >= 0 and spans[k][0] == li else {}))
                                for li in range(len(lines))]).arrange(DOWN, buff=px(16))
                bg = RoundedRectangle(width=rows.width + px(70), height=rows.height + px(44), corner_radius=px(26),
                                      fill_color="#0F172A", fill_opacity=0.93, stroke_width=0)
                return VGroup(bg, rows.move_to(bg)).move_to([0, Y(1410), 0])
            variants = [make(k) for k in range(-1, len(words))]
            starts = np.array(K.WT[i]["starts"]) + K._shift(i)
            t0 = -1.0 if i == 0 else C[i] - 0.05
            t1 = (C[i + 1] - 0.03) if i + 1 < len(C) else E[i] + 0.3
            caps.append((t0, t1, starts, variants))
        live = VGroup(); live.key = None
        def show_caption(m):
            t = now(); idx = next((j for j, c in enumerate(caps) if c[0] <= t < c[1]), None)
            k = None if idx is None else int(np.searchsorted(caps[idx][2], t, side="right")) - 1
            if (idx, k) != m.key:                                  # swap only when the spoken word changes
                m.become(caps[idx][3][k + 1].copy() if idx is not None else VGroup()); m.key = (idx, k)
        live.add_updater(show_caption); show_caption(live)
        self.add(live)

        # ================= HOOK (on screen at frame 0) =================
        title = T("Which is more pizza?", 70).move_to([0, Y(340), 0])
        big = pizza_img(px(190)).move_to([X(315), Y(745), 0])
        s1, s2 = pizza_img(px(128), 1.1).move_to([X(780), Y(605), 0]), pizza_img(px(128), 2.6).move_to([X(780), Y(885), 0])
        for p, rate in ((big, 0.2), (s1, -0.26), (s2, -0.26)): p.add_updater(lambda m, dt, rate=rate: m.rotate(rate * dt))
        vs = pill("VS", 46, WHITE, NAVY, padx=0.22, pady=0.12).move_to([X(578), Y(745), 0])
        lab1 = T("1 × 12-inch", 52).move_to([X(315), Y(1080), 0]); lab2 = T("2 × 8-inch", 52).move_to([X(780), Y(1080), 0])
        hook = Group(title, big, s1, s2, vs, lab1, lab2)
        self.add(hook)
        self.until(K.TWO_T); self.play(Indicate(vs, color=AMBER_D, scale_factor=1.15), run_time=0.7)
        ring_hl = Ellipse(width=px(282), height=px(590), stroke_color=AMBER, stroke_width=7).move_to([X(790), Y(745), 0]).rotate(-0.05)
        self.until(K.LOOKS_T); self.play(Create(ring_hl), run_time=0.7, rate_func=smooth)
        qm = M(r"\int_0^{r} \; ? \;\, dx", 72, NAVY)
        qc = RoundedRectangle(width=qm.width + px(80), height=qm.height + px(40), corner_radius=px(24), fill_color="#F1F5F9",
                              fill_opacity=1, stroke_color="#CBD5E1", stroke_width=2)
        q = VGroup(qc, qm.move_to(qc)).move_to([0, Y(1215), 0])
        self.until(K.INTEG_T)
        self.play(Write(q), s1.animate.set_opacity(0.45), s2.animate.set_opacity(0.45), ring_hl.animate.set_stroke(opacity=0.4), run_time=0.4)

        # ================= PROOF =================
        self.until(K.T1 - 0.35)
        for p in (big, s1, s2): p.clear_updaters()
        self.play(FadeOut(Group(hook, ring_hl, q), shift=LEFT * 1.2), run_time=0.35, rate_func=rush_into)

        N, RB = 8, px(300)                       # big pizza for slicing and marking x
        CB = np.array([0, Y(780), 0])
        pz = pizza_img(RB, 0.4).move_to(CB)
        self.play(FadeIn(pz, shift=LEFT * 1.0, scale=0.95), run_time=0.45, rate_func=rush_from)
        dxB = RB / N
        rings = VGroup(*[Annulus(inner_radius=k * dxB, outer_radius=(k + 1) * dxB, fill_color=ring_color(k, N), fill_opacity=1,
                                 stroke_color=WHITE, stroke_width=2.5).move_to(CB) for k in range(N)])
        self.until(K.RINGS_T)
        self.play(FadeOut(pz), LaggedStart(*[DrawBorderThenFill(rg) for rg in reversed(rings)], lag_ratio=0.08), run_time=0.9)
        KX = N - 2
        hl = Annulus(inner_radius=KX * dxB, outer_radius=(KX + 1) * dxB, fill_opacity=0, stroke_color=AMBER_D, stroke_width=7).move_to(CB)
        self.until(K.RING_T); self.play(Create(hl), rings[KX].animate.set_fill(AMBER), run_time=0.45)
        xr_big = (KX + 0.5) * dxB; ang = 0.62
        arr = Arrow(CB, CB + xr_big * np.array([math.cos(ang), math.sin(ang), 0]), buff=0, color=NAVY, stroke_width=7,
                    max_tip_length_to_length_ratio=0.12)
        xl = M("x", 70, NAVY); xl_bg = Circle(px(34), fill_color=WHITE, fill_opacity=0.95, stroke_color=NAVY, stroke_width=3)
        xlab = VGroup(xl_bg, xl.move_to(xl_bg)).move_to(CB + 0.5 * xr_big * np.array([math.cos(ang), math.sin(ang), 0]) + px(52) * np.array([-math.sin(ang), math.cos(ang), 0]))
        self.until(K.X_T); self.play(GrowArrow(arr), FadeIn(xlab, scale=0.8), run_time=0.5)

        # shrink to the proof scale, then unroll ring KX into its strip
        R, CS = px(122), np.array([0, Y(540), 0])
        dx = R / N; BASE = Y(780)
        rows_y = [BASE + dx / 2 + (N - 1 - k) * dx for k in range(N)]
        self.until(K.UN1_T - 0.5)
        self.play(FadeOut(VGroup(hl, arr, xlab)), run_time=0.15)
        self.play(rings.animate.scale(R / RB, about_point=CB).shift(CS - CB), run_time=0.35)
        u = [ValueTracker(0.0) for _ in range(N)]
        bands = VGroup()
        for k in range(N):
            b = VMobject(fill_color=AMBER if k == KX else ring_color(k, N), fill_opacity=1, stroke_color=WHITE, stroke_width=1.5)
            b.add_updater(lambda m, k=k: m.set_points_as_corners(band(CS[0], CS[1], (k + 0.5) * dx, dx * 0.92, rows_y[k], u[k].get_value())))
            b.update(); bands.add(b)
        self.remove(rings); self.add(bands)
        self.play(u[KX].animate.set_value(1), run_time=0.7, rate_func=smooth)
        xr = (KX + 0.5) * dx
        strip_ref = Line([CS[0] - PI * xr, rows_y[KX], 0], [CS[0] + PI * xr, rows_y[KX], 0])
        br_len = Brace(strip_ref, DOWN, buff=px(18), color=TEAL_D); lab_len = M(r"2\pi x", 66, TEAL_D).next_to(br_len, DOWN, buff=px(8))
        self.until(K.LEN_T); self.play(GrowFromCenter(br_len), FadeIn(lab_len, shift=UP * 0.1), run_time=0.5)
        # magnified dx, drawn in vectors (5x)
        end_pt = np.array([CS[0] + PI * xr, rows_y[KX], 0])
        spot = Circle(px(26), stroke_color=NAVY, stroke_width=4).move_to(end_pt)
        lc = np.array([X(785), Y(560), 0]); lr = px(118)
        lens = Circle(lr, fill_color=WHITE, fill_opacity=1, stroke_color=NAVY, stroke_width=6).move_to(lc)
        seg = Rectangle(width=lr * 1.25, height=dx * 0.92 * 6.5, fill_color=AMBER, fill_opacity=1, stroke_width=0)
        seg.move_to(lc + LEFT * lr * 0.38)
        bdx = Brace(seg, RIGHT, buff=px(10), color=AMBER_D, sharpness=1.2); ldx = M("dx", 64, AMBER_D).next_to(bdx, RIGHT, buff=px(6))
        mag = VGroup(lens, seg, bdx, ldx)
        link = Line(spot.get_top(), lens.get_bottom() + LEFT * px(10), color=NAVY, stroke_width=3)
        self.until(K.DX_T)
        self.play(Create(spot), Create(link), FadeIn(mag, scale=0.6), run_time=0.35)

        # stack the rest into a triangle
        self.until(K.ALL_T - 0.1)
        rest = [k for k in range(N - 1, -1, -1) if k != KX]
        self.play(FadeOut(VGroup(br_len, lab_len, spot, link, mag), run_time=0.2),
                  LaggedStart(*[u[k].animate.set_value(1) for k in rest], lag_ratio=0.12, run_time=0.95, rate_func=smooth))
        tri = Polygon([CS[0] - PI * R, BASE, 0], [CS[0] + PI * R, BASE, 0], [CS[0], BASE + R, 0], stroke_color=AMBER_D, stroke_width=6)
        hgt = DashedLine([0, BASE, 0], [0, BASE + R, 0], color=NAVY, stroke_width=4, dash_length=px(10))
        br_b = Brace(Line([CS[0] - PI * R, BASE, 0], [CS[0] + PI * R, BASE, 0]), DOWN, buff=px(10), color=TEAL_D)
        lab_b = M(r"2\pi r", 66, TEAL_D).next_to(br_b, DOWN, buff=px(6))
        rtag = M("r", 60, NAVY); rbg = RoundedRectangle(width=px(52), height=px(56), corner_radius=px(12), fill_color=WHITE,
                                                    fill_opacity=0.95, stroke_color=NAVY, stroke_width=3)
        hlab = VGroup(rbg, rtag.move_to(rbg)).move_to([px(46), BASE + R / 2, 0])
        ghost = DashedVMobject(Circle(R, stroke_color=CRUST_D, stroke_width=4), num_dashes=40).move_to(CS)
        ghost_fill = Circle(R, fill_color=CHEESE, fill_opacity=0.45, stroke_width=0).move_to(CS)
        ghost_lab = M(r"\pi r^2", 66, NAVY).move_to(CS)
        self.until(K.TRI_T - 0.05)
        self.play(Create(tri), Create(hgt), GrowFromCenter(br_b), FadeIn(lab_b, shift=UP * 0.1), FadeIn(hlab, scale=0.8),
                  Create(ghost), run_time=0.55)

        # the integral, then its evaluation (the one bouncy moment)
        l1 = MathTex(r"\text{Area}", "=", r"\int_0^{r}", r"2\pi x", r"\,dx", color=INK, font_size=66)
        l1.next_to(lab_b, DOWN, buff=px(34)).set_x(0)
        self.until(K.AREA_T); self.play(Write(l1), run_time=0.9)
        # follow the voice: "0 to r" -> the limits and the triangle's height; "2 pi x, dx" -> the integrand and the strips
        self.until(wt(5, 2, 0.1)); self.play(Indicate(l1[2], color=TEAL_D, scale_factor=1.12), Indicate(hlab[1], color=AMBER_D, scale_factor=1.3), run_time=0.7)
        l2 = MathTex("=", r"\left[\pi x^2\right]_0^{r}", "=", r"\pi r^2", color=NAVY, font_size=70)
        l2.next_to(l1, DOWN, buff=px(64)).set_x(0)
        self.until(wt(5, 6, 0.12))
        self.play(Indicate(l1[3:5], color=AMBER_D, scale_factor=1.1), Write(l2[0:2]), run_time=0.5)
        box = RoundedRectangle(width=l2.width + px(90), height=l2.height + px(56), corner_radius=px(30),
                               fill_color=YEL, fill_opacity=1, stroke_width=0).move_to(l2)
        self.until(K.ANS_T - 0.05)
        box.set_z_index(-1)
        self.play(FadeIn(box, scale=0.6, rate_func=rate_functions.ease_out_back), Write(l2[2:4]),
                  ShowPassingFlash(tri.copy().set_stroke(AMBER, 12), time_width=0.6),
                  FadeIn(ghost_fill), FadeIn(ghost_lab, scale=0.7), run_time=0.6)
        proof = VGroup(bands, tri, hgt, br_b, lab_b, hlab, l1, l2, box, ghost, ghost_fill, ghost_lab)

        # ================= REAL LIFE =================
        self.until(K.REAL_T - 0.3)
        self.play(FadeOut(proof, shift=LEFT * 1.2), run_time=0.35, rate_func=rush_into)
        B = pizza_img(px(170)).move_to([X(300), Y(545), 0])
        b1, b2 = pizza_img(px(113), 1.1).move_to([X(740), Y(470), 0]), pizza_img(px(113), 2.6).move_to([X(740), Y(700), 0])
        for p, rate in ((B, 0.2), (b1, -0.26), (b2, -0.26)): p.add_updater(lambda m, dt, rate=rate: m.rotate(rate * dt))
        X0, BW, BH = X(125), px(770), px(60)
        la = T("1 × 12-inch", 46).move_to([X0, Y(960), 0], aligned_edge=LEFT)
        lb = T("2 × 8-inch", 46).move_to([X0, Y(1170), 0], aligned_edge=LEFT)
        trA = RoundedRectangle(width=BW, height=BH, corner_radius=BH / 2, fill_color="#0F172A", fill_opacity=0.06, stroke_width=0).move_to([X0 + BW / 2, Y(1022), 0])
        trB = trA.copy().move_to([X0 + BW / 2, Y(1232), 0])
        self.play(LaggedStart(FadeIn(B, scale=0.9), FadeIn(b1, scale=0.9), FadeIn(b2, scale=0.9), lag_ratio=0.15),
                  FadeIn(VGroup(la, lb, trA, trB)), run_time=0.6, rate_func=rush_from)
        fA = M(r"\pi \cdot 6^2 = 36\pi", 62).move_to([X(300), Y(868), 0])
        fB = M(r"2 \cdot \pi \cdot 4^2 = 32\pi", 62).move_to([X(740), Y(868), 0])
        fB.align_to(fA, DOWN)
        vA, vB = ValueTracker(0), ValueTracker(0)
        def bar(v, vmax, y, color):
            return always_redraw(lambda: RoundedRectangle(width=max(BH, BW * v.get_value() / vmax), height=BH, corner_radius=BH / 2,
                                                          fill_color=color, fill_opacity=1 if v.get_value() > 0.5 else 0, stroke_width=0)
                                 .move_to([X0, y, 0], aligned_edge=LEFT))
        barA, barB = bar(vA, 36 * PI, Y(1022), YEL), bar(vB, 36 * PI, Y(1232), "#CBD5E1")
        numA = always_redraw(lambda: T(f"≈ {int(math.floor(vA.get_value() + 0.5))} sq in", 46, AMBER_D).move_to([X0 + BW, Y(960), 0], aligned_edge=RIGHT))
        numB = always_redraw(lambda: T(f"≈ {int(math.floor(vB.get_value() + 0.5))} sq in", 46, INK2).move_to([X0 + BW, Y(1170), 0], aligned_edge=RIGHT))
        self.add(barA, barB)
        self.until(K.P36_T); self.play(Write(fA), run_time=0.6)
        self.until(K.P113_T); self.add(numA); self.play(vA.animate.set_value(36 * PI), run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.until(K.P32_T); self.play(Write(fB), run_time=0.6)
        self.until(K.P101_T); self.add(numB); self.play(vB.animate.set_value(32 * PI), run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        xs = X0 + BW * 32 / 36
        extra = VGroup(Rectangle(width=X0 + BW - BH / 2 - xs, height=BH, fill_color=AMBER, fill_opacity=1, stroke_width=0)
                       .move_to([xs, Y(1022), 0], aligned_edge=LEFT),
                       Circle(BH / 2, fill_color=AMBER, fill_opacity=1, stroke_width=0).move_to([X0 + BW - BH / 2, Y(1022), 0]))
        gap = Line([xs, Y(1022) - BH / 2, 0], [xs, Y(1022) + BH / 2, 0], color=WHITE, stroke_width=4)
        tag = pill("+12.5%", 48, NAVY, YEL, stroke=AMBER_D).move_to([min(X0 + BW - px(100), (xs + X0 + BW) / 2), Y(1100), 0])
        self.until(K.WIN_T)
        self.play(FadeIn(extra), Create(gap), run_time=0.4)
        self.play(FadeIn(tag, scale=0.7), Flash(B, color=AMBER, line_length=0.22, num_lines=14, flash_radius=px(186)), run_time=0.6)
        real = Group(B, b1, b2, la, lb, trA, trB, fA, fB, barA, barB, numA, numB, extra, gap, tag)

        # ================= END CARD =================
        self.until(K.END_T)
        for p in (B, b1, b2): p.clear_updaters()
        big_logo = ImageMobject(logo_png).scale_to_fit_height(px(76 * 1.75)).move_to([0, Y(800), 0])
        f1 = T("Follow for more Class 12 maths", 54).move_to([0, Y(960), 0])
        f2 = T("JEE  ·  NEET  ·  Boards", 44, AMBER_D).move_to([0, Y(1045), 0])
        f3 = pill("www.tutorda.org", 58, NAVY, YEL, padx=0.4, pady=0.2).move_to([0, Y(1190), 0])
        self.play(FadeOut(real), FadeOut(header), run_time=0.35)
        self.play(FadeIn(big_logo, scale=0.85), run_time=0.45, rate_func=rush_from)
        self.play(LaggedStart(FadeIn(f1, shift=UP * 0.15), FadeIn(f2, shift=UP * 0.15), FadeIn(f3, scale=0.9), lag_ratio=0.25), run_time=0.7)
        self.until(DUR)
