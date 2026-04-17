"""nbi — high-level REST client for the Stechs ACS NBI API.

Public surface
--------------
    NbiClient   — facade (main entry point)
    NbiConfig   — configuration dataclass

    DeviceService, FaultService, FileService, TaskService, HealthService
        — domain services (accessible via client attributes)

    Re-exported exceptions from openapi_client so consumers never need to
    import directly from nbi_cli:
        ApiException, NotFoundException, UnauthorizedException, ...
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "nbi_cli"))

from .client import NbiClient
from configurations.nbi import NbiConfig
from .exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    OpenApiException,
)
from .services import DeviceService, FaultService, FileService, HealthService, TaskService

try:
    from .exceptions import (
        BadRequestException,
        ConflictException,
        ForbiddenException,
        NotFoundException,
        ServiceException,
        UnauthorizedException,
        UnprocessableEntityException,
    )
except ImportError:
    pass

__all__ = [
    # Entry points
    "NbiClient",
    "NbiConfig",
    # Services (for type hints in call sites)
    "DeviceService",
    "FaultService",
    "FileService",
    "HealthService",
    "TaskService",
    # Exceptions
    "OpenApiException",
    "ApiException",
    "ApiTypeError",
    "ApiValueError",
    "ApiKeyError",
    "ApiAttributeError",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "UnprocessableEntityException",
    "ServiceException",
]
