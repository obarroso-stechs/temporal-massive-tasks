from pathlib import Path

from environs import Env

# Prefer project root .env; fallback to configurations/.env.
_BASE_DIR = Path(__file__).resolve().parent
_ENV_CANDIDATES = (
    _BASE_DIR.parent / ".env",
    _BASE_DIR / ".env",
)

env = Env()
for env_file in _ENV_CANDIDATES:
    if not env_file.is_file():
        continue
    try:
        env.read_env(str(env_file), override=False)
        break
    except OSError:
        continue
