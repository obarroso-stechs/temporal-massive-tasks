# CallbackRequest

Base callback registration object for async operations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 

## Example

```python
from openapi_client.models.callback_request import CallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CallbackRequest from a JSON string
callback_request_instance = CallbackRequest.from_json(json)
# print the JSON string representation of the object
print(CallbackRequest.to_json())

# convert the object into a dict
callback_request_dict = callback_request_instance.to_dict()
# create an instance of CallbackRequest from a dict
callback_request_from_dict = CallbackRequest.from_dict(callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


