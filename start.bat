@echo off
REM ============================================================
REM start.bat — One-time setup + development starter (Windows)
REM Usage:
REM   start.bat          → setup if needed, start both servers
REM   start.bat setup    → setup only
REM   start.bat prod     → build react, start FastAPI only
REM ============================================================

setlocal enabledelayedexpansion

set VENV_DIR=.venv
set FRONTEND_DIR=frontend

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

REM ── Step 3: React dependencies ──────────────────────────────
if not exist "%FRONTEND_DIR%\node_modules" (
    echo [sigmoid] Installing Node dependencies...
    cd %FRONTEND_DIR%
    npm install
    cd ..
    echo [sigmoid] Node dependencies installed.
) else (
    echo [sigmoid] Node modules found, skipping npm install.
)

REM ── Exit if setup-only ──────────────────────────────────────
if "%1"=="setup" (
    echo [sigmoid] Setup complete.
    goto :end
)

REM ── Prod mode ────────────────────────────────────────────────
if "%1"=="prod" (
    echo [sigmoid] Building React for production...
    cd %FRONTEND_DIR%
    npm run build
    cd ..
    echo [sigmoid] Starting FastAPI...
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    goto :end
)

REM ── Dev mode: start both servers ─────────────────────────────
echo.
echo [sigmoid] Backend:  http://localhost:8000
echo [sigmoid] Frontend: http://localhost:5173
echo [sigmoid] Admin:    http://localhost:5173/admin
echo [sigmoid] API docs: http://localhost:8000/api/docs
echo.
echo [sigmoid] Starting both servers (open two terminals if this fails)...
echo.

REM Start FastAPI in a new window
start "FastAPI Backend" cmd /k "%VENV_DIR%\Scripts\activate.bat && uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

REM Start React in a new window
start "React Frontend" cmd /k "cd %FRONTEND_DIR% && npm run dev"

echo [sigmoid] Both servers started in separate windows.
echo [sigmoid] Close those windows to stop the servers.

:end
endlocal
