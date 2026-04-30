@echo off
REM ============================================================
REM start.bat — Setup + development starter (Windows)
REM Usage:
REM   start.bat        → setup if needed, start FastAPI server
REM   start.bat setup  → setup only
REM ============================================================

setlocal enabledelayedexpansion

set VENV_DIR=.venv

echo [sigmoid] Starting setup...

REM ── Step 1: Python virtual environment ──────────────────────
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [sigmoid] Creating Python virtual environment...
    python -m venv %VENV_DIR%
    echo [sigmoid] Virtual environment created.
) else (
    echo [sigmoid] Virtual environment found, skipping creation.
)

REM Activate venv
call %VENV_DIR%\Scripts\activate.bat

REM ── Step 2: Python dependencies ─────────────────────────────
echo [sigmoid] Installing Python dependencies...
pip install -r requirements.txt -q
echo [sigmoid] Python dependencies installed.

REM ── Exit if setup-only ──────────────────────────────────────
if "%1"=="setup" (
    echo [sigmoid] Setup complete.
    goto :end
)

REM ── Start FastAPI ─────────────────────────────────────────────
echo.
echo [sigmoid] App:      http://localhost:8000
echo [sigmoid] Admin:    http://localhost:8000/admin
echo [sigmoid] API docs: http://localhost:8000/api/docs
echo.
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

:end
endlocal
