# FaultsGetSerialNumberAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**List[DeviceFault]**](DeviceFault.md) |  | [optional] 

## Example

```python
from openapi_client.models.faults_get_serial_number_async_post_request import FaultsGetSerialNumberAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FaultsGetSerialNumberAsyncPostRequest from a JSON string
faults_get_serial_number_async_post_request_instance = FaultsGetSerialNumberAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(FaultsGetSerialNumberAsyncPostRequest.to_json())

# convert the object into a dict
faults_get_serial_number_async_post_request_dict = faults_get_serial_number_async_post_request_instance.to_dict()
# create an instance of FaultsGetSerialNumberAsyncPostRequest from a dict
faults_get_serial_number_async_post_request_from_dict = FaultsGetSerialNumberAsyncPostRequest.from_dict(faults_get_serial_number_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


