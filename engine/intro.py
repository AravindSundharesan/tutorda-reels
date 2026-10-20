"""TutorDA introduction reel: timing (from the voice + word times) and the audio mix.
Used by engine/manim_intro.py (picture) and tools/manim_build.sh (audio)."""
import os, sys, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/tutorda_intro")
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
    for t in SCENES[:6]: smp(t - 0.12, "whoosh-short", 0.20)      # scene changes
    smp(wt(0, 5, 0.1), "tap", 0.20)                                 # "All in one place" -> logo
    smp(wt(3, 13, -0.1), "success-chime", 0.20)                     # after "free" (not on the word)
    smp(C[6] + 0.05, "success-bell", 0.20)                          # call to action

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.42, music_dips=[(C[6] - 0.3, 0.45, 10)], samples=load_samples())
