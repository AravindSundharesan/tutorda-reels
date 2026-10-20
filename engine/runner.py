"""Fast build runner for kit reels (reel5b, reel6 and newer).

python3 engine/runner.py <module> final OUT.mp4   [--from A --to B] [--workers N]
python3 engine/runner.py <module> draft OUT.mp4   [--from A --to B] [--workers N]

final : 1080x1920 @ 30 fps, ONE encode straight to upload size (x264 veryfast, CRF 18, capped at 5.5 Mbps,
        so a 40 s reel stays under 30 MB). Replaces the old master + two-pass upload encode (~2x faster overall).
draft : 540x960 @ 15 fps, ultrafast encode, for checking timing and motion (~4x faster than final).
--from/--to : render only that stretch (seconds), e.g. to re-check one scene after a fix.

A reel module must provide: init() (builds reel4.SCENE), make_audio(path), and use reel4.render(t).
The scene is built once in the parent and shared with the workers (fork), audio is cached until its inputs change.
"""
import os, sys, time, json, hashlib, argparse, subprocess, importlib
import multiprocessing as mp
import numpy as np

ENGINE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)

MODES = {
    "final": dict(fps_div=1, scale=None, x264=["-preset", "veryfast", "-crf", "18", "-maxrate", "5500k", "-bufsize", "11000k"]),
    "draft": dict(fps_div=2, scale="540:960", x264=["-preset", "ultrafast", "-crf", "26"]),
}
M = None; V = None; CFG = None

def encode_chunk(job):
    i0, i1, path = job
    R = sys.modules["reel2"]; fps = R.FPS // CFG["fps_div"]
    vf = ["-vf", f"scale={CFG['scale']}:flags=area"] if CFG["scale"] else []
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{R.W}x{R.H}",
                          "-r", str(fps), "-i", "-", *vf, "-c:v", "libx264", *CFG["x264"], "-pix_fmt", "yuv420p", path],
                         stdin=subprocess.PIPE)
    for n in range(i0, i1, CFG["fps_div"]): p.stdin.write(V.render(n / R.FPS).tobytes())
    p.stdin.close(); p.wait(); return path

def audio_cached(out_dir):
    """Rebuild the mix only when the script, voice clips, word times, sounds or the reel code changed."""
    R = sys.modules["reel2"]; h = hashlib.sha1()
    vo = os.environ["VO"]; files = [os.environ["CLIPS"], M.__file__, os.path.join(ENGINE, "reel2.py")]
    files += sorted(os.path.join(vo, f) for f in os.listdir(vo) if f.endswith((".wav", ".json")))
    for f in files: h.update(open(f, "rb").read())
    path = os.path.join(out_dir, f"mix_{M.__name__}_{h.hexdigest()[:10]}.wav")
    if not os.path.exists(path):
        for f in os.listdir(out_dir):
            if f.startswith(f"mix_{M.__name__}_"): os.remove(os.path.join(out_dir, f))
        M.make_audio(path)
    return path

# Instagram/Shorts overlays: top bar, bottom caption/username/audio, right-hand like/comment/share column.
# Key content (maths, numbers, captions) must sit inside this box; the logo header and the website line are exempt.
SAFE = dict(left=85, top=220, right=1080 - 120, bottom=1520)

def safe_check(M):
    """Flags key content whose resting box leaves the safe area. Returns a list of problems."""
    V = sys.modules["reel4"]; R = sys.modules["reel2"]
    content, ui, fx, end = V.SCENE; bad = []
    cam = getattr(M, "CAM_MAX", 1.0)        # content is zoomed by the camera (breathe + punch-ins); captions/UI are not
    def box_of(e):
        img = getattr(e, "img", None)
        if img is None and getattr(e, "imgs", None): img = max(e.imgs, key=lambda im: im.width)
        if img is None and getattr(e, "base", None) is not None: img = e.base
        if img is None: return None
        cx = getattr(e, "cx", R.W / 2)          # caption bars are centred
        bb = img.getchannel("A").point(lambda v: 255 if v > 100 else 0).getbbox() or (0, 0, img.width, img.height)
        X, Y = cx - img.width / 2, e.cy - img.height / 2   # only the visible part counts (not soft glow margins)
        return (X + bb[0], Y + bb[1], X + bb[2], Y + bb[3])
    items = [(e, "content") for e in content] + [(e, "caption") for e in ui if type(e).__name__.startswith("Karaoke")]
    for e, kind in items:
        b = box_of(e)
        if b is None: continue
        x0, y0, x1, y1 = b; why = []
        if kind == "content" and cam != 1.0:
            fx, fy = R.W / 2, R.H / 2 - 40
            x0, x1 = fx + (x0 - fx) * cam, fx + (x1 - fx) * cam; y0, y1 = fy + (y0 - fy) * cam, fy + (y1 - fy) * cam
        if x0 < SAFE["left"] - 1: why.append(f"left edge {x0:.0f}")
        if x1 > SAFE["right"] + 1: why.append(f"right edge {x1:.0f} (button column)")
        if y0 < SAFE["top"] - 1: why.append(f"top {y0:.0f}")
        if y1 > SAFE["bottom"] + 1: why.append(f"bottom {y1:.0f} (caption overlay)")
        if why:
            t = getattr(e, "t_in", getattr(e, "t0", getattr(e, "ti", 0)))
            bad.append(f"{kind} {type(e).__name__} at ({getattr(e, 'cx', R.W / 2):.0f},{e.cy:.0f}) from {max(0, t):.1f}s: " + ", ".join(why))
    return bad

def stills(M, times, out):
    """Stills with the platform overlay zones shaded red, for eyeballing collisions."""
    from PIL import Image, ImageDraw
    V = sys.modules["reel4"]; R = sys.modules["reel2"]; ims = []
    for t in times:
        im = V.render(t).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for r in ([0, 0, R.W, SAFE["top"]], [0, SAFE["bottom"], R.W, R.H], [SAFE["right"], 0, R.W, R.H], [0, 0, SAFE["left"], R.H]):
            d.rectangle(r, fill=(229, 72, 77, 55))
        im.alpha_composite(ov); ims.append(im.convert("RGB").resize((360, 640)))
    sheet = Image.new("RGB", (370 * len(ims), 640), "white")
    for k, im in enumerate(ims): sheet.paste(im, (k * 370, 0))
    sheet.save(out); print("stills with safe zones:", out)

def main():
    global M, V, CFG
    if len(sys.argv) > 2 and sys.argv[2] in ("check", "stills"):
        M = importlib.import_module(sys.argv[1]); M.init()
        if sys.argv[2] == "stills":
            stills(M, [float(x) for x in sys.argv[3:]], os.path.join(KIT, "chk", f"{sys.argv[1]}_safe.png"))
        bad = safe_check(M)
        print("SAFE AREA: " + ("OK - all key content inside the platform-safe box" if not bad else f"{len(bad)} problem(s)"))
        for b in bad: print("  !", b)
        return
    ap = argparse.ArgumentParser(); ap.add_argument("module"); ap.add_argument("mode", choices=MODES); ap.add_argument("out")
    ap.add_argument("--from", dest="t0", type=float, default=0.0); ap.add_argument("--to", dest="t1", type=float, default=None)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 2)
    a = ap.parse_args(); CFG = MODES[a.mode]
    T = time.time()
    M = importlib.import_module(a.module); V = sys.modules["reel4"]; R = sys.modules["reel2"]
    M.init()                                            # built once, inherited by the forked workers
    n0 = int(round(a.t0 * R.FPS)); n1 = R.NF if a.t1 is None else min(R.NF, int(round(a.t1 * R.FPS)))
    out_dir = os.path.join(KIT, "out"); os.makedirs(out_dir, exist_ok=True)
    nchunks = max(1, a.workers * 3)
    step = CFG["fps_div"]
    edges = np.linspace(n0, n1, nchunks + 1).astype(int); edges = (edges // step) * step; edges[-1] = n1
    jobs = [(int(edges[k]), int(edges[k + 1]), os.path.join(out_dir, f"seg_{a.mode}_{k:03d}.mp4"))
            for k in range(nchunks) if edges[k + 1] > edges[k]]
    mix = audio_cached(out_dir)
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers) as pool: segs = pool.map(encode_chunk, jobs, chunksize=1)
    lst = os.path.join(out_dir, f"segs_{a.mode}.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    t_from, t_dur = n0 / R.FPS, (n1 - n0) / R.FPS
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-ss", f"{t_from:.3f}", "-t", f"{t_dur:.3f}", "-i", mix, "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", a.out], check=True)
    for s in segs: os.remove(s)
    os.remove(lst)
    print(f"{a.mode}: {a.out}  ({t_dur:.1f}s of video, {len(range(n0, n1, step))} frames, {a.workers} workers) in {time.time() - T:.0f}s")

if __name__ == "__main__":
    main()
