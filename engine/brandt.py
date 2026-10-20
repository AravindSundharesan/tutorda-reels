"""TutorDA introduction reel: timing (from the voice + word times) and the audio mix.
Used by engine/manim_intro.py (picture) and tools/manim_build.sh (audio)."""
import os, sys, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/tutorda_brand")
os.environ["CLIPS"] = os.path.join(TOPIC, "clips.json")
os.environ["VO"] = os.path.join(TOPIC, "vo")
os.environ["MUSIC"] = "cinematic"
os.environ["END_HOLD"] = "2.2"
os.environ["START"] = "0.3"; os.environ["IN_GAP"] = "0.25"; os.environ["BEAT_GAP"] = "0.55"
import numpy as np
import reel2 as R
import reel4 as V
from reel2 import C, E, DUR, CLIPS
from reel4 import logo_light

WT = json.load(open(os.path.join(TOPIC, "word_times.json")))
def _shift(i): return C[i] - WT[i].get("clip_start", C[i])
def wt(i, k, lead=0.0): return WT[i]["starts"][k] + _shift(i) - lead

# scene changes (just before each new idea is spoken)
SCENES = [C[i] - 0.3 for i in range(1, 8)]

def load_samples():
    out, sd = {}, os.path.join(KIT, "assets", "sfx")
    for f in os.listdir(sd):
        if not f.endswith(".wav"): continue
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(sd, f), "-ac", "1", "-ar", str(R.SR), "-f", "f32le", "-"],
                             capture_output=True).stdout
        a = np.frombuffer(raw, np.float32).astype(np.float64); out[f[:-4]] = a / max(1e-9, np.abs(a).max())
    return out

os.environ["MUSIC_CUES"] = ",".join(str(round(x, 2)) for x in (C[2] - 0.2, C[3] - 0.25, C[9] - 0.3, C[11] - 0.3))
def sfx_schedule(s):
    smp = s["sample"]
    smp(wt(0, 6, 0.05), "stinger-hit-short", 0.12)                    # THE SAME WAY stamp
    for k in (0, 2, 4): smp(wt(1, k, 0.03), "tap", 0.16)              # SAME / SAME / SAME
    smp(C[2] - 0.3, "whoosh-short", 0.2)                               # strips slide in
    smp(C[3] - 0.6, "sweep-long", 0.14)                                # light streak
    smp(wt(4, 3, 0.05), "pop-2", 0.14); smp(wt(4, 4, 0.05), "pop-2", 0.14)
    smp(wt(5, 1, 0.05), "check-mark", 0.16)
    smp(wt(6, 5, 0.12), "stinger-hit-short", 0.14)                    # THE END stamp
    smp(wt(6, 8, 0.1), "whoosh-short", 0.18)                           # paper -> engine
    smp(wt(7, 13, 0.05), "success-chime", 0.18)                        # mastered
    for i in (8, 9, 10, 11): smp(C[i] - 0.38, "whoosh-short", 0.15)
    smp(wt(8, 12, 0.1), "pop-2", 0.14)                                 # 24/7
    for k in (2, 4, 7, 9, 11): smp(wt(9, k, 0.08), "tap", 0.12)       # breadth nodes
    for k in (4, 5, 7): smp(wt(10, k, 0.08), "tap", 0.12)             # FREE tiles
    smp(C[12] - 0.25, "success-bell", 0.18)                            # wordmark

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.55, music_dips=[], samples=load_samples())
