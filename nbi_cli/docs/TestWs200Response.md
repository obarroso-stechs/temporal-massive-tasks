# TestWs200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_version** | **str** |  | [optional] 
**ws_status** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.test_ws200_response import TestWs200Response

# TODO update the JSON string below
json = "{}"
# create an instance of TestWs200Response from a JSON string
test_ws200_response_instance = TestWs200Response.from_json(json)
# print the JSON string representation of the object
print(TestWs200Response.to_json())

# convert the object into a dict
test_ws200_response_dict = test_ws200_response_instance.to_dict()
# create an instance of TestWs200Response from a dict
test_ws200_response_from_dict = TestWs200Response.from_dict(test_ws200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


