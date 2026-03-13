# DeviceTask

Device task information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Task ID | [optional] 
**device** | **str** | Device serial number | [optional] 
**status** | **str** | Task status | [optional] 
**name** | **str** | Task name/type | [optional] 
**timestamp** | **datetime** | Task creation timestamp | [optional] 

## Example

```python
from openapi_client.models.device_task import DeviceTask

# TODO update the JSON string below
json = "{}"
# create an instance of DeviceTask from a JSON string
device_task_instance = DeviceTask.from_json(json)
# print the JSON string representation of the object
print(DeviceTask.to_json())

# convert the object into a dict
device_task_dict = device_task_instance.to_dict()
# create an instance of DeviceTask from a dict
device_task_from_dict = DeviceTask.from_dict(device_task_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


