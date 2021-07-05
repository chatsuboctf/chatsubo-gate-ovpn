#!/usr/bin/bash
set -euo pipefail

WORKER_TEMP_DIR=${WORKER_TEMP_DIR:-/dev/shm}
ACCESS_LOG=${ACCESS_LOG:--}
ERROR_LOG=${ERROR_LOG:--}

echo "Starting Chatsubo"
exec /opt/chatsubo-gate/venv/bin/gunicorn app:server \
  --bind 0.0.0.0:8000 \
  --worker-tmp-dir "$WORKER_TEMP_DIR" \
  --workers 1 \
  --access-logfile "$ACCESS_LOG" \
  --error-logfile "$ERROR_LOG"
