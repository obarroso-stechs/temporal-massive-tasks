# DownloadFileRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filename** | **str** | URL of the file to download | 
**file_type** | **str** | Type of file to download | 

## Example

```python
from openapi_client.models.download_file_request import DownloadFileRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DownloadFileRequest from a JSON string
download_file_request_instance = DownloadFileRequest.from_json(json)
# print the JSON string representation of the object
print(DownloadFileRequest.to_json())

# convert the object into a dict
download_file_request_dict = download_file_request_instance.to_dict()
# create an instance of DownloadFileRequest from a dict
download_file_request_from_dict = DownloadFileRequest.from_dict(download_file_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


