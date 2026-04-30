#!/usr/bin/env bash
# ============================================================
# start.sh — Setup + development starter
# Usage:
#   ./start.sh        → setup if needed, start FastAPI server
#   ./start.sh setup  → setup only
# ============================================================

set -e

VENV_DIR=".venv"

log() { echo -e "\033[1;36m[sigmoid]\033[0m $1"; }
success() { echo -e "\033[1;32m[sigmoid]\033[0m $1"; }
warn() { echo -e "\033[1;33m[sigmoid]\033[0m $1"; }

# ── Step 1: Python virtual environment ────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    log "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
    success "Virtual environment created at $VENV_DIR"
else
    log "Virtual environment found, skipping creation."
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# ── Step 2: Python dependencies ────────────────────────────────
log "Installing Python dependencies..."
pip install -r requirements.txt -q
success "Python dependencies installed."

# ── Exit here if setup-only mode ───────────────────────────────
if [ "$1" = "setup" ]; then
    success "Setup complete. Run ./start.sh to start the server."
    exit 0
fi

# ── Start FastAPI ───────────────────────────────────────────────
echo ""
warn "App:      http://localhost:8000"
warn "Admin:    http://localhost:8000/admin"
warn "API docs: http://localhost:8000/api/docs"
echo ""
warn "Press Ctrl+C to stop."
echo ""

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
