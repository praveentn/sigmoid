"""
Railway entry point.
Starts Ollama (if available) then the FastAPI app with uvicorn.
"""
import os
import shutil
import subprocess
import time
import urllib.request
import json


# ── Ollama setup ──────────────────────────────────────────────────────────────

def _ollama_ready(base: str, timeout: int = 90) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{base}/api/tags", timeout=2)
            return True
        except Exception:
            time.sleep(2)
    return False


def _model_pulled(base: str, model: str) -> bool:
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as r:
            data = json.loads(r.read())
        names = [m.get("name", "") for m in data.get("models", [])]
        return any(model.split(":")[0] in n for n in names)
    except Exception:
        return False


def start_ollama():
    ollama_bin = shutil.which("ollama")
    if not ollama_bin:
        print("[ollama] binary not found in PATH — skipping Ollama setup")
        return

    print(f"[ollama] found binary at {ollama_bin}")

    models_dir = os.getenv("OLLAMA_MODELS", "/models")
    model = os.getenv("OLLAMA_MODEL", "phi3:mini")
    base = "http://localhost:11434"

    env = os.environ.copy()
    env["OLLAMA_MODELS"] = models_dir
    env["OLLAMA_HOST"] = "127.0.0.1:11434"

    print(f"[ollama] starting server (OLLAMA_MODELS={models_dir})")
    subprocess.Popen(
        [ollama_bin, "serve"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not _ollama_ready(base, timeout=90):
        print("[ollama] server did not become ready — skipping")
        return

    print("[ollama] server is ready")

    if _model_pulled(base, model):
        print(f"[ollama] model '{model}' already cached in {models_dir}")
    else:
        print(f"[ollama] pulling '{model}' into {models_dir} (first boot — may take a few minutes)")
        result = subprocess.run(
            [ollama_bin, "pull", model],
            env=env,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[ollama] '{model}' pulled successfully")
        else:
            print(f"[ollama] pull failed (rc={result.returncode}): {result.stderr[:400]}")
            return

    # Expose to the FastAPI app (overrides any pre-set env var)
    os.environ["OLLAMA_BASE_URL"] = base
    print(f"[ollama] OLLAMA_BASE_URL={base}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start_ollama()

    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
