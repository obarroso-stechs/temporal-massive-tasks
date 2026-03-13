# FilesAllAsyncPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** |  | [optional] 
**payload** | [**List[FirmwareFile]**](FirmwareFile.md) |  | [optional] 

## Example

```python
from openapi_client.models.files_all_async_post_request import FilesAllAsyncPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FilesAllAsyncPostRequest from a JSON string
files_all_async_post_request_instance = FilesAllAsyncPostRequest.from_json(json)
# print the JSON string representation of the object
print(FilesAllAsyncPostRequest.to_json())

# convert the object into a dict
files_all_async_post_request_dict = files_all_async_post_request_instance.to_dict()
# create an instance of FilesAllAsyncPostRequest from a dict
files_all_async_post_request_from_dict = FilesAllAsyncPostRequest.from_dict(files_all_async_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


