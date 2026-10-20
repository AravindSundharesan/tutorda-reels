"""TutorDA JEE reel (30 s): timing (from the voice + word times) and the audio mix.
Used by engine/manim_intro.py (picture) and tools/manim_build.sh (audio)."""
import os, sys, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/math_area")
os.environ["CLIPS"] = os.path.join(TOPIC, "clips.json")
os.environ["VO"] = os.path.join(TOPIC, "vo")
os.environ["MUSIC"] = "cinematic"
os.environ["MUSIC_FILE"] = os.path.join(KIT, "assets/svc/score.mp3")      # ACE-Step (Hugging Face) score
os.environ["MUSIC_OFFSET"] = "10.0"
os.environ["END_HOLD"] = "0.9"
os.environ["START"] = "0.05"; os.environ["IN_GAP"] = "0.12"; os.environ["BEAT_GAP"] = "0.18"
import numpy as np
import reel2 as R
import reel4 as V
from reel2 import C, E, DUR, CLIPS
from reel4 import logo_light

WT = json.load(open(os.path.join(TOPIC, "word_times.json")))
def _shift(i): return C[i] - WT[i].get("clip_start", C[i])
def wt(i, k, lead=0.0): return WT[i]["starts"][k] + _shift(i) - lead

# scene changes (just before each new idea is spoken)


def load_samples():
    out, sd = {}, os.path.join(KIT, "assets", "sfx")
    for f in os.listdir(sd):
        if not f.endswith(".wav"): continue
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(sd, f), "-ac", "1", "-ar", str(R.SR), "-f", "f32le", "-"],
                             capture_output=True).stdout
        a = np.frombuffer(raw, np.float32).astype(np.float64); out[f[:-4]] = a / max(1e-9, np.abs(a).max())
    rd = os.path.join(KIT, "assets", "sfx_rw")                              # Runway (ElevenLabs SFX) one-shots
    for f in os.listdir(rd):
        if f.endswith(".mp3") and f != "score.mp3":
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(rd, f), "-ac", "1", "-ar", str(R.SR), "-f", "f32le", "-"],
                                 capture_output=True).stdout
            a = np.frombuffer(raw, np.float32).astype(np.float64); out["rw_" + f[:-4]] = a / max(1e-9, np.abs(a).max())
    return out

os.environ["TICK_UNTIL"] = "0"
def events():
    f = os.path.join(KIT, "out", "area_events.json")
    return json.load(open(f)) if os.path.exists(f) else []
def sfx_schedule(s):
    smp = s["sample"]
    for name, t in events():
        if name == "wipe": smp(t - 0.05, "rw_whoosh", 0.15)
        elif name == "tick": smp(t - 0.02, "rw_tick", 0.16)
        elif name == "chime": smp(t - 0.02, "rw_chime", 0.20)
        elif name == "stamp": smp(t - 0.02, "rw_marker", 0.26)
        elif name == "wordmark": smp(t - 0.04, "rw_impact", 0.26)

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.5, music_dips=[], samples=load_samples())
