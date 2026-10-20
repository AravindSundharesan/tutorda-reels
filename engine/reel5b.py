"""Birthday Paradox v2: same scenes, upgraded with craft rules from the video-skills research.
- word-level karaoke + key animations fired on real word times (Zipformer alignment)
- hook fully composed on frame 0
- one spring moment (answer box + 51% sticker); everything else lands without overshoot
- fewer, cleaner CC0 sound effects; music lower with a dip before the big reveals
- shorter end card
python3 reel5b.py preview t ... | build out.mp4
"""
import os, sys, json, subprocess
os.environ["END_HOLD"] = "0.35"
import numpy as np
from PIL import Image
import reel5 as B
import reel4 as V
import reel2 as R
from reel2 import W, H, FPS, C, E, DUR, NF, CLIPS, EXPO_OUT, clamp, El

WT = json.load(open(os.path.join(B.TOPIC, "word_times.json")))
def wt(i, word_idx, lead=0.0):
    return WT[i]["starts"][word_idx] - lead

# ---- re-time key moments to the spoken words (visual leads the word slightly) ----
B.MATCH_T = wt(0, 9, 0.15)          # "share"
B.STRIKE_T = wt(1, 3, 0.0)          # "tiny."
B.FIFTY_T = wt(1, 6, 0.25)          # "50%!"
B.STICK_T = wt(9, 1, 0.12)          # "51%!"
B.LINES_A = C[10] + 0.45
B.LINES_B = wt(10, 7, -0.55)        # count completes just after "253"
B.END_T = C[13] - 0.1
V.END_T = B.END_T
# fewer, calmer punch-ins: only on the three stressed reveals, no shake
V.PUNCH = [(B.FIFTY_T, 0.04, (W / 2, 1000), False), (B.ANS_T, 0.035, (W / 2, 1480), False),
           (B.LINES_B, 0.035, (W / 2, 1200), False)]
# network avatars: critically damped (no overshoot)
B.spring = lambda t, bounce=0.0, visual_duration=0.4: R.spring(t, 0.0, visual_duration)

class KaraokeW(V.Karaoke):
    """Highlights each word at its real spoken start time; no bouncy scale."""
    def __init__(self, i):
        super().__init__(i)
        self.starts = np.array(WT[i]["starts"])
        if i == 0: self.t0 = -1.0                      # hook question readable on frame 0
    def draw(self, frame, t):
        if t < self.t0 or t >= self.t1: return
        k = int(np.searchsorted(self.starts, t, side="right")) - 1
        im = self.base.copy()
        if k >= 0:
            x, y = self.wpos[k]; im.alpha_composite(self.wimg[k], dest=(int(x), int(y)))
        el = t - self.t0
        sc = 0.96 + 0.04 * EXPO_OUT(clamp(el / 0.25))
        V.comp(frame, im, W / 2, self.cy, alpha=1.0 if self.t0 < 0 else EXPO_OUT(clamp(el / 0.12)), scale=sc)

def build():
    content, ui, fx, end = B.build()
    spring_moments = {round(B.ANS_T, 3), round(B.STICK_T, 3)}
    hook_window = C[0] + 0.25 + 23 * 0.035 + 0.05
    for lst in (content, end):
        for e in lst:
            if isinstance(e, El):
                if e.kind == "pop" and round(e.t_in, 3) not in spring_moments: e.kind = "land"
                if lst is content and C[0] - 0.01 <= e.t_in <= hook_window and e.t_out is not None and e.t_out < B.T1 + 0.1:
                    e.t_in = -1.0                       # hook title, subtitle and students already on screen
    new_ui = []
    for e in ui:
        if isinstance(e, V.Karaoke): continue
        if isinstance(e, El) and e.t_in <= 0.2: e.t_in = -1.0   # header/footer present on frame 0
        new_ui.append(e)
    for i in range(len(CLIPS) - 1): new_ui.append(KaraokeW(i))
    # keep the board alive between lines: hand-drawn circle around the first fraction while it is discussed
    line = B.tex(r"\mathrm{1st\ student:}\ \ \dfrac{365}{365}", 56, B.INK)
    frac = B.tex(r"\dfrac{365}{365}", 56, B.INK)
    fx_c = W / 2 + 70 + line.width / 2 - frac.width / 2
    content.append(B.RoughEllipse(fx_c, 645, frac.width / 2 + 34, frac.height / 2 + 18, wt(4, 4) + 0.35, 0.9, C[5] - 0.05, color=B.AMBER, seed=7))
    # 'Try it in your class!' pill keeps breathing until the end card
    content.append(B.Pulse(B.radial(260, B.YEL, 90), W / 2, 1490, C[12] + 0.55, 1.0))
    return content, new_ui, fx, end

def init():
    if V.SCENE is None:
        V.SCENE = build(); V.finishing_assets()

def load_samples():
    out = {}
    sd = os.path.join(B.KIT, "assets", "sfx")
    for f in os.listdir(sd):
        if not f.endswith(".wav"): continue
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(sd, f), "-ac", "1", "-ar", str(R.SR), "-f", "f32le", "-"],
                             capture_output=True).stdout
        a = np.frombuffer(raw, np.float32).astype(np.float64)
        out[f[:-4]] = a / max(1e-9, np.abs(a).max())
    return out

def sfx_schedule(s):
    smp = s["sample"]
    smp(B.T1 - 0.17, "whoosh-short", 0.30)           # the one whip
    smp(B.STRIKE_T - 0.05, "error-2", 0.28)          # 'tiny' crossed out
    smp(B.FIFTY_T - 0.06, "stinger-hit-short", 0.30) # hero 1: over 50%
    smp(B.T1 + 0.02, "tap", 0.22)                    # 'THE TRICK' label
    smp(B.ANS_T - 0.06, "success-bell", 0.28)        # hero 2: the answer
    smp(B.STICK_T - 0.06, "pop-2", 0.32)             # 51% sticker
    smp(B.LINES_A, "sweep-long", 0.16)               # pair lines start drawing
    smp(B.LINES_B - 0.06, "success-chime", 0.24)     # hero 3: 253 pairs
    smp(C[12] - 0.04, "check-mark", 0.22)            # 'Try it in your class!'

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.42,
                  music_dips=[(B.FIFTY_T - 0.35, 0.45, 10), (B.ANS_T - 0.35, 0.45, 10)], samples=load_samples())

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
        print(json.dumps(dict(DUR=DUR, END_T=B.END_T, T1=B.T1, MATCH=B.MATCH_T, STRIKE=B.STRIKE_T, FIFTY=B.FIFTY_T,
                              ANS=B.ANS_T, STICK=B.STICK_T, LA=B.LINES_A, LB=B.LINES_B, C=[round(c, 2) for c in C])))
    elif sys.argv[1] == "preview":
        init()
        ims = [V.render(float(t)).resize((360, 640)) for t in sys.argv[2:]]
        sheet = Image.new("RGB", (370 * len(ims), 640), "white")
        for k, im in enumerate(ims): sheet.paste(im, (k * 370, 0))
        sheet.save(os.path.join(B.KIT, "chk", "bday_v2_sheet.png")); print("ok")
    else:
        import multiprocessing as mp
        out = sys.argv[2]; nw = 2
        bounds = np.linspace(0, NF, nw * 2 + 1).astype(int)
        jobs = [(int(bounds[k]), int(bounds[k + 1]), os.path.join(B.KIT, "out", f"seg5b_{k:02d}.mp4")) for k in range(len(bounds) - 1)]
        R.build_audio(os.path.join(B.KIT, "out", "mix_v5b.wav"), schedule=sfx_schedule, music_gain=0.42,
                      music_dips=[(B.FIFTY_T - 0.35, 0.45, 10), (B.ANS_T - 0.35, 0.45, 10)], samples=load_samples())
        with mp.Pool(nw) as pool: segs = pool.map(render_chunk, jobs)
        open(os.path.join(B.KIT, "out", "segs5b.txt"), "w").write("".join(f"file '{s}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(B.KIT, "out", "segs5b.txt"),
                        "-i", os.path.join(B.KIT, "out", "mix_v5b.wav"), "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
        print("done", NF, DUR)
