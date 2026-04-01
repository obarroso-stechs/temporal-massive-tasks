from pathlib import Path

from configurations.env import env

REPORTS_OUTPUT_DIR: Path = Path(
    env.str("REPORTS_OUTPUT_DIR", str(Path(__file__).resolve().parent.parent / "reports_output"))
)
