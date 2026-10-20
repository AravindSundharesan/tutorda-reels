"""Shared Manim pieces for TutorDA reels: frame setup, brand, text helpers, header, word-timed captions, cue timing.
A reel module (`K`) must provide: CLIPS, C, E, DUR, WT, _shift(i), logo_light(scale)."""
import os, sys, math, inspect
import numpy as np
from manim import *
import manimpango

ENGINE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(ENGINE)
for w in ("Bold", "Medium"): manimpango.register_font(os.path.join(KIT, "assets", "fonts", f"Poppins-{w}.ttf"))
if os.environ.get("MANIM_DRAFT") == "1": config.pixel_width, config.pixel_height, config.frame_rate = 540, 960, 15
else: config.pixel_width, config.pixel_height, config.frame_rate = 1080, 1920, 30
config.frame_width, config.frame_height = 9, 16
config.background_color = "#FFFFFF"

# Manim encodes its pieces at CRF 23; use 14 (the final encode sets the upload size)
import manim.scene.scene_file_writer as _sfw
if not getattr(_sfw.SceneFileWriter, "_tutorda_crf", False):
    _src = inspect.getsource(_sfw.SceneFileWriter.open_partial_movie_stream).replace('"crf": "23"', '"crf": "14"')
    _ns = {}; exec(compile("\n".join(l[4:] for l in _src.splitlines()), _sfw.__file__, "exec"), _sfw.__dict__, _ns)
    _sfw.SceneFileWriter.open_partial_movie_stream = _ns["open_partial_movie_stream"]; _sfw.SceneFileWriter._tutorda_crf = True

# brand
INK, INK2, NAVY = "#0F172A", "#475569", "#0E142A"
YEL, AMBER, AMBER_D, TEAL, TEAL_D, RED = "#FFC83D", "#D97706", "#B45309", "#2DD4BF", "#0D9488", "#E5484D"
TINT_Y, TINT_T, TINT_N, TINT_R = "#FFF4D6", "#E3F6F3", "#E8EBF3", "#FDECEC"
def px(v): return v / 120.0
def Y(py): return 8 - py / 120.0
def X(pxx): return pxx / 120.0 - 4.5

def T(s, size, color=INK, weight=BOLD):
    return Text(s, font="Poppins", weight=weight, color=color, font_size=size * 0.6)
def M(s, size, color=INK, **kw):
    return MathTex(s, color=color, font_size=size * 0.8, **kw)
def pill(s, size, fg, bg, padx=0.28, pady=0.14, stroke=None):
    t = T(s, size, fg)
    r = RoundedRectangle(width=t.width + 2 * padx, height=t.height + 2 * pady, corner_radius=(t.height + 2 * pady) / 2,
                         fill_color=bg, fill_opacity=1, stroke_width=3 if stroke else 0, stroke_color=stroke or bg)
    return VGroup(r, t.move_to(r))

_FLAT = set("acemnorsuvwxzACEHIKLMNORSTUVWXZ0123456789.")
def baseline(t):
    """y of a Text's baseline: bottom of its first character that sits on the line (no descender, no round overshoot)."""
    chars = [c for c in t.text if not c.isspace()]
    for idx, c in enumerate(chars):
        if c in _FLAT and idx < len(t.submobjects): return t[idx].get_bottom()[1]
    return t.get_bottom()[1]

class ReelScene(Scene):
    K = None
    def until(self, t):
        dt = t - self.renderer.time
        if dt > 1 / 60: self.wait(dt)
        elif dt < -0.08: print(f"LATE {-dt:.2f}s for cue at {t:.2f}s", file=sys.stderr)

    def setup_ui(self, subject, logo_png):
        """Header (logo + subject line), progress bar, website line, word-timed captions. Returns the header group."""
        K = self.K; now = lambda: self.renderer.time
        self.K.logo_light(2.0).save(logo_png)
        logo = ImageMobject(logo_png).scale_to_fit_height(px(76)).move_to([0, Y(118), 0])
        subj = T(subject, 36, INK2).move_to([0, Y(205), 0])
        site = T("www.tutorda.org", 40, INK2).move_to([0, Y(1560), 0])
        track = Line([-4.5, 7.97, 0], [4.5, 7.97, 0], stroke_width=9, color="#E7E9EF")
        prog = always_redraw(lambda: Line([-4.5, 7.97, 0], [-4.5 + 9 * min(1, max(0.001, now() / K.DUR)), 7.97, 0],
                                          stroke_width=9, color=YEL))
        header = Group(logo, subj, site)
        self.add(track, prog, header)
        caps = []
        for i in range(len(K.CLIPS) - 1):
            cap = K.CLIPS[i][2]; words = cap.replace("|", " ").split(); n = len(words); _w = {}
            def width(a, b):  # real rendered width of the joined line (summing word probes underestimates it)
                if (a, b) not in _w: _w[(a, b)] = T(" ".join(words[a:b]), 48, WHITE).width
                return _w[(a, b)]
            SMALL = {"to", "from", "for", "and", "the", "a", "an", "with", "at", "of", "in", "by", "or"}
            def pen(k):  # cost of breaking before words[k]
                if words[k][0].isdigit() and words[k - 1][-1] not in ",.:;!?": return px(999)  # keep "Class 10" together
                if words[k - 1][-1] in ",.:;!?": return 0
                return px(200)
            MAXW = px(780)  # widest line; bar = line + 60 px, centred -> stays inside the safe box x 85-960
            if "|" in cap:  # the script author's own line breaks win
                lines = [l.split() for l in cap.split("|") if l.strip()]
                assert max(T(" ".join(l), 48, WHITE).width for l in lines) <= MAXW, f"caption {i}: a line is wider than 780 px"
            else:  # fewest lines that fit; least ragged, breaking after punctuation, never inside "Class 10"
                lines = None
                for nl in range(1, 5):
                    best = None
                    for cuts in __import__("itertools").combinations(range(1, n), nl - 1):
                        b = (0,) + cuts + (n,); ws = [width(b[j], b[j + 1]) for j in range(nl)]
                        if max(ws) > MAXW: continue
                        score = max(ws) - min(ws) + sum(pen(c) for c in cuts)
                        if best is None or score < best[0]: best = (score, b)
                    if best: lines = [words[best[1][j]:best[1][j + 1]] for j in range(nl)]; break
                assert lines, f"caption {i} does not fit in 4 lines: {cap}"
            line_txt = [" ".join(l) for l in lines]; spans = []
            for li, l in enumerate(lines):
                c = 0
                for w_ in l: spans.append((li, c, c + len(w_))); c += len(w_) + 1
            def make(k, lines=lines, line_txt=line_txt, spans=spans):
                rows = VGroup(*[Text(line_txt[li], font="Poppins", weight=BOLD, color=WHITE, font_size=48 * 0.6,
                                     t2c=({f"[{spans[k][1]}:{spans[k][2]}]": YEL} if k >= 0 and spans[k][0] == li else {}))
                                for li in range(len(lines))])
                for li, r in enumerate(rows):  # even line pitch on the baseline (bounding boxes vary with g/p/y descenders)
                    r.shift(UP * (-li * px(64) - baseline(r)))
                bg = RoundedRectangle(width=rows.width + px(60), height=rows.height + px(44), corner_radius=px(26),
                                      fill_color="#0F172A", fill_opacity=0.93, stroke_width=0)
                # bottom edge fixed at y=1500 px (clear of the website line and the platform's bottom UI); taller bars grow upward
                g = VGroup(bg, rows.move_to(bg)); return g.move_to([0, Y(1500) + g.height / 2, 0])
            variants = [make(k) for k in range(-1, len(words))]
            starts = np.array(K.WT[i]["starts"]) + K._shift(i)
            t0 = -1.0 if i == 0 else K.C[i] - 0.05
            t1 = (K.C[i + 1] - 0.03) if i + 1 < len(K.C) else K.E[i] + 0.3
            caps.append((t0, t1, starts, variants))
        live = VGroup(); live.key = None
        def show_caption(m):
            t = now(); idx = next((j for j, c in enumerate(caps) if c[0] <= t < c[1]), None)
            k = None if idx is None else int(np.searchsorted(caps[idx][2], t, side="right")) - 1
            if (idx, k) != m.key:
                m.become(caps[idx][3][k + 1].copy() if idx is not None else VGroup()); m.key = (idx, k)
        live.add_updater(show_caption); show_caption(live)
        self.add(live)
        return header
