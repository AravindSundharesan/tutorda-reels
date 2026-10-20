"""TutorDA reel v4 (white theme): upgraded editing / motion graphics on the same script + energetic voice.
python3 reel3.py preview t1 t2 ...   -> chk/v3_sheet.png
python3 reel3.py build out.mp4       -> parallel render + audio
"""
import os, sys, math, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("CLIPS", os.path.join(KIT, "topics/x_power_x/clips.json"))
os.environ.setdefault("VO", os.path.join(KIT, "topics/x_power_x/vo"))
os.environ.setdefault("MUSIC", "energetic")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import reel2 as R
from reel2 import (W, H, FPS, C, E, at, DUR, NF, CLIPS, tex, text_img, pill, ink_runs, logo, star,
                   spring, EXPO_OUT, clamp, ease_out, ease_io, El, font, YEL, TEAL, RED, NAVY, WHITE, MUTED)

INK = (15, 23, 42); INK2 = (71, 85, 105); AMBER = (217, 119, 6); AMBER_D = (180, 83, 9)
TEAL_D = (13, 148, 136); RED_D = (229, 72, 77)

def logo_light(scale=1.0):
    im = logo(scale); a = np.array(im)
    tile = int(76 * scale) + 2
    sub = a[:, tile:]; white = (sub[..., 0] > 200) & (sub[..., 1] > 200) & (sub[..., 2] > 200)
    yel = (sub[..., 0] > 200) & (sub[..., 1] > 150) & (sub[..., 2] < 120)
    sub[white, :3] = INK; sub[yel, :3] = AMBER; a[:, tile:] = sub
    return Image.fromarray(a)

# ---------------- key times ----------------
# defaults for the x^x script (14 clips); other reels overwrite these after import.
_n = len(C) - 1; _c = lambda i: C[min(i, _n)]
T1 = E[1] + 0.15            # whip: hook -> problem
BOARD_T = _c(6) - 0.25      # glide into solution board
REAL_T = _c(10) - 0.35      # board -> real life
END_T = _c(13) - 0.3        # end card
X_T = at(min(3, _n), 0.6)   # red X
ANS_T = at(min(9, _n), 0.15)  # answer box
STAR_T = at(0, 0.8)

# ---------------- small helpers ----------------
def text_line(s, f, color):
    """Baseline-consistent text (full ascent/descent height) so pieces line up."""
    asc, desc = f.getmetrics()
    w = int(f.getlength(s)) + 4
    im = Image.new("RGBA", (w, asc + desc), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), s, font=f, fill=color)
    return im

def radial(r, color, a0, power=2.0):
    y, x = np.mgrid[-r:r, -r:r]
    d = np.sqrt(x * x + y * y) / r
    arr = np.zeros((2 * r, 2 * r, 4), np.uint8)
    arr[..., :3] = color
    arr[..., 3] = (np.clip(1 - d, 0, 1) ** power * a0).astype(np.uint8)
    return Image.fromarray(arr)

def comp(frame, im, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0.004: return
    if abs(scale - 1) > 0.003:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 1:
        a = np.array(im); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); im = Image.fromarray(a)
    x = int(round(cx - im.width / 2)); y = int(round(cy - im.height / 2))
    if x >= frame.width or y >= frame.height or x + im.width <= 0 or y + im.height <= 0: return
    frame.alpha_composite(im, dest=(max(x, 0), max(y, 0)), source=(max(-x, 0), max(-y, 0)))

# ---------------- backgrounds ----------------
PAL = [((252, 250, 255), (238, 232, 255)),  # hook: lavender white
       ((253, 254, 255), (232, 240, 255)),  # problem: cool white
       ((251, 255, 254), (226, 246, 241)),  # solution: mint white
       ((252, 250, 255), (238, 232, 255)),  # real life: lavender white
       ((255, 254, 250), (255, 243, 214))]  # end: warm white

def make_grad(top, bot):
    g = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(top) * (1 - g) + np.array(bot) * g) * np.ones((H, W, 3))
    im = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(grid)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(15, 23, 42, 9))
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(15, 23, 42, 9))
    im.alpha_composite(grid)
    return im

BLOBS = [radial(420, (120, 140, 255), 55), radial(380, (190, 120, 250), 45), radial(360, (45, 212, 191), 45)]
SYMS = []
def build_symbols():
    rng = np.random.default_rng(11)
    pieces = [r"\int", r"\pi", r"\Sigma", r"\sqrt{x}", r"e^{x}", r"dx", r"\infty", r"\log", r"f(x)",
              r"\theta", r"\frac{dy}{dx}", r"x^{2}", r"\Delta", r"\lim", r"\alpha", r"\int_0^1"]
    for i, p in enumerate(pieces):
        size = int(rng.uniform(46, 110))
        im = tex(p, size, (40, 50, 100))
        a = np.array(im); a[..., 3] = (a[..., 3] * rng.uniform(0.06, 0.11)).astype(np.uint8)
        SYMS.append(dict(img=Image.fromarray(a), x=rng.uniform(60, W - 60), y=rng.uniform(0, H),
                         v=8 + size * 0.22, amp=rng.uniform(10, 30), fq=rng.uniform(0.15, 0.4), ph=rng.uniform(0, 6)))

def background(t):
    bounds = [T1, BOARD_T, REAL_T, END_T]
    idx = sum(t >= b for b in bounds)
    bg = BGS[idx]
    for k, b in enumerate(bounds[1:], start=1):   # T1 is a hard cut hidden by the whip
        if b <= t < b + 0.6:
            bg = Image.blend(BGS[k], BGS[k + 1], ease_io((t - b) / 0.6))
    fr = bg.copy()
    pos = [(W * 0.25 + 170 * math.sin(0.21 * t), H * 0.28 + 230 * math.sin(0.15 * t + 1.0)),
           (W * 0.78 + 150 * math.sin(0.17 * t + 2.0), H * 0.62 + 260 * math.sin(0.12 * t + 0.4)),
           (W * 0.5 + 220 * math.sin(0.13 * t + 4.0), H * 0.9 + 140 * math.sin(0.19 * t + 2.2))]
    for b, (x, y) in zip(BLOBS, pos): comp(fr, b, x, y)
    for s in SYMS:
        y = (s["y"] - s["v"] * t) % (H + 240) - 120
        x = s["x"] + s["amp"] * math.sin(s["fq"] * 2 * math.pi * t + s["ph"])
        comp(fr, s["img"], x, y)
    return fr

# ---------------- dynamic graphic elements (pure functions of t) ----------------
class Dyn:
    def draw(self, frame, t): pass

class WEl(El):
    """El with a glowing pen tip riding the handwriting wipe."""
    GLOW = None
    def draw(self, frame, t):
        super().draw(frame, t)
        if self.kind != "wipe" or t < self.t_in: return
        if self.t_out is not None and t > self.t_out: return
        p = clamp((t - self.t_in) / self.dur)
        if not 0.01 < p < 0.97: return
        wipe = EXPO_OUT(p); w = self.img.width
        x = self.cx - w / 2 + wipe * (w + 60) - 30
        comp(frame, WEl.GLOW, min(x, self.cx + w / 2), self.cy, alpha=1 - p ** 3)

class Counter(Dyn):
    def __init__(self, imgs, cx, cy, t0, dur, t_out=None, out_dur=0.02, anchor="center"):
        self.imgs, self.cx, self.cy, self.t0, self.dur, self.t_out, self.od = imgs, cx, cy, t0, dur, t_out, out_dur
    def draw(self, frame, t):
        if t < self.t0 or (self.t_out is not None and t > self.t_out + self.od): return
        k = int(round((len(self.imgs) - 1) * EXPO_OUT(clamp((t - self.t0) / self.dur))))
        sc = 1 + 0.08 * math.exp(-max(0, t - self.t0 - self.dur) * 8) * (k == len(self.imgs) - 1)
        comp(frame, self.imgs[k], self.cx, self.cy, alpha=EXPO_OUT(clamp((t - self.t0) / 0.2)), scale=sc)

class Magnifier(Dyn):
    def __init__(self, xs, cy, t_a, t_b, t_jump, x_jump, t_out):
        self.xs, self.cy, self.ta, self.tb, self.tj, self.xj, self.to = xs, cy, t_a, t_b, t_jump, x_jump, t_out
        im = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.line([(80, 80), (128, 128)], fill=INK, width=14)
        d.ellipse([12, 12, 96, 96], fill=(120, 160, 255, 60), outline=INK, width=8)
        d.arc([26, 26, 70, 70], 200, 260, fill=(255, 255, 255, 230), width=5)
        self.img = im
    def draw(self, frame, t):
        if t < self.ta - 0.25 or t > self.to: return
        q = EXPO_OUT(clamp((t - self.ta) / (self.tb - self.ta)))
        x = self.xs[0] + (self.xs[-1] - self.xs[0]) * q
        if t > self.tj: x = self.xs[-1] + (self.xj - self.xs[-1]) * spring(t - self.tj, 0.3, 0.35)
        hop = 18 * abs(math.sin(q * math.pi * 3)) if t < self.tb else 0
        sc = math.exp(math.log(0.5) * (1 - spring(t - (self.ta - 0.25), 0.35, 0.4)))
        comp(frame, self.img, x + 22, self.cy - 10 - hop, alpha=clamp((t - self.ta + 0.25) / 0.15), scale=sc)

class Confetti(Dyn):
    COLS = [YEL, TEAL, RED, (37, 99, 235), (140, 90, 240), (255, 120, 190)]
    def __init__(self, t0, x, y, n=90, seed=1, speed=(700, 1500), cone=(-170, -10)):
        r = np.random.default_rng(seed)
        ang = np.radians(r.uniform(cone[0], cone[1], n)); sp = r.uniform(*speed, n)
        self.vx, self.vy = np.cos(ang) * sp, np.sin(ang) * sp
        self.sz = r.uniform(9, 17, n); self.spin = r.uniform(-14, 14, n); self.ph = r.uniform(0, 6, n)
        self.col = [self.COLS[i % len(self.COLS)] for i in r.integers(0, 60, n)]
        self.t0, self.x, self.y, self.n = t0, x, y, n
    def draw(self, frame, t):
        el = t - self.t0
        if el < 0 or el > 2.4: return
        d = ImageDraw.Draw(frame)
        k = 2.2; f = (1 - math.exp(-k * el)) / k
        shrink = clamp(1 - (el - 1.6) / 0.8)
        for i in range(self.n):
            x = self.x + self.vx[i] * f + 22 * math.sin(6 * el + self.ph[i])
            y = self.y + self.vy[i] * f + 0.5 * 900 * el * el
            if y > H + 40: continue
            a = self.spin[i] * el + self.ph[i]; s = self.sz[i] * shrink
            hw, hh = s, s * 0.55 * abs(math.cos(a * 0.7)) + 1.5
            ca, sa = math.cos(a), math.sin(a)
            pts = [(x + ca * dx - sa * dy, y + sa * dx + ca * dy) for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
            d.polygon(pts, fill=self.col[i] + (255,))

class RoughEllipse(Dyn):
    def __init__(self, cx, cy, rx, ry, t0, dur, t_out, color=YEL, seed=3):
        r = np.random.default_rng(seed); pts = []
        for loop in range(2):
            for k in range(70):
                a = -2.4 + loop * 0.35 + k / 69 * 2 * math.pi * (1.08 if loop == 0 else 0.98)
                j = 1 + r.normal(0, 0.018)
                pts.append((cx + rx * j * math.cos(a) + loop * 4, cy + ry * j * math.sin(a) - loop * 3))
        self.pts, self.t0, self.dur, self.to, self.col = pts, t0, dur, t_out, color
    def draw(self, frame, t):
        if t < self.t0 or t > self.to: return
        n = max(2, int(len(self.pts) * EXPO_OUT(clamp((t - self.t0) / self.dur))))
        ImageDraw.Draw(frame).line(self.pts[:n], fill=self.col + (255,), width=7, joint="curve")

class Shine(Dyn):
    def __init__(self, box_img, cx, cy, t0, dur=0.7):
        self.mask = np.array(box_img)[..., 3].astype(np.float32) / 255
        self.cx, self.cy, self.t0, self.dur = cx, cy, t0, dur
        h, w = self.mask.shape; yy, xx = np.mgrid[0:h, 0:w]; self.diag = xx + yy * 0.5
    def draw(self, frame, t):
        el = t - self.t0
        if el < 0 or el > self.dur: return
        h, w = self.mask.shape
        u = -0.2 * w + (w * 1.6) * ease_io(el / self.dur)
        band = np.exp(-((self.diag - u) / 46) ** 2) * 150 * self.mask
        arr = np.zeros((h, w, 4), np.uint8); arr[..., :3] = 255; arr[..., 3] = band.astype(np.uint8)
        comp(frame, Image.fromarray(arr), self.cx, self.cy)

class Pulse(Dyn):
    def __init__(self, sprite, cx, cy, t0, dur=0.9, peak=1.0):
        self.s, self.cx, self.cy, self.t0, self.dur, self.peak = sprite, cx, cy, t0, dur, peak
    def draw(self, frame, t):
        el = t - self.t0
        if el < 0 or el > self.dur: return
        a = self.peak * EXPO_OUT(clamp(el / 0.12)) * (1 - ease_io(clamp((el - 0.12) / (self.dur - 0.12))))
        comp(frame, self.s, self.cx, self.cy, alpha=a, scale=0.85 + 0.3 * el / self.dur)

class Rings(Dyn):
    def __init__(self, cx, cy, t0):
        self.cx, self.cy, self.t0 = cx, cy, t0
    def draw(self, frame, t):
        el = t - self.t0
        if el < 0: return
        ov = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for k in range(3):
            f = ((el - k * 0.45) % 1.35) / 1.35
            if el - k * 0.45 < 0: continue
            r = 140 + 300 * EXPO_OUT(f); a = int(150 * (1 - f))
            d.ellipse([450 - r, 450 - r, 450 + r, 450 + r], outline=AMBER + (a,), width=5)
        comp(frame, ov, self.cx, self.cy)

class Karaoke(Dyn):
    def __init__(self, i, cy=1670):
        txt = CLIPS[i][2]; f = font("Bold", 50); words = txt.split()
        lines, cur = [], []
        for w_ in words:
            trial = " ".join(cur + [w_])
            if f.getlength(trial) > 900 and cur: lines.append(cur); cur = [w_]
            else: cur.append(w_)
        lines.append(cur)
        lh = 66; bw = int(max(f.getlength(" ".join(l)) for l in lines)) + 70; bh = lh * len(lines) + 36
        base = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(base)
        d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=26, fill=(15, 23, 42, 235))
        self.wpos, self.wimg = [], []
        for li, l in enumerate(lines):
            x = (bw - f.getlength(" ".join(l))) / 2; y = 16 + li * lh
            for w_ in l:
                d.text((x, y), w_, font=f, fill=WHITE)
                self.wpos.append((x, y)); self.wimg.append(text_line(w_, f, YEL))
                x += f.getlength(w_ + " ")
        self.base, self.cy = base, cy
        wts = np.array([len(w_) + 2.5 for w_ in words], float); cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum()
        self.starts = C[i] + cum[:-1] * (E[i] - C[i])
        self.t0 = C[i] - 0.05
        self.t1 = (C[i + 1] - 0.03) if i + 1 < len(C) else E[i] + 0.3
    def draw(self, frame, t):
        if t < self.t0 or t >= self.t1: return
        k = int(np.searchsorted(self.starts, t, side="right")) - 1
        im = self.base.copy()
        if k >= 0:
            x, y = self.wpos[k]; im.alpha_composite(self.wimg[k], dest=(int(x), int(y)))
        sc = 0.9 + 0.1 * spring(t - self.t0, 0.3, 0.3)
        comp(frame, im, W / 2, self.cy, alpha=EXPO_OUT(clamp((t - self.t0) / 0.12)), scale=sc)

def house2(w, roof, lit=True, wall=(64, 80, 128)):
    h = int(w * 1.1); o = 8
    im = Image.new("RGBA", (w + 2 * o, h + 2 * o), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rh = int(h * 0.42)
    dark = tuple(int(c * 0.7) for c in roof)
    d.rectangle([o + w * 0.66, o + rh * 0.1, o + w * 0.8, o + rh * 0.75], fill=dark)
    d.polygon([(o - 5, o + rh), (o + w / 2, o), (o + w + 5, o + rh)], fill=roof)
    d.rounded_rectangle([o + w * 0.1, o + rh - 2, o + w * 0.9, o + h], radius=6, fill=wall)
    d.rounded_rectangle([o + w * 0.2, o + rh + w * 0.1, o + w * 0.42, o + rh + w * 0.32], radius=3,
                        fill=(255, 214, 120) if lit else (40, 50, 80))
    d.rounded_rectangle([o + w * 0.54, o + h * 0.62, o + w * 0.76, o + h], radius=4, fill=(28, 34, 62))
    return im

ROOFS = [(120, 140, 210), (160, 120, 210), (100, 170, 200), (180, 130, 190), (120, 160, 220),
         (150, 120, 200), (110, 160, 190), (170, 140, 210), (120, 130, 200), (150, 150, 220)]

# ---------------- scene ----------------
def build():
    global BGS
    BGS = [make_grad(*p) for p in PAL]
    build_symbols()
    WEl.GLOW = radial(34, (255, 176, 20), 230, power=1.6)
    content, ui, fx = [], [], []
    MATH = 70
    n, hw, sp = 10, 76, 92
    x0 = W / 2 - (n - 1) * sp / 2

    # ===== UI layer (not affected by camera) =====
    ui.append(El(logo_light(1.0), W / 2, 118, 0.0, 0.5, t_out=END_T))
    ui.append(El(text_img("CLASS 12 MATHS  ·  DIFFERENTIATION", font("Bold", 36), INK2), W / 2, 205, 0.15, 0.5, t_out=END_T))
    ui.append(El(text_img("www.tutorda.org", font("Bold", 40), INK2), W / 2, 1790, 0.2, 0.5, t_out=END_T))
    for i in range(len(CLIPS) - 1): ui.append(Karaoke(i))

    # ===== HOOK =====
    hook_out = T1 - 0.02
    fT = font("Bold", 100)
    the, rule, num = text_line("The ", fT, INK), text_line(" Rule", fT, INK), text_line("37%", fT, AMBER)
    total = the.width + num.width + rule.width; xs = W / 2 - total / 2
    content.append(El(the, xs + the.width / 2, 395, C[0], 0.45, t_out=hook_out, out_dur=0.02))
    content.append(Counter([text_line(f"{k}%", fT, AMBER) for k in range(38)], xs + the.width + num.width / 2, 395,
                           C[0] + 0.15, 0.9, t_out=hook_out))
    content.append(El(rule, xs + the.width + num.width + rule.width / 2, 395, C[0] + 0.05, 0.45, t_out=hook_out, out_dur=0.02))
    content.append(El(text_img("Hunting for a flat or PG?", font("Medium", 48), INK2), W / 2, 510, C[0] + 0.25, t_out=hook_out, out_dur=0.02))
    HY = 760
    t_a, t_b = at(0, 0.42), at(0, 0.74)
    for i in range(n):
        visit = t_a + (i / 3) * (t_b - t_a) + 0.12 if i < 4 else None
        content.append(El(house2(hw, ROOFS[i]), x0 + i * sp, HY, C[0] + 0.3 + i * 0.06, 0.4, kind="pop",
                          t_out=hook_out, out_dur=0.02, dims=[(visit, 0.45)] if visit else ()))
    left = x0 - sp / 2; right = left + 0.37 * n * sp
    band = Image.new("RGBA", (int(right - left), 160), (0, 0, 0, 0))
    ImageDraw.Draw(band).rounded_rectangle([0, 0, band.width - 1, 159], radius=26, fill=TEAL + (45,), outline=TEAL_D + (230,), width=5)
    content.append(El(band, (left + right) / 2, HY + 4, t_a - 0.1, 0.5, kind="wipe", t_out=hook_out, out_dur=0.02))
    lab = text_img("first 37%: just look", font("Bold", 44), TEAL_D)
    content.append(El(lab, max(left + lab.width / 2, 85 + lab.width / 2), HY + 125, t_a + 0.1, t_out=hook_out, out_dur=0.02))
    sx = x0 + 5 * sp
    content.append(El(house2(hw, (255, 214, 90), wall=(255, 190, 60)), sx, HY, STAR_T, 0.4, kind="pop", t_out=hook_out, out_dur=0.02))
    content.append(Pulse(radial(150, YEL, 120), sx, HY, STAR_T, 1.0))
    content.append(El(star(34), sx, HY - 100, STAR_T + 0.1, 0.4, kind="pop", t_out=hook_out, out_dur=0.02))
    lab2 = text_img("then pick the next better one", font("Bold", 44), AMBER_D)
    content.append(El(lab2, min(sx, W - lab2.width / 2 - 85), HY + 185, STAR_T + 0.15, t_out=hook_out, out_dur=0.02))
    content.append(Magnifier([x0 + i * sp for i in range(4)], HY, t_a, t_b, STAR_T - 0.05, sx, hook_out))
    content.append(El(pill("WHY 37%?", font("Bold", 72), NAVY, YEL, padx=50, pady=24), W / 2, 1180, C[1], 0.45, kind="pop", t_out=hook_out, out_dur=0.02))

    # ===== PROBLEM + TRAP =====
    q_out = C[4]
    content.append(El(text_img("Find dy/dx if", font("Bold", 72), INK), W / 2, 385, T1 + 0.05, t_out=q_out))
    big_w = tex(r"y = x^{x}", 220, INK)
    runs = ink_runs(big_w); bx0, bx1 = runs[-2]; sx0, sx1 = runs[-1]
    col = np.array(big_w).copy(); col[:, bx0:bx1, :3] = TEAL_D; col[:, sx0:sx1, :3] = AMBER
    big_c = Image.fromarray(col)
    BIG_CY = 570
    mv = (BOARD_T - 0.3, BOARD_T + 0.3, W / 2, 440, 0.48)
    board_out = REAL_T
    content.append(El(big_w, W / 2, BIG_CY, at(2, 0.2), 0.5, kind="pop", dims=[(C[9], 0.35)], move=mv, t_out=board_out))
    content.append(El(big_c, W / 2, BIG_CY, C[4], 0.5, dims=[(C[9], 0.35)], move=mv, t_out=board_out))
    pr_out = C[4] - 0.05
    content.append(El(text_img("Power rule?", font("Bold", 54), INK2), W / 2, 830, C[3] - 0.1, t_out=pr_out))
    pr = tex(r"\frac{dy}{dx} = x\cdot x^{x-1}", 76, INK)
    content.append(WEl(pr, W / 2, 975, C[3] - 0.05, 0.5, kind="wipe", t_out=pr_out))
    xw, xh = pr.width + 70, pr.height + 60
    X = Image.new("RGBA", (xw, xh), (0, 0, 0, 0)); d = ImageDraw.Draw(X)
    for (p0, p1) in [((16, 16), (xw - 16, xh - 16)), ((xw - 16, 16), (16, xh - 16))]:
        d.line([p0, p1], fill=RED_D + (240,), width=18)
    content.append(El(X, W / 2, 975, X_T, 0.35, kind="pop", t_out=pr_out))
    content.append(Pulse(radial(260, RED, 110), W / 2, 975, X_T, 0.6))
    content.append(El(pill("WRONG", font("Bold", 40), WHITE, RED, padx=26, pady=12), W / 2 + 330, 875, X_T + 0.1, 0.3, kind="pop", t_out=pr_out))
    # base / power annotations
    bw_, bh_ = big_w.size; lft = W / 2 - bw_ / 2; top = BIG_CY - bh_ / 2
    base_cx = lft + (bx0 + bx1) / 2; sup_cx = lft + (sx0 + sx1) / 2
    ann_out = BOARD_T - 0.4
    stem = Image.new("RGBA", (24, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(stem)
    d.line([(12, 0), (12, 100)], fill=TEAL_D, width=6); d.ellipse([3, 90, 21, 108], fill=TEAL_D)
    content.append(El(stem, base_cx, top + bh_ + 40, C[4] + 0.15, t_out=ann_out))
    content.append(El(text_img("base changes", font("Bold", 46), TEAL_D), base_cx, top + bh_ + 128, C[4] + 0.15, t_out=ann_out))
    lab = text_img("power changes", font("Bold", 46), AMBER_D)
    content.append(El(lab, min(sup_cx, W - lab.width / 2 - 85), top - 120, C[4] + 0.5, t_out=ann_out))
    arr = Image.new("RGBA", (24, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(arr)
    d.line([(12, 0), (12, 62)], fill=AMBER, width=6); d.ellipse([3, 52, 21, 70], fill=AMBER)
    content.append(El(arr, sup_cx, top - 50, C[4] + 0.5, t_out=ann_out))
    content.append(El(pill("TRICK:  take log first", font("Bold", 56), NAVY, YEL, padx=44, pady=24), W / 2, 1080, C[5], 0.4, kind="pop", t_out=ann_out))
    content.append(Pulse(radial(300, YEL, 70), W / 2, 1080, C[5], 0.8))

    # ===== SOLUTION BOARD (glass card) =====
    card = Image.new("RGBA", (1000, 860), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, 979, 849], radius=40, fill=(15, 23, 42, 40))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    ImageDraw.Draw(card).rounded_rectangle([20, 20, 979, 839], radius=40, fill=(255, 255, 255, 225), outline=(15, 23, 42, 22), width=2)
    content.append(El(card, W / 2, 920, BOARD_T, 0.5, t_out=board_out))
    chip_f = font("Bold", 40)
    def chip(s): return pill(s, chip_f, AMBER_D, (255, 200, 61, 70), padx=26, pady=12, outline=AMBER + (170,))
    bd = dict(dims=[(C[9], 0.35)], t_out=board_out)
    content.append(El(chip("STEP 1  ·  take log on both sides"), W / 2, 590, BOARD_T, 0.4, **bd))
    content.append(WEl(tex(r"\log y = \log\,(x^{x})", MATH, INK), W / 2, 700, C[6], 0.6, kind="wipe", **bd))
    content.append(WEl(tex(r"\log y = x\,\log x", MATH, INK), W / 2, 820, at(6, 0.45), 0.6, kind="wipe", **bd))
    content.append(El(text_img("power comes down", font("Bold", 42), TEAL_D), W / 2, 890, E[6] - 0.2, t_out=C[8]))
    content.append(El(chip("STEP 2  ·  differentiate both sides"), W / 2, 960, C[7], 0.4, **bd))
    content.append(WEl(tex(r"\frac{1}{y}\,\frac{dy}{dx} = x\cdot\frac{1}{x} + \log x\cdot 1", MATH, INK), W / 2, 1100, at(7, 0.4), 0.9, kind="wipe", **bd))
    content.append(El(text_img("product rule", font("Bold", 42), TEAL_D), W / 2, 1200, C[8], t_out=at(8, 0.55)))
    content.append(WEl(tex(r"\frac{1}{y}\,\frac{dy}{dx} = 1 + \log x", MATH, INK), W / 2, 1255, at(8, 0.55), 0.6, kind="wipe", **bd))
    # answer box
    ans_m = tex(r"\frac{dy}{dx} = x^{x}\,(1 + \log x)", 86, NAVY)
    padx, pady = 56, 34
    bw2, bh2 = ans_m.width + 2 * padx, ans_m.height + 2 * pady
    box = Image.new("RGBA", (bw2 + 80, bh2 + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", box.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([30, 30, bw2 + 50, bh2 + 50], radius=36, fill=YEL + (160,))
    box.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    inner = Image.new("RGBA", box.size, (0, 0, 0, 0))
    ImageDraw.Draw(inner).rounded_rectangle([40, 40, bw2 + 40, bh2 + 40], radius=32, fill=YEL)
    box.alpha_composite(inner); box.alpha_composite(ans_m, dest=(40 + padx, 40 + pady))
    content.append(Pulse(radial(420, (255, 220, 120), 120), W / 2, 1450, ANS_T, 1.0))
    content.append(Confetti(ANS_T + 0.05, W / 2, 1450, n=90, seed=5))
    content.append(El(box, W / 2, 1450, ANS_T, 0.5, kind="pop", move=(board_out, board_out + 0.6, W / 2, 470, 0.72), t_out=END_T))
    content.append(Shine(inner, W / 2, 1450, ANS_T + 0.45))

    # ===== REAL LIFE =====
    r_out = END_T
    content.append(El(chip("REAL LIFE  ·  set dy/dx = 0"), W / 2, 640, C[10], 0.4, t_out=r_out))
    content.append(WEl(tex(r"1 + \log x = 0", 76, INK), W / 2, 755, C[10] + 0.25, 0.6, kind="wipe", t_out=r_out))
    content.append(WEl(tex(r"x = \frac{1}{e}", 96, INK), W / 2 - 160, 905, at(10, 0.6), 0.5, kind="wipe", t_out=r_out))
    nums = [tex(r"\approx %.2f" % (k / 100), 96, AMBER) for k in range(38)]
    NX, NY = W / 2 + 150, 910
    content.append(Counter(nums, NX, NY, C[11], 0.7, t_out=r_out))
    content.append(RoughEllipse(NX + 8, NY, nums[-1].width / 2 + 40, nums[-1].height / 2 + 34, at(11, 0.55), 0.55, r_out, color=AMBER))
    RY = 1150
    for i in range(n):
        content.append(El(house2(hw, ROOFS[i]), x0 + i * sp, RY, C[11] + 0.1 + i * 0.035, 0.4, kind="pop", t_out=r_out,
                          dims=[(C[12] + 0.1, 0.45)] if i < 4 else ()))
    band2 = band.copy()
    content.append(El(band2, (left + right) / 2, RY + 4, C[12], 0.5, kind="wipe", t_out=r_out))
    content.append(El(house2(hw, (255, 214, 90), wall=(255, 190, 60)), sx, RY, at(12, 0.45), 0.4, kind="pop", t_out=r_out))
    content.append(El(star(34), sx, RY - 100, at(12, 0.5), 0.4, kind="pop", t_out=r_out))
    content.append(Confetti(at(12, 0.5), W / 2, 1340, n=80, seed=9))
    content.append(El(pill("= the 37% rule", font("Bold", 56), NAVY, YEL, padx=40, pady=20), W / 2, 1340, at(12, 0.45), 0.4, kind="pop", t_out=r_out))

    # ===== END CARD =====
    end = []
    end.append(Rings(W / 2, 800, C[13] + 0.1))
    end.append(El(logo_light(1.75), W / 2, 800, C[13], 0.5, kind="pop"))
    end.append(El(text_img("Follow for daily Class 12 maths", font("Bold", 54), INK), W / 2, 960, C[13] + 0.15))
    end.append(El(text_img("JEE  ·  NEET  ·  Boards", font("Bold", 44), AMBER_D), W / 2, 1045, C[13] + 0.3))
    web = pill("www.tutorda.org", font("Bold", 58), NAVY, YEL, padx=48, pady=24)
    end.append(El(web, W / 2, 1190, C[13] + 0.4, 0.4, kind="pop"))
    end.append(Confetti(C[13] + 0.1, 60, 300, n=70, seed=13, speed=(700, 1500), cone=(-75, -15)))
    end.append(Confetti(C[13] + 0.1, W - 60, 300, n=70, seed=14, speed=(700, 1500), cone=(-165, -105)))
    return content, ui, fx, end

# ---------------- camera, transitions, finishing ----------------
PUNCH = [(STAR_T, 0.035, (W / 2, 760), False), (X_T, 0.05, (W / 2, 900), True),
         (_c(5), 0.03, (W / 2, 1000), False), (ANS_T, 0.05, (W / 2, 1450), False),
         (_c(11), 0.05, (W / 2 + 150, 910), False), (at(min(12, _n), 0.45), 0.035, (W / 2, 1250), False)]

def bump(el):
    if el < 0: return 0.0
    return EXPO_OUT(min(el / 0.16, 1)) * math.exp(-max(el - 0.16, 0) * 2.0)

def camera(fr, t):
    s = 1.025 + 0.015 * math.sin(2 * math.pi * t / 11)
    fx, fy = W / 2, H / 2 - 40
    shx = shy = 0.0
    for (t0, amp, (px, py), shake) in PUNCH:
        b = bump(t - t0); s += amp * b
        fx += (px - W / 2) * b * 0.55; fy += (py - (H / 2 - 40)) * b * 0.55
        el = t - t0
        if shake and 0 < el < 0.45:
            shx += 16 * math.exp(-el * 8) * math.sin(el * 75); shy += 11 * math.exp(-el * 8) * math.cos(el * 58)
    if t > END_T: s = 1 + (s - 1) * (1 - ease_io(clamp((t - END_T) / 0.6)))  # settle for the end card
    cw, ch = W / s, H / s
    l = clamp(fx - cw / 2 + shx, 0, W - cw); tp = clamp(fy - ch / 2 + shy, 0, H - ch)
    return fr.resize((W, H), Image.BILINEAR, box=(l, tp, l + cw, tp + ch))

def whip(fr, t, T, span=0.2):
    d = t - T
    if abs(d) >= span: return fr
    q = (d + span) / span if d < 0 else 1 - d / span
    dx = int(-(q ** 2) * W * 0.7) if d < 0 else int((q ** 2) * W * 0.7)
    a = np.roll(np.asarray(fr), dx, axis=1).astype(np.float32)
    L = int(8 + 220 * q)
    pad = np.pad(a, ((0, 0), (L, L), (0, 0)), mode="edge")
    c = np.cumsum(pad, axis=1)
    out = (c[:, 2 * L:2 * L + W] - c[:, 0:W]) / (2 * L)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def flash(fr, t, T, dur=0.25):
    d = t - T
    if not 0 <= d < dur: return fr
    a = int(150 * (1 - d / dur))
    return Image.blend(fr, Image.new(fr.mode, fr.size, (255, 246, 220)), a / 255)

VIGNETTE = None; GRAIN = []
def finishing_assets():
    global VIGNETTE, GRAIN
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    v = np.zeros((H, W, 4), np.uint8); v[..., :3] = INK; v[..., 3] = (np.clip(d - 0.6, 0, 1) ** 1.6 * 70).astype(np.uint8)
    VIGNETTE = Image.fromarray(v)
    r = np.random.default_rng(2)
    for _ in range(6):
        g = np.zeros((H, W, 4), np.uint8); n = r.integers(0, 256, (H, W), dtype=np.uint8)
        g[..., 0] = g[..., 1] = g[..., 2] = n; g[..., 3] = 5
        GRAIN.append(Image.fromarray(g))
    # vignette + grain pre-merged ('over' is associative): one full-frame composite per frame instead of two
    GRAIN = [Image.alpha_composite(VIGNETTE, g) for g in GRAIN]

SCENE = None
def init():
    global SCENE
    if SCENE is None:
        SCENE = build(); finishing_assets()

def render(t):
    content, ui, fx, end = SCENE
    fr = background(t)
    for e in content: e.draw(fr, t)
    for e in fx: e.draw(fr, t)
    q = ease_io(clamp((t - END_T) / 0.4))
    if q > 0: fr.alpha_composite(Image.new("RGBA", (W, H), (255, 252, 244, int(225 * q))))
    for e in end: e.draw(fr, t)
    fr = camera(fr.convert("RGB"), t)
    fr = whip(fr, t, T1)
    fr = flash(fr, t, END_T)
    fr = fr.convert("RGBA")
    fr.alpha_composite(GRAIN[int(t * FPS) % len(GRAIN)])   # vignette is merged into each grain layer
    for e in ui: e.draw(fr, t)
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, 9], fill=(15, 23, 42, 22))
    d.rectangle([0, 0, int(W * clamp(t / DUR)), 9], fill=YEL)
    return fr.convert("RGB")

def render_chunk(args):
    i0, i1, path = args
    init()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(i0, i1): p.stdin.write(render(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return path

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        init()
        ts = [float(x) for x in sys.argv[2:]]
        ims = [render(t).resize((360, 640)) for t in ts]
        sheet = Image.new("RGB", (370 * len(ims), 640), "white")
        for k, im in enumerate(ims): sheet.paste(im, (k * 370, 0))
        sheet.save(os.path.join(KIT, "chk", "white_x_power_x_sheet.png")); print("ok")
    elif sys.argv[1] == "times":
        print(json.dumps(dict(T1=T1, BOARD_T=BOARD_T, REAL_T=REAL_T, END_T=END_T, X_T=X_T, ANS_T=ANS_T, STAR_T=STAR_T,
                              C=[round(c, 2) for c in C], DUR=DUR)))
    else:
        import multiprocessing as mp
        out = sys.argv[2]; nw = int(os.environ.get("WORKERS", "2"))
        bounds = np.linspace(0, NF, nw * 2 + 1).astype(int)
        jobs = [(int(bounds[k]), int(bounds[k + 1]), os.path.join(KIT, "out", f"seg4_{k:02d}.mp4")) for k in range(len(bounds) - 1)]
        R.build_audio(os.path.join(KIT, "out", "mix_v4.wav"))
        with mp.Pool(nw) as pool: segs = pool.map(render_chunk, jobs)
        open(os.path.join(KIT, "out", "segs4.txt"), "w").write("".join(f"file '{s}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(KIT, "out", "segs4.txt"),
                        "-i", os.path.join(KIT, "out", "mix_v4.wav"), "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
        print("done", NF, DUR)
