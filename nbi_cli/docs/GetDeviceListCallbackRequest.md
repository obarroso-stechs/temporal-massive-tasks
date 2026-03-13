# GetDeviceListCallbackRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Callback URL where results will be POSTed | 
**username** | **str** | Username for HTTP basic auth when calling the callback URL | [optional] 
**password** | **str** | Password for HTTP basic auth when calling the callback URL | [optional] 
**callback_id** | **str** | Optional custom callback ID (auto-generated if not provided) | [optional] 
**limit** | **int** |  | [optional] 
**offset** | **int** |  | [optional] 
**serial_number** | **str** |  | [optional] 
**tags** | **str** |  | [optional] 
**product_class** | **str** |  | [optional] 
**last_inform** | **datetime** |  | [optional] 
**last_inform_operator** | **str** |  | [optional] [default to 'lte']
**projection** | **List[str]** |  | [optional] 

## Example

```python
from openapi_client.models.get_device_list_callback_request import GetDeviceListCallbackRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeviceListCallbackRequest from a JSON string
get_device_list_callback_request_instance = GetDeviceListCallbackRequest.from_json(json)
# print the JSON string representation of the object
print(GetDeviceListCallbackRequest.to_json())

# convert the object into a dict
get_device_list_callback_request_dict = get_device_list_callback_request_instance.to_dict()
# create an instance of GetDeviceListCallbackRequest from a dict
get_device_list_callback_request_from_dict = GetDeviceListCallbackRequest.from_dict(get_device_list_callback_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


