# GetParameterValueCallbackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 
**params_list** | **List[str]** | List of parameter names to retrieve | 
**connection_request** | **bool** |  | [optional] [default to True]

## Example

```python
from openapi_client.models.get_parameter_value_callback_request import GetParameterValueCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetParameterValueCallbackRequest from a JSON string
get_parameter_value_callback_request_instance = GetParameterValueCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(GetParameterValueCallbackRequest.to_json())

# convert the object into a dict
get_parameter_value_callback_request_dict = get_parameter_value_callback_request_instance.to_dict()
# create an instance of GetParameterValueCallbackRequest from a dict
get_parameter_value_callback_request_from_dict = GetParameterValueCallbackRequest.from_dict(get_parameter_value_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


