"""Transcribe each voice clip to confirm it is clearly spoken.
Usage: python3 tools/check_voice.py TOPIC_DIR
Note: the model is American-English; it mishears Indian 'tutor'/'maths' - judge those by ear."""
import os, sys, json, glob
import soundfile as sf, sherpa_onnx
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(os.environ.get("MODELS_DIR", os.path.join(KIT, "models")), "sherpa-onnx-whisper-tiny.en")
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/tiny.en-encoder.int8.onnx", decoder=f"{d}/tiny.en-decoder.int8.onnx",
                                                 tokens=f"{d}/tiny.en-tokens.txt", language="en", task="transcribe")
topic = sys.argv[1]; clips = json.load(open(os.path.join(topic, "clips.json")))
for i, f in enumerate(sorted(glob.glob(os.path.join(topic, "vo", "c*.wav")))):
    a, sr = sf.read(f, dtype="float32"); st = rec.create_stream(); st.accept_waveform(sr, a); rec.decode_stream(st)
    print(f"{i:2d} said : {clips[i][1]}\n   heard: {st.result.text.strip()}")
