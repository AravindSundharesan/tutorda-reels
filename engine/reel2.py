"""TutorDA reel: d/dx(x^x) + the 37% rule. Voice-synced, 1080x1920 @30fps.
python3 reel2.py preview <t> ...    -> stills
python3 reel2.py build out.mp4      -> full video with audio
"""
import sys, io, os, json, math, subprocess, wave
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"] = "cm"

W, H, FPS = 1080, 1920, 30
BG1 = (12, 18, 38); BG2 = (22, 32, 64)
WHITE = (245, 247, 252); MUTED = (160, 172, 200)
YEL = (255, 200, 61); TEAL = (45, 212, 191); RED = (255, 90, 95); NAVY = (14, 20, 42)
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.environ.get("FONT_DIR", os.path.join(KIT, "assets", "fonts")) + "/"
def font(w, s): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)

# ---------------- timeline from voice clips ----------------
CLIPS = json.load(open(os.environ.get("CLIPS", os.path.join(KIT, "topics/x_power_x/clips.json"))))
VO = os.environ.get("VO", os.path.join(KIT, "topics/x_power_x/vo"))
DURS = json.load(open(f"{VO}/durs.json"))
START = float(os.environ.get("START", "0.4")); IN_GAP, BEAT_GAP = float(os.environ.get("IN_GAP", "0.15")), float(os.environ.get("BEAT_GAP", "0.30"))
END_HOLD = float(os.environ.get("END_HOLD", "1.1"))
C, E = [], []
t = START
for i, d in enumerate(DURS):
    if i > 0:
        t += IN_GAP if CLIPS[i][0] == CLIPS[i - 1][0] else BEAT_GAP
    C.append(t); E.append(t + d); t += d
DUR = round(E[-1] + END_HOLD, 2)
NF = int(DUR * FPS)

# ---------------- helpers ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(p): return 1 - (1 - p) ** 3
def ease_io(p): return 3 * p * p - 2 * p * p * p

def spring(t, bounce=0.25, visual_duration=0.45):
    """Motion's duration-based spring (mass 1): unit step 0->1, may overshoot.
    stiffness = (2pi / (1.2*visualDuration))^2, damping = 2*(1-bounce)*sqrt(stiffness)."""
    if t <= 0: return 0.0
    w0 = 2 * math.pi / (visual_duration * 1.2)
    z = max(0.05, min(1.0, 1 - bounce))
    if z < 1:
        wd = w0 * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w0 * t) * (math.cos(wd * t) + (z * w0 / wd) * math.sin(wd * t))
    return 1 - math.exp(-w0 * t) * (1 + w0 * t)

def bezier(x1, y1, x2, y2):
    """CSS cubic-bezier easing (e.g. Remotion's Easing.bezier(0.16, 1, 0.3, 1))."""
    def f(p):
        if p <= 0: return 0.0
        if p >= 1: return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(30):
            u = (lo + hi) / 2
            x = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u * u * x2 + u ** 3
            lo, hi = (u, hi) if x < p else (lo, u)
        u = (lo + hi) / 2
        return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u * u * y2 + u ** 3
    return f
EXPO_OUT = bezier(0.16, 1, 0.3, 1)

def back_out(p, s=1.7):
    p -= 1; return p * p * ((s + 1) * p + s) + 1

def tex(s, px, color=WHITE):
    dpi = 200
    fig = plt.figure(figsize=(0.01, 0.01), dpi=dpi)
    fig.text(0, 0, f"${s}$", fontsize=px * 72 / dpi, color=tuple(c / 255 for c in color))
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig); buf.seek(0)
    return Image.open(buf).convert("RGBA")

def text_img(s, f, color):
    l, t_, r, b = f.getbbox(s)
    im = Image.new("RGBA", (r - l, b - t_), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-l, -t_), s, font=f, fill=color)
    return im

def pill(s, f, fg, bg, padx=30, pady=16, outline=None):
    l, t_, r, b = f.getbbox(s)
    w, h = r - l + 2 * padx, b - t_ + 2 * pady
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg, outline=outline, width=3 if outline else 0)
    d.text((padx - l, pady - t_), s, font=f, fill=fg)
    return im

def ink_runs(im):
    a = np.array(im)[..., 3].max(axis=0) > 20
    runs, x = [], 0
    while x < len(a):
        if a[x]:
            s = x
            while x < len(a) and a[x]: x += 1
            runs.append((s, x))
        x += 1
    return runs

def logo(scale=1.0):
    """TutorDA wordmark: yellow tile with T + 'Tutor' white 'DA' yellow."""
    s = scale; tile = int(76 * s)
    f = font("Bold", int(58 * s)); ft = font("Bold", int(52 * s))
    w1 = f.getlength("Tutor"); w2 = f.getlength("DA")
    gap = int(18 * s)
    W_ = int(tile + gap + w1 + w2 + 4); H_ = int(tile + 4)
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, tile, tile], radius=int(20 * s), fill=YEL)
    # little graduation-cap notch: a navy diamond on the T
    l, t_, r, b = ft.getbbox("T")
    d.text(((tile - (r - l)) / 2 - l, (tile - (b - t_)) / 2 - t_ + 2 * s), "T", font=ft, fill=NAVY)
    l, t_, r, b = f.getbbox("TutorDA")
    ty = (tile - (b - t_)) / 2 - t_
    d.text((tile + gap, ty), "Tutor", font=f, fill=WHITE)
    d.text((tile + gap + w1, ty), "DA", font=f, fill=YEL)
    return im

def house(w=72, fill=(55, 70, 110), line=(120, 140, 190), door=(30, 40, 70)):
    h = int(w * 1.05)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    o = 4; roof = int(h * 0.42)
    d.polygon([(o, o + roof), (o + w / 2, o), (o + w, o + roof)], fill=line)
    d.rounded_rectangle([o + w * 0.12, o + roof - 2, o + w * 0.88, o + h], radius=6, fill=fill)
    d.rounded_rectangle([o + w * 0.40, o + h * 0.68, o + w * 0.60, o + h], radius=4, fill=door)
    return im

def star(r=30, color=YEL):
    im = Image.new("RGBA", (2 * r + 4, 2 * r + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for k in range(10):
        ang = -np.pi / 2 + k * np.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((r + 2 + rr * np.cos(ang), r + 2 + rr * np.sin(ang)))
    d.polygon(pts, fill=color)
    return im

# ---------------- element system ----------------
class El:
    def __init__(self, img, cx, cy, t_in, dur=0.45, kind="fade", t_out=None, out_dur=0.35, dims=(), move=None):
        self.img, self.cx, self.cy = img, cx, cy
        self.t_in, self.dur, self.kind = t_in, dur, kind
        self.t_out, self.out_dur, self.dims, self.move = t_out, out_dur, dims, move
        self._a = np.array(img)

    def draw(self, frame, t):
        if t < self.t_in: return
        if self.t_out is not None and t > self.t_out + self.out_dur: return
        p = clamp((t - self.t_in) / self.dur)
        alpha, dy, scale, wipe = 1.0, 0.0, 1.0, 1.0
        el = t - self.t_in
        if self.kind == "fade":   # slide up on a gentle spring, opacity on expo-out
            alpha = EXPO_OUT(clamp(el / 0.35)); dy = (1 - spring(el, 0.15, 0.45)) * 40
        elif self.kind == "wipe": # handwriting-style reveal, no overshoot
            wipe = EXPO_OUT(p); alpha = clamp(p * 4)
        elif self.kind == "land":  # arrive 8% oversize, settle with expo-out, no overshoot
            q = EXPO_OUT(clamp(el / 0.38)); scale = 1 + 0.08 * (1 - q); alpha = EXPO_OUT(clamp(el / 0.18))
        elif self.kind == "pop":  # bouncy pop, scale interpolated perceptually (log space)
            sp = spring(el, 0.35, 0.42)
            scale = math.exp(math.log(0.5) * (1 - sp)); alpha = EXPO_OUT(clamp(el / 0.18))
        for (td, lvl) in self.dims:
            q = ease_io(clamp((t - td) / 0.4)); alpha *= 1 - q * (1 - lvl)
        if self.t_out is not None:
            alpha *= 1 - ease_io(clamp((t - self.t_out) / self.out_dur))
        cx, cy = self.cx, self.cy
        if self.move:
            t0, t1, cx1, cy1, s1 = self.move
            q = spring(t - t0, 0.0, t1 - t0) if t > t0 else 0.0  # critically damped glide
            cx += (cx1 - cx) * q; cy += (cy1 - cy) * q; scale *= 1 + (s1 - 1) * q
        if alpha <= 0.004: return
        a = self._a.copy() if (alpha < 1 or wipe < 1) else self._a
        h, w = a.shape[:2]
        if wipe < 1:
            edge = 60; xs = np.arange(w)
            m = np.clip((wipe * (w + edge) - xs) / edge, 0, 1)
            a[..., 3] = (a[..., 3] * m[None, :]).astype(np.uint8)
        if alpha < 1: a[..., 3] = (a[..., 3] * alpha).astype(np.uint8)
        im = Image.fromarray(a)
        if abs(scale - 1) > 0.003:
            im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
        x = int(round(cx - im.width / 2)); y = int(round(cy - im.height / 2 + dy))
        frame.alpha_composite(im, dest=(max(x, 0), max(y, 0)), source=(max(-x, 0), max(-y, 0)))

def make_bg():
    g = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(BG1) * (1 - g) + np.array(BG2) * g) * np.ones((H, W, 3))
    bg = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(grid)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 9))
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(255, 255, 255, 9))
    bg.alpha_composite(grid)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-200, 500, W + 200, 1500], fill=(70, 110, 220, 38))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))
    return bg

def at(i, frac):  # time at a fraction through clip i
    return C[i] + frac * (E[i] - C[i])

def house_row(els, cy, t0, stagger=0.07, t_out=None, band_t=None, star_t=None, band_label=True):
    n, hw, sp = 10, 76, 92
    x0 = W / 2 - (n - 1) * sp / 2
    for i in range(n):
        els.append(El(house(hw), x0 + i * sp, cy, t0 + i * stagger, 0.35, kind="pop", t_out=t_out))
    if band_t is not None:
        left = x0 - sp / 2; right = left + 0.37 * n * sp
        band = Image.new("RGBA", (int(right - left), 150), (0, 0, 0, 0))
        ImageDraw.Draw(band).rounded_rectangle([0, 0, band.width - 1, 149], radius=24,
                                               fill=TEAL + (46,), outline=TEAL + (220,), width=4)
        els.append(El(band, (left + right) / 2, cy + 4, band_t, 0.5, kind="wipe", t_out=t_out))
        if band_label:
            lab = text_img("first 37%: just look", font("Bold", 42), TEAL)
            els.append(El(lab, max(left + lab.width / 2, 85 + lab.width / 2), cy + 115, band_t + 0.2, t_out=t_out))
    if star_t is not None:
        sx = x0 + 5 * sp
        els.append(El(house(hw, fill=YEL, line=(255, 225, 140), door=NAVY), sx, cy, star_t, 0.4, kind="pop", t_out=t_out))
        els.append(El(star(30), sx, cy - 90, star_t + 0.1, 0.4, kind="pop", t_out=t_out))
        if band_label:
            lab = text_img("then pick the next better one", font("Bold", 42), YEL)
            els.append(El(lab, min(sx, W - lab.width / 2 - 85), cy + 170, star_t + 0.2, t_out=t_out))

# ---------------- build ----------------
def build():
    els, over, caps = [], [], []
    MATH = 70

    # branding (persistent)
    els.append(El(logo(1.0), W / 2, 118, 0.0, 0.5))
    els.append(El(text_img("CLASS 12 MATHS  ·  DIFFERENTIATION", font("Bold", 36), MUTED), W / 2, 205, 0.15, 0.5))
    els.append(El(text_img("www.tutorda.org", font("Bold", 40), (210, 216, 234)), W / 2, 1790, 0.2, 0.5, t_out=C[13] - 0.3))

    # ---- Hook: the 37% rule
    hook_out = E[1] + 0.05
    els.append(El(text_img("The 37% Rule", font("Bold", 92), WHITE), W / 2, 390, C[0], 0.45, t_out=hook_out))
    els.append(El(text_img("Hunting for a flat or PG?", font("Medium", 44), MUTED), W / 2, 495, C[0] + 0.2, t_out=hook_out))
    house_row(els, 740, C[0] + 0.3, t_out=hook_out, band_t=at(0, 0.45), star_t=at(0, 0.8))
    els.append(El(pill("WHY 37%?", font("Bold", 64), NAVY, YEL, padx=44, pady=22), W / 2, 1110, C[1], 0.45, kind="pop", t_out=hook_out))
    els.append(El(text_img("The answer is one Class 12 derivative", font("Medium", 40), WHITE), W / 2, 1240, at(1, 0.3), t_out=hook_out))

    # ---- Problem + trap
    q_out = C[4]
    els.append(El(text_img("Find dy/dx if", font("Bold", 66), WHITE), W / 2, 360, C[2], t_out=q_out))
    big_w = tex(r"y = x^{x}", 210)
    runs = ink_runs(big_w); bx0, bx1 = runs[-2]; sx0, sx1 = runs[-1]
    col = np.array(big_w).copy(); col[:, bx0:bx1, :3] = TEAL; col[:, sx0:sx1, :3] = YEL
    big_c = Image.fromarray(col)
    BIG_CY = 560
    board_t = C[6] - 0.25
    mv = (board_t - 0.3, board_t + 0.3, W / 2, 440, 0.48)
    board_out = C[10] - 0.35
    els.append(El(big_w, W / 2, BIG_CY, at(2, 0.25), 0.5, dims=[(C[9], 0.35)], move=mv, t_out=board_out))
    els.append(El(big_c, W / 2, BIG_CY, C[4], 0.5, dims=[(C[9], 0.35)], move=mv, t_out=board_out))

    pr_out = C[4] - 0.05
    els.append(El(text_img("Power rule?", font("Bold", 50), MUTED), W / 2, 820, C[3] - 0.1, t_out=pr_out))
    pr = tex(r"\frac{dy}{dx} = x\cdot x^{x-1}", MATH)
    els.append(El(pr, W / 2, 960, C[3] - 0.05, 0.5, kind="wipe", t_out=pr_out))
    xw, xh = pr.width + 60, pr.height + 50
    X = Image.new("RGBA", (xw, xh), (0, 0, 0, 0)); d = ImageDraw.Draw(X)
    for (p0, p1) in [((14, 14), (xw - 14, xh - 14)), ((xw - 14, 14), (14, xh - 14))]:
        d.line([p0, p1], fill=RED + (235,), width=16)
    x_t = at(3, 0.6)
    els.append(El(X, W / 2, 960, x_t, 0.35, kind="pop", t_out=pr_out))
    els.append(El(pill("WRONG", font("Bold", 34), WHITE, RED, padx=24, pady=10), W / 2 + 330, 870, x_t + 0.1, 0.3, kind="pop", t_out=pr_out))

    # annotations
    bw, bh = big_w.size
    left = W / 2 - bw / 2; top = BIG_CY - bh / 2
    base_cx = left + (bx0 + bx1) / 2; sup_cx = left + (sx0 + sx1) / 2
    ann_out = board_t - 0.4
    stem = Image.new("RGBA", (24, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(stem)
    d.line([(12, 0), (12, 100)], fill=TEAL, width=6); d.ellipse([3, 90, 21, 108], fill=TEAL)
    els.append(El(stem, base_cx, top + bh + 40, C[4] + 0.15, t_out=ann_out))
    els.append(El(text_img("base changes", font("Bold", 42), TEAL), base_cx, top + bh + 125, C[4] + 0.15, t_out=ann_out))
    lab = text_img("power changes", font("Bold", 42), YEL)
    els.append(El(lab, min(sup_cx, W - lab.width / 2 - 40), top - 120, C[4] + 0.5, t_out=ann_out))
    arr = Image.new("RGBA", (24, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(arr)
    d.line([(12, 0), (12, 62)], fill=YEL, width=6); d.ellipse([3, 52, 21, 70], fill=YEL)
    els.append(El(arr, sup_cx, top - 50, C[4] + 0.5, t_out=ann_out))
    els.append(El(pill("TRICK:  take log first", font("Bold", 52), NAVY, YEL, padx=40, pady=22), W / 2, 1060, C[5], 0.4, kind="pop", t_out=ann_out))

    # ---- Board
    chip_f = font("Bold", 40)
    def chip(s): return pill(s, chip_f, YEL, (255, 200, 61, 28), padx=26, pady=12, outline=YEL + (140,))
    bd = dict(dims=[(C[9], 0.35)], t_out=board_out)
    els.append(El(chip("STEP 1  ·  take log on both sides"), W / 2, 590, board_t, 0.4, **bd))
    els.append(El(tex(r"\log y = \log\,(x^{x})", MATH), W / 2, 700, C[6], 0.6, kind="wipe", **bd))
    els.append(El(tex(r"\log y = x\,\log x", MATH), W / 2, 820, at(6, 0.45), 0.6, kind="wipe", **bd))
    els.append(El(text_img("power comes down", font("Bold", 42), TEAL), W / 2, 890, E[6] - 0.2, t_out=C[8]))
    els.append(El(chip("STEP 2  ·  differentiate both sides"), W / 2, 960, C[7], 0.4, **bd))
    els.append(El(tex(r"\frac{1}{y}\,\frac{dy}{dx} = x\cdot\frac{1}{x} + \log x\cdot 1", MATH), W / 2, 1100, at(7, 0.4), 0.9, kind="wipe", **bd))
    els.append(El(text_img("product rule", font("Bold", 42), TEAL), W / 2, 1200, C[8], t_out=at(8, 0.55)))
    els.append(El(tex(r"\frac{1}{y}\,\frac{dy}{dx} = 1 + \log x", MATH), W / 2, 1255, at(8, 0.55), 0.6, kind="wipe", **bd))

    ans_m = tex(r"\frac{dy}{dx} = x^{x}\,(1 + \log x)", 84, NAVY)
    padx, pady = 56, 34
    bw2, bh2 = ans_m.width + 2 * padx, ans_m.height + 2 * pady
    box = Image.new("RGBA", (bw2 + 80, bh2 + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", box.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([30, 30, bw2 + 50, bh2 + 50], radius=36, fill=YEL + (150,))
    box.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    ImageDraw.Draw(box).rounded_rectangle([40, 40, bw2 + 40, bh2 + 40], radius=32, fill=YEL)
    box.alpha_composite(ans_m, dest=(40 + padx, 40 + pady))
    # answer box slides up to the top for the real-life part
    els.append(El(box, W / 2, 1450, at(9, 0.15), 0.5, kind="pop",
                  move=(board_out, board_out + 0.6, W / 2, 470, 0.72), t_out=C[13] - 0.3))

    # ---- Real life: set to zero -> 1/e -> 37% rule
    els.append(El(chip("REAL LIFE  ·  set dy/dx = 0"), W / 2, 640, C[10], 0.4, t_out=C[13] - 0.3))
    els.append(El(tex(r"1 + \log x = 0", MATH), W / 2, 750, C[10] + 0.25, 0.6, kind="wipe", t_out=C[13] - 0.3))
    els.append(El(tex(r"x = \frac{1}{e}", 92), W / 2 - 150, 900, at(10, 0.6), 0.5, kind="wipe", t_out=C[13] - 0.3))
    els.append(El(tex(r"\approx 0.37", 92, YEL), W / 2 + 140, 905, C[11], 0.4, kind="pop", t_out=C[13] - 0.3))
    house_row(els, 1150, C[11] + 0.1, stagger=0.04, t_out=C[13] - 0.3, band_t=C[12], star_t=at(12, 0.5), band_label=False)
    els.append(El(pill("= the 37% rule", font("Bold", 50), NAVY, YEL, padx=36, pady=18), W / 2, 1330, at(12, 0.45), 0.4, kind="pop", t_out=C[13] - 0.3))

    # ---- End card
    over.append(El(logo(1.6), W / 2, 820, C[13], 0.5, kind="pop"))
    over.append(El(text_img("Follow for daily Class 12 maths", font("Bold", 50), WHITE), W / 2, 960, C[13] + 0.15))
    over.append(El(text_img("JEE · NEET · Boards", font("Medium", 40), YEL), W / 2, 1040, C[13] + 0.3))
    web = pill("www.tutorda.org", font("Bold", 52), NAVY, YEL, padx=44, pady=22)
    over.append(El(web, W / 2, 1180, C[13] + 0.4, 0.4, kind="pop"))

    # ---- captions (one per voice clip, wrapped)
    cf = font("Bold", 44)
    for i, clip in enumerate(CLIPS):
        if i == len(CLIPS) - 1: break
        words, lines, cur = clip[2].replace("|", " ").split(), [], ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if cf.getlength(trial) > 880 and cur: lines.append(cur); cur = w_
            else: cur = trial
        lines.append(cur)
        lh = 60; boxw = int(max(cf.getlength(l) for l in lines)) + 64; boxh = lh * len(lines) + 34
        im = Image.new("RGBA", (boxw, boxh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, boxw - 1, boxh - 1], radius=22, fill=(0, 0, 0, 150))
        for k, l in enumerate(lines):
            d.text(((boxw - cf.getlength(l)) / 2, 14 + k * lh), l, font=cf, fill=WHITE)
        end = C[i + 1] - 0.02
        caps.append(El(im, W / 2, 1670, C[i] - 0.05, 0.15, t_out=end - 0.1, out_dur=0.1))
    return els, over, caps

def render_frame(t, BG, ELS, OVER, CAPS):
    fr = BG.copy()
    for e in ELS: e.draw(fr, t)
    q = ease_io(clamp((t - (C[13] - 0.3)) / 0.4))
    if q > 0: fr.alpha_composite(Image.new("RGBA", (W, H), BG1 + (int(215 * q),)))
    for e in OVER: e.draw(fr, t)
    for e in CAPS: e.draw(fr, t)
    ImageDraw.Draw(fr).rectangle([0, 0, int(W * clamp(t / DUR)), 9], fill=YEL)
    return fr.convert("RGB")

# ---------------- audio ----------------
SR = 24000
def build_audio(path, schedule=None, music_gain=0.75, music_dips=(), samples=None):
    N = int(DUR * SR); tt_all = np.arange(N) / SR
    rng = np.random.default_rng(7)
    def note(m): return 440.0 * 2 ** ((m - 69) / 12)
    def lowpass(x, fc):
        a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
        for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
        return y
    def add(buf, start, sig):
        i = int(start * SR); j = min(N, i + len(sig))
        if 0 <= i < N: buf[i:j] += sig[: j - i]

    # voice
    vo = np.zeros(N)
    for i in range(len(CLIPS)):
        a, sr = sf.read(f"{VO}/c{i:02d}.wav"); assert sr == SR
        add(vo, C[i], a)
    vo *= 0.92 / np.abs(vo).max()

    # music bed
    music = np.zeros(N); beat = 60 / 96; bar = 4 * beat
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    for b in range(int(np.ceil(DUR / bar))):
        ch = chords[b % 4]; t0 = b * bar
        L = int((bar + 0.6) * SR); tt = np.arange(L) / SR
        env = np.minimum(tt / 0.35, 1) * np.clip((bar + 0.6 - tt) / 0.6, 0, 1)
        pad = sum(np.sin(2 * np.pi * note(m) * tt) + 0.3 * np.sin(2 * np.pi * note(m) * 2.006 * tt) for m in ch)
        pad += 0.6 * np.sin(2 * np.pi * note(ch[0] - 12) * tt)
        add(music, t0, 0.035 * env * pad)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
        for k in range(8):
            f = note(arp[k % 4]); Lp = int(0.5 * SR); tp = np.arange(Lp) / SR
            add(music, t0 + k * beat / 2, 0.045 * np.sin(2 * np.pi * f * tp) * np.exp(-tp * 9) * (1 - np.exp(-tp * 400)))
    for b in range(int(DUR / beat)):
        if b % 2 == 0 and b * beat > C[2]:
            Lk = int(0.25 * SR); tk = np.arange(Lk) / SR
            f = 110 * np.exp(-tk * 25) + 45
            add(music, b * beat, 0.09 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 18))
    if os.environ.get("MUSIC") == "energetic":
        music = np.zeros(N); beat = 60 / 118; bar = 4 * beat
        prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]
        for b in range(int(np.ceil(DUR / bar))):
            ch = prog[b % 4]; t0 = b * bar
            L = int((bar + 0.3) * SR); tt = np.arange(L) / SR
            env = np.minimum(tt / 0.05, 1) * np.clip((bar + 0.3 - tt) / 0.3, 0, 1)
            pad = sum(np.sin(2 * np.pi * note(m) * tt) + 0.35 * np.sin(2 * np.pi * note(m) * 2.004 * tt) for m in ch[:3])
            add(music, t0, 0.022 * env * pad)
            for k in range(8):  # driving bass on 8ths
                Lb = int(beat / 2 * SR); tb = np.arange(Lb) / SR
                add(music, t0 + k * beat / 2, 0.11 * np.sin(2 * np.pi * note(ch[0] - 24) * tb) * np.exp(-tb * 6) * np.minimum(tb / 0.004, 1))
            arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 24, ch[1] + 12]
            for k in range(16):  # bright 16th plucks
                f = note(arp[k % 8]); Lp = int(0.25 * SR); tp = np.arange(Lp) / SR
                add(music, t0 + k * beat / 4, 0.03 * (np.sin(2 * np.pi * f * tp) + 0.3 * np.sin(4 * np.pi * f * tp)) * np.exp(-tp * 14) * np.minimum(tp / 0.002, 1))
        nb = int(DUR / beat)
        for b in range(nb):
            tb0 = b * beat
            if tb0 < C[0] + 0.2: continue
            Lk = int(0.22 * SR); tk = np.arange(Lk) / SR      # four-on-the-floor kick
            f = 140 * np.exp(-tk * 30) + 48
            add(music, tb0, 0.16 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 16))
            Lh = int(0.045 * SR); nh = rng.standard_normal(Lh); nh = nh - lowpass(nh, 6000)  # offbeat hat
            add(music, tb0 + beat / 2, 0.05 * nh * np.exp(-np.arange(Lh) / SR * 70))
            if b % 2 == 1:                                     # clap on 2 & 4
                Lc = int(0.14 * SR); nc = rng.standard_normal(Lc); nc = lowpass(nc - lowpass(nc, 900), 4000) * 2.5
                add(music, tb0, 0.09 * nc * np.exp(-np.arange(Lc) / SR * 24))
    if os.environ.get("MUSIC") == "cinematic":
        # brand-film score: cold ticking minor drone (sameness) -> drop + riser -> warm piano + pads that build to the tagline
        music = np.zeros(N); MC = [float(x) for x in os.environ.get("MUSIC_CUES", "7,9,35,46").split(",")]
        t_cold, t_rev, t_build, t_peak = MC
        def tone(f, L, harm=(1, .5, .25, .12), dec=3.0, att=0.004):
            tt = np.arange(int(L * SR)) / SR
            s = sum(a * np.sin(2 * np.pi * f * (k + 1) * tt * (1 + 0.0007 * k)) for k, a in enumerate(harm))
            return s * np.exp(-tt * dec) * np.minimum(tt / att, 1)
        def padc(ch, L, att=0.6):
            tt = np.arange(int(L * SR)) / SR
            s = sum(np.sin(2 * np.pi * note(m) * tt) + 0.3 * np.sin(2 * np.pi * note(m) * 1.003 * tt) + 0.15 * np.sin(2 * np.pi * note(m) * 2.001 * tt) for m in ch)
            return s * np.minimum(tt / att, 1) * np.clip((L - tt) / 0.8, 0, 1)
        # act 1: drone + clock tick
        L1 = t_cold + 1.2; tt = np.arange(int(L1 * SR)) / SR
        drone = (np.sin(2 * np.pi * note(33) * tt) + 0.6 * np.sin(2 * np.pi * note(40) * tt) + 0.3 * np.sin(2 * np.pi * note(45) * tt * 1.002))
        add(music, 0, 0.05 * drone * np.minimum(tt / 1.5, 1) * np.clip((L1 - tt) / 1.0, 0, 1))
        for k in range(int(t_cold / 0.5)):
            Lt = int(0.05 * SR); nt = rng.standard_normal(Lt); nt = nt - lowpass(nt, 3000)
            add(music, k * 0.5, (0.06 if k % 4 == 0 else 0.035) * nt * np.exp(-np.arange(Lt) / SR * 90))
        # riser into the reveal + impact
        Lr = t_rev - t_cold + 0.1; tr = np.arange(int(Lr * SR)) / SR
        nr = lowpass(rng.standard_normal(len(tr)), 2500)
        add(music, t_cold, 0.10 * nr * (tr / Lr) ** 2.5)
        Li = 2.5; ti = np.arange(int(Li * SR)) / SR; fi = 70 * np.exp(-ti * 3) + 38
        add(music, t_rev - 0.02, 0.32 * np.sin(2 * np.pi * np.cumsum(fi) / SR) * np.exp(-ti * 2.2))
        # act 2+: I-V-vi-IV in D, 96 bpm, piano arps; intensity rises at t_build, peaks at t_peak
        beat = 60 / 96; bar = 4 * beat
        prog = [[50, 54, 57, 62], [45, 49, 52, 57], [47, 50, 54, 59], [43, 47, 50, 55]]
        b = 0; t0 = t_rev
        while t0 < DUR:
            ch = prog[b % 4]; inten = 0.55 + 0.25 * (t0 >= t_build) + 0.25 * (t0 >= t_peak)
            add(music, t0, 0.020 * inten * padc([m + 12 for m in ch[1:]], bar + 0.8))
            add(music, t0, 0.07 * tone(note(ch[0] - 12), bar, (1, .3), dec=0.6, att=0.02))
            arp = [ch[0] + 12, ch[2] + 12, ch[3] + 12, ch[1] + 24, ch[3] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 12]
            for k in range(8):
                add(music, t0 + k * beat / 2, 0.042 * inten * tone(note(arp[k]), 1.2, dec=3.5))
            if t0 >= t_build:
                for k in range(4):   # soft pulse kick + shaker
                    Lk = int(0.25 * SR); tk = np.arange(Lk) / SR; fk = 100 * np.exp(-tk * 28) + 46
                    add(music, t0 + k * beat, 0.10 * np.sin(2 * np.pi * np.cumsum(fk) / SR) * np.exp(-tk * 14))
                    Lh = int(0.06 * SR); nh = rng.standard_normal(Lh); nh = nh - lowpass(nh, 7000)
                    add(music, t0 + k * beat + beat / 2, 0.03 * inten * nh * np.exp(-np.arange(Lh) / SR * 60))
            b += 1; t0 += bar
        # final sustained chord under the end card
        add(music, DUR - 3.2, 0.03 * padc([62, 66, 69, 74], 3.2, att=0.3))
    if os.environ.get("MUSIC_FILE"):
        # real score (e.g. ACE-Step) replaces the synth bed, matched to its loudness; synth clock ticks kept for the cold open
        ref = np.sqrt(np.mean(music[int(min(12, DUR / 2) * SR):] ** 2)) + 1e-9
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", os.environ.get("MUSIC_OFFSET", "0"), "-i", os.environ["MUSIC_FILE"],
                              "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
        sc = np.frombuffer(raw, np.float32).astype(np.float64)[:N]; sc = np.pad(sc, (0, N - len(sc)))
        sc *= ref / (np.sqrt(np.mean(sc[int(12 * SR):int(50 * SR)] ** 2)) + 1e-9) * float(os.environ.get("MUSIC_FILE_GAIN", "1.0"))
        tick = np.zeros(N); t_end = float(os.environ.get("TICK_UNTIL", "0"))
        for k in range(int(t_end / 0.5)):
            Lt = int(0.05 * SR); nt = rng.standard_normal(Lt); nt = nt - lowpass(nt, 3000)
            add(tick, k * 0.5, (0.05 if k % 4 == 0 else 0.03) * nt * np.exp(-np.arange(Lt) / SR * 90))
        music = sc + tick
    music *= np.minimum(tt_all / 0.3, 1) * np.clip((DUR - tt_all) / 1.2, 0, 1)

    # sfx
    sfx = np.zeros(N)
    def pop(t, f=880, v=0.22):
        L = int(0.12 * SR); tt = np.arange(L) / SR
        fr = f * (1 + 0.6 * np.exp(-tt * 60))
        add(sfx, t, v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 38))
    def chalk(t, d=0.6, v=0.08):
        L = int(d * SR); tt = np.arange(L) / SR; n = rng.standard_normal(L); n = n - lowpass(n, 1800)
        jit = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 11 * tt + rng.random() * 6))
        add(sfx, t, v * n * jit * np.minimum(tt / 0.03, 1) * np.clip((d - tt) / 0.15, 0, 1))
    def buzz(t):
        L = int(0.4 * SR); tt = np.arange(L) / SR
        s = lowpass(np.sign(np.sin(2 * np.pi * 140 * tt)) * 0.5 + np.sin(2 * np.pi * 147 * tt) * 0.5, 1400)
        add(sfx, t, 0.20 * s * np.minimum(tt / 0.01, 1) * np.clip((0.4 - tt) / 0.08, 0, 1))
    def whoosh(t, d=0.6, v=0.12):
        L = int(d * SR); tt = np.arange(L) / SR
        add(sfx, t, v * lowpass(rng.standard_normal(L), 900) * 3 * np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2)
    def ding(t, base=1046.5, v=0.18):
        L = int(1.5 * SR); tt = np.arange(L) / SR
        s = np.sin(2 * np.pi * base * tt) + 0.5 * np.sin(2 * np.pi * base * 1.5 * tt) + 0.25 * np.sin(2 * np.pi * base * 2 * tt)
        add(sfx, t, v * s * np.exp(-tt * 3.2) * np.minimum(tt / 0.005, 1))
    def shimmer(t):
        for i, m in enumerate([76, 79, 83, 88]): ding(t + i * 0.06, note(m), 0.045)

    if schedule is not None:
        def sample(t, name, v=1.0):
            add(sfx, t, v * samples[name])
        schedule(dict(pop=pop, chalk=chalk, buzz=buzz, whoosh=whoosh, ding=ding, shimmer=shimmer, note=note, sample=sample))
    else:
        for i in range(10): pop(C[0] + 0.3 + i * 0.07, 700 + 25 * i, 0.07)
        whoosh(at(0, 0.45) - 0.1, 0.5, 0.08); pop(at(0, 0.8), 1050, 0.14)
        pop(C[1], 1100, 0.2)
        whoosh(E[1], 0.5, 0.10); pop(at(2, 0.25), 650, 0.18)
        chalk(C[3] - 0.05, 0.5); buzz(at(3, 0.6))
        shimmer(C[4]); pop(C[5], 1100, 0.2)
        whoosh(board_t := C[6] - 0.55, 0.6, 0.12)
        chalk(C[6], 0.6); chalk(at(6, 0.45), 0.6)
        pop(C[7], 820, 0.12); chalk(at(7, 0.4), 0.9); chalk(at(8, 0.55), 0.6)
        ding(at(9, 0.15)); ding(at(9, 0.15) + 0.12, 1568, 0.1)
        whoosh(C[10] - 0.4, 0.6, 0.10); chalk(C[10] + 0.25, 0.6); chalk(at(10, 0.6), 0.5)
        pop(C[11], 1200, 0.2); shimmer(C[12]); pop(at(12, 0.5), 1300, 0.16)
        whoosh(C[13] - 0.45, 0.4, 0.08); shimmer(E[13] + 0.05)

    # duck music under the voice
    env = np.convolve((np.abs(vo) > 0.02).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = 1 - (0.45 if os.environ.get("MUSIC") == "energetic" else 0.55) * np.clip(env * 4, 0, 1)
    dip = np.ones(N)
    for (td, dd, db) in music_dips:
        i0, i1 = int(td * SR), int((td + dd) * SR); ramp = int(0.08 * SR)
        g = 10 ** (-db / 20)
        seg = np.ones(max(0, i1 - i0)) * g
        if len(seg) > 2 * ramp: seg[:ramp] = np.linspace(1, g, ramp); seg[-ramp:] = np.linspace(g, 1, ramp)
        dip[i0:i0 + len(seg)] *= seg[:max(0, N - i0)]
    mix = vo + music_gain * music * duck * dip + 0.8 * sfx
    mix *= 0.9 / np.abs(mix).max()
    pcm = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

if __name__ == "__main__":
    BG = make_bg(); ELS, OVER, CAPS = build()
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            render_frame(float(ts), BG, ELS, OVER, CAPS).save(f"p2_{ts}.png")
        print("C", [round(c, 2) for c in C], "DUR", DUR)
    else:
        out = sys.argv[2]
        build_audio(f"mix_{VO}.wav")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"mix_{VO}.wav",
                              "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                              "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out],
                             stdin=subprocess.PIPE)
        for i in range(NF):
            p.stdin.write(render_frame(i / FPS, BG, ELS, OVER, CAPS).tobytes())
        p.stdin.close(); p.wait(); print("done", NF, DUR)
