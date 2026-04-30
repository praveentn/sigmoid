"""
Railway entry point.
Downloads Ollama binary if needed, starts the server, then boots FastAPI.
"""
import os
import shutil
import stat
import subprocess
import time
import urllib.request
import json

OLLAMA_BIN = "/app/ollama"
OLLAMA_URL = "https://ollama.com/download/ollama-linux-amd64"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_bin() -> str | None:
    """Return path to ollama binary, downloading it to /app/ollama if needed."""
    # Already in PATH (e.g. local dev)
    found = shutil.which("ollama")
    if found:
        return found

    # Already downloaded to our app dir
    if os.path.isfile(OLLAMA_BIN) and os.access(OLLAMA_BIN, os.X_OK):
        return OLLAMA_BIN

    # Download the Linux amd64 binary
    print(f"[ollama] downloading binary from GitHub releases…")
    try:
        urllib.request.urlretrieve(OLLAMA_URL, OLLAMA_BIN)
        os.chmod(OLLAMA_BIN, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        print(f"[ollama] binary ready at {OLLAMA_BIN}")
        return OLLAMA_BIN
    except Exception as e:
        print(f"[ollama] download failed: {e}")
        return None


def _ready(base: str, timeout: int = 90) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{base}/api/tags", timeout=2)
            return True
        except Exception:
            time.sleep(2)
    return False


def _model_cached(base: str, model: str) -> bool:
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as r:
            data = json.loads(r.read())
        names = [m.get("name", "") for m in data.get("models", [])]
        stem = model.split(":")[0]
        return any(stem in n for n in names)
    except Exception:
        return False


# ── Ollama startup ────────────────────────────────────────────────────────────

def start_ollama():
    bin_path = _get_bin()
    if not bin_path:
        print("[ollama] no binary available — Ollama disabled")
        return

    models_dir = os.getenv("OLLAMA_MODELS", "/models")
    model = os.getenv("OLLAMA_MODEL", "phi3:mini")
    base = "http://localhost:11434"

    env = os.environ.copy()
    env["OLLAMA_MODELS"] = models_dir
    env["OLLAMA_HOST"] = "127.0.0.1:11434"
    env["PATH"] = os.path.dirname(bin_path) + ":" + env.get("PATH", "")

    print(f"[ollama] starting server (OLLAMA_MODELS={models_dir})")
    subprocess.Popen(
        [bin_path, "serve"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not _ready(base, timeout=90):
        print("[ollama] server did not become ready — skipping")
        return

    print("[ollama] server ready")

    if _model_cached(base, model):
        print(f"[ollama] '{model}' already in {models_dir}")
    else:
        print(f"[ollama] pulling '{model}' into {models_dir} (first boot — may take a few minutes)")
        result = subprocess.run(
            [bin_path, "pull", model],
            env=env,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[ollama] '{model}' pulled successfully")
        else:
            print(f"[ollama] pull failed (rc={result.returncode}): {result.stderr[:400]}")
            print("[ollama] SSH in and run: "
                  f"OLLAMA_MODELS={models_dir} {bin_path} pull <model>")
            # Server is still running — SSH pull can fix this later

    # Expose to FastAPI only if not already set by the environment
    if not os.environ.get("OLLAMA_BASE_URL"):
        os.environ["OLLAMA_BASE_URL"] = base
    print(f"[ollama] OLLAMA_BASE_URL={os.environ['OLLAMA_BASE_URL']}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start_ollama()

    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
