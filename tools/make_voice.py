"""Generate one voice clip per sentence (Kokoro) with the energetic chain.
Usage: python3 tools/make_voice.py TOPIC_DIR [voice=hm_omega] [speed=1.22] [expand=1.35] [lift=1.5] [--only 3,5 --speed-only 1.17]
- reads TOPIC_DIR/clips.json: [[beat, spoken_text, caption_text], ...]; spoken text may start with PHONEMES:
- writes TOPIC_DIR/vo/cNN.wav and vo/durs.json
- expand=1.0 lift=0 gives the plain (non-energetic) voice"""
import os, sys, json, subprocess, argparse
import numpy as np, soundfile as sf, pyworld as pw
from kokoro_onnx import Kokoro
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.environ.get("MODELS_DIR", os.path.join(KIT, "models"))
ap = argparse.ArgumentParser(); ap.add_argument("topic"); ap.add_argument("voice", nargs="?", default="hm_omega")
ap.add_argument("speed", nargs="?", type=float, default=1.22); ap.add_argument("expand", nargs="?", type=float, default=1.35)
ap.add_argument("lift", nargs="?", type=float, default=1.5); ap.add_argument("--lang", default="en-us")
ap.add_argument("--only", default=""); a = ap.parse_args()
k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
clips = json.load(open(os.path.join(a.topic, "clips.json")))
out = os.path.join(a.topic, "vo"); os.makedirs(out, exist_ok=True)
dpath = os.path.join(out, "durs.json")
durs = json.load(open(dpath)) if os.path.exists(dpath) else [0.0] * len(clips)
durs += [0.0] * (len(clips) - len(durs)); durs = durs[:len(clips)]
only = {int(x) for x in a.only.split(",") if x.strip()}
CHAIN = ("highpass=f=85,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=4,"
         "equalizer=f=8000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=4:attack=4:release=70:makeup=5,alimiter=limit=0.95")
for i, (_, say, _) in enumerate(clips):
    if only and i not in only: continue
    if say.startswith("PHONEMES:"):
        y, sr = k.create(say[9:], voice=a.voice, speed=min(a.speed, 1.05), is_phonemes=True)
    else:
        y, sr = k.create(say, voice=a.voice, speed=a.speed, lang=a.lang)
    x = y.astype(np.float64)
    if a.expand != 1.0 or a.lift != 0:
        f0, t = pw.harvest(x, sr, f0_floor=60, f0_ceil=450, frame_period=5.0)
        sp = pw.cheaptrick(x, f0, t, sr); ap_ = pw.d4c(x, f0, t, sr)
        v = f0 > 0; med = np.median(f0[v])
        f1 = f0.copy(); f1[v] = med * (f0[v] / med) ** a.expand * 2 ** (a.lift / 12)
        x = pw.synthesize(f1, sp, ap_, sr, frame_period=5.0)
    idx = np.where(np.abs(x) > 0.008)[0]; x = x[max(0, idx[0] - 480): idx[-1] + 1900]
    raw = os.path.join(out, f"raw{i:02d}.wav"); sf.write(raw, x / max(1e-9, np.abs(x).max()) * 0.7, sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", CHAIN, "-ar", str(sr), os.path.join(out, f"c{i:02d}.wav")], check=True)
    os.remove(raw)
    yy, _ = sf.read(os.path.join(out, f"c{i:02d}.wav")); durs[i] = round(len(yy) / sr, 3)
json.dump(durs, open(dpath, "w")); print(durs, "total", round(sum(durs), 2), "s")
