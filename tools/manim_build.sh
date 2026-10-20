#!/usr/bin/env bash
# Manim reel: render picture, add the kit's audio mix (voice + music + sounds), encode to upload size, QA.
# Usage: tools/manim_build.sh <engine/manim_file.py> <SceneClass> <reel6-style audio module> <out.mp4> [draft]
set -euo pipefail
KIT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$KIT"
SRC="$1"; SCENE="$2"; AUD="$3"; OUT="$4"; MODE="${5:-final}"
NAME="$(basename "$SRC" .py)"
if [ "$MODE" = draft ]; then RES=(-r 540,960 --fps 15); DIR=960p15; else RES=(); DIR=1920p30; fi
T0=$(date +%s)
MANIM_DRAFT=$([ "$MODE" = draft ] && echo 1 || echo 0) manim render --disable_caching --progress_bar none "${RES[@]}" \
  --media_dir out/manim "$SRC" "$SCENE" -o "${NAME}_${MODE}.mp4" > "out/${NAME}_${MODE}.log" 2>&1 || { tail -30 "out/${NAME}_${MODE}.log"; exit 1; }
VID="out/manim/videos/$NAME/$DIR/${NAME}_${MODE}.mp4"
(cd engine && python3 -c "import $AUD as A; A.make_audio('../out/mix_${NAME}.wav')" > /dev/null)
ffmpeg -y -loglevel error -i "$VID" -i "out/mix_${NAME}.wav" -c:v libx264 -preset veryfast -crf 18 -maxrate 5500k -bufsize 11000k \
  -pix_fmt yuv420p -af loudnorm=I=-14:TP=-1.5:LRA=9 -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
echo "$MODE: $OUT in $(( $(date +%s) - T0 ))s"
