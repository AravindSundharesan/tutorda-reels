"""Kokoro voice shaped to the Niki profile + word emphasis.
Mark stressed words with *asterisks* in each line. Each stressed word gets the three cues a speaker uses:
higher pitch peak (+EMPH_ST semitones), a little longer (x EMPH_DUR), a little louder (+EMPH_DB dB); the words around it stay level.
Usage: kokoro_niki2.py VOICE OUT.wav "line with *stress*" ...   (env SPEED, PAUSE, EMPH_ST, EMPH_DUR, EMPH_DB)"""
import sys, os, json, re, numpy as np, soundfile as sf, parselmouth
from parselmouth.praat import call
from scipy.signal import firwin2, fftconvolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niki_profile import stats, speech_mask
from align_words import recognise, align
import sherpa_onnx
from kokoro_onnx import Kokoro
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prof = json.load(open(os.path.join(KIT, "assets/niki_profile.json")))
voice, out, lines = sys.argv[1], sys.argv[2], sys.argv[3:]
E = os.environ.get
SPEED, PAUSE = float(E("SPEED", "1.0")), float(E("PAUSE", "0.55"))
EST, EDUR, EDB = float(E("EMPH_ST", "2.5")), float(E("EMPH_DUR", "1.15")), float(E("EMPH_DB", "3.0"))
k = Kokoro(os.path.join(KIT, "models/kokoro-v1.0.onnx"), os.path.join(KIT, "models/voices-v1.0.bin"))
d = os.path.join(KIT, "models", "sherpa-onnx-zipformer-en-2023-06-26")
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder-epoch-99-avg-1.int8.onnx", decoder=f"{d}/decoder-epoch-99-avg-1.onnx",
      joiner=f"{d}/joiner-epoch-99-avg-1.int8.onnx", tokens=f"{d}/tokens.txt", num_threads=2)
sr = 24000; tmp = "/tmp/_kn_line.wav"; outs = []
for line in lines:
    words = line.split(); stress = [w.startswith("*") or w.rstrip(".,!?").endswith("*") for w in words]
    plain = [w.replace("*", "") for w in words]
    a, sr = k.create(" ".join(plain), voice=voice, speed=SPEED, lang="en-us"); a = a.astype(np.float64)
    m, h = speech_mask(a, sr, -40); idx = np.where(m)[0]; a = a[max(0, idx[0] * h - 480): (idx[-1] + 1) * h + 960]
    sf.write(tmp, a, sr); rw, dur = recognise(rec, tmp)
    starts, _ = align(plain, rw, 0.0, dur); ends = starts[1:] + [dur]
    spans = [(max(0, s - 0.02), e) for s, e, f in zip(starts, ends, stress) if f]
    snd = parselmouth.Sound(a, sr); man = call(snd, "To Manipulation", 0.01, 75, 500)
    pt = call(man, "Extract pitch tier"); n = call(pt, "Get number of points")
    ts = np.array([call(pt, "Get time from index", i + 1) for i in range(n)]); fs = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
    outs.append(dict(snd=snd, man=man, ts=ts, fs=fs, spans=spans, dur=dur, st0=starts, en0=ends, flags=stress, words=plain))
# global pitch mapping (median + spread) from all lines together, then emphasis per word
allf = np.concatenate([o["fs"] for o in outs]); med = np.median(allf); sd = (12 * np.log2(allf / med)).std()
g = (prof["f0_sd_st"] * float(E("RANGE", "1.0"))) / max(0.5, sd)      # leave headroom: the stressed words supply the rest of the range
pieces = []
for o in outs:
    st = 12 * np.log2(o["fs"] / med) * g
    w = np.zeros_like(o["ts"])
    for s, e in o["spans"]:
        mid = (s + e) / 2; half = max(0.06, (e - s) / 2)
        w = np.maximum(w, np.clip(1 - np.abs(o["ts"] - mid) / (half + 0.05), 0, 1))
    flat = float(E("FLAT", "0.6"))                 # unstressed words keep only part of their own pitch swings
    sf_ = st * (flat + (1 - flat) * w); top = np.percentile(sf_, 80)       # stressed words rise above the line's usual peaks
    new = float(E("F0", prof["f0_median"])) * 2 ** ((sf_ + w * (np.maximum(0, top - sf_) + EST)) / 12)
    pt2 = call("Create PitchTier", "p", 0, o["snd"].duration)
    for t, f in zip(o["ts"], new): call(pt2, "Add point", float(t), float(f))
    call([pt2, o["man"]], "Replace pitch tier")
    dt = call("Create DurationTier", "d", 0, o["snd"].duration); call(dt, "Add point", 0.0, 1.0)
    for s, e in o["spans"]:
        call(dt, "Add point", max(0.001, s - 0.01), 1.0); call(dt, "Add point", s + 0.02, EDUR); call(dt, "Add point", max(s + 0.03, e - 0.02), EDUR); call(dt, "Add point", e + 0.01, 1.0)
    call([o["man"], dt], "Replace duration tier")
    y = call(o["man"], "Get resynthesis (overlap-add)"); y_t = y.xs(); yv = y.values[0].copy()
    # loudness lift on the (time-stretched) stressed spans
    scale = y.duration / o["snd"].duration if o["snd"].duration else 1
    gain = np.ones_like(yv); tt = np.arange(len(yv)) / sr
    for s, e in o["spans"]:
        s2, e2 = s * scale, e * scale; ramp = np.clip(np.minimum(tt - s2 + 0.04, e2 + 0.04 - tt) / 0.04, 0, 1)
        gain = np.maximum(gain, 1 + (10 ** (EDB / 20) - 1) * ramp)
    pieces += [yv * gain, np.zeros(int(sr * PAUSE))]
    if E("DEBUG"):
        ps = parselmouth.Sound(yv, sr).to_pitch(0.01, 75, 500)
        def pk(s, e):
            v = [x for x in [ps.get_value_at_time(t) for t in np.arange(s, e, 0.01)] if x == x and x > 0]; return max(v) if v else np.nan
        sp = [pk(s * scale, e * scale) for s, e in o["spans"]]
        wsp = [(s, e) for s, e in zip(o["st0"], o["en0"])]
        un = [pk(s * scale, e * scale) for (s, e), f in zip(wsp, o["flags"]) if not f]
        print("line stress contrast %.1f st" % (12 * np.log2(np.nanmedian(sp) / np.nanmedian(un))) if sp and un else "", [(w, round(t, 2)) for w, t in zip(o["words"], o["st0"])][:8], file=sys.stderr)
y = np.concatenate(pieces[:-1])
_, fr, P = stats(y, sr); diff = np.array(prof["ltas_db"]) - 10 * np.log10(P + 1e-20)
fr = np.array(prof["ltas_hz"]); oc = np.log2(np.maximum(fr, 50))
sm = np.array([diff[(oc > o - 1 / 6) & (oc < o + 1 / 6)].mean() for o in oc]); sm -= np.interp(1000, fr, sm)
sm = np.clip(sm, -8, 8); sm[fr < 70] = -12
y = fftconvolve(y, firwin2(1025, fr / (sr / 2), 10 ** (sm / 20)), "same"); y = y / np.abs(y).max() * 0.89; sf.write(out, y, sr)
s, _, _ = stats(y, sr); print(json.dumps({k_: round(v, 1) for k_, v in s.items()}), "stressed words:", sum(len(o["spans"]) for o in outs))
