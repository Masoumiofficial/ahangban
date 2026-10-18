#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
PORT="${PORT:-8000}"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Install Python 3 or serve this folder using your static web server." >&2
  exit 1
fi
printf 'Ahangban Brand Kit: http://127.0.0.1:%s/hub.html\n' "$PORT"
printf 'Prompt studio:     http://127.0.0.1:%s/prompts.html\n' "$PORT"
printf 'Press Ctrl+C to stop. This server binds to localhost only.\n'
exec python3 -m http.server "$PORT" --bind 127.0.0.1
