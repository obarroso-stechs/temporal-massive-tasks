# openapi_client.FaultsApi

All URIs are relative to *https://demo1.lab2.local.stechs.io/acs/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_device_fault**](FaultsApi.md#delete_device_fault) | **DELETE** /faults/{FaultId} | Delete device fault
[**delete_device_fault_async**](FaultsApi.md#delete_device_fault_async) | **POST** /faults/del/{FaultId}/async | Delete device fault (asynchronous)
[**get_device_faults**](FaultsApi.md#get_device_faults) | **GET** /faults/{SerialNumber} | Get device faults
[**get_device_faults_async**](FaultsApi.md#get_device_faults_async) | **POST** /faults/get/{SerialNumber}/async | Get device faults (asynchronous)


# **delete_device_fault**
> DeleteDeviceTask200Response delete_device_fault(fault_id, timeout=timeout)

Delete device fault

Deletes a specific fault record

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.delete_device_task200_response import DeleteDeviceTask200Response
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
    api_instance = openapi_client.FaultsApi(api_client)
    fault_id = '34D856-GN630V-JBLNGG40351:inform' # str | Fault ID to delete
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Delete device fault
        api_response = api_instance.delete_device_fault(fault_id, timeout=timeout)
        print("The response of FaultsApi->delete_device_fault:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FaultsApi->delete_device_fault: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fault_id** | **str**| Fault ID to delete | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**DeleteDeviceTask200Response**](DeleteDeviceTask200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fault deleted successfully |  -  |
**404** | Fault not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_device_fault_async**
> AsyncResponse delete_device_fault_async(fault_id, callback_request, timeout=timeout)

Delete device fault (asynchronous)

Asynchronously deletes a specific fault record

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
    api_instance = openapi_client.FaultsApi(api_client)
    fault_id = '34D856-GN630V-JBLNGG40351:inform' # str | Fault ID to delete
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Delete device fault (asynchronous)
        api_response = api_instance.delete_device_fault_async(fault_id, callback_request, timeout=timeout)
        print("The response of FaultsApi->delete_device_fault_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FaultsApi->delete_device_fault_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fault_id** | **str**| Fault ID to delete | 
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
**404** | Fault not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device_faults**
> List[DeviceFault] get_device_faults(serial_number, timeout=timeout)

Get device faults

Retrieves fault records for a specific device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.device_fault import DeviceFault
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
    api_instance = openapi_client.FaultsApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get device faults
        api_response = api_instance.get_device_faults(serial_number, timeout=timeout)
        print("The response of FaultsApi->get_device_faults:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FaultsApi->get_device_faults: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**List[DeviceFault]**](DeviceFault.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Device faults retrieved successfully |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device_faults_async**
> AsyncResponse get_device_faults_async(serial_number, callback_request, timeout=timeout)

Get device faults (asynchronous)

Asynchronously retrieves fault records for a device

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
    api_instance = openapi_client.FaultsApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get device faults (asynchronous)
        api_response = api_instance.get_device_faults_async(serial_number, callback_request, timeout=timeout)
        print("The response of FaultsApi->get_device_faults_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FaultsApi->get_device_faults_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
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
**404** | Device not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

