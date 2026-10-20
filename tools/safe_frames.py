"""Safe-area check on a rendered video (works for any engine, incl. Manim).
Flags frames where content shows inside Instagram's overlay zones: right column x>960 and left strip x<85 (y 220-1520),
and the bottom area y>1600 (below the website line). Header (y<220) and the website line are exempt.
Usage: python3 tools/safe_frames.py VIDEO.mp4"""
import sys, subprocess, numpy as np
v = sys.argv[1]; W, H = 540, 960; s = 0.5                       # half-size frames, scale zone limits by 0.5
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", v, "-vf", f"fps=4,scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
zones = {"right column": (slice(110, 760), slice(480, W)), "left strip": (slice(110, 760), slice(0, 42)), "bottom": (slice(800, H), slice(0, W))}
bad = {}
for i, f in enumerate(fr):
    bgc = np.median(f[300:700, :, :].reshape(-1, 3), axis=0)      # background colour of this frame
    for name, (ys, xs) in zones.items():
        z = f[ys, xs]; ink = (np.abs(z - bgc).sum(-1) > 60).mean()
        if ink > 0.004: bad.setdefault(name, []).append(i / 4)
if not bad: print("SAFE AREA (frames): OK")
for name, ts in bad.items():
    print(f"SAFE AREA (frames): content in {name} at " + ", ".join(f"{t:.2f}s" for t in ts[:12]) + (" ..." if len(ts) > 12 else ""))
