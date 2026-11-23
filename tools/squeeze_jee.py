"""Make every spoken 'JEE' one fluid word (Aro, 23 Nov: 'pronounce JayEeEe', no gaps before, after or inside).
Finds J..E..E in each clip with the zipformer recogniser and squeezes any silence inside that span to 15 ms.
Usage: python3 tools/squeeze_jee.py TOPIC_DIR   (run after voice_natural.py, before align_words.py)"""
import sys, os, json, numpy as np, soundfile as sf, sherpa_onnx
T = sys.argv[1]; d = "models/sherpa-onnx-zipformer-en-2023-06-26"
r = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder-epoch-99-avg-1.int8.onnx", decoder=f"{d}/decoder-epoch-99-avg-1.onnx",
                                                  joiner=f"{d}/joiner-epoch-99-avg-1.int8.onnx", tokens=f"{d}/tokens.txt")
durs = json.load(open(f"{T}/vo/durs.json")); clips = json.load(open(f"{T}/clips.json"))
for i, c in enumerate(clips):
    if "JEE" not in c[2]: continue
    p = f"{T}/vo/c{i:02d}.wav"; a, sr = sf.read(p)
    s = r.create_stream(); s.accept_waveform(sr, a); r.decode_stream(s)
    toks = [(t.strip(), x) for t, x in zip(s.result.tokens, s.result.timestamps)]
    js = [k for k, (t, _) in enumerate(toks) if t == "J"]
    if not js: print(f"c{i:02d}: J not found, left as is"); continue
    k = js[0]; t0 = toks[k][1]; t1 = toks[k + 3][1] if k + 3 < len(toks) else toks[-1][1]   # J E E -> next token
    env = np.convolve(np.abs(a), np.ones(int(0.006 * sr)) / int(0.006 * sr), "same") > 0.008
    lo, hi = int(t0 * sr), int(t1 * sr); keep = int(0.015 * sr); out = [a[:lo]]; run = []; removed = 0
    for n in range(lo, hi):
        if env[n]:
            if len(run) > keep: removed += len(run) - keep; run = run[:keep]
            out.append(a[run[0]:run[0] + len(run)] if run else a[0:0]); run = []; out.append(a[n:n + 1])
        else: run.append(n)
    if run: out.append(a[run[0]:run[0] + min(len(run), keep)]); removed += max(0, len(run) - keep)
    out.append(a[hi:]); b = np.concatenate(out); sf.write(p, b, sr); durs[i] = round(len(b) / sr, 3)
    print(f"c{i:02d}: JEE {t0:.2f}-{t1:.2f}s, removed {1000 * removed / sr:.0f} ms of silence")
json.dump(durs, open(f"{T}/vo/durs.json", "w"))
