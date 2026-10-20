#!/usr/bin/env bash
# Usage:
#   ./make.sh <reel> preview <t1> <t2> ...   -> chk/<sheet>.png  stills at those seconds (seconds to make)
#   ./make.sh <reel> draft [from to]         -> out/<reel>_draft.mp4  540x960 @ 15 fps, fast check of timing/motion
#   ./make.sh <reel> build [from to]         -> out/<reel>.mp4  final 1080x1920 @ 30 fps, upload size, + QA report
#                                               (with from/to: just that stretch, as out/<reel>_part.mp4, no QA)
#   ./make.sh <reel> safe <t1> <t2> ...      -> chk/<module>_safe.png  stills with the Instagram overlay zones shaded
#   ./make.sh <reel> times                    -> key timestamps (useful for picking preview times)
# Reels: pizza-m (integral, Manim edition, current standard) | pizza (same reel, PIL engine) | bday (Birthday Paradox v2) | bday-v1 | xx-white | xx-dark
# Speed: WORKERS=N to override the worker count (default: all CPU cores).
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"; cd "$KIT"
FAST=""
if [ "$1" = pizza-m ]; then   # Manim edition (current standard look)
  case "$2" in
    draft) MANIM_DRAFT=1 tools/manim_build.sh engine/manim_pizza.py Reel reel6 out/pizza-m_draft.mp4 draft
           grep LATE out/manim_pizza_draft.log || true;;
    build) tools/manim_build.sh engine/manim_pizza.py Reel reel6 out/pizza-m.mp4
           grep LATE out/manim_pizza_final.log || true
           python3 tools/safe_frames.py out/pizza-m.mp4 && python3 tools/qa.py out/pizza-m.mp4;;
    *) echo "pizza-m supports: draft | build"; exit 1;;
  esac; exit 0
fi
case "$1" in
  pizza) S=engine/reel6.py; FAST=reel6;; bday) S=engine/reel5b.py; FAST=reel5b;;
  bday-v1) S=engine/reel5.py;; xx-white) S=engine/reel4.py;; xx-dark) S=engine/reel3.py;;
  *) echo "unknown reel $1"; exit 1;;
esac
W=(); [ -n "${WORKERS:-}" ] && W=(--workers "$WORKERS")
RANGE=(); [ $# -ge 4 ] && RANGE=(--from "$3" --to "$4")
case "$2" in
  draft)
    [ -n "$FAST" ] || { echo "draft needs a runner-ready reel (pizza, bday)"; exit 1; }
    python3 engine/runner.py "$FAST" draft "out/$1_draft.mp4" "${RANGE[@]}" "${W[@]}";;
  build)
    if [ -n "$FAST" ]; then
      if [ ${#RANGE[@]} -gt 0 ]; then python3 engine/runner.py "$FAST" final "out/$1_part.mp4" "${RANGE[@]}" "${W[@]}"
      else python3 engine/runner.py "$FAST" check && python3 engine/runner.py "$FAST" final "out/$1.mp4" "${W[@]}" && python3 tools/qa.py "out/$1.mp4"; fi
    else  # older reels: original master + two-pass path
      python3 "$S" build "out/$1_master.mp4" && tools/encode_upload.sh "out/$1_master.mp4" "out/$1.mp4" && python3 tools/qa.py "out/$1.mp4"
    fi;;
  safe) python3 engine/runner.py "$FAST" stills "${@:3}";;   # stills with Instagram overlay zones shaded
  *) python3 "$S" "${@:2}";;
esac
