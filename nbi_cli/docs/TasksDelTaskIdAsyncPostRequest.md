# TasksDelTaskIdAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**DeleteDeviceTask200Response**](DeleteDeviceTask200Response.md) |  | [optional] 

## Example

```python
from openapi_client.models.tasks_del_task_id_async_post_request import TasksDelTaskIdAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TasksDelTaskIdAsyncPostRequest from a JSON string
tasks_del_task_id_async_post_request_instance = TasksDelTaskIdAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(TasksDelTaskIdAsyncPostRequest.to_json())

# convert the object into a dict
tasks_del_task_id_async_post_request_dict = tasks_del_task_id_async_post_request_instance.to_dict()
# create an instance of TasksDelTaskIdAsyncPostRequest from a dict
tasks_del_task_id_async_post_request_from_dict = TasksDelTaskIdAsyncPostRequest.from_dict(tasks_del_task_id_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


