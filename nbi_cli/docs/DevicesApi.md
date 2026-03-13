# openapi_client.DevicesApi

All URIs are relative to *https://demo1.lab2.local.stechs.io/acs/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_object_async**](DevicesApi.md#add_object_async) | **POST** /devices/{SerialNumber}/addObject/async | Add object (asynchronous)
[**add_object_sync**](DevicesApi.md#add_object_sync) | **POST** /devices/{SerialNumber}/addObject | Add object (synchronous)
[**delete_object_async**](DevicesApi.md#delete_object_async) | **POST** /devices/{SerialNumber}/deleteObject/async | Delete object (asynchronous)
[**delete_object_sync**](DevicesApi.md#delete_object_sync) | **DELETE** /devices/{SerialNumber}/deleteObject/{ObjectName} | Delete object (synchronous)
[**factory_reset_async**](DevicesApi.md#factory_reset_async) | **POST** /devices/{SerialNumber}/factoryReset/async | Factory reset device (asynchronous)
[**factory_reset_sync**](DevicesApi.md#factory_reset_sync) | **POST** /devices/{SerialNumber}/factoryReset | Factory reset device (synchronous)
[**get_parameter_value_async**](DevicesApi.md#get_parameter_value_async) | **POST** /devices/{SerialNumber}/getParameterValue/async | Get parameter values (asynchronous)
[**get_parameter_value_sync**](DevicesApi.md#get_parameter_value_sync) | **GET** /devices/{SerialNumber}/getParameterValue | Get parameter values (synchronous)
[**list_devices_async**](DevicesApi.md#list_devices_async) | **POST** /devices/async | List devices (asynchronous)
[**list_devices_sync**](DevicesApi.md#list_devices_sync) | **GET** /devices | List devices (synchronous)
[**reboot_async**](DevicesApi.md#reboot_async) | **POST** /devices/{SerialNumber}/reboot/async | Reboot device (asynchronous)
[**reboot_sync**](DevicesApi.md#reboot_sync) | **POST** /devices/{SerialNumber}/reboot | Reboot device (synchronous)
[**refresh_object_async**](DevicesApi.md#refresh_object_async) | **POST** /devices/{SerialNumber}/refreshObject/async | Refresh object (asynchronous)
[**refresh_object_sync**](DevicesApi.md#refresh_object_sync) | **PUT** /devices/{SerialNumber}/refreshObject | Refresh object (synchronous)
[**set_parameter_value_async**](DevicesApi.md#set_parameter_value_async) | **POST** /devices/{SerialNumber}/setParameterValue/async | Set parameter values (asynchronous)
[**set_parameter_value_sync**](DevicesApi.md#set_parameter_value_sync) | **POST** /devices/{SerialNumber}/setParameterValue | Set parameter values (synchronous)


# **add_object_async**
> AsyncResponse add_object_async(serial_number, add_object_callback_request, timeout=timeout)

Add object (asynchronous)

Asynchronously adds a new TR-069 object instance

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.add_object_callback_request import AddObjectCallbackRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    add_object_callback_request = openapi_client.AddObjectCallbackRequest() # AddObjectCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Add object (asynchronous)
        api_response = api_instance.add_object_async(serial_number, add_object_callback_request, timeout=timeout)
        print("The response of DevicesApi->add_object_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->add_object_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **add_object_callback_request** | [**AddObjectCallbackRequest**](AddObjectCallbackRequest.md)|  | 
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

# **add_object_sync**
> List[ParameterValue] add_object_sync(serial_number, object_operation_request, timeout=timeout)

Add object (synchronous)

Adds a new TR-069 object instance to the device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.object_operation_request import ObjectOperationRequest
from openapi_client.models.parameter_value import ParameterValue
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    object_operation_request = openapi_client.ObjectOperationRequest() # ObjectOperationRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Add object (synchronous)
        api_response = api_instance.add_object_sync(serial_number, object_operation_request, timeout=timeout)
        print("The response of DevicesApi->add_object_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->add_object_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **object_operation_request** | [**ObjectOperationRequest**](ObjectOperationRequest.md)|  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**List[ParameterValue]**](ParameterValue.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Object added successfully |  -  |
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_object_async**
> AsyncResponse delete_object_async(serial_number, delete_object_callback_request, timeout=timeout)

Delete object (asynchronous)

Asynchronously deletes a TR-069 object instance

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.delete_object_callback_request import DeleteObjectCallbackRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    delete_object_callback_request = openapi_client.DeleteObjectCallbackRequest() # DeleteObjectCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Delete object (asynchronous)
        api_response = api_instance.delete_object_async(serial_number, delete_object_callback_request, timeout=timeout)
        print("The response of DevicesApi->delete_object_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->delete_object_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **delete_object_callback_request** | [**DeleteObjectCallbackRequest**](DeleteObjectCallbackRequest.md)|  | 
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

# **delete_object_sync**
> object delete_object_sync(serial_number, object_name, timeout=timeout)

Delete object (synchronous)

Deletes a TR-069 object instance from the device

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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    object_name = 'Device.WiFi.AccessPoint.2' # str | TR-069 object name to delete
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Delete object (synchronous)
        api_response = api_instance.delete_object_sync(serial_number, object_name, timeout=timeout)
        print("The response of DevicesApi->delete_object_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->delete_object_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **object_name** | **str**| TR-069 object name to delete | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

**object**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Object deleted successfully |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **factory_reset_async**
> AsyncResponse factory_reset_async(serial_number, callback_request, timeout=timeout)

Factory reset device (asynchronous)

Asynchronously performs a factory reset on the device

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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Factory reset device (asynchronous)
        api_response = api_instance.factory_reset_async(serial_number, callback_request, timeout=timeout)
        print("The response of DevicesApi->factory_reset_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->factory_reset_async: %s\n" % e)
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
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **factory_reset_sync**
> FactoryResetSync200Response factory_reset_sync(serial_number, timeout=timeout)

Factory reset device (synchronous)

Performs a factory reset on the device via TR-069

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.factory_reset_sync200_response import FactoryResetSync200Response
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Factory reset device (synchronous)
        api_response = api_instance.factory_reset_sync(serial_number, timeout=timeout)
        print("The response of DevicesApi->factory_reset_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->factory_reset_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**FactoryResetSync200Response**](FactoryResetSync200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Factory reset command sent successfully |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_parameter_value_async**
> AsyncResponse get_parameter_value_async(serial_number, get_parameter_value_callback_request, timeout=timeout)

Get parameter values (asynchronous)

Asynchronously retrieves TR-069 parameter values from a device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.get_parameter_value_callback_request import GetParameterValueCallbackRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    get_parameter_value_callback_request = openapi_client.GetParameterValueCallbackRequest() # GetParameterValueCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get parameter values (asynchronous)
        api_response = api_instance.get_parameter_value_async(serial_number, get_parameter_value_callback_request, timeout=timeout)
        print("The response of DevicesApi->get_parameter_value_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->get_parameter_value_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **get_parameter_value_callback_request** | [**GetParameterValueCallbackRequest**](GetParameterValueCallbackRequest.md)|  | 
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

# **get_parameter_value_sync**
> List[ParameterValue] get_parameter_value_sync(serial_number, params_list, connection_request=connection_request, timeout=timeout)

Get parameter values (synchronous)

Retrieves TR-069 parameter values from a device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.parameter_value import ParameterValue
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    params_list = ['[\"Device.DeviceInfo.ModelName\",\"Device.DeviceInfo.Manufacturer\"]'] # List[str] | List of TR-069 parameter names to retrieve
    connection_request = True # bool | When true (default), a TR-069 Connection Request is immediately sent to the device. When false, parameters will take effect at the device's next periodic communication.  (optional) (default to True)
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get parameter values (synchronous)
        api_response = api_instance.get_parameter_value_sync(serial_number, params_list, connection_request=connection_request, timeout=timeout)
        print("The response of DevicesApi->get_parameter_value_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->get_parameter_value_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **params_list** | [**List[str]**](str.md)| List of TR-069 parameter names to retrieve | 
 **connection_request** | **bool**| When true (default), a TR-069 Connection Request is immediately sent to the device. When false, parameters will take effect at the device&#39;s next periodic communication.  | [optional] [default to True]
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**List[ParameterValue]**](ParameterValue.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Parameter values retrieved successfully |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_devices_async**
> AsyncResponse list_devices_async(get_device_list_callback_request, timeout=timeout)

List devices (asynchronous)

Asynchronously retrieves a list of devices. Results will be sent to the provided callback URL.

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.get_device_list_callback_request import GetDeviceListCallbackRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    get_device_list_callback_request = openapi_client.GetDeviceListCallbackRequest() # GetDeviceListCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # List devices (asynchronous)
        api_response = api_instance.list_devices_async(get_device_list_callback_request, timeout=timeout)
        print("The response of DevicesApi->list_devices_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->list_devices_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **get_device_list_callback_request** | [**GetDeviceListCallbackRequest**](GetDeviceListCallbackRequest.md)|  | 
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_devices_sync**
> List[Device] list_devices_sync(limit=limit, offset=offset, serial_number=serial_number, tags=tags, product_class=product_class, last_inform=last_inform, last_inform_operator=last_inform_operator, projection=projection, timeout=timeout)

List devices (synchronous)

Retrieves a list of devices from the ACS server with optional filtering and pagination.
Supports filtering by serial number, tags, product class, and last inform time.


### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.device import Device
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
    api_instance = openapi_client.DevicesApi(api_client)
    limit = 100 # int | Maximum number of results to return (optional) (default to 100)
    offset = 0 # int | Number of results to skip (for pagination) (optional) (default to 0)
    serial_number = 'abcdea2332da' # str | Filter devices by serial number (supports regex patterns) (optional)
    tags = 'ManufacturerStechs' # str | Filter devices by tags (optional)
    product_class = 'StechsDevice' # str | Filter devices by product class (optional)
    last_inform = '2023-10-01T12:00:00Z' # datetime | Filter devices by last inform time (ISO 8601 format) (optional)
    last_inform_operator = lte # str | Comparison operator for lastInform filter (optional) (default to lte)
    projection = ['[\"VirtualParameters.DeviceInfoExtended\",\"Device.DeviceInfo.ModelName\"]'] # List[str] | Specify which fields to include in the response (optional)
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # List devices (synchronous)
        api_response = api_instance.list_devices_sync(limit=limit, offset=offset, serial_number=serial_number, tags=tags, product_class=product_class, last_inform=last_inform, last_inform_operator=last_inform_operator, projection=projection, timeout=timeout)
        print("The response of DevicesApi->list_devices_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->list_devices_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of results to return | [optional] [default to 100]
 **offset** | **int**| Number of results to skip (for pagination) | [optional] [default to 0]
 **serial_number** | **str**| Filter devices by serial number (supports regex patterns) | [optional] 
 **tags** | **str**| Filter devices by tags | [optional] 
 **product_class** | **str**| Filter devices by product class | [optional] 
 **last_inform** | **datetime**| Filter devices by last inform time (ISO 8601 format) | [optional] 
 **last_inform_operator** | **str**| Comparison operator for lastInform filter | [optional] [default to lte]
 **projection** | [**List[str]**](str.md)| Specify which fields to include in the response | [optional] 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**List[Device]**](Device.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of devices |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reboot_async**
> AsyncResponse reboot_async(serial_number, callback_request, timeout=timeout)

Reboot device (asynchronous)

Asynchronously sends a reboot command to the device

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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Reboot device (asynchronous)
        api_response = api_instance.reboot_async(serial_number, callback_request, timeout=timeout)
        print("The response of DevicesApi->reboot_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->reboot_async: %s\n" % e)
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
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reboot_sync**
> RebootSync200Response reboot_sync(serial_number, timeout=timeout)

Reboot device (synchronous)

Sends a reboot command to the device via TR-069

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.reboot_sync200_response import RebootSync200Response
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Reboot device (synchronous)
        api_response = api_instance.reboot_sync(serial_number, timeout=timeout)
        print("The response of DevicesApi->reboot_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->reboot_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**RebootSync200Response**](RebootSync200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Reboot command sent successfully |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refresh_object_async**
> AsyncResponse refresh_object_async(serial_number, refresh_object_callback_request, timeout=timeout)

Refresh object (asynchronous)

Asynchronously refreshes a TR-069 object

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.refresh_object_callback_request import RefreshObjectCallbackRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    refresh_object_callback_request = openapi_client.RefreshObjectCallbackRequest() # RefreshObjectCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Refresh object (asynchronous)
        api_response = api_instance.refresh_object_async(serial_number, refresh_object_callback_request, timeout=timeout)
        print("The response of DevicesApi->refresh_object_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->refresh_object_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **refresh_object_callback_request** | [**RefreshObjectCallbackRequest**](RefreshObjectCallbackRequest.md)|  | 
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

# **refresh_object_sync**
> List[ParameterValue] refresh_object_sync(serial_number, object_operation_request, timeout=timeout)

Refresh object (synchronous)

Refreshes a TR-069 object and retrieves all its parameters

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.object_operation_request import ObjectOperationRequest
from openapi_client.models.parameter_value import ParameterValue
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    object_operation_request = openapi_client.ObjectOperationRequest() # ObjectOperationRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Refresh object (synchronous)
        api_response = api_instance.refresh_object_sync(serial_number, object_operation_request, timeout=timeout)
        print("The response of DevicesApi->refresh_object_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->refresh_object_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **object_operation_request** | [**ObjectOperationRequest**](ObjectOperationRequest.md)|  | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**List[ParameterValue]**](ParameterValue.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Object refreshed successfully |  -  |
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_parameter_value_async**
> AsyncResponse set_parameter_value_async(serial_number, set_parameter_value_callback_request, timeout=timeout)

Set parameter values (asynchronous)

Asynchronously sets TR-069 parameter values on a device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.async_response import AsyncResponse
from openapi_client.models.set_parameter_value_callback_request import SetParameterValueCallbackRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    set_parameter_value_callback_request = openapi_client.SetParameterValueCallbackRequest() # SetParameterValueCallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Set parameter values (asynchronous)
        api_response = api_instance.set_parameter_value_async(serial_number, set_parameter_value_callback_request, timeout=timeout)
        print("The response of DevicesApi->set_parameter_value_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->set_parameter_value_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **set_parameter_value_callback_request** | [**SetParameterValueCallbackRequest**](SetParameterValueCallbackRequest.md)|  | 
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

# **set_parameter_value_sync**
> object set_parameter_value_sync(serial_number, set_parameter_value_request, timeout=timeout)

Set parameter values (synchronous)

Sets TR-069 parameter values on a device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.set_parameter_value_request import SetParameterValueRequest
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
    api_instance = openapi_client.DevicesApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    set_parameter_value_request = openapi_client.SetParameterValueRequest() # SetParameterValueRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Set parameter values (synchronous)
        api_response = api_instance.set_parameter_value_sync(serial_number, set_parameter_value_request, timeout=timeout)
        print("The response of DevicesApi->set_parameter_value_sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DevicesApi->set_parameter_value_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **set_parameter_value_request** | [**SetParameterValueRequest**](SetParameterValueRequest.md)|  | 
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
**200** | Parameters set successfully |  -  |
**400** | Bad request - invalid parameters or missing required fields |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |
**500** | ACS server interaction error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

