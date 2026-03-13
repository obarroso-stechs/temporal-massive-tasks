# SetParameterValueCallbackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 
**params_list** | [**List[TR181Parameter]**](TR181Parameter.md) | List of parameters to set | 
**connection_request** | **bool** | Send connection request immediately | [optional] [default to True]

## Example

```python
from openapi_client.models.set_parameter_value_callback_request import SetParameterValueCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetParameterValueCallbackRequest from a JSON string
set_parameter_value_callback_request_instance = SetParameterValueCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(SetParameterValueCallbackRequest.to_json())

# convert the object into a dict
set_parameter_value_callback_request_dict = set_parameter_value_callback_request_instance.to_dict()
# create an instance of SetParameterValueCallbackRequest from a dict
set_parameter_value_callback_request_from_dict = SetParameterValueCallbackRequest.from_dict(set_parameter_value_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


