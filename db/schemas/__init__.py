from db.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from db.schemas.device_group import (
    DeviceGroupCreate,
    DeviceGroupDetailResponse,
    DeviceGroupResponse,
    DeviceGroupUpdate,
)
from db.schemas.report import ReportCreate, ReportResponse, ReportUpdate
from db.schemas.task import (
    TaskCreate,
    TaskDeviceStatusCreate,
    TaskDeviceStatusResponse,
    TaskResponse,
)

__all__ = [
    # Device schemas
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceResponse",
    # DeviceGroup schemas
    "DeviceGroupCreate",
    "DeviceGroupUpdate",
    "DeviceGroupResponse",
    "DeviceGroupDetailResponse",
    # Task schemas
    "TaskCreate",
    "TaskResponse",
    "TaskDeviceStatusCreate",
    "TaskDeviceStatusResponse",
    # Report schemas
    "ReportCreate",
    "ReportUpdate",
    "ReportResponse",
]
