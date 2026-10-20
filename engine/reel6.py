"""TutorDA reel: Integral calculus - area of a circle by rings (pizza sizes). White theme, voice v2.
python3 reel6.py times | preview t1 t2 ... | build out.mp4
v2 (after critique): plain background (no floating symbols / tints / grid), proof is the hero (x on the pizza,
magnified dx, bigger triangle, [pi x^2] evaluation), bold maths, balanced captions, one value per number, ~31 s."""
import os, sys, math, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/pizza_integral")
os.environ["CLIPS"] = os.path.join(TOPIC, "clips.json")
os.environ["VO"] = os.path.join(TOPIC, "vo")
os.environ["MUSIC"] = "energetic"
os.environ["END_HOLD"] = "0.35"
os.environ["START"] = "0.15"                  # voice starts almost at once (no near-silent first 0.4 s)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import reel2 as R
import reel4 as V
from reel2 import (W, H, FPS, C, E, DUR, NF, CLIPS, tex, text_img, pill, EXPO_OUT, clamp, ease_io, El, font,
                   YEL, NAVY, WHITE)
from reel4 import INK, INK2, AMBER, AMBER_D, TEAL_D, logo_light, comp, radial, text_line, Dyn, WEl, Counter, Pulse

WT = json.load(open(os.path.join(TOPIC, "word_times.json")))
def _shift(i): return C[i] - WT[i].get("clip_start", C[i])   # word times stay right if START/gaps change
def wt(i, k, lead=0.0): return WT[i]["starts"][k] + _shift(i) - lead

# ---------------- key times (from spoken words) ----------------
T1 = E[1] + 0.15                    # whip: hook -> proof
TWO_T = wt(0, 4, 0.1)               # "or two"
LOOKS_T = wt(1, 1, 0.1)             # "looks like more"
INTEG_T = wt(1, 5, 0.15)            # "integrate"
RINGS_T = wt(2, 4, 0.3)             # "rings"
RING_T = wt(3, 2, 0.1)              # "a ring" -> highlight it
X_T = wt(3, 4, 0.1)                 # "radius x" -> x arrow
UN1_T = wt(3, 7, 0.2)               # "strip" -> unroll it
LEN_T = wt(3, 8, 0.2)               # "2πx long"
DX_T = wt(3, 11, 0.3)               # "dx thick" -> magnifier
ALL_T = wt(4, 0, 0.1)               # "Stack them all"
TRI_T = wt(4, 5, 0.15)              # "triangle"
AREA_T = wt(5, 0, 0.1)              # "Area: integral ..."
ANS_T = wt(5, 8, 0.25)              # "pi r squared!" -> the one spring moment
REAL_T = C[6] - 0.35                # -> real life
P36_T, P113_T = wt(6, 1, 0.15), wt(6, 3, 0.45)
P32_T, P101_T = wt(7, 3, 0.15), wt(7, 5, 0.45)
WIN_T = wt(8, 3, 0.15)              # "12.5%"
END_T = C[9] - 0.3
V.T1, V.BOARD_T, V.REAL_T, V.END_T = T1, T1 + 0.01, REAL_T, END_T
GLIDE_T, DY = TRI_T + 0.15, 0          # once stacked, the triangle rises to the optical centre (no empty top half)
def offy(t): return DY * ease_io(clamp((t - GLIDE_T) / 0.6))
V.PUNCH = [(TRI_T + 0.25, 0.03, (W / 2, 900), False), (ANS_T, 0.035, (W / 2, 1170), False),
           (WIN_T, 0.03, (W / 2, 1180), False)]

# ---------------- camera: slow push-in on the small ring diagram, pulled back before the strip gets wide ----------------
ZOOM_A, ZOOM_B = None, None          # set in build() once the times are known
def zoom(t):
    """returns (extra scale, weight toward the pizza focus)"""
    if t < ZOOM_A or t > ZOOM_B + 0.7: return 1.0, 0.0
    w = ease_io(clamp((t - ZOOM_A) / 0.6)) * (1 - ease_io(clamp((t - ZOOM_B) / 0.7)))
    z = 1.38 + 0.12 * clamp((t - ZOOM_A) / (ZOOM_B - ZOOM_A))      # keeps creeping in: no still frames
    return 1 + (z - 1) * w, w
def camera(fr, t):
    s = 1.012 + 0.01 * math.sin(2 * math.pi * t / 11)          # gentler breathe: content stays inside the safe box
    fx, fy = W / 2, H / 2 - 40
    for (t0, amp, (px, py), _) in V.PUNCH:
        b = V.bump(t - t0); s += amp * b
        fx += (px - W / 2) * b * 0.55; fy += (py - (H / 2 - 40)) * b * 0.55
    z, w = zoom(t); s *= z; fx += (PCX - fx) * w; fy += (720 - fy) * w
    if t > END_T: s = 1 + (s - 1) * (1 - ease_io(clamp((t - END_T) / 0.6)))
    cw, ch = W / s, H / s
    l = clamp(fx - cw / 2, 0, W - cw); tp = clamp(fy - ch / 2, 0, H - ch)
    return fr.resize((W, H), Image.BILINEAR, box=(l, tp, l + cw, tp + ch))
V.camera = camera
CAM_MAX = 1.06                       # largest camera scale outside the ring zoom (used by the safe-area check)

# ---------------- plain background (no grid, blobs, symbols or scene tints) ----------------
def make_plain(top, bot):
    g = np.linspace(0, 1, H)[:, None, None]
    return Image.fromarray(((np.array(top) * (1 - g) + np.array(bot) * g) * np.ones((H, W, 3))).astype(np.uint8)).convert("RGBA")
BG = None
def background(t):
    return BG.copy()
V.background = background

def texb(s, px, color):
    """Maths in Computer Modern, thickened to sit with Poppins Bold."""
    im = tex(s, px, color); a = im.getchannel("A").filter(ImageFilter.MaxFilter(3))
    out = Image.new("RGBA", im.size, color + (0,)); out.putalpha(a); return out

# ---------------- pizza ----------------
CRUST, CRUST_D = (214, 150, 74), (160, 98, 40)
CHEESE, CHEESE_D = (253, 214, 99), (243, 186, 60)
PEP, PEP_D = (196, 52, 46), (150, 34, 30)
LEAF = (64, 145, 72)

def pizza(r, seed=1, toppings=True, shadow=True):
    s = 3; R_ = r * s; size = 2 * R_ + 8 * s
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size / 2
    if shadow:
        sh = Image.new("RGBA", (size, size), (15, 23, 42, 0))
        ImageDraw.Draw(sh).ellipse([c - R_ + 2 * s, c - R_ + 5 * s, c + R_ + 2 * s, c + R_ + 5 * s], fill=(15, 23, 42, 40))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 * s)))
    d.ellipse([c - R_, c - R_, c + R_, c + R_], fill=CRUST, outline=CRUST_D, width=2 * s)
    ri = R_ * 0.86; d.ellipse([c - ri, c - ri, c + ri, c + ri], fill=(205, 70, 50))
    rc = R_ * 0.82; d.ellipse([c - rc, c - rc, c + rc, c + rc], fill=CHEESE)
    if toppings:
        rng = np.random.default_rng(seed); pts = []
        while len(pts) < max(5, int(r / 18)):
            a, rr = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0.02, 1)) * rc * 0.78
            p = (c + rr * math.cos(a), c + rr * math.sin(a))
            if all(math.dist(p, q) > R_ * 0.33 for q in pts): pts.append(p)
        pr = R_ * 0.13
        for (x, y) in pts: d.ellipse([x - pr, y - pr, x + pr, y + pr], fill=PEP, outline=PEP_D, width=2 * s)
        for k in range(len(pts)):
            a, rr = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0.05, 1)) * rc * 0.8
            x, y = c + rr * math.cos(a), c + rr * math.sin(a); l = R_ * 0.07; b = rng.uniform(0, math.pi)
            d.line([(x - l * math.cos(b), y - l * math.sin(b)), (x + l * math.cos(b), y + l * math.sin(b))], fill=LEAF, width=int(R_ * 0.045))
    return im.resize((size // s, size // s), Image.LANCZOS)

class Spin(Dyn):
    """A pizza that lands, then turns slowly (keeps still frames alive without drawing attention)."""
    def __init__(self, img, cx, cy, t_in, t_out, rate=5.0, phase=0.0, dims=()):
        self.img, self.cx, self.cy, self.ti, self.to, self.rate, self.ph, self.dims = img, cx, cy, t_in, t_out, rate, phase, dims
    def draw(self, frame, t):
        if t < self.ti or t > self.to + 0.3: return
        el = t - self.ti
        a = (1.0 if self.ti < 0 else EXPO_OUT(clamp(el / 0.18))) * (1 - ease_io(clamp((t - self.to) / 0.3)))
        for (td, lvl) in self.dims: a *= 1 - ease_io(clamp((t - td) / 0.4)) * (1 - lvl)
        sc = 1.0 if self.ti < 0 else 1 + 0.08 * (1 - EXPO_OUT(clamp(el / 0.38)))
        im = self.img.rotate(-(self.rate * t + self.ph), resample=Image.BICUBIC)
        comp(frame, im, self.cx, self.cy, alpha=a, scale=sc)

# ---------------- the proof: rings -> strips -> triangle ----------------
N = 6; PR = 126; PCX, PCY = W / 2, 545          # pizza for the proof; triangle base 2*pi*134 = 842 px (stays >= 85 px from the edges even with camera zoom)
TH = PR / N                                       # ring thickness = dx on screen (24 px)
BASE_Y = 805                                      # bottom of the stacked triangle (stacks right under the pizza)
KX = N - 2                                        # the ring we unroll first ("a ring at radius x")
XK = (KX + 0.5) * TH

def ring_color(k):
    if k == N - 1: return CRUST
    q = k / (N - 2); return tuple(int(CHEESE[j] * (1 - q) + CHEESE_D[j] * q) for j in range(3))

class Unroll(Dyn):
    def __init__(self, t_show, t_hi, t_one, t_all, t_out):
        self.ts, self.th, self.t1, self.ta, self.to = t_show, t_hi, t_one, t_all, t_out
        self.xk = [(k + 0.5) * TH for k in range(N)]
        self.yk = [BASE_Y - TH / 2 - (N - 1 - k) * TH for k in range(N)]
        rest = [k for k in range(N - 1, -1, -1) if k != KX]
        self.start = {KX: t_one}; self.start.update({k: t_all + j * 0.09 for j, k in enumerate(rest)})
        self.s = np.linspace(0, 1, 160)
    def draw(self, frame, t):
        if t < self.ts or t > self.to + 0.35: return
        a = clamp((t - self.ts) / 0.35) * (1 - ease_io(clamp((t - self.to) / 0.35)))
        y0, S = 330, 2
        ov = Image.new("RGBA", (W * S, (900 - y0) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for k in range(N - 1, -1, -1):
            x = self.xk[k]; u = EXPO_OUT(clamp((t - self.start[k]) / (0.9 if k == KX else 0.7)))
            phi = math.pi / 2 + 2 * math.pi * self.s
            cxs, cys = PCX + x * np.cos(phi), PCY + x * np.sin(phi)
            lxs = PCX - math.pi * x + 2 * math.pi * x * self.s; lys = np.full_like(lxs, self.yk[k])
            lift = 36 * math.sin(math.pi * u)
            xs = cxs * (1 - u) + lxs * u; ys = cys * (1 - u) + lys * u - lift + offy(t)
            d.line([(px * S, (py - y0) * S) for px, py in zip(xs, ys)], fill=ring_color(k) + (int(255 * a),),
                   width=int((TH - 2) * S), joint="curve")
            if k == KX and self.th <= t and u < 0.02:       # highlight "a ring" before it unrolls
                q = EXPO_OUT(clamp((t - self.th) / 0.3)); rr = x * S
                for w_, col in ((int((TH + 6) * S), AMBER_D + (int(255 * q * a),)),):
                    d.ellipse([PCX * S - rr, (PCY - y0) * S - rr, PCX * S + rr, (PCY - y0) * S + rr], outline=col, width=5 * S)
        frame.alpha_composite(ov.resize((W, 900 - y0), Image.BILINEAR), dest=(0, y0))

class Arrow(Dyn):
    """Radius arrow from the centre to the highlighted ring, labelled x."""
    def __init__(self, t0, t_out, label):
        self.t0, self.to, self.lab = t0, t_out, label
    def draw(self, frame, t):
        if t < self.t0 or t > self.to + 0.25: return
        p = EXPO_OUT(clamp((t - self.t0) / 0.4)); a = int(255 * (1 - ease_io(clamp((t - self.to) / 0.25))))
        d = ImageDraw.Draw(frame); ang = math.radians(-35)
        x1, y1 = PCX + XK * p * math.cos(ang), PCY + XK * p * math.sin(ang)
        d.line([(PCX, PCY), (x1, y1)], fill=NAVY + (a,), width=7)
        d.ellipse([PCX - 8, PCY - 8, PCX + 8, PCY + 8], fill=NAVY + (a,))
        if p > 0.5:
            for s_ in (1, -1):
                b = ang + math.pi + s_ * 0.45
                d.line([(x1, y1), (x1 + 22 * math.cos(b), y1 + 22 * math.sin(b))], fill=NAVY + (a,), width=7)
            lx = PCX + XK * 0.5 * math.cos(ang) + 64 * math.sin(ang); ly = PCY + XK * 0.5 * math.sin(ang) - 64 * math.cos(ang)
            r_ = max(self.lab.size) // 2 + 2
            d.ellipse([lx - r_, ly - r_, lx + r_, ly + r_], fill=(255, 255, 255, int(0.92 * a)))
            comp(frame, self.lab, lx, ly, alpha=clamp((p - 0.5) * 2) * a / 255)

class Dim(Dyn):
    def __init__(self, x0, x1, y, t0, t_out, color=TEAL_D):
        self.x0, self.x1, self.y, self.t0, self.to, self.col = x0, x1, y, t0, t_out, color
    def draw(self, frame, t):
        if t < self.t0 or t > self.to + 0.3: return
        p = EXPO_OUT(clamp((t - self.t0) / 0.5)); a = int(255 * (1 - ease_io(clamp((t - self.to) / 0.3))))
        d = ImageDraw.Draw(frame); m = (self.x0 + self.x1) / 2; h = (self.x1 - self.x0) / 2 * p; c = self.col + (a,)
        d.line([(m - h, self.y), (m + h, self.y)], fill=c, width=5)
        for x, s in ((m - h, 1), (m + h, -1)):
            d.line([(x, self.y - 14), (x, self.y + 14)], fill=c, width=5)
            d.line([(x, self.y), (x + 18 * s, self.y - 10)], fill=c, width=5); d.line([(x, self.y), (x + 18 * s, self.y + 10)], fill=c, width=5)

class Magnifier(Dyn):
    """Circular 3.5x inset of the strip's end so 'dx thick' is visible."""
    def __init__(self, sx, sy, cx, cy, t0, t_out, label):
        self.sx, self.sy, self.cx, self.cy, self.t0, self.to, self.lab = sx, sy, cx, cy, t0, t_out, label
        self.r, self.z = 118, 3.5
        m = Image.new("L", (2 * self.r, 2 * self.r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * self.r - 1, 2 * self.r - 1], fill=255)
        self.mask = m
    def draw(self, frame, t):
        if t < self.t0 or t > self.to + 0.3: return
        p = EXPO_OUT(clamp((t - self.t0) / 0.4)); a = (1 - ease_io(clamp((t - self.to) / 0.3)))
        half = self.r / self.z
        crop = frame.crop((int(self.sx - half), int(self.sy - half), int(self.sx + half), int(self.sy + half)))
        crop = crop.resize((2 * self.r, 2 * self.r), Image.LANCZOS)
        lens = Image.new("RGBA", (2 * self.r + 16, 2 * self.r + 16), (0, 0, 0, 0))
        bgc = Image.new("RGBA", (2 * self.r, 2 * self.r), (255, 255, 255, 255)); bgc.alpha_composite(crop)
        lens.paste(bgc, (8, 8), self.mask)
        dl = ImageDraw.Draw(lens)
        dl.ellipse([4, 4, 2 * self.r + 11, 2 * self.r + 11], outline=NAVY, width=7)
        # dx bracket across the strip thickness, inside the lens
        c = self.r + 8; hh = TH * self.z / 2
        bx = c - 30
        dl.line([(bx, c - hh), (bx, c + hh)], fill=AMBER_D, width=6)
        for yy in (c - hh, c + hh): dl.line([(bx - 14, yy), (bx + 14, yy)], fill=AMBER_D, width=6)
        lens.alpha_composite(self.lab, dest=(int(bx + 18), int(c - self.lab.height / 2)))
        d = ImageDraw.Draw(frame)
        if p > 0.05:
            d.line([(self.sx, self.sy - half), (self.cx + (self.sx - self.cx) * 0.25, self.cy + self.r * 0.97)], fill=NAVY + (int(160 * a),), width=4)
            d.ellipse([self.sx - half, self.sy - half, self.sx + half, self.sy + half], outline=NAVY + (int(200 * a),), width=4)
        comp(frame, lens, self.cx, self.cy, alpha=a * clamp(p * 1.5), scale=0.9 + 0.1 * p)

class TriOutline(Dyn):
    def __init__(self, t0, t_out):
        self.t0, self.to = t0, t_out
        top = BASE_Y - PR; L = math.pi * PR
        self.top = top
        self.pts = [(PCX - L - 5, BASE_Y + 4), (PCX + L + 5, BASE_Y + 4), (PCX, top - 7), (PCX - L - 5, BASE_Y + 4)]
    def draw(self, frame, t):
        if t < self.t0 or t > self.to + 0.35: return
        p = EXPO_OUT(clamp((t - self.t0) / 0.7)); a = 1 - ease_io(clamp((t - self.to) / 0.35))
        oy = offy(t); pts = [(x, y + oy) for x, y in self.pts]
        segs = [(pts[i], pts[i + 1]) for i in range(3)]
        lens = [math.dist(*s) for s in segs]; tot = sum(lens) * p; d = ImageDraw.Draw(frame)
        for (p1, p2), L in zip(segs, lens):
            if tot <= 0: break
            f = min(1, tot / L); tot -= L
            d.line([p1, (p1[0] + (p2[0] - p1[0]) * f, p1[1] + (p2[1] - p1[1]) * f)], fill=AMBER_D + (int(255 * a),), width=7)
        if p > 0.6:
            q = clamp((p - 0.6) / 0.4)
            for y in range(int(self.top), int(BASE_Y), 16):
                if y > self.top + PR * q: break
                d.line([(PCX, y + oy), (PCX, min(y + 8, BASE_Y) + oy)], fill=NAVY + (int(230 * a),), width=5)

# ---------------- real-life comparison ----------------
class AreaBar(Dyn):
    def __init__(self, x0, cy, w_full, val, vmax, t0, t_out, fill, t_hi=None, hi_from=None, t_track=None):
        self.x0, self.cy, self.w, self.v, self.vm, self.t0, self.to, self.fill = x0, cy, w_full, val, vmax, t0, t_out, fill
        self.th, self.hf, self.tt = t_hi, hi_from, (t0 if t_track is None else t_track)
    def draw(self, frame, t):
        if t < self.tt or t > self.to + 0.35: return
        p = EXPO_OUT(clamp((t - self.t0) / 0.7)) if t >= self.t0 else 0.0
        a = EXPO_OUT(clamp((t - self.tt) / 0.3)) * (1 - ease_io(clamp((t - self.to) / 0.35)))
        h = 60; L = self.w * self.v / self.vm * p
        ov = Image.new("RGBA", (W, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        d.rounded_rectangle([self.x0, 10, self.x0 + self.w, 10 + h], radius=h // 2, fill=(15, 23, 42, 14))
        if L > h: d.rounded_rectangle([self.x0, 10, self.x0 + L, 10 + h], radius=h // 2, fill=self.fill)
        if self.th is not None and t >= self.th:
            q = EXPO_OUT(clamp((t - self.th) / 0.5)); xs = self.x0 + self.w * self.hf / self.vm
            d.rounded_rectangle([xs, 10, xs + (self.x0 + L - xs) * q, 10 + h], radius=h // 2, fill=AMBER)
        comp(frame, ov, W / 2, self.cy, alpha=a)

def chip(s): return pill(s, font("Bold", 40), AMBER_D, (255, 200, 61, 70), padx=26, pady=12, outline=AMBER + (170,))

class KaraokeW(Dyn):
    """Word-timed captions with balanced line breaks (no single-word last lines)."""
    def __init__(self, i, cy=1410):
        txt = CLIPS[i][2]; f = font("Bold", 48); words = txt.split(); sp = f.getlength(" ")
        wl = [f.getlength(w_) for w_ in words]
        def width(a, b): return sum(wl[a:b]) + sp * (b - a - 1)
        if width(0, len(words)) <= 760: lines = [words]
        else:
            # balanced, but prefer breaking after punctuation (never "0 / to r")
            best = min(range(1, len(words)), key=lambda k: max(width(0, k), width(k, len(words)))
                       + (0 if words[k - 1][-1] in ",.:;!?" else 120))
            lines = [words[:best], words[best:]]
        lh = 66; bw = int(max(f.getlength(" ".join(l)) for l in lines)) + 70; bh = lh * len(lines) + 36
        base = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(base)
        d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=26, fill=(15, 23, 42, 235))
        self.wpos, self.wimg = [], []
        for li, l in enumerate(lines):
            x = (bw - f.getlength(" ".join(l))) / 2; y = 16 + li * lh
            for w_ in l:
                d.text((x, y), w_, font=f, fill=WHITE)
                self.wpos.append((x, y)); self.wimg.append(text_line(w_, f, YEL)); x += f.getlength(w_ + " ")
        self.base, self.cy = base, cy
        self.starts = np.array(WT[i]["starts"]) + _shift(i)
        self.t0 = -1.0 if i == 0 else C[i] - 0.05
        self.t1 = (C[i + 1] - 0.03) if i + 1 < len(C) else E[i] + 0.3
    def draw(self, frame, t):
        if t < self.t0 or t >= self.t1: return
        k = int(np.searchsorted(self.starts, t, side="right")) - 1
        im = self.base.copy()
        if k >= 0:
            x, y = self.wpos[k]; im.alpha_composite(self.wimg[k], dest=(int(x), int(y)))
        el = t - self.t0
        comp(frame, im, W / 2, self.cy, alpha=1.0 if self.t0 < 0 else EXPO_OUT(clamp(el / 0.12)),
             scale=0.96 + 0.04 * EXPO_OUT(clamp(el / 0.25)))

# ---------------- scene ----------------
def build():
    global BG, ZOOM_A, ZOOM_B
    ZOOM_A, ZOOM_B = RINGS_T - 0.35, UN1_T - 0.1
    BG = make_plain((255, 255, 255), (244, 246, 250))          # white, cooled very slightly toward the navy brand hue
    WEl.GLOW = radial(34, (255, 176, 20), 230, power=1.6)
    content, ui, fx, end = [], [], [], []
    ui.append(El(logo_light(1.0), W / 2, 118, -1, 0.5, t_out=END_T))
    ui.append(El(text_img("CLASS 12 MATHS  ·  INTEGRAL CALCULUS", font("Bold", 36), INK2), W / 2, 205, -1, 0.5, t_out=END_T))
    ui.append(El(text_img("www.tutorda.org", font("Bold", 40), INK2), W / 2, 1560, -1, 0.5, t_out=END_T))
    for i in range(len(CLIPS) - 1): ui.append(KaraokeW(i))

    # ===== HOOK (fully on screen at frame 0) =====
    ho = T1 - 0.02; k = dict(t_out=ho, out_dur=0.02)
    content.append(El(text_img("Which is more pizza?", font("Bold", 70), INK), W / 2, 340, -1, **k))
    content.append(Spin(pizza(190, 3), 315, 745, -1, ho, rate=4))
    for y, sd, ph in ((605, 5, 40), (885, 8, 200)):
        content.append(Spin(pizza(128, sd), 780, y, -1, ho, rate=-5, phase=ph, dims=[(INTEG_T, 0.55)]))
    content.append(Pulse(radial(150, YEL, 150), 578, 745, TWO_T, 0.9))
    content.append(El(pill("VS", font("Bold", 46), (255, 255, 255), NAVY, padx=26, pady=14), 578, 745, -1, **k))
    content.append(El(text_img("1 × 12-inch", font("Bold", 52), INK), 315, 1080, -1, **k))
    content.append(El(text_img("2 × 8-inch", font("Bold", 52), INK), 780, 1080, -1, **k))
    content.append(V.RoughEllipse(780, 745, 148, 298, LOOKS_T, 0.8, ho, color=AMBER, seed=4))
    content.append(Pulse(radial(240, YEL, 120), W / 2, 1215, INTEG_T, 0.9))
    content.append(El(texb(r"\int_0^{r} \; ? \; dx", 96, NAVY), W / 2, 1215, INTEG_T, 0.4, kind="land", **k))

    # ===== PROOF =====
    po = REAL_T
    content.append(El(chip("SLICE  ·  UNROLL  ·  STACK"), W / 2, 325, T1 + 0.05, 0.4, t_out=po))
    content.append(El(pizza(PR, 11, shadow=False), PCX, PCY, T1 + 0.05, 0.45, kind="land", t_out=RINGS_T + 0.25, out_dur=0.3))
    content.append(Unroll(RINGS_T, RING_T, UN1_T, ALL_T, po))
    content.append(Arrow(X_T, UN1_T + 0.15, texb(r"x", 64, NAVY)))
    L1 = 2 * math.pi * XK; ys = BASE_Y - TH / 2 - (N - 1 - KX) * TH
    content.append(Dim(PCX - L1 / 2, PCX + L1 / 2, BASE_Y + 40, LEN_T, ALL_T + 0.1))
    content.append(El(texb(r"2\pi x", 64, TEAL_D), PCX, BASE_Y + 98, LEN_T + 0.1, 0.4, kind="land", t_out=ALL_T + 0.1, out_dur=0.3))
    content.append(Magnifier(PCX + L1 / 2 - 22, ys, 805, 590, DX_T, ALL_T + 0.1, texb(r"dx", 56, AMBER_D)))
    content.append(TriOutline(TRI_T, po))
    content.append(El(texb(r"\mathrm{base} = 2\pi r", 60, TEAL_D), PCX, BASE_Y + 62, TRI_T + 0.35, 0.4, kind="land", t_out=po))
    rt = texb(r"r", 56, NAVY); tag = Image.new("RGBA", (rt.width + 26, rt.height + 18), (0, 0, 0, 0))
    ImageDraw.Draw(tag).rounded_rectangle([0, 0, tag.width - 1, tag.height - 1], radius=14, fill=(255, 255, 255, 240), outline=NAVY + (255,), width=3)
    tag.alpha_composite(rt, dest=(13, 9))
    content.append(El(tag, PCX + 42, BASE_Y - PR / 2, TRI_T + 0.6, 0.4, kind="land", t_out=po))     # height r, on the dashed line
    content.append(WEl(texb(r"\mathrm{Area} = \int_0^{r} 2\pi x \, dx", 76, INK), W / 2, 1030, AREA_T, 1.0, kind="wipe", t_out=po))
    ans = texb(r"= \left[\pi x^2\right]_0^{r} = \pi r^2", 80, NAVY)
    padx, pady, M = 52, 26, 90
    bw, bh = ans.width + 2 * padx, ans.height + 2 * pady
    box = Image.new("RGBA", (bw + 2 * M, bh + 2 * M), YEL + (0,))
    gl = Image.new("RGBA", box.size, YEL + (0,))
    ImageDraw.Draw(gl).rounded_rectangle([M - 10, M - 10, bw + M + 10, bh + M + 10], radius=36, fill=YEL + (150,))
    box.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    inner = Image.new("RGBA", box.size, YEL + (0,))
    ImageDraw.Draw(inner).rounded_rectangle([M, M, bw + M, bh + M], radius=32, fill=YEL)
    box.alpha_composite(inner); box.alpha_composite(ans, dest=(M + padx, M + pady))
    content.append(Pulse(radial(420, (255, 220, 120), 120), W / 2, 1232, ANS_T, 1.0))
    content.append(El(box, W / 2, 1232, ANS_T, 0.5, kind="pop", t_out=po))           # the one spring moment
    content.append(V.Shine(inner, W / 2, 1232, ANS_T + 0.45))

    # ===== REAL LIFE (all three pizzas arrive together; every number shown once) =====
    ro = END_T
    content.append(El(chip("AREA = πr²  ·  BACK TO THE PIZZAS"), W / 2, 325, C[6], 0.4, t_out=ro))
    content.append(Spin(pizza(170, 3), 300, 545, C[6], ro, rate=7))
    for y, sd, ph in ((470, 5, 40), (700, 8, 200)):
        content.append(Spin(pizza(113, sd), 745, y, C[6] + 0.08, ro, rate=-8, phase=ph))
    content.append(El(texb(r"\pi \cdot 6^2 = 36\pi", 58, INK), 300, 770, P36_T, 0.4, kind="land", t_out=ro))
    content.append(El(texb(r"2 \cdot \pi \cdot 4^2 = 32\pi", 54, INK), 745, 860, P32_T, 0.4, kind="land", t_out=ro))
    X0, BW_ = 125, 770                                        # bars end at x = 895, clear of the like/comment column
    fL = font("Bold", 46)
    la = text_img("1 × 12-inch", fL, INK); content.append(El(la, X0 + la.width / 2, 950, C[6] + 0.3, 0.4, t_out=ro))
    nA = [text_line(f"≈ {v} sq in", fL, AMBER_D) for v in range(114)]
    content.append(Counter(nA, X0 + BW_ - nA[-1].width / 2, 950, P113_T, 0.7, t_out=ro))
    content.append(AreaBar(X0, 1012, BW_, 113.1, 113.1, P113_T, ro, YEL, t_hi=WIN_T, hi_from=100.5, t_track=C[6] + 0.3))
    lb = text_img("2 × 8-inch", fL, INK); content.append(El(lb, X0 + lb.width / 2, 1150, C[6] + 0.4, 0.4, t_out=ro))
    nB = [text_line(f"≈ {v} sq in", fL, INK2) for v in range(102)]
    content.append(Counter(nB, X0 + BW_ - nB[-1].width / 2, 1150, P101_T, 0.7, t_out=ro))
    content.append(AreaBar(X0, 1212, BW_, 100.5, 113.1, P101_T, ro, (203, 213, 225), t_track=C[6] + 0.4))
    xs = X0 + BW_ * 100.5 / 113.1
    pl = pill("+12.5%", font("Bold", 50), NAVY, YEL, padx=28, pady=12, outline=AMBER_D + (255,))
    content.append(El(pl, min(X0 + BW_ - pl.width / 2, (xs + X0 + BW_) / 2), 1078, WIN_T + 0.1, 0.4, kind="land", t_out=ro))
    content.append(Pulse(radial(300, YEL, 110), 300, 545, WIN_T, 1.0))

    # ===== END CARD =====
    end.append(Pulse(radial(330, YEL, 120), W / 2, 800, C[9] + 0.1, 1.4))
    end.append(El(logo_light(1.75), W / 2, 800, C[9], 0.5, kind="land"))
    end.append(El(text_img("Follow for more Class 12 maths", font("Bold", 54), INK), W / 2, 960, C[9] + 0.15))
    end.append(El(text_img("JEE  ·  NEET  ·  Boards", font("Bold", 44), AMBER_D), W / 2, 1045, C[9] + 0.3))
    end.append(El(pill("www.tutorda.org", font("Bold", 58), NAVY, YEL, padx=48, pady=24), W / 2, 1190, C[9] + 0.4, 0.4, kind="land"))
    return content, ui, fx, end

def init():
    if V.SCENE is None:
        V.SCENE = build(); V.finishing_assets()

def load_samples():
    out, sd = {}, os.path.join(KIT, "assets", "sfx")
    for f in os.listdir(sd):
        if not f.endswith(".wav"): continue
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(sd, f), "-ac", "1", "-ar", str(R.SR), "-f", "f32le", "-"],
                             capture_output=True).stdout
        a = np.frombuffer(raw, np.float32).astype(np.float64); out[f[:-4]] = a / max(1e-9, np.abs(a).max())
    return out

def sfx_schedule(s):
    smp = s["sample"]
    smp(T1 - 0.17, "whoosh-short", 0.30)            # hook -> proof
    smp(RINGS_T + 0.05, "tap", 0.22)                # pizza becomes rings
    smp(UN1_T, "sweep-long", 0.14)                  # first unroll
    smp(DX_T + 0.02, "pop-2", 0.18)                 # magnifier
    smp(TRI_T + 0.05, "check-mark", 0.22)           # triangle outline
    smp(ANS_T - 0.06, "success-bell", 0.24)         # hero: pi r^2
    smp(REAL_T - 0.1, "whoosh-short", 0.22)         # -> real life
    smp(wt(8, 4, -0.1), "success-chime", 0.22)      # after "more", not on the number

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.38,
                  music_dips=[(ANS_T - 0.35, 0.45, 10), (WIN_T - 0.35, 0.45, 10)], samples=load_samples())

def render_chunk(args):
    i0, i1, path = args
    init()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(i0, i1): p.stdin.write(V.render(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return path

if __name__ == "__main__":
    if sys.argv[1] == "times":
        print(json.dumps(dict(DUR=DUR, T1=T1, RINGS=RINGS_T, RING=RING_T, X=X_T, UN1=UN1_T, LEN=LEN_T, DX=DX_T, ALL=ALL_T, TRI=TRI_T,
                              AREA=AREA_T, ANS=ANS_T, REAL=REAL_T, P113=P113_T, P101=P101_T, WIN=WIN_T, END=END_T,
                              C=[round(c, 2) for c in C])))
    elif sys.argv[1] == "preview":
        init()
        ims = [V.render(float(t)).resize((360, 640)) for t in sys.argv[2:]]
        sheet = Image.new("RGB", (370 * len(ims), 640), "white")
        for k, im in enumerate(ims): sheet.paste(im, (k * 370, 0))
        sheet.save(os.path.join(KIT, "chk", "pizza_sheet.png")); print("ok")
    else:
        import multiprocessing as mp
        out = sys.argv[2]; nw = int(os.environ.get("WORKERS", "2"))
        bounds = np.linspace(0, NF, nw * 2 + 1).astype(int)
        jobs = [(int(bounds[k]), int(bounds[k + 1]), os.path.join(KIT, "out", f"seg6_{k:02d}.mp4")) for k in range(len(bounds) - 1)]
        make_audio(os.path.join(KIT, "out", "mix_v6.wav"))
        with mp.Pool(nw) as pool: segs = pool.map(render_chunk, jobs)
        open(os.path.join(KIT, "out", "segs6.txt"), "w").write("".join(f"file '{s}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(KIT, "out", "segs6.txt"),
                        "-i", os.path.join(KIT, "out", "mix_v6.wav"), "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
        print("done", NF, DUR)
