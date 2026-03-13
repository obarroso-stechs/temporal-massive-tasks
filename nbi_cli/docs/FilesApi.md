# openapi_client.FilesApi

All URIs are relative to *https://demo1.lab2.local.stechs.io/acs/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_file_async**](FilesApi.md#download_file_async) | **POST** /files/{SerialNumber}/downloadFile/async | Download file to device (asynchronous)
[**download_file_sync**](FilesApi.md#download_file_sync) | **POST** /files/{SerialNumber}/downloadFile | Download file to device (synchronous)
[**get_all_firmware_files**](FilesApi.md#get_all_firmware_files) | **GET** /files/all | Get all firmware files (synchronous)
[**get_all_firmware_files_async**](FilesApi.md#get_all_firmware_files_async) | **POST** /files/all/async | Get all firmware files (asynchronous)
[**get_firmware_file_detail**](FilesApi.md#get_firmware_file_detail) | **GET** /files/{Filename} | Get firmware file details (synchronous)
[**get_firmware_file_detail_async**](FilesApi.md#get_firmware_file_detail_async) | **POST** /files/{Filename}/async | Get firmware file details (asynchronous)
[**upload_firmware_file_async**](FilesApi.md#upload_firmware_file_async) | **POST** /files/upload/async | Upload firmware file (asynchronous)
[**upload_firmware_file_sync**](FilesApi.md#upload_firmware_file_sync) | **POST** /files/upload | Upload firmware file (synchronous)


# **download_file_async**
> AsyncResponse download_file_async(serial_number, download_file_callback_request, timeout=timeout)

Download file to device (asynchronous)

Asynchronously instructs a device to download a file

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.download_file_callback_request import DownloadFileCallbackRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    download_file_callback_request = openapi_client.DownloadFileCallbackRequest() # DownloadFileCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Download file to device (asynchronous)
        api_response = api_instance.download_file_async(serial_number, download_file_callback_request, timeout=timeout)
        print("The response of FilesApi->download_file_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->download_file_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **download_file_callback_request** | [**DownloadFileCallbackRequest**](DownloadFileCallbackRequest.md)|  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**AsyncResponse**](AsyncResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operation queued successfully |  -  |
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_file_sync**
> object download_file_sync(serial_number, download_file_request, timeout=timeout)

Download file to device (synchronous)

Instructs a device to download a file from a specified URL via TR-069.
Typically used for firmware upgrades.


### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.download_file_request import DownloadFileRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    download_file_request = openapi_client.DownloadFileRequest() # DownloadFileRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Download file to device (synchronous)
        api_response = api_instance.download_file_sync(serial_number, download_file_request, timeout=timeout)
        print("The response of FilesApi->download_file_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->download_file_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **download_file_request** | [**DownloadFileRequest**](DownloadFileRequest.md)|  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

**object**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Download command sent successfully |  -  |
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_firmware_files**
> List[FirmwareFile] get_all_firmware_files(limit=limit, offset=offset, sort_order=sort_order, timeout=timeout)

Get all firmware files (synchronous)

Retrieves a list of all firmware files stored on the ACS server

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.firmware_file import FirmwareFile
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    limit = 100 # int | Maximum number of results to return (optional) (default to 100)
    offset = 0 # int | Number of results to skip (for pagination) (optional) (default to 0)
    sort_order = asc # str | Sort order for results (optional) (default to asc)
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get all firmware files (synchronous)
        api_response = api_instance.get_all_firmware_files(limit=limit, offset=offset, sort_order=sort_order, timeout=timeout)
        print("The response of FilesApi->get_all_firmware_files:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->get_all_firmware_files: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of results to return | [optional] [default to 100]
 **offset** | **int**| Number of results to skip (for pagination) | [optional] [default to 0]
 **sort_order** | **str**| Sort order for results | [optional] [default to asc]
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**List[FirmwareFile]**](FirmwareFile.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Firmware files retrieved successfully |  -  |
**408** | Operation timeout - device did not respond in time |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_firmware_files_async**
> AsyncResponse get_all_firmware_files_async(get_all_firmware_files_callback_request, timeout=timeout)

Get all firmware files (asynchronous)

Asynchronously retrieves a list of all firmware files

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.get_all_firmware_files_callback_request import GetAllFirmwareFilesCallbackRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    get_all_firmware_files_callback_request = openapi_client.GetAllFirmwareFilesCallbackRequest() # GetAllFirmwareFilesCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get all firmware files (asynchronous)
        api_response = api_instance.get_all_firmware_files_async(get_all_firmware_files_callback_request, timeout=timeout)
        print("The response of FilesApi->get_all_firmware_files_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->get_all_firmware_files_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **get_all_firmware_files_callback_request** | [**GetAllFirmwareFilesCallbackRequest**](GetAllFirmwareFilesCallbackRequest.md)|  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**AsyncResponse**](AsyncResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operation queued successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_file_detail**
> FirmwareFile get_firmware_file_detail(filename, timeout=timeout)

Get firmware file details (synchronous)

Retrieves details about a specific firmware file

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.firmware_file import FirmwareFile
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    filename = 'firmware.bin' # str | Firmware filename
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get firmware file details (synchronous)
        api_response = api_instance.get_firmware_file_detail(filename, timeout=timeout)
        print("The response of FilesApi->get_firmware_file_detail:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->get_firmware_file_detail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **str**| Firmware filename | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**FirmwareFile**](FirmwareFile.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Firmware file details retrieved |  -  |
**404** | File not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_file_detail_async**
> AsyncResponse get_firmware_file_detail_async(filename, callback_request, timeout=timeout)

Get firmware file details (asynchronous)

Asynchronously retrieves details about a specific firmware file

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.callback_request import CallbackRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    filename = 'firmware.bin' # str | Firmware filename
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get firmware file details (asynchronous)
        api_response = api_instance.get_firmware_file_detail_async(filename, callback_request, timeout=timeout)
        print("The response of FilesApi->get_firmware_file_detail_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->get_firmware_file_detail_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **str**| Firmware filename | 
 **callback_request** | [**CallbackRequest**](CallbackRequest.md)|  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**AsyncResponse**](AsyncResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operation queued successfully |  -  |
**404** | File not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_firmware_file_async**
> AsyncResponse upload_firmware_file_async(file, callback_data, timeout=timeout)

Upload firmware file (asynchronous)

Asynchronously uploads a firmware file to the ACS server.

**IMPORTANT**: Both `file` and `callbackData` must be sent as multipart/form-data fields.
The `callbackData` field must contain a JSON file with the callback URL and device parameters.

### How to use in Insomnia/Postman:
1. Set request type to POST
2. Set body type to "Multipart Form"
3. Add field `file` - select "File" type and choose your firmware binary file
4. Add field `callbackData` - select "File" type and upload a JSON file OR create a text file with the JSON content

### callbackData JSON structure:
```json
{
  "url": "https://webhook.site/your-callback-url",
  "username": "optional-user",
  "password": "optional-pass",
  "oui": "654321",
  "productClass": "AsyncTestProduct",
  "version": "2.0.0"
}
```


### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    file = None # bytearray | Firmware file to upload (binary data)
    callback_data = None # bytearray | JSON file containing callback registration data. Must be sent as a file field, not a regular form parameter. 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Upload firmware file (asynchronous)
        api_response = api_instance.upload_firmware_file_async(file, callback_data, timeout=timeout)
        print("The response of FilesApi->upload_firmware_file_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->upload_firmware_file_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**| Firmware file to upload (binary data) | 
 **callback_data** | **bytearray**| JSON file containing callback registration data. Must be sent as a file field, not a regular form parameter.  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**AsyncResponse**](AsyncResponse.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upload request accepted and queued |  -  |
**400** | Bad request - missing required fields or invalid JSON |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_firmware_file_sync**
> str upload_firmware_file_sync(oui, product_class, version, file, timeout=timeout)

Upload firmware file (synchronous)

Uploads a firmware file to the ACS server. The file is stored with metadata including OUI, product class, and version.


### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://demo1.lab2.local.stechs.io/acs/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://demo1.lab2.local.stechs.io/acs/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = openapi_client.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilesApi(api_client)
    oui = '123456' # str | Organizationally Unique Identifier
    product_class = 'ABC123' # str | Product class identifier
    version = '1.0.0' # str | Firmware version
    file = None # bytearray | Firmware file to upload
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Upload firmware file (synchronous)
        api_response = api_instance.upload_firmware_file_sync(oui, product_class, version, file, timeout=timeout)
        print("The response of FilesApi->upload_firmware_file_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->upload_firmware_file_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **oui** | **str**| Organizationally Unique Identifier | 
 **product_class** | **str**| Product class identifier | 
 **version** | **str**| Firmware version | 
 **file** | **bytearray**| Firmware file to upload | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File uploaded successfully |  -  |
**400** | Bad request - invalid parameters or missing required fields |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

