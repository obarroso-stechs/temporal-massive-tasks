from api.schemas.devices import DeviceCreate, DeviceResponse, DeviceUpdate
from api.schemas.device_groups import (
    AssignDevicesRequest,
    DeviceGroupCreate,
    DeviceGroupResponse,
    DeviceGroupUpdate,
)
from api.schemas.firmware import (
    FirmwareBatchRequest,
    FirmwareBatchScheduledRequest,
    FirmwareBatchStartResponse,
    FirmwareItem,
    FirmwareResultItem,
)
from api.schemas.parameter_update import (
    ParameterBatchRequest,
    ParameterBatchScheduledRequest,
    ParameterBatchStartResponse,
    ParameterUpdateItem,
)
from api.schemas.parameter_set import (
    ParameterSetBatchRequest,
    ParameterSetBatchScheduledRequest,
    ParameterSetBatchStartResponse,
    ParameterSetItem,
)
from api.schemas.tasks import (
    TaskDetailResponse,
    TaskDeviceStatusResponse,
    TaskSummaryResponse,
)
from api.schemas.reports import ReportSummaryResponse, ReportDetailResponse, ReportDeviceResponse
from api.schemas.workflow import (
    BatchGroupStatusRequest,
    BatchGroupStatusResponse,
    BatchGroupSummary,
    BatchProgress,
    DeviceExecutionStatus,
    DeviceStatusResponse,
    DeviceWithEvents,
    WorkflowEvent,
    WorkflowStatusResponse,
)

__all__ = [
    "DeviceCreate", "DeviceUpdate", "DeviceResponse",
    "DeviceGroupCreate", "DeviceGroupUpdate", "DeviceGroupResponse", "AssignDevicesRequest",
    "FirmwareItem", "FirmwareBatchRequest", "FirmwareBatchScheduledRequest",
    "FirmwareBatchStartResponse", "FirmwareResultItem",
    "ParameterUpdateItem", "ParameterBatchRequest", "ParameterBatchScheduledRequest",
    "ParameterBatchStartResponse",
    "ParameterSetItem", "ParameterSetBatchRequest", "ParameterSetBatchScheduledRequest",
    "ParameterSetBatchStartResponse",
    "TaskDeviceStatusResponse", "TaskSummaryResponse", "TaskDetailResponse",
    "DeviceExecutionStatus", "WorkflowEvent", "BatchProgress", "DeviceWithEvents",
    "DeviceStatusResponse", "WorkflowStatusResponse",
    "BatchGroupStatusRequest", "BatchGroupSummary", "BatchGroupStatusResponse",
    "ReportSummaryResponse", "ReportDetailResponse", "ReportDeviceResponse",
]
