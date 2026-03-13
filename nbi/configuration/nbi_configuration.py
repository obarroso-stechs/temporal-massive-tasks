import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "nbi_cli"))

from .configuration import env
from openapi_client import Configuration


@dataclass
class NbiConfig:

    host: str = field(
        default_factory=lambda: env.str(
            "NBI_HOST", "https://demo1.lab2.local.stechs.io/acs/v1.0"
        )
    )
    username: str = field(default_factory=lambda: env.str("NBI_USERNAME", ""))
    password: str = field(default_factory=lambda: env.str("NBI_PASSWORD", ""))
    verify_ssl: bool = field(
        default_factory=lambda: env.bool("NBI_VERIFY_SSL", True)
    )
    debug: bool = field(
        default_factory=lambda: env.bool("NBI_DEBUG", False)
    )

    def to_openapi_configuration(self) -> Configuration:
        """Build the underlying openapi_client.Configuration from this config."""
        configuration = Configuration(
            host=self.host,
            username=self.username,
            password=self.password,
        )
        configuration.verify_ssl = self.verify_ssl
        configuration.debug = self.debug
        return configuration
