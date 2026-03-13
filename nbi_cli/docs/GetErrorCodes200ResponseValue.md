# GetErrorCodes200ResponseValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | [optional] 
**message** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.get_error_codes200_response_value import GetErrorCodes200ResponseValue

# TODO update the JSON string below
json = "{}"
# create an instance of GetErrorCodes200ResponseValue from a JSON string
get_error_codes200_response_value_instance = GetErrorCodes200ResponseValue.from_json(json)
# print the JSON string representation of the object
print(GetErrorCodes200ResponseValue.to_json())

# convert the object into a dict
get_error_codes200_response_value_dict = get_error_codes200_response_value_instance.to_dict()
# create an instance of GetErrorCodes200ResponseValue from a dict
get_error_codes200_response_value_from_dict = GetErrorCodes200ResponseValue.from_dict(get_error_codes200_response_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


