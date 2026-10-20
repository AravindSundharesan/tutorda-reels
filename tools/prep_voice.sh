#!/usr/bin/env bash
# Short-format voice prep: decode pane result -> wav -> line cuts (ASR) -> split -> word times.
# Usage: tools/prep_voice.sh topics/<t> <tool-result.txt or .mp3> "head2;head3;..."
set -euo pipefail
T="$1"; SRC="$2"; HEADS="$3"
case "$SRC" in *.txt) python3 tools/b64file.py "$SRC" "$T/vo_full.mp3" >/dev/null ;; *) cp "$SRC" "$T/vo_full.mp3" ;; esac
ffmpeg -loglevel error -y -i "$T/vo_full.mp3" -ac 1 -ar 24000 "$T/vo_full.wav"
CUTS=$(python3 tools/cuts_asr.py "$T" "$HEADS" 2>/tmp/_asr.txt); grep -v "resampl\|rate:" /tmp/_asr.txt | grep "@" | head -1
echo "cuts: $CUTS"
python3 tools/split_vo.py "$T" "$CUTS" 1.08 0.16
START=0.05 IN_GAP=0.12 BEAT_GAP=0.18 END_HOLD=0.9 python3 tools/align_words.py "$T" 2>&1 | grep match
