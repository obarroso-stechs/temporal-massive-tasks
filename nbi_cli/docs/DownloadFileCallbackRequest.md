# DownloadFileCallbackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 
**filename** | **str** | URL of the file to download | 
**file_type** | **str** | Type of file to download | 

## Example

```python
from openapi_client.models.download_file_callback_request import DownloadFileCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DownloadFileCallbackRequest from a JSON string
download_file_callback_request_instance = DownloadFileCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(DownloadFileCallbackRequest.to_json())

# convert the object into a dict
download_file_callback_request_dict = download_file_callback_request_instance.to_dict()
# create an instance of DownloadFileCallbackRequest from a dict
download_file_callback_request_from_dict = DownloadFileCallbackRequest.from_dict(download_file_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


