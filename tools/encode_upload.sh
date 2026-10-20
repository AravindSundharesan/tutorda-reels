#!/usr/bin/env bash
# Two-pass encode to an upload-friendly size (~25 MB for 38 s) at a bitrate above what Reels/Shorts keep.
# Usage: tools/encode_upload.sh master.mp4 final.mp4 [kbps=5200]
set -euo pipefail
IN="$1"; OUT="$2"; BR="${3:-5200}"; LOG="$(mktemp -d)/pass"
ffmpeg -y -loglevel error -i "$IN" -c:v libx264 -preset slow -b:v ${BR}k -pass 1 -passlogfile "$LOG" -an -f null /dev/null
ffmpeg -y -loglevel error -i "$IN" -c:v libx264 -preset slow -b:v ${BR}k -maxrate $((BR*13/10))k -bufsize $((BR*2))k \
  -pass 2 -passlogfile "$LOG" -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
ls -la "$OUT"
