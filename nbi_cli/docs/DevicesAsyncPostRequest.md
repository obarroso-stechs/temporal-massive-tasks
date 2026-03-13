# DevicesAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**List[Device]**](Device.md) |  | [optional] 

## Example

```python
from openapi_client.models.devices_async_post_request import DevicesAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DevicesAsyncPostRequest from a JSON string
devices_async_post_request_instance = DevicesAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(DevicesAsyncPostRequest.to_json())

# convert the object into a dict
devices_async_post_request_dict = devices_async_post_request_instance.to_dict()
# create an instance of DevicesAsyncPostRequest from a dict
devices_async_post_request_from_dict = DevicesAsyncPostRequest.from_dict(devices_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


