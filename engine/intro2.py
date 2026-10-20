"""TutorDA introduction reel: timing (from the voice + word times) and the audio mix.
Used by engine/manim_intro.py (picture) and tools/manim_build.sh (audio)."""
import os, sys, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/tutorda_intro2")
os.environ["CLIPS"] = os.path.join(TOPIC, "clips.json")
os.environ["VO"] = os.path.join(TOPIC, "vo")
os.environ["MUSIC"] = "energetic"
os.environ["END_HOLD"] = "1.4"
os.environ["START"] = "0.15"
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

def sfx_schedule(s):
    smp = s["sample"]
    for k in (1, 2, 3): smp(wt(0, k, 0.04), "tap", 0.22)            # hook words land
    smp(wt(0, 6, 0.05), "pop-2", 0.2)                                # "5 APPS?"
    smp(C[1] - 0.45, "sweep-long", 0.16)                             # words collapse into the logo
    smp(C[1] - 0.1, "stinger-hit-short", 0.22)                       # logo reveal
    for i in (2, 3, 4, 5, 6, 7): smp(C[i] - 0.37, "whoosh-short", 0.18)   # scene changes
    smp(wt(3, 7, 0.1) + 0.9, "check-mark", 0.18)                     # solution ticked
    for k in (5, 6, 7, 9): smp(wt(5, k, 0.08), "tap", 0.14)          # exam chips
    smp(wt(5, 14, 0.05), "success-chime", 0.2)                       # Mock 1 free
    smp(wt(7, 4, 0.15), "success-bell", 0.2)                         # tutorda.org

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.42, music_dips=[(C[7] - 0.3, 0.45, 10)], samples=load_samples())
