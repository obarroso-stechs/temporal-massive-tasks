# GetAllFirmwareFilesCallbackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 
**limit** | **int** | Number of files to return | [optional] 
**offset** | **int** | Number of files to skip | [optional] 
**sort_order** | **str** | Sort order for results | [optional] [default to 'asc']

## Example

```python
from openapi_client.models.get_all_firmware_files_callback_request import GetAllFirmwareFilesCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetAllFirmwareFilesCallbackRequest from a JSON string
get_all_firmware_files_callback_request_instance = GetAllFirmwareFilesCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(GetAllFirmwareFilesCallbackRequest.to_json())

# convert the object into a dict
get_all_firmware_files_callback_request_dict = get_all_firmware_files_callback_request_instance.to_dict()
# create an instance of GetAllFirmwareFilesCallbackRequest from a dict
get_all_firmware_files_callback_request_from_dict = GetAllFirmwareFilesCallbackRequest.from_dict(get_all_firmware_files_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


