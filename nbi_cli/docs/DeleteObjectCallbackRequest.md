# DeleteObjectCallbackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 
**object_name** | **str** | TR-069 object name | 
**connection_request** | **bool** |  | [optional] [default to True]

## Example

```python
from openapi_client.models.delete_object_callback_request import DeleteObjectCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteObjectCallbackRequest from a JSON string
delete_object_callback_request_instance = DeleteObjectCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteObjectCallbackRequest.to_json())

# convert the object into a dict
delete_object_callback_request_dict = delete_object_callback_request_instance.to_dict()
# create an instance of DeleteObjectCallbackRequest from a dict
delete_object_callback_request_from_dict = DeleteObjectCallbackRequest.from_dict(delete_object_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


