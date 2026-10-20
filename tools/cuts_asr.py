"""Line cut points from ASR word times on vo_full.wav. Usage: cuts_asr.py TOPIC "first words of lines 2..N" (semicolon separated)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import sherpa_onnx, numpy as np, soundfile as sf
from align_words import recognise, same
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(KIT, "models", "sherpa-onnx-zipformer-en-2023-06-26")
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder-epoch-99-avg-1.int8.onnx", decoder=f"{d}/decoder-epoch-99-avg-1.onnx",
      joiner=f"{d}/joiner-epoch-99-avg-1.int8.onnx", tokens=f"{d}/tokens.txt", num_threads=2)
T = sys.argv[1]; heads = [h.strip().lower().split() for h in sys.argv[2].split(";")]
a, sr = sf.read(os.path.join(T, "vo_full.wav"))
words, dur = recognise(rec, os.path.join(T, "vo_full.wav"))
print(" ".join(f"{w}@{t:.2f}" for w, t in words), file=sys.stderr)
env = np.convolve(np.abs(a), np.ones(480) / 480, "same")
cuts, j = [], 0
for h in heads:
    while j < len(words) - 1 and not (same(words[j][0], h[0]) and (len(h) < 2 or same(words[j + 1][0], h[1]))): j += 1
    t = words[j][1]; tp = words[j - 1][1] if j > 0 else 0
    # the longest silence between the previous word and just after this word's stamp: cut at its middle
    lo, hi = int((tp + 0.12) * sr), int(min(len(a) / sr, t + 0.35) * sr); q = env[lo:hi] < 0.006
    best, k = (0, (lo + hi) // 2), 0
    while k < len(q):
        m = k
        while m < len(q) and q[m] == q[k]: m += 1
        if q[k] and m - k > best[0]: best = (m - k, lo + (k + m) // 2)
        k = m
    cuts.append(round(best[1] / sr, 2)); print(h, "gap", round(best[0] / sr, 2), file=sys.stderr); j += 1
print(",".join(map(str, cuts)))
