#!/usr/bin/env bash
# ============================================================
# start.sh — One-time setup + development starter
# Usage:
#   ./start.sh          → setup if needed, then start both servers
#   ./start.sh setup    → setup only (venv + deps + react build)
#   ./start.sh prod     → build react, start FastAPI only (prod-like)
# ============================================================

set -e

VENV_DIR=".venv"
FRONTEND_DIR="frontend"

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

# ── Step 3: React dependencies ─────────────────────────────────
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    log "Installing React/Node dependencies..."
    cd "$FRONTEND_DIR" && npm install && cd ..
    success "Node dependencies installed."
else
    log "Node modules found, skipping npm install."
fi

# ── Exit here if setup-only mode ───────────────────────────────
if [ "$1" = "setup" ]; then
    success "Setup complete. Run ./start.sh to start servers."
    exit 0
fi

# ── Step 4: Build React (prod mode) ────────────────────────────
if [ "$1" = "prod" ]; then
    log "Building React for production..."
    cd "$FRONTEND_DIR" && npm run build && cd ..
    success "React built. Starting FastAPI..."
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    exit 0
fi

# ── Step 5: Dev mode — start both servers ──────────────────────
log "Starting development servers..."
echo ""
warn "Backend:  http://localhost:8000"
warn "Frontend: http://localhost:5173"
warn "Admin:    http://localhost:5173/admin"
warn "API docs: http://localhost:8000/api/docs"
echo ""
warn "Press Ctrl+C to stop both servers."
echo ""

# Start FastAPI in background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start React dev server in background
cd "$FRONTEND_DIR" && npm run dev &
FRONTEND_PID=$!
cd ..

# Trap Ctrl+C to kill both
cleanup() {
    log "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}
trap cleanup INT TERM

# Wait for either process to exit
wait $BACKEND_PID $FRONTEND_PID
