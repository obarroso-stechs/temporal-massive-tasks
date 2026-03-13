# TR181Parameter

TR-181 parameter for setting values

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Parameter name (TR-069/TR-181 path) | 
**value** | [**TR181ParameterValue**](TR181ParameterValue.md) |  | 
**type** | **str** | Parameter data type (boolean, string, int, uint, etc.) | [optional] 

## Example

```python
from openapi_client.models.tr181_parameter import TR181Parameter

# TODO update the JSON string below
json = "{}"
# create an instance of TR181Parameter from a JSON string
tr181_parameter_instance = TR181Parameter.from_json(json)
# print the JSON string representation of the object
print(TR181Parameter.to_json())

# convert the object into a dict
tr181_parameter_dict = tr181_parameter_instance.to_dict()
# create an instance of TR181Parameter from a dict
tr181_parameter_from_dict = TR181Parameter.from_dict(tr181_parameter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


