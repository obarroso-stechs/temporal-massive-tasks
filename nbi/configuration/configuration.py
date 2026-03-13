from pathlib import Path

from environs import Env

# Absolute path to nbi/.env so it's found regardless of the working directory
# (e.g. when the Temporal worker is launched from the project root)
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

env = Env()
try:
    env.read_env(str(_ENV_FILE), override=False)
except OSError:
    pass  # No .env file found — rely on real environment variables