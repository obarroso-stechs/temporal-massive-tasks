# DeviceDeviceId


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**serial_number** | **str** |  | [optional] 
**product_class** | **str** |  | [optional] 
**manufacturer** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.device_device_id import DeviceDeviceId

# TODO update the JSON string below
json = "{}"
# create an instance of DeviceDeviceId from a JSON string
device_device_id_instance = DeviceDeviceId.from_json(json)
# print the JSON string representation of the object
print(DeviceDeviceId.to_json())

# convert the object into a dict
device_device_id_dict = device_device_id_instance.to_dict()
# create an instance of DeviceDeviceId from a dict
device_device_id_from_dict = DeviceDeviceId.from_dict(device_device_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


