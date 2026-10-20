"""Word-level timing: Zipformer word starts per voice clip, aligned to caption words."""
import os, re, json, sys
import numpy as np, soundfile as sf, sherpa_onnx

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
ORD = {"1st": ["first"], "2nd": ["second"], "3rd": ["third"], "23rd": ["twenty", "third"]}
def n2w(n):
    n = int(n)
    if n < 20: return [ONES[n]]
    if n < 100: return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    return [ONES[n // 100], "hundred"] + (n2w(n % 100) if n % 100 else [])
def expand(w):
    w = w.lower().strip(".,!?:;\"'()…")
    if not w: return []
    if w in ORD: return ORD[w]
    if w in ("-", "−"): return ["minus"]
    if w == "=": return ["equals"]
    if "/" in w and all(p.replace(".", "").isdigit() for p in w.split("/") if p):
        a, b = w.split("/"); return expand(a) + ["by"] + expand(b)
    pct = w.endswith("%"); w2 = w.rstrip("%")
    if re.fullmatch(r"\d+\.\d+", w2):
        i, f = w2.split("."); out = n2w(i) + ["point"] + [ONES[int(c)] for c in f]
    elif w2.isdigit(): out = n2w(w2)
    else: out = [re.sub(r"[^a-z']", "", w2)]
    return [x for x in out if x] + (["percent"] if pct else [])

def lev(a, b):
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (ca != cb))
    return d[-1]
def same(a, b):
    a, b = a.replace("'", ""), b.replace("'", "")
    if a == b: return True
    if min(len(a), len(b)) <= 3: return False
    return lev(a, b) / max(len(a), len(b)) <= 0.34

def recognise(rec, path):
    a, sr = sf.read(path, dtype="float32")
    st = rec.create_stream(); st.accept_waveform(sr, a); rec.decode_stream(st)
    r = st.result; words = []
    for tok, ts in zip(r.tokens, r.timestamps):
        if tok.startswith(" ") or not words: words.append([tok.strip().lower(), float(ts)])
        else: words[-1][0] += tok.lower()
    return words, len(a) / sr

def align(disp_words, rec_words, t0, t1):
    toks = [(k, x) for k, w in enumerate(disp_words) for x in expand(w)]
    n, m = len(toks), len(rec_words)
    D = np.zeros((n + 1, m + 1)); D[:, 0] = np.arange(n + 1); D[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = min(D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 1, j - 1] + (0 if same(toks[i - 1][1], rec_words[j - 1][0]) else 1.6))
    i, j, match = n, m, {}
    while i > 0 and j > 0:
        if D[i, j] == D[i - 1, j - 1] + (0 if same(toks[i - 1][1], rec_words[j - 1][0]) else 1.6):
            if same(toks[i - 1][1], rec_words[j - 1][0]): match[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif D[i, j] == D[i - 1, j] + 1: i -= 1
        else: j -= 1
    starts = [None] * len(disp_words)
    for ti, rj in match.items():
        k = toks[ti][0]; t = t0 + rec_words[rj][1]
        starts[k] = t if starts[k] is None else min(starts[k], t)
    # fill gaps by character length between confirmed neighbours
    known = [(k, s) for k, s in enumerate(starts) if s is not None]
    rate = len(match) / max(1, len(toks))
    if not known: known = [(-1, t0)]
    anchors = [(-1, t0)] + known + [(len(disp_words), t1)]
    anchors = sorted({a[0]: a for a in anchors}.values())
    for (ka, ta), (kb, tb) in zip(anchors, anchors[1:]):
        gap = list(range(ka + 1, kb))
        if not gap: continue
        lens = [len(disp_words[k]) + 1 for k in gap]; tot = sum(lens) + (len(disp_words[ka]) + 1 if ka >= 0 else 0)
        acc = len(disp_words[ka]) + 1 if ka >= 0 else 0
        for k, L in zip(gap, lens):
            starts[k] = ta + (tb - ta) * acc / max(1, tot); acc += L
    for k in range(1, len(starts)): starts[k] = max(starts[k], starts[k - 1] + 0.05)
    return starts, rate

if __name__ == "__main__":
    # Usage: python3 tools/align_words.py TOPIC_DIR   -> TOPIC_DIR/word_times.json
    KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topic = sys.argv[1]
    os.environ["CLIPS"] = os.path.join(topic, "clips.json"); os.environ["VO"] = os.path.join(topic, "vo")
    os.environ.setdefault("OUT", os.path.join(topic, "word_times.json"))
    sys.path.insert(0, os.path.join(KIT, "engine"))
    import reel2 as R
    d = os.path.join(os.environ.get("MODELS_DIR", os.path.join(KIT, "models")), "sherpa-onnx-zipformer-en-2023-06-26")
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder-epoch-99-avg-1.int8.onnx",
          decoder=f"{d}/decoder-epoch-99-avg-1.onnx", joiner=f"{d}/joiner-epoch-99-avg-1.int8.onnx", tokens=f"{d}/tokens.txt", num_threads=2)
    out = []
    for i, clip in enumerate(R.CLIPS[:-1]):
        words, _ = recognise(rec, f"{R.VO}/c{i:02d}.wav")
        disp = clip[2].replace("|", " ").split()
        starts, rate = align(disp, words, R.C[i], R.E[i])
        out.append(dict(words=disp, starts=[round(s, 3) for s in starts], match=round(rate, 2), clip_start=round(R.C[i], 3)))
        print(f"{i:2d} match {rate:.2f} | " + "  ".join(f"{w}@{s - R.C[i]:.2f}" for w, s in zip(disp, starts)))
    json.dump(out, open(os.environ["OUT"], "w"), indent=1)
