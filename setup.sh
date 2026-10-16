#!/usr/bin/env bash
# One-time setup for a cloud run: ffmpeg + Python packages.
set -e
if ! command -v ffmpeg >/dev/null 2>&1; then
  (sudo -n apt-get update -qq && sudo -n apt-get install -y -qq ffmpeg) || (apt-get update -qq && apt-get install -y -qq ffmpeg)
fi
python3 -m pip install -q -r requirements.txt
ffmpeg -version | head -1
python3 -c "import PIL, numpy, scipy, faster_whisper; print('python deps ok')"
