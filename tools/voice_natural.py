"""Natural-paced Kokoro voice (22 Nov, Aro: 'feels like AI'). Per-sentence speed, real varied pauses, no tempo-up,
no pause capping; light warmth + small-room processing. Usage: python3 tools/voice_natural.py TOPIC_DIR [voice=af_sarah]"""
import sys, json, re, os, subprocess, tempfile, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
T = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else "af_sarah"
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin"); P = lambda t: k.tokenizer.phonemize(t, "en-us")
SPECIAL = {"TutorDA's": "tjˈuːtəɹ dˈɑːz", "TutorDA": "tjˈuːtəɹ dˈɑː", "JEE": "dʒˈeɪ ˈiː ˈiː"}
def ph(line):
    return " ".join(SPECIAL[p] if p in SPECIAL else P(p.strip()) for p in re.split(r"(TutorDA's|TutorDA|JEE)", line) if p.strip())
def trim(a, sr):
    env = np.convolve(np.abs(a), np.ones(240) / 240, "same"); on = np.where(env > 0.01)[0]
    return a[max(0, on[0] - int(0.03 * sr)):min(len(a), on[-1] + int(0.06 * sr))]
plan = json.load(open(f"{T}/plan.json")); durs = []; offs = []
FX = "highpass=f=75,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1.5,aecho=0.85:0.6:18|31:0.10|0.06"
for i, clip in enumerate(plan):
    parts = []; o = []; t = 0.0
    for text, spd, gap in clip:
        a, sr = k.create(ph(text), voice=V, speed=spd, is_phonemes=True); a = trim(a, sr)
        o.append(round(t, 3)); t += len(a) / sr + gap
        parts.append(a)
        if gap: parts.append(np.zeros(int(gap * sr)))
    c = np.concatenate(parts); f = int(0.01 * sr); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
    tmp = tempfile.mktemp(suffix=".wav"); sf.write(tmp, c, sr); p = os.path.join(T, "vo", f"c{i:02d}.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", FX, "-ar", str(sr), "-ac", "1", p]); os.remove(tmp)
    durs.append(round(sf.info(p).duration, 3)); offs.append(o)
json.dump(durs, open(os.path.join(T, "vo", "durs.json"), "w")); json.dump(offs, open(os.path.join(T, "vo", "offsets.json"), "w")); print(durs, round(sum(durs), 2)); print(offs)
