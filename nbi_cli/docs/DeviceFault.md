# DeviceFault

Device fault record

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Fault ID | [optional] 
**device** | **str** | Device serial number | [optional] 
**fault_code** | **str** | TR-069 fault code | [optional] 
**fault_string** | **str** | Fault description | [optional] 
**timestamp** | **datetime** | Fault occurrence timestamp | [optional] 

## Example

```python
from openapi_client.models.device_fault import DeviceFault

# TODO update the JSON string below
json = "{}"
# create an instance of DeviceFault from a JSON string
device_fault_instance = DeviceFault.from_json(json)
# print the JSON string representation of the object
print(DeviceFault.to_json())

# convert the object into a dict
device_fault_dict = device_fault_instance.to_dict()
# create an instance of DeviceFault from a dict
device_fault_from_dict = DeviceFault.from_dict(device_fault_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


