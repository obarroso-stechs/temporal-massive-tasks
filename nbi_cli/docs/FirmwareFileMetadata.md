# FirmwareFileMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**oui** | **str** |  | [optional] 
**product_class** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**file_type** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.firmware_file_metadata import FirmwareFileMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of FirmwareFileMetadata from a JSON string
firmware_file_metadata_instance = FirmwareFileMetadata.from_json(json)
# print the JSON string representation of the object
print(FirmwareFileMetadata.to_json())

# convert the object into a dict
firmware_file_metadata_dict = firmware_file_metadata_instance.to_dict()
# create an instance of FirmwareFileMetadata from a dict
firmware_file_metadata_from_dict = FirmwareFileMetadata.from_dict(firmware_file_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


