"""Pick N-1 cut points (mid-pause) in vo_full.wav for N lines: the N-1 longest pauses, in time order.
Usage: find_cuts.py TOPIC N  -> prints comma list"""
import sys, os, numpy as np, soundfile as sf
T, N = sys.argv[1], int(sys.argv[2])
a, sr = sf.read(os.path.join(T, "vo_full.wav")); a = a if a.ndim == 1 else a.mean(1)
env = np.convolve(np.abs(a), np.ones(480) / 480, "same"); q = env < 0.006
gaps, k, n = [], 0, len(a)
while k < n:
    j = k
    while j < n and q[j] == q[k]: j += 1
    if q[k] and k > 0 and j < n: gaps.append(((j - k) / sr, (k + j) / 2 / sr))
    k = j
top = sorted(gaps, reverse=True)[:N - 1]
print(",".join(f"{t:.2f}" for _, t in sorted(top, key=lambda g: g[1])))
print("pauses:", [(round(d, 2), round(t, 2)) for d, t in sorted(top, key=lambda g: g[1])], file=sys.stderr)
print("next:", [round(d, 2) for d, _ in sorted(gaps, reverse=True)[N - 1:N + 2]], file=sys.stderr)
