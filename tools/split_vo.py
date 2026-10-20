"""Split one long ElevenLabs take into per-line clips: trim edges, cap inner pauses, optional tempo.
Usage: python3 tools/split_vo.py TOPIC_DIR "c1,c2,..." [tempo=1.04] [cap=0.2]   (cut times in seconds, mid-pause)"""
import sys, json, os, subprocess, tempfile
import numpy as np, soundfile as sf
T = sys.argv[1]; cuts = [float(x) for x in sys.argv[2].split(",")]
tempo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.04; cap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
a, sr = sf.read(os.path.join(T, "vo_full.wav")); os.makedirs(os.path.join(T, "vo"), exist_ok=True)
cuts = [0.0] + cuts + [len(a) / sr]; durs = []
for i in range(len(cuts) - 1):
    s = a[int(cuts[i] * sr):int(cuts[i + 1] * sr)]
    env = np.convolve(np.abs(s), np.ones(240) / 240, "same"); on = np.where(env > 0.01)[0]
    s = s[max(0, on[0] - int(0.04 * sr)):min(len(s), on[-1] + int(0.08 * sr))]
    env = np.convolve(np.abs(s), np.ones(480) / 480, "same"); q = env < 0.006; out, k, n = [], 0, len(s)
    while k < n:
        j = k
        while j < n and q[j] == q[k]: j += 1
        if q[k] and k > 0 and j < n and j - k > int((cap + 0.06) * sr):
            h = int(cap * sr) // 2; out += [s[k:k + h], s[j - h:j]]
        else: out.append(s[k:j])
        k = j
    c = np.concatenate(out); f = int(0.01 * sr); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
    tmp = tempfile.mktemp(suffix=".wav"); sf.write(tmp, c, sr); p = os.path.join(T, "vo", f"c{i:02d}.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", f"atempo={tempo}", "-ar", str(sr), "-ac", "1", p]); os.remove(tmp)
    durs.append(round(sf.info(p).duration, 3))
json.dump(durs, open(os.path.join(T, "vo", "durs.json"), "w")); print(durs, round(sum(durs), 2))
