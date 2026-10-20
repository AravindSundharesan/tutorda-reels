"""Critic QA for a rendered reel. Usage: python3 tools/qa.py VIDEO.mp4 [--sheet-frames 0,95,400,...]
Checks: streams/size/duration, frozen stretches > 0.6 s, black frames, silence, loudness (-14 LUFS, true peak <= -1),
speech clarity on the FINAL MIX (music not drowning the voice), and writes a contact sheet to chk/ for visual review.
It never certifies looks: open the sheet and describe each frame before calling the video done."""
import os, re, sys, json, subprocess
import numpy as np
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v = sys.argv[1]
def run(args): return subprocess.run(args, capture_output=True, text=True)
warn, ok = [], []
p = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_type,width,height,r_frame_rate", "-of", "json", v]).stdout)
dur = float(p["format"]["duration"]); size_mb = int(p["format"]["size"]) / 1e6
vs = [s for s in p["streams"] if s["codec_type"] == "video"]; aus = [s for s in p["streams"] if s["codec_type"] == "audio"]
(ok if vs and aus else warn).append(f"streams: video={len(vs)} audio={len(aus)}")
if vs: (ok if (vs[0]["width"], vs[0]["height"]) == (1080, 1920) else warn).append(f"size {vs[0]['width']}x{vs[0]['height']} @ {vs[0]['r_frame_rate']}")
(ok if dur <= 45 else warn).append(f"duration {dur:.1f}s")
(ok if size_mb <= 30 else warn).append(f"file {size_mb:.1f} MB (chat upload limit 30 MB)")
# one decode for the picture checks, one for the sound checks
fr = run(["ffmpeg", "-hide_banner", "-nostats", "-i", v, "-vf", "freezedetect=n=0.003:d=0.6,blackdetect=d=0.4:pix_th=0.08", "-an", "-f", "null", "-"]).stderr
au = run(["ffmpeg", "-hide_banner", "-nostats", "-i", v, "-af", "silencedetect=n=-50dB:d=2.5,ebur128=peak=true", "-vn", "-f", "null", "-"]).stderr
fz = list(zip(re.findall(r"freeze_start: ([\d.]+)", fr), re.findall(r"freeze_duration: ([\d.]+)", fr)))
(warn if fz else ok).append("frozen > 0.6s: " + (", ".join(f"{float(a):.1f}s ({float(b):.1f}s)" for a, b in fz) or "none"))
bl = re.findall(r"black_start:([\d.]+)", fr)
(warn if bl else ok).append("black frames: " + (", ".join(bl) or "none"))
si = re.findall(r"silence_start: ([\d.]+)", au)
(warn if si else ok).append("silence > 2.5s: " + (", ".join(si) or "none"))
lo = au
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lo)[-1]); pk = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lo)[-1])
(ok if abs(I + 14) <= 1.5 and pk <= -1 else warn).append(f"loudness {I} LUFS, true peak {pk} dBFS")
try:
    import sherpa_onnx
    d = os.path.join(os.environ.get("MODELS_DIR", os.path.join(KIT, "models")), "sherpa-onnx-whisper-tiny.en")
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/tiny.en-encoder.int8.onnx", decoder=f"{d}/tiny.en-decoder.int8.onnx",
                                                     tokens=f"{d}/tiny.en-tokens.txt", language="en", task="transcribe")
    print("\nSpeech heard in the final mix (should match the script):")
    for a in np.arange(0, dur, 8.0):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(a), "-t", "8", "-i", v, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
        st = rec.create_stream(); st.accept_waveform(16000, np.frombuffer(raw, np.float32)); rec.decode_stream(st)
        print(f"  {a:5.1f}s  {st.result.text.strip()}")
except Exception as e:
    warn.append(f"speech check skipped: {e}")
frames = [int(x) for x in sys.argv[sys.argv.index("--sheet-frames") + 1].split(",")] if "--sheet-frames" in sys.argv else \
         [int(f * dur * 30) for f in (0, 0.08, 0.2, 0.33, 0.5, 0.62, 0.75, 0.88, 0.98)]
sel = "+".join(f"eq(n\\,{n})" for n in frames)
sheet = os.path.join(KIT, "chk", os.path.splitext(os.path.basename(v))[0] + "_qa_sheet.png")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-vf", f"select='{sel}',scale=216:384,tile={len(frames)}x1", "-frames:v", "1", sheet])
print("\nPASS:"); [print("  ✓", x) for x in ok]
print("CHECK:"); [print("  !", x) for x in warn] or print("  (none)")
print(f"\nContact sheet: {sheet}  <- view it and describe every frame before delivering.")
