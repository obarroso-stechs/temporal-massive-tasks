# AsyncResponse

Standard response for asynchronous operations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**callback_id** | **str** | Unique identifier for tracking the callback | 

## Example

```python
from openapi_client.models.async_response import AsyncResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AsyncResponse from a JSON string
async_response_instance = AsyncResponse.from_json(json)
# print the JSON string representation of the object
print(AsyncResponse.to_json())

# convert the object into a dict
async_response_dict = async_response_instance.to_dict()
# create an instance of AsyncResponse from a dict
async_response_from_dict = AsyncResponse.from_dict(async_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


