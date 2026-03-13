"""NBI exception hierarchy.

Re-exports the generated openapi_client exceptions so consumers only need
to import from `nbi`, without depending directly on nbi_cli internals.
"""

from openapi_client.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    OpenApiException,
)

__all__ = [
    "OpenApiException",
    "ApiException",
    "ApiTypeError",
    "ApiValueError",
    "ApiKeyError",
    "ApiAttributeError",
    # HTTP-specific subclasses (raised automatically by the client)
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "UnprocessableEntityException",
    "ServiceException",
]

# HTTP-status-specific exceptions — the generated client raises these
# automatically based on the response status code.
try:
    from openapi_client.exceptions import BadRequestException
    from openapi_client.exceptions import UnauthorizedException
    from openapi_client.exceptions import ForbiddenException
    from openapi_client.exceptions import NotFoundException
    from openapi_client.exceptions import ConflictException
    from openapi_client.exceptions import UnprocessableEntityException
    from openapi_client.exceptions import ServiceException
except ImportError:
    # Fallback: define thin subclasses in case the generated client
    # does not expose them (older generator versions).
    class BadRequestException(ApiException): ...         # noqa: E701
    class UnauthorizedException(ApiException): ...       # noqa: E701
    class ForbiddenException(ApiException): ...          # noqa: E701
    class NotFoundException(ApiException): ...           # noqa: E701
    class ConflictException(ApiException): ...           # noqa: E701
    class UnprocessableEntityException(ApiException): ... # noqa: E701
    class ServiceException(ApiException): ...            # noqa: E701
