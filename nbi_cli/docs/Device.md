# Device

Device information object

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Device unique identifier | [optional] 
**device_id** | [**DeviceDeviceId**](DeviceDeviceId.md) |  | [optional] 
**last_inform** | **datetime** | Last time device contacted the ACS | [optional] 
**tags** | **List[str]** | Device tags | [optional] 

## Example

```python
from openapi_client.models.device import Device

# TODO update the JSON string below
json = "{}"
# create an instance of Device from a JSON string
device_instance = Device.from_json(json)
# print the JSON string representation of the object
print(Device.to_json())

# convert the object into a dict
device_dict = device_instance.to_dict()
# create an instance of Device from a dict
device_from_dict = Device.from_dict(device_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


