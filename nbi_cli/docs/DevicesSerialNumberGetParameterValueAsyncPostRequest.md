# DevicesSerialNumberGetParameterValueAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**List[ParameterValue]**](ParameterValue.md) |  | [optional] 

## Example

```python
from openapi_client.models.devices_serial_number_get_parameter_value_async_post_request import DevicesSerialNumberGetParameterValueAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DevicesSerialNumberGetParameterValueAsyncPostRequest from a JSON string
devices_serial_number_get_parameter_value_async_post_request_instance = DevicesSerialNumberGetParameterValueAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(DevicesSerialNumberGetParameterValueAsyncPostRequest.to_json())

# convert the object into a dict
devices_serial_number_get_parameter_value_async_post_request_dict = devices_serial_number_get_parameter_value_async_post_request_instance.to_dict()
# create an instance of DevicesSerialNumberGetParameterValueAsyncPostRequest from a dict
devices_serial_number_get_parameter_value_async_post_request_from_dict = DevicesSerialNumberGetParameterValueAsyncPostRequest.from_dict(devices_serial_number_get_parameter_value_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


