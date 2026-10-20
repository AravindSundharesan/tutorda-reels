#!/usr/bin/env bash
# One-time setup: Python packages + voice/speech models (downloaded from GitHub releases; no Hugging Face needed).
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"; M="${MODELS_DIR:-$KIT/models}"; mkdir -p "$M" "$KIT/out" "$KIT/chk"
command -v ffmpeg >/dev/null || { echo "ffmpeg is required (apt install ffmpeg / brew install ffmpeg)"; exit 1; }
pip install -q -r "$KIT/requirements.txt" 2>/dev/null || pip install -q --break-system-packages -r "$KIT/requirements.txt"
get() { [ -s "$M/$2" ] || { echo "downloading $2"; curl -sSL -o "$M/$2" "$1"; }; }
get https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx kokoro-v1.0.onnx
get https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin voices-v1.0.bin
for m in sherpa-onnx-whisper-tiny.en sherpa-onnx-zipformer-en-2023-06-26; do
  [ -s "$M/$m/tokens.txt" ] || [ -s "$M/$m/tiny.en-tokens.txt" ] || { rm -rf "$M/$m"; echo "downloading $m"; curl -sSL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/$m.tar.bz2 | tar xj -C "$M"; }
done
# drop unused full-precision copies and sample audio (saves ~500 MB)
rm -f "$M/sherpa-onnx-whisper-tiny.en/tiny.en-encoder.onnx" "$M/sherpa-onnx-whisper-tiny.en/tiny.en-decoder.onnx" \
      "$M/sherpa-onnx-zipformer-en-2023-06-26/encoder-epoch-99-avg-1.onnx" "$M/sherpa-onnx-zipformer-en-2023-06-26/joiner-epoch-99-avg-1.onnx"
rm -rf "$M"/sherpa-onnx-*/test_wavs
du -sh "$M"
python3 -c "import kokoro_onnx, sherpa_onnx, pyworld, matplotlib, PIL, soundfile; print('setup OK')"
# Manim edition (optional): ./setup.sh manim
if [ "${1:-}" = manim ]; then
  if command -v apt-get >/dev/null; then sudo apt-get install -y libpango1.0-dev pkg-config dvisvgm texlive-latex-extra texlive-fonts-recommended texlive-science || true
  elif command -v brew >/dev/null; then brew install pango pkg-config; echo "Also install MacTeX or BasicTeX (+ dvisvgm) for maths text."; fi
  pip install -q --upgrade setuptools 2>/dev/null || pip install -q --break-system-packages --ignore-installed --upgrade setuptools
  pip install -q "manim==0.19.0" 2>/dev/null || pip install -q --break-system-packages "manim==0.19.0"
  python3 -c "import manim; print('manim', manim.__version__, 'OK')"; command -v dvisvgm >/dev/null || echo "WARNING: dvisvgm missing (needed for maths)"
fi
