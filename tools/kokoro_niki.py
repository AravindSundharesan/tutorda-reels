"""Kokoro voice shaped toward the measured Niki delivery profile (assets/niki_profile.json):
speaking rate, pitch level + range (Praat PSOLA, keeps the voice's own timbre), long-term spectrum EQ, line pauses.
Usage: kokoro_niki.py VOICE OUT.wav "line 1" "line 2" ...   (env SPEED, PAUSE)"""
import sys, os, json, numpy as np, soundfile as sf, parselmouth, re
from parselmouth.praat import call
from scipy.signal import firwin2, fftconvolve, welch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niki_profile import stats, speech_mask
from kokoro_onnx import Kokoro
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prof = json.load(open(os.path.join(KIT, "assets/niki_profile.json")))
voice, out, lines = sys.argv[1], sys.argv[2], sys.argv[3:]
k = Kokoro(os.path.join(KIT, "models/kokoro-v1.0.onnx"), os.path.join(KIT, "models/voices-v1.0.bin"))
SPEED = float(os.environ.get("SPEED", "1.0")); PAUSE = float(os.environ.get("PAUSE", "0.55"))
sr = 24000; parts = []
for l in lines:
    a, sr = k.create(l, voice=voice, speed=SPEED, lang="en-us"); a = a.astype(np.float64)
    m, h = speech_mask(a, sr, -40); idx = np.where(m)[0]; a = a[max(0, idx[0] * h - 480): (idx[-1] + 1) * h + 960]
    parts += [a, np.zeros(int(sr * PAUSE))]
x = np.concatenate(parts[:-1])
# --- pitch: map median and spread (in semitones) to the Niki profile, PSOLA resynthesis
snd = parselmouth.Sound(x, sr); man = call(snd, "To Manipulation", 0.01, 75, 500)
pt = call(man, "Extract pitch tier"); n = call(pt, "Get number of points")
fs = np.array([call(pt, "Get value at index", i + 1) for i in range(n)]); ts = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
st = 12 * np.log2(fs / np.median(fs)); g = prof["f0_sd_st"] / max(0.5, st.std())
new = prof["f0_median"] * 2 ** (st * g / 12)
pt2 = call("Create PitchTier", "p", 0, snd.duration)
for t, f in zip(ts, new): call(pt2, "Add point", float(t), float(f))
call([pt2, man], "Replace pitch tier"); y = call(man, "Get resynthesis (overlap-add)").values[0]
# --- long-term spectrum EQ toward Niki (smoothed, limited to +-8 dB)
_, fr, P = stats(y, sr); diff = np.array(prof["ltas_db"]) - 10 * np.log10(P + 1e-20)
fr = np.array(prof["ltas_hz"]); oct_ = np.log2(np.maximum(fr, 50))
sm = np.array([diff[(oct_ > o - 1 / 6) & (oct_ < o + 1 / 6)].mean() for o in oct_]); sm -= np.interp(1000, fr, sm)
sm = np.clip(sm, -8, 8); sm[fr < 70] = -12; gain = 10 ** (sm / 20)
fir = firwin2(1025, fr / (sr / 2), gain); y = fftconvolve(y, fir, "same")
y = y / np.abs(y).max() * 0.89; sf.write(out, y, sr)
s, _, _ = stats(y, sr); s0, _, _ = stats(x, sr)
print(json.dumps({"before": {k: round(v, 1) for k, v in s0.items()}, "after": {k: round(v, 1) for k, v in s.items()}, "niki": {k: round(prof[k], 1) for k in ("f0_median", "f0_sd_st", "f0_range_st")}}))
