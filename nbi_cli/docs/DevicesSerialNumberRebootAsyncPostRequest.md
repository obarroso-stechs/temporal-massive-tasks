# DevicesSerialNumberRebootAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**DevicesSerialNumberRebootAsyncPostRequestPayload**](DevicesSerialNumberRebootAsyncPostRequestPayload.md) |  | [optional] 

## Example

```python
from openapi_client.models.devices_serial_number_reboot_async_post_request import DevicesSerialNumberRebootAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DevicesSerialNumberRebootAsyncPostRequest from a JSON string
devices_serial_number_reboot_async_post_request_instance = DevicesSerialNumberRebootAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(DevicesSerialNumberRebootAsyncPostRequest.to_json())

# convert the object into a dict
devices_serial_number_reboot_async_post_request_dict = devices_serial_number_reboot_async_post_request_instance.to_dict()
# create an instance of DevicesSerialNumberRebootAsyncPostRequest from a dict
devices_serial_number_reboot_async_post_request_from_dict = DevicesSerialNumberRebootAsyncPostRequest.from_dict(devices_serial_number_reboot_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


