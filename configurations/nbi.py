from dataclasses import dataclass, field

from configurations.env import env


@dataclass
class NbiConfig:
    host: str = field(
        default_factory=lambda: env.str(
            "NBI_HOST", "http://localhost:5001/acs/v1.0"
        )
    )
    username: str = field(default_factory=lambda: env.str("NBI_USERNAME", ""))
    password: str = field(default_factory=lambda: env.str("NBI_PASSWORD", ""))
    verify_ssl: bool = field(default_factory=lambda: env.bool("NBI_VERIFY_SSL", True))
    debug: bool = field(default_factory=lambda: env.bool("NBI_DEBUG", False))
