# FirmwareFile

Firmware file metadata

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Firmware filename | [optional] 
**size** | **int** | File size in bytes | [optional] 
**hash** | **str** | File hash/checksum | [optional] 
**upload_date** | **datetime** | Upload timestamp | [optional] 
**metadata** | [**FirmwareFileMetadata**](FirmwareFileMetadata.md) |  | [optional] 

## Example

```python
from openapi_client.models.firmware_file import FirmwareFile

# TODO update the JSON string below
json = "{}"
# create an instance of FirmwareFile from a JSON string
firmware_file_instance = FirmwareFile.from_json(json)
# print the JSON string representation of the object
print(FirmwareFile.to_json())

# convert the object into a dict
firmware_file_dict = firmware_file_instance.to_dict()
# create an instance of FirmwareFile from a dict
firmware_file_from_dict = FirmwareFile.from_dict(firmware_file_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


