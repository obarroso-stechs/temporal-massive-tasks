# RefreshObjectCallbackRequest


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
from openapi_client.models.refresh_object_callback_request import RefreshObjectCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefreshObjectCallbackRequest from a JSON string
refresh_object_callback_request_instance = RefreshObjectCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(RefreshObjectCallbackRequest.to_json())

# convert the object into a dict
refresh_object_callback_request_dict = refresh_object_callback_request_instance.to_dict()
# create an instance of RefreshObjectCallbackRequest from a dict
refresh_object_callback_request_from_dict = RefreshObjectCallbackRequest.from_dict(refresh_object_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


