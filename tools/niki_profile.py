"""Measure the 'Niki' delivery profile from all ElevenLabs takes: pitch level/range, speaking rate, spectrum (LTAS)."""
import numpy as np, parselmouth, glob, json, subprocess, re
from scipy.signal import welch
def load(p, sr=24000):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f64le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float64).copy(), sr
def speech_mask(a, sr, thr_db=-38):
    h = int(0.02 * sr); n = len(a) // h; e = np.array([np.sqrt(np.mean(a[i*h:(i+1)*h]**2)) + 1e-9 for i in range(n)])
    db = 20 * np.log10(e / e.max()); return db > thr_db, h
def stats(a, sr, text=None):
    snd = parselmouth.Sound(a, sr); p = snd.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    f = p.selected_array["frequency"]; f = f[f > 0]; st = 12 * np.log2(f / np.median(f))
    m, h = speech_mask(a, sr); speech_s = m.sum() * h / sr
    mk = np.repeat(m, h)[:len(a)]; fr, P = welch(a[:len(mk)][mk], sr, nperseg=2048)
    out = dict(f0_median=float(np.median(f)), f0_sd_st=float(st.std()), f0_range_st=float(np.percentile(st, 95) - np.percentile(st, 5)), speech_s=float(speech_s))
    if text: out["chars_per_s"] = len(re.sub(r"[^a-z]", "", text.lower())) / speech_s
    return out, fr, P
if __name__ == "__main__":
    import sys
    files = {"motiv": "topics/motiv_1pct/vo_full.mp3", "sinx": "topics/math_sinx/vo_full.mp3", "epi": "topics/math_epi_log_backup/vo_full.mp3",
             "modcos": "topics/math_modcos/vo_full.mp3", "pow": "topics/math_pow/vo_full.mp3"}
    Ps, rows = [], {}
    for k, f in files.items():
        try: a, sr = load(f)
        except Exception: continue
        if len(a) == 0: continue
        s, fr, P = stats(a, sr); rows[k] = s; Ps.append(P)
    prof = {k: float(np.median([r[k] for r in rows.values()])) for k in ("f0_median", "f0_sd_st", "f0_range_st")}
    prof["ltas_db"] = (10 * np.log10(np.mean(Ps, axis=0) + 1e-20)).tolist(); prof["ltas_hz"] = fr.tolist()
    json.dump(prof, open("assets/niki_profile.json", "w")); print({k: round(v, 2) for k, v in prof.items() if not isinstance(v, list)}); print({k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in rows.items()})
