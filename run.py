"""
Railway entry point.
Starts Ollama (if available) then the FastAPI app with uvicorn.
"""
import os
import subprocess
import time
import urllib.request
import urllib.error
import json


# ── Ollama setup ──────────────────────────────────────────────────────────────

def _ollama_ready(base: str, timeout: int = 60) -> bool:
    """Wait until Ollama HTTP server is accepting requests."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{base}/api/tags", timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False


def _model_pulled(base: str, model: str) -> bool:
    """Return True if model already exists in the Ollama library."""
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as r:
            data = json.loads(r.read())
        names = [m.get("name", "") for m in data.get("models", [])]
        return any(model in n for n in names)
    except Exception:
        return False


def start_ollama():
    ollama_bin = "/usr/local/bin/ollama"
    if not os.path.exists(ollama_bin):
        print("[ollama] binary not found — skipping Ollama setup")
        return

    models_dir = os.getenv("OLLAMA_MODELS", "/models")
    model = os.getenv("OLLAMA_MODEL", "phi3:mini")
    base = "http://localhost:11434"

    env = os.environ.copy()
    env["OLLAMA_MODELS"] = models_dir
    env["OLLAMA_HOST"] = "0.0.0.0"

    print(f"[ollama] starting server (models dir: {models_dir})")
    subprocess.Popen(
        [ollama_bin, "serve"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not _ollama_ready(base, timeout=60):
        print("[ollama] server did not become ready in time — skipping")
        return

    print("[ollama] server ready")

    if _model_pulled(base, model):
        print(f"[ollama] model '{model}' already cached in {models_dir}")
    else:
        print(f"[ollama] pulling '{model}' to {models_dir} — may take a few minutes on first boot")
        result = subprocess.run(
            [ollama_bin, "pull", model],
            env=env,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[ollama] model '{model}' pulled successfully")
        else:
            print(f"[ollama] pull failed: {result.stderr[:300]}")
            return

    os.environ["OLLAMA_BASE_URL"] = base
    print(f"[ollama] OLLAMA_BASE_URL={base}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start_ollama()

    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
