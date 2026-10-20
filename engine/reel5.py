"""TutorDA reel: the Birthday Paradox (Class 12 probability), white theme, energetic Indian voice.
python3 reel5.py preview t1 t2 ...   -> chk/v5_sheet.png
python3 reel5.py times
python3 reel5.py build out.mp4
"""
import os, sys, math, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/birthday_paradox")
os.environ["CLIPS"] = os.path.join(TOPIC, "clips.json")
os.environ["VO"] = os.path.join(TOPIC, "vo")
os.environ["MUSIC"] = "energetic"
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import reel2 as R
import reel4 as V
from reel2 import (W, H, FPS, C, E, at, DUR, NF, CLIPS, tex, text_img, pill, star, spring, EXPO_OUT, clamp,
                   ease_io, El, font, YEL, TEAL, RED, NAVY, WHITE)
from reel4 import (INK, INK2, AMBER, AMBER_D, TEAL_D, RED_D, logo_light, comp, radial, text_line, Dyn, WEl,
                   Counter, Confetti, RoughEllipse, Pulse, Rings, Karaoke)

# ---------------- key times ----------------
T1 = E[1] + 0.15                 # whip: hook -> trick
BOARD_T = C[4] - 0.3             # trick -> board
REAL_T = C[10] - 0.35            # board -> why-so-high
END_T = C[13] - 0.3              # end card
MATCH_T = at(0, 0.62)            # "share a birthday"
STRIKE_T = at(1, 0.38)           # "tiny" crossed out
FIFTY_T = at(1, 0.5)             # "over fifty percent"
ANS_T = C[8] + 0.05
STICK_T = C[9]
LINES_A, LINES_B = at(10, 0.25), at(10, 0.97)
V.T1, V.BOARD_T, V.REAL_T, V.END_T = T1, BOARD_T, REAL_T, END_T
V.PUNCH = [(MATCH_T, 0.035, (W / 2, 850), False), (FIFTY_T, 0.045, (W / 2, 1000), True),
           (ANS_T, 0.04, (W / 2, 1500), False), (STICK_T, 0.045, (W / 2 + 280, 1400), False),
           (LINES_B, 0.04, (W / 2, 1200), False)]

PALETTE = [(99, 102, 241), (236, 72, 153), (20, 184, 166), (245, 158, 11), (59, 130, 246), (168, 85, 247),
           (239, 68, 68), (16, 185, 129), (234, 88, 12), (14, 165, 233), (217, 70, 239), (132, 204, 22)]

def student(size, color):
    s = size; im = Image.new("RGBA", (s + 8, s + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = 4
    d.ellipse([o, o, o + s, o + s], fill=tuple(int(c * 0.18 + 255 * 0.82) for c in color))
    d.ellipse([o + s * 0.33, o + s * 0.16, o + s * 0.67, o + s * 0.5], fill=color)
    d.chord([o + s * 0.16, o + s * 0.55, o + s * 0.84, o + s * 1.15], 180, 360, fill=color)
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).ellipse([o, o, o + s, o + s], fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), mask)
    return out

def cake(s=46):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, s * 0.48, s - 4, s - 4], radius=6, fill=(236, 72, 153))
    d.rectangle([4, s * 0.62, s - 4, s * 0.7], fill=(255, 255, 255))
    d.rectangle([s / 2 - 2.5, s * 0.2, s / 2 + 2.5, s * 0.48], fill=(59, 130, 246))
    d.ellipse([s / 2 - 5, s * 0.02, s / 2 + 5, s * 0.22], fill=(245, 158, 11))
    return im

def ring(size, color, width=7):
    im = Image.new("RGBA", (size + 20, size + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([4, 4, size + 15, size + 15], outline=color, width=width)
    return im

def strike_line(w):
    im = Image.new("RGBA", (w + 20, 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).line([(10, 28), (w + 10, 12)], fill=RED_D, width=12)
    return im

class DashLink(Dyn):
    def __init__(self, p, q, t0, t_out):
        self.p, self.q, self.t0, self.to = p, q, t0, t_out
    def draw(self, frame, t):
        if t < self.t0 or t > self.to: return
        k = EXPO_OUT(clamp((t - self.t0) / 0.5)); d = ImageDraw.Draw(frame)
        (x1, y1), (x2, y2) = self.p, self.q; L = math.hypot(x2 - x1, y2 - y1); n = int(L / 26)
        for i in range(n):
            a, b = i / n, (i + 0.55) / n
            if a > k: break
            b = min(b, k)
            d.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)], fill=AMBER + (255,), width=7)

class Bar(Dyn):
    """Complement bar: 'no match' (0.49) + 'match' (0.51) = 1."""
    def __init__(self, cx, cy, w, h, t_no, t_match, t_out):
        self.cx, self.cy, self.w, self.h, self.tn, self.tm, self.to = cx, cy, w, h, t_no, t_match, t_out
        f = font("Bold", 42)
        self.l_no = text_img("no match", f, AMBER_D); self.l_m = text_img("match", f, TEAL_D)
        self.l_one = text_img("total = 1", font("Bold", 40), INK2)
    def draw(self, frame, t):
        if t < self.tn - 0.2 or t > self.to: return
        a_all = EXPO_OUT(clamp((t - self.tn + 0.2) / 0.3))
        ov = Image.new("RGBA", (self.w + 20, self.h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        d.rounded_rectangle([10, 10, self.w + 9, self.h + 9], radius=self.h // 2, fill=(15, 23, 42, 14), outline=INK2 + (120,), width=3)
        split = 0.4927 * self.w
        pn = EXPO_OUT(clamp((t - self.tn) / 0.7)); pm = EXPO_OUT(clamp((t - self.tm) / 0.6))
        if pn > 0: d.rounded_rectangle([10, 10, 10 + max(self.h, split * pn), self.h + 9], radius=self.h // 2, fill=AMBER)
        if pm > 0: d.rounded_rectangle([10 + self.w - max(self.h, (self.w - split) * pm), 10, self.w + 9, self.h + 9], radius=self.h // 2, fill=TEAL)
        comp(frame, ov, self.cx, self.cy, alpha=a_all)
        x0 = self.cx - self.w / 2
        if pn > 0.3: comp(frame, self.l_no, x0 + split / 2, self.cy + self.h / 2 + 50, alpha=clamp((pn - 0.3) / 0.4))
        if pm > 0.3:
            comp(frame, self.l_m, x0 + split + (self.w - split) / 2, self.cy + self.h / 2 + 50, alpha=clamp((pm - 0.3) / 0.4))
            comp(frame, self.l_one, self.cx, self.cy - self.h / 2 - 48, alpha=clamp((pm - 0.3) / 0.4))

class Network(Dyn):
    """23 students on a circle; all 253 pairs drawn progressively, then single pairs highlighted."""
    def __init__(self, cx, cy, r, t_pop, t_a, t_b, t_hi, t_hi_end, t_out):
        self.cx, self.cy, self.r = cx, cy, r
        self.tp, self.ta, self.tb, self.th, self.the, self.to = t_pop, t_a, t_b, t_hi, t_hi_end, t_out
        self.pos = [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * k / 23), cy + r * math.sin(-math.pi / 2 + 2 * math.pi * k / 23)) for k in range(23)]
        self.pairs = [(i, j) for i in range(23) for j in range(i + 1, 23)]
        rng = np.random.default_rng(4); self.hi = [self.pairs[k] for k in rng.choice(253, 12, replace=False)]
        self.av = [student(66, PALETTE[k % len(PALETTE)]) for k in range(23)]
        self.ring = ring(66, AMBER, 6)
    def draw(self, frame, t):
        if t < self.tp or t > self.to + 0.35: return
        fade = 1 - ease_io(clamp((t - self.to) / 0.35))
        S = 2 * self.r + 140; ov = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        off = (self.cx - S / 2, self.cy - S / 2)
        n = int(253 * ease_io(clamp((t - self.ta) / (self.tb - self.ta))))
        for (i, j) in self.pairs[:n]:
            (x1, y1), (x2, y2) = self.pos[i], self.pos[j]
            d.line([(x1 - off[0], y1 - off[1]), (x2 - off[0], y2 - off[1])], fill=AMBER + (int(80 * fade),), width=2)
        hp = None
        if self.th <= t < self.the:
            hp = self.hi[int((t - self.th) / 0.2) % len(self.hi)]
            (x1, y1), (x2, y2) = self.pos[hp[0]], self.pos[hp[1]]
            d.line([(x1 - off[0], y1 - off[1]), (x2 - off[0], y2 - off[1])], fill=AMBER_D + (int(255 * fade),), width=8)
        frame.alpha_composite(ov, dest=(int(off[0]), int(off[1])))
        for k, (x, y) in enumerate(self.pos):
            el = t - (self.tp + k * 0.025)
            if el < 0: continue
            sc = math.exp(math.log(0.5) * (1 - spring(el, 0.35, 0.4)))
            comp(frame, self.av[k], x, y, alpha=fade * EXPO_OUT(clamp(el / 0.15)), scale=sc)
            if hp and k in hp: comp(frame, self.ring, x, y, alpha=fade)

def sticker(text, rot=-8):
    p = pill(text, font("Bold", 80), NAVY, YEL, padx=46, pady=22)
    sh = Image.new("RGBA", (p.width + 40, p.height + 40), (0, 0, 0, 0))
    m = Image.new("RGBA", p.size, (15, 23, 42, 70)); m.putalpha(p.getchannel("A").point(lambda v: v * 70 // 255))
    sh.alpha_composite(m, dest=(24, 28)); sh = sh.filter(ImageFilter.GaussianBlur(8)); sh.alpha_composite(p, dest=(20, 20))
    return sh.rotate(rot, resample=Image.BICUBIC, expand=True)

def build_symbols():
    rng = np.random.default_rng(21); V.SYMS.clear()
    pieces = [r"P(A)", r"n!", r"\binom{n}{r}", r"\%", r"\frac{1}{6}", r"\cap", r"\cup", r"365", r"\Omega",
              r"E(X)", r"p+q=1", r"\sigma", r"{}^{n}C_{r}", r"\mu", r"P(A')", r"\frac{364}{365}"]
    for p in pieces:
        size = int(rng.uniform(46, 104)); im = tex(p, size, (40, 50, 100))
        a = np.array(im); a[..., 3] = (a[..., 3] * rng.uniform(0.06, 0.11)).astype(np.uint8)
        V.SYMS.append(dict(img=Image.fromarray(a), x=rng.uniform(60, W - 60), y=rng.uniform(0, H),
                           v=8 + size * 0.22, amp=rng.uniform(10, 30), fq=rng.uniform(0.15, 0.4), ph=rng.uniform(0, 6)))

# ---------------- scene ----------------
def build():
    V.BGS = [V.make_grad(*p) for p in V.PAL]
    build_symbols()
    WEl.GLOW = radial(34, (255, 176, 20), 230, power=1.6)
    content, ui, fx, end = [], [], [], []

    # UI
    ui.append(El(logo_light(1.0), W / 2, 118, 0.0, 0.5, t_out=END_T))
    ui.append(El(text_img("CLASS 12 MATHS  ·  PROBABILITY", font("Bold", 36), INK2), W / 2, 205, 0.15, 0.5, t_out=END_T))
    ui.append(El(text_img("www.tutorda.org", font("Bold", 40), INK2), W / 2, 1790, 0.2, 0.5, t_out=END_T))
    for i in range(len(CLIPS) - 1): ui.append(Karaoke(i))

    # ===== HOOK: 23 students =====
    ho = T1 - 0.02
    content.append(El(text_img("The Birthday Paradox", font("Bold", 76), INK), W / 2, 365, C[0], 0.45, t_out=ho, out_dur=0.02))
    content.append(El(text_img("23 students  ·  365 days", font("Medium", 48), INK2), W / 2, 460, C[0] + 0.2, t_out=ho, out_dur=0.02))
    pos = []
    for k in range(23):
        r_, c_ = divmod(k, 6)
        x = W / 2 + ((c_ - 2.5) if r_ < 3 else (c_ - 2)) * 140
        pos.append((x, 640 + r_ * 140))
    A, B = 8, 15
    grid_dims = [(C[1], 0.3)]
    for k, (x, y) in enumerate(pos):
        content.append(El(student(100, PALETTE[k % len(PALETTE)]), x, y, C[0] + 0.25 + k * 0.035, 0.4, kind="pop",
                          t_out=ho, out_dur=0.02, dims=grid_dims))
    content.append(DashLink(pos[A], pos[B], MATCH_T + 0.1, C[1] + 0.2))
    for k in (A, B):
        x, y = pos[k]
        content.append(Pulse(radial(110, YEL, 140), x, y, MATCH_T, 0.9))
        content.append(El(ring(100, AMBER, 8), x, y, MATCH_T, 0.35, kind="pop", t_out=C[1] + 0.1))
        content.append(El(cake(50), x + 40, y - 42, MATCH_T + 0.08, 0.35, kind="pop", t_out=C[1] + 0.1))
    tiny = text_img("tiny?", font("Bold", 64), INK2)
    content.append(El(tiny, W / 2, 1130, C[1] + 0.05, 0.35, kind="pop", t_out=FIFTY_T - 0.05, out_dur=0.15))
    content.append(El(strike_line(tiny.width + 30), W / 2, 1130, STRIKE_T, 0.25, kind="wipe", t_out=FIFTY_T - 0.05, out_dur=0.15))
    fifty = [text_line(f"{k}%", font("Bold", 190), AMBER) for k in range(50)] + [text_line("50%+", font("Bold", 190), AMBER)]
    content.append(Pulse(radial(330, YEL, 110), W / 2, 1210, FIFTY_T, 1.0))
    content.append(Counter(fifty, W / 2, 1210, FIFTY_T, 0.7, t_out=ho))

    # ===== THE TRICK: complement =====
    tr_out = BOARD_T - 0.1
    content.append(El(pill("THE TRICK", font("Bold", 56), NAVY, YEL, padx=44, pady=20), W / 2, 400, T1 + 0.05, 0.4, kind="pop", t_out=tr_out))
    content.append(WEl(tex(r"P(\mathrm{nobody\ matches})", 92, AMBER_D), W / 2, 580, at(2, 0.35), 0.6, kind="wipe", t_out=tr_out))
    content.append(Bar(W / 2, 830, 880, 90, at(2, 0.6), C[3] + 0.1, tr_out))
    content.append(WEl(tex(r"P(\mathrm{match}) = 1 - P(\mathrm{nobody\ matches})", 62, INK), W / 2, 1060, C[3] + 0.35, 0.8, kind="wipe", t_out=tr_out))

    # ===== BOARD =====
    bo = REAL_T
    card = Image.new("RGBA", (1000, 960), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, 979, 949], radius=40, fill=(15, 23, 42, 40))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    ImageDraw.Draw(card).rounded_rectangle([20, 20, 979, 939], radius=40, fill=(255, 255, 255, 228), outline=(15, 23, 42, 22), width=2)
    content.append(El(card, W / 2, 930, BOARD_T, 0.5, t_out=bo))
    def chip(s): return pill(s, font("Bold", 40), AMBER_D, (255, 200, 61, 70), padx=26, pady=12, outline=AMBER + (170,))
    bd = dict(dims=[(C[8], 0.35)], t_out=bo)
    content.append(El(chip("STEP 1  ·  everyone on a different day"), W / 2, 520, BOARD_T + 0.1, 0.4, **bd))
    LX = 250
    rows = [(4, 645, r"\mathrm{1st\ student:}\ \ \dfrac{365}{365}", 0), (5, 800, r"\mathrm{2nd\ student:}\ \ \dfrac{364}{365}", 1)]
    for (ci, y, s, k) in rows:
        content.append(El(student(78, PALETTE[k]), LX - 40, y, C[ci], 0.4, kind="pop", **bd))
        content.append(WEl(tex(s, 56, INK), W / 2 + 70, y, at(ci, 0.3), 0.7, kind="wipe", **bd))
    content.append(El(tex(r"\vdots", 56, INK2), W / 2 + 70, 900, C[6], 0.3, **bd))
    content.append(El(student(78, PALETTE[10]), LX - 40, 1000, C[6] + 0.1, 0.4, kind="pop", **bd))
    content.append(WEl(tex(r"\mathrm{23rd\ student:}\ \ \dfrac{343}{365}", 56, INK), W / 2 + 70, 1000, at(6, 0.3), 0.7, kind="wipe", **bd))
    content.append(El(text_img("365 - 22 = 343", font("Bold", 42), TEAL_D), W / 2 + 70, 1095, at(6, 0.75), t_out=C[8]))
    content.append(El(chip("STEP 2  ·  multiply them all"), W / 2, 1170, C[7], 0.4, **bd))
    content.append(WEl(tex(r"\dfrac{365}{365}\cdot\dfrac{364}{365}\cdots\dfrac{343}{365}\ \approx\ 0.49", 60, INK), W / 2, 1295, at(7, 0.15), 1.0, kind="wipe", **bd))
    # answer + sticker
    ans_m = tex(r"P(\mathrm{match}) = 1 - 0.49 \approx 0.51", 72, NAVY)
    padx, pady = 50, 30
    bw2, bh2 = ans_m.width + 2 * padx, ans_m.height + 2 * pady
    box = Image.new("RGBA", (bw2 + 80, bh2 + 80), (0, 0, 0, 0))
    gl = Image.new("RGBA", box.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([30, 30, bw2 + 50, bh2 + 50], radius=36, fill=YEL + (160,))
    box.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22)))
    inner = Image.new("RGBA", box.size, (0, 0, 0, 0))
    ImageDraw.Draw(inner).rounded_rectangle([40, 40, bw2 + 40, bh2 + 40], radius=32, fill=YEL)
    box.alpha_composite(inner); box.alpha_composite(ans_m, dest=(40 + padx, 40 + pady))
    content.append(Pulse(radial(420, (255, 220, 120), 120), W / 2, 1490, ANS_T, 1.0))
    content.append(El(box, W / 2, 1490, ANS_T, 0.5, kind="pop", t_out=bo))
    content.append(V.Shine(inner, W / 2, 1490, ANS_T + 0.45))
    content.append(El(sticker("51%!"), W / 2 + 270, 1385, STICK_T, 0.45, kind="pop", t_out=bo))

    # ===== WHY SO HIGH: 253 pairs =====
    wo = END_T
    content.append(El(chip("WHY SO HIGH?"), W / 2, 400, C[10], 0.4, t_out=wo))
    content.append(Network(W / 2, 790, 285, C[10] + 0.05, LINES_A, LINES_B, C[11], E[11] + 0.1, wo))
    pairs = [text_line(f"{k} pairs", font("Bold", 104), AMBER) for k in range(254)]
    content.append(Counter(pairs, W / 2, 1200, LINES_A, LINES_B - LINES_A, t_out=wo))
    content.append(WEl(tex(r"{}^{23}C_{2} = \dfrac{23 \times 22}{2} = 253", 62, INK), W / 2, 1335, C[11], 0.7, kind="wipe", t_out=wo))
    content.append(El(pill("Try it in your class!", font("Bold", 56), NAVY, YEL, padx=40, pady=20), W / 2, 1490, C[12], 0.4, kind="pop", t_out=wo))

    # ===== END CARD =====
    end.append(Rings(W / 2, 800, C[13] + 0.1))
    end.append(El(logo_light(1.75), W / 2, 800, C[13], 0.5, kind="pop"))
    end.append(El(text_img("Follow for daily Class 12 maths", font("Bold", 54), INK), W / 2, 960, C[13] + 0.15))
    end.append(El(text_img("JEE  ·  NEET  ·  Boards", font("Bold", 44), AMBER_D), W / 2, 1045, C[13] + 0.3))
    end.append(El(pill("www.tutorda.org", font("Bold", 58), NAVY, YEL, padx=48, pady=24), W / 2, 1190, C[13] + 0.4, 0.4, kind="pop"))
    return content, ui, fx, end

def init():
    if V.SCENE is None:
        V.SCENE = build(); V.finishing_assets()

def sfx_schedule(s):
    pop, chalk, buzz, whoosh, ding, shimmer, note = (s[k] for k in ("pop", "chalk", "buzz", "whoosh", "ding", "shimmer", "note"))
    for k in range(23): pop(C[0] + 0.25 + k * 0.035, 600 + k * 22, 0.045)
    shimmer(MATCH_T); pop(MATCH_T + 0.08, 1150, 0.12)
    pop(C[1] + 0.05, 800, 0.1); buzz(STRIKE_T); pop(FIFTY_T, 1200, 0.2); shimmer(FIFTY_T + 0.6)
    whoosh(T1 - 0.2, 0.45, 0.12)
    pop(T1 + 0.05, 1000, 0.16); chalk(at(2, 0.35), 0.6); whoosh(at(2, 0.6), 0.6, 0.07)
    whoosh(C[3] + 0.1, 0.5, 0.07); chalk(C[3] + 0.35, 0.8)
    whoosh(BOARD_T - 0.3, 0.6, 0.11)
    for ci in (4, 5): pop(C[ci], 900, 0.1); chalk(at(ci, 0.3), 0.6)
    pop(C[6] + 0.1, 900, 0.1); chalk(at(6, 0.3), 0.6); pop(C[7], 820, 0.1); chalk(at(7, 0.15), 1.0)
    ding(ANS_T); ding(ANS_T + 0.12, 1568, 0.1)
    pop(STICK_T, 1300, 0.22); shimmer(STICK_T + 0.05)
    whoosh(REAL_T - 0.1, 0.6, 0.1)
    for k in range(23): pop(C[10] + 0.05 + k * 0.025, 700 + k * 25, 0.035)
    for k in range(8): ding(LINES_A + k * (LINES_B - LINES_A) / 8, note(72 + [0, 2, 4, 7, 9, 12, 14, 16][k]), 0.035)
    pop(LINES_B, 1250, 0.16); chalk(C[11], 0.7)
    pop(C[12], 1200, 0.2); shimmer(C[12] + 0.05)
    whoosh(C[13] - 0.45, 0.4, 0.08); shimmer(E[13] + 0.05)

def render_chunk(args):
    i0, i1, path = args
    init()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(i0, i1): p.stdin.write(V.render(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return path

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        init()
        ts = [float(x) for x in sys.argv[2:]]
        ims = [V.render(t).resize((360, 640)) for t in ts]
        sheet = Image.new("RGB", (370 * len(ims), 640), "white")
        for k, im in enumerate(ims): sheet.paste(im, (k * 370, 0))
        sheet.save(os.path.join(KIT, "chk", "bday_v1_sheet.png")); print("ok")
    elif sys.argv[1] == "times":
        print(json.dumps(dict(T1=T1, BOARD_T=BOARD_T, REAL_T=REAL_T, END_T=END_T, MATCH_T=MATCH_T, FIFTY_T=FIFTY_T,
                              ANS_T=ANS_T, STICK_T=STICK_T, LA=LINES_A, LB=LINES_B, C=[round(c, 2) for c in C], DUR=DUR)))
    else:
        import multiprocessing as mp
        out = sys.argv[2]; nw = int(os.environ.get("WORKERS", "2"))
        bounds = np.linspace(0, NF, nw * 2 + 1).astype(int)
        jobs = [(int(bounds[k]), int(bounds[k + 1]), os.path.join(KIT, "out", f"seg5_{k:02d}.mp4")) for k in range(len(bounds) - 1)]
        R.build_audio(os.path.join(KIT, "out", "mix_v5.wav"), schedule=sfx_schedule)
        with mp.Pool(nw) as pool: segs = pool.map(render_chunk, jobs)
        open(os.path.join(KIT, "out", "segs5.txt"), "w").write("".join(f"file '{s}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(KIT, "out", "segs5.txt"),
                        "-i", os.path.join(KIT, "out", "mix_v5.wav"), "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
        print("done", NF, DUR)
