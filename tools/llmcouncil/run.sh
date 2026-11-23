#!/usr/bin/env bash
# Lansează serverul MCP LLM Council; la prima rulare instalează dependențele și compilează.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
if [ ! -f dist/server.js ] || [ src -nt dist/server.js ]; then
  [ -d node_modules ] || npm ci --ignore-scripts --silent >&2
  npm run build --silent >&2
fi
exec node dist/server.js
