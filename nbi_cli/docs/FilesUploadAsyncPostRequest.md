# FilesUploadAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.files_upload_async_post_request import FilesUploadAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FilesUploadAsyncPostRequest from a JSON string
files_upload_async_post_request_instance = FilesUploadAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(FilesUploadAsyncPostRequest.to_json())

# convert the object into a dict
files_upload_async_post_request_dict = files_upload_async_post_request_instance.to_dict()
# create an instance of FilesUploadAsyncPostRequest from a dict
files_upload_async_post_request_from_dict = FilesUploadAsyncPostRequest.from_dict(files_upload_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


