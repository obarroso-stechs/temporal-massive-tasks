# TasksGetSerialNumberAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**DeviceTask**](DeviceTask.md) |  | [optional] 

## Example

```python
from openapi_client.models.tasks_get_serial_number_async_post_request import TasksGetSerialNumberAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TasksGetSerialNumberAsyncPostRequest from a JSON string
tasks_get_serial_number_async_post_request_instance = TasksGetSerialNumberAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(TasksGetSerialNumberAsyncPostRequest.to_json())

# convert the object into a dict
tasks_get_serial_number_async_post_request_dict = tasks_get_serial_number_async_post_request_instance.to_dict()
# create an instance of TasksGetSerialNumberAsyncPostRequest from a dict
tasks_get_serial_number_async_post_request_from_dict = TasksGetSerialNumberAsyncPostRequest.from_dict(tasks_get_serial_number_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


