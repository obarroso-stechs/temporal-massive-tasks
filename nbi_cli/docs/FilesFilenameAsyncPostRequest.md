# FilesFilenameAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**FirmwareFile**](FirmwareFile.md) |  | [optional] 

## Example

```python
from openapi_client.models.files_filename_async_post_request import FilesFilenameAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FilesFilenameAsyncPostRequest from a JSON string
files_filename_async_post_request_instance = FilesFilenameAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(FilesFilenameAsyncPostRequest.to_json())

# convert the object into a dict
files_filename_async_post_request_dict = files_filename_async_post_request_instance.to_dict()
# create an instance of FilesFilenameAsyncPostRequest from a dict
files_filename_async_post_request_from_dict = FilesFilenameAsyncPostRequest.from_dict(files_filename_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


