"""TutorDA introduction reel: timing (from the voice + word times) and the audio mix.
Used by engine/manim_intro.py (picture) and tools/manim_build.sh (audio)."""
import os, sys, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = os.path.join(KIT, "topics/tutorda_brand_niki")
os.environ["CLIPS"] = os.path.join(TOPIC, "clips.json")
os.environ["VO"] = os.path.join(TOPIC, "vo")
os.environ["MUSIC"] = "cinematic"
os.environ["MUSIC_FILE"] = os.path.join(KIT, "assets/sfx_rw/score.mp3")   # ACE-Step (Hugging Face) score
os.environ["MUSIC_OFFSET"] = "0.75"                                        # its build lands on "Meet TutorDA"
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
    rd = os.path.join(KIT, "assets", "sfx_rw")                              # Runway (ElevenLabs SFX) one-shots
    for f in os.listdir(rd):
        if f.endswith(".mp3") and f != "score.mp3":
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(rd, f), "-ac", "1", "-ar", str(R.SR), "-f", "f32le", "-"],
                                 capture_output=True).stdout
            a = np.frombuffer(raw, np.float32).astype(np.float64); out["rw_" + f[:-4]] = a / max(1e-9, np.abs(a).max())
    return out

os.environ["MUSIC_CUES"] = ",".join(str(round(x, 2)) for x in (C[2] - 0.2, C[3] - 0.25, C[9] - 0.3, C[11] - 0.3))
os.environ["TICK_UNTIL"] = str(round(C[2] - 0.3, 2))                       # clock ticks under the "sameness" open
def events():
    f = os.path.join(KIT, "out", "film2_events.json")
    return json.load(open(f)) if os.path.exists(f) else []
def sfx_schedule(s):
    smp = s["sample"]; ev = events()
    smp(wt(0, 6, 0.05), "stinger-hit-short", 0.10)                    # THE SAME WAY stamp
    for k in (0, 2, 4): smp(wt(1, k, 0.02), "rw_tick", 0.22)          # SAME / SAME / SAME
    for name, t in ev:
        if name == "wipe": smp(t - 0.05, "rw_whoosh", 0.16)           # panel wipes
        if name in ("strike", "strike2"): smp(t - 0.02, "rw_marker", 0.30)
        if name == "wordmark": smp(t - 0.04, "rw_impact", 0.34)        # Meet TutorDA
        if name == "wordmark_end": smp(t - 0.04, "rw_impact", 0.22)
    smp(wt(5, 1, 0.05), "rw_tick", 0.16)
    smp(wt(7, 13, 0.05), "rw_chime", 0.22)                            # mastered
    smp(wt(8, 12, 0.1), "rw_chime", 0.14)                             # 24/7
    for k in (2, 4, 7, 9, 11): smp(wt(9, k, 0.06), "rw_tick", 0.14)   # breadth list
    for k in (4, 5, 7): smp(wt(10, k, 0.06), "rw_tick", 0.14)         # FREE tiles

def make_audio(path):
    R.build_audio(path, schedule=sfx_schedule, music_gain=0.55, music_dips=[], samples=load_samples())
