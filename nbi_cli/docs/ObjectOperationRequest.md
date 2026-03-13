# ObjectOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object_name** | **str** | TR-069 object name | 
**connection_request** | **bool** |  | [optional] [default to True]

## Example

```python
from openapi_client.models.object_operation_request import ObjectOperationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ObjectOperationRequest from a JSON string
object_operation_request_instance = ObjectOperationRequest.from_json(json)
# print the JSON string representation of the object
print(ObjectOperationRequest.to_json())

# convert the object into a dict
object_operation_request_dict = object_operation_request_instance.to_dict()
# create an instance of ObjectOperationRequest from a dict
object_operation_request_from_dict = ObjectOperationRequest.from_dict(object_operation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


