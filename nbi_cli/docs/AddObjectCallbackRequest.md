# AddObjectCallbackRequest


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
from openapi_client.models.add_object_callback_request import AddObjectCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddObjectCallbackRequest from a JSON string
add_object_callback_request_instance = AddObjectCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(AddObjectCallbackRequest.to_json())

# convert the object into a dict
add_object_callback_request_dict = add_object_callback_request_instance.to_dict()
# create an instance of AddObjectCallbackRequest from a dict
add_object_callback_request_from_dict = AddObjectCallbackRequest.from_dict(add_object_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


