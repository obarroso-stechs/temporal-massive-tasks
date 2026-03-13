# SetParameterValueRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**params_list** | [**List[TR181Parameter]**](TR181Parameter.md) | List of parameters to set | 
**connection_request** | **bool** | Send connection request immediately | [optional] [default to True]

## Example

```python
from openapi_client.models.set_parameter_value_request import SetParameterValueRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetParameterValueRequest from a JSON string
set_parameter_value_request_instance = SetParameterValueRequest.from_json(json)
# print the JSON string representation of the object
print(SetParameterValueRequest.to_json())

# convert the object into a dict
set_parameter_value_request_dict = set_parameter_value_request_instance.to_dict()
# create an instance of SetParameterValueRequest from a dict
set_parameter_value_request_from_dict = SetParameterValueRequest.from_dict(set_parameter_value_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


