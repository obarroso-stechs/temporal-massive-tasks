# DevicesSerialNumberFactoryResetAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**DevicesSerialNumberFactoryResetAsyncPostRequestPayload**](DevicesSerialNumberFactoryResetAsyncPostRequestPayload.md) |  | [optional] 

## Example

```python
from openapi_client.models.devices_serial_number_factory_reset_async_post_request import DevicesSerialNumberFactoryResetAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DevicesSerialNumberFactoryResetAsyncPostRequest from a JSON string
devices_serial_number_factory_reset_async_post_request_instance = DevicesSerialNumberFactoryResetAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(DevicesSerialNumberFactoryResetAsyncPostRequest.to_json())

# convert the object into a dict
devices_serial_number_factory_reset_async_post_request_dict = devices_serial_number_factory_reset_async_post_request_instance.to_dict()
# create an instance of DevicesSerialNumberFactoryResetAsyncPostRequest from a dict
devices_serial_number_factory_reset_async_post_request_from_dict = DevicesSerialNumberFactoryResetAsyncPostRequest.from_dict(devices_serial_number_factory_reset_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


