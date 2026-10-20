"""Voice v2 ("clean energetic"): one Kokoro clip per sentence, no vocoder resynthesis.
Why: v1 re-synthesised every line through WORLD (pitch x1.35, +1.5 st) at speed 1.22, which adds a buzzy,
robotic edge and rushes the words. v2 keeps the model's own audio, gets energy from the voice blend,
punctuation and a lighter broadcast chain, and runs at a calmer speed.

Usage: python3 tools/make_voice2.py TOPIC_DIR [--voice hm_omega] [--blend am_puck:0.25] [--speed 1.12] [--only 3,5]
- voice blend mixes style vectors (e.g. 75% hm_omega + 25% am_puck): keeps the Indian accent, adds lift.
- writes TOPIC_DIR/vo/cNN.wav and vo/durs.json (same format as make_voice.py)"""
import os, sys, json, subprocess, argparse
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.environ.get("MODELS_DIR", os.path.join(KIT, "models"))
CHAIN = ("highpass=f=75,equalizer=f=180:t=q:w=1:g=-1.5,equalizer=f=2800:t=q:w=1.4:g=2.5,"
         "equalizer=f=6500:t=q:w=2:g=-1.5,"                       # tame sibilance instead of boosting it
         "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=3,alimiter=limit=0.97")

def style(k, voice, blend):
    if not blend: return voice
    v = k.get_voice_style(voice); other, w = blend.split(":"); w = float(w)
    return (1 - w) * v + w * k.get_voice_style(other)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("topic")
    ap.add_argument("--voice", default="hm_omega"); ap.add_argument("--blend", default="am_puck:0.25")
    ap.add_argument("--speed", type=float, default=1.12); ap.add_argument("--only", default="")
    ap.add_argument("--lang", default="en-us"); a = ap.parse_args()
    k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
    sty = style(k, a.voice, a.blend)
    clips = json.load(open(os.path.join(a.topic, "clips.json")))
    out = os.path.join(a.topic, "vo"); os.makedirs(out, exist_ok=True)
    dpath = os.path.join(out, "durs.json")
    durs = json.load(open(dpath)) if os.path.exists(dpath) else [0.0] * len(clips)
    durs += [0.0] * (len(clips) - len(durs)); durs = durs[:len(clips)]
    only = {int(x) for x in a.only.split(",") if x.strip()}
    for i, (_, say, _) in enumerate(clips):
        if only and i not in only: continue
        if say.startswith("PHONEMES:"):
            y, sr = k.create(say[9:], voice=sty, speed=min(a.speed, 1.05), is_phonemes=True)
        else:
            y, sr = k.create(say, voice=sty, speed=a.speed, lang=a.lang)
        x = y.astype(np.float64)
        idx = np.where(np.abs(x) > 0.008)[0]; x = x[max(0, idx[0] - 480): idx[-1] + 2400]
        raw = os.path.join(out, f"raw{i:02d}.wav"); sf.write(raw, x / max(1e-9, np.abs(x).max()) * 0.7, sr)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", CHAIN, "-ar", str(sr),
                        os.path.join(out, f"c{i:02d}.wav")], check=True)
        os.remove(raw)
        yy, _ = sf.read(os.path.join(out, f"c{i:02d}.wav")); durs[i] = round(len(yy) / sr, 3)
    json.dump(durs, open(dpath, "w")); print(durs, "total", round(sum(durs), 2), "s")
