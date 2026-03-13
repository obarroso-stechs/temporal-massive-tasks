# openapi_client.TasksApi

All URIs are relative to *https://demo1.lab2.local.stechs.io/acs/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_device_task**](TasksApi.md#delete_device_task) | **DELETE** /tasks/{TaskId} | Delete device task
[**delete_device_task_async**](TasksApi.md#delete_device_task_async) | **POST** /tasks/del/{TaskId}/async | Delete device task (asynchronous)
[**get_device_tasks**](TasksApi.md#get_device_tasks) | **GET** /tasks/{SerialNumber} | Get device tasks
[**get_device_tasks_async**](TasksApi.md#get_device_tasks_async) | **POST** /tasks/get/{SerialNumber}/async | Get device tasks (asynchronous)


# **delete_device_task**
> DeleteDeviceTask200Response delete_device_task(task_id, timeout=timeout)

Delete device task

Deletes a specific device task

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
    api_instance = openapi_client.TasksApi(api_client)
    task_id = '6895fbe203373319060500c7' # str | Task ID to delete
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Delete device task
        api_response = api_instance.delete_device_task(task_id, timeout=timeout)
        print("The response of TasksApi->delete_device_task:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TasksApi->delete_device_task: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**| Task ID to delete | 
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
**200** | Task deleted successfully |  -  |
**404** | Task not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_device_task_async**
> AsyncResponse delete_device_task_async(task_id, callback_request, timeout=timeout)

Delete device task (asynchronous)

Asynchronously deletes a specific device task

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
    api_instance = openapi_client.TasksApi(api_client)
    task_id = '6895fbe203373319060500c7' # str | Task ID to delete
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Delete device task (asynchronous)
        api_response = api_instance.delete_device_task_async(task_id, callback_request, timeout=timeout)
        print("The response of TasksApi->delete_device_task_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TasksApi->delete_device_task_async: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**| Task ID to delete | 
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
**404** | Task not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device_tasks**
> DeviceTask get_device_tasks(serial_number, timeout=timeout)

Get device tasks

Retrieves pending tasks for a specific device

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.device_task import DeviceTask
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
    api_instance = openapi_client.TasksApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get device tasks
        api_response = api_instance.get_device_tasks(serial_number, timeout=timeout)
        print("The response of TasksApi->get_device_tasks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TasksApi->get_device_tasks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **serial_number** | **str**| Device serial number | 
 **timeout** | **int**| Operation timeout in seconds | [optional] 

### Return type

[**DeviceTask**](DeviceTask.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Device tasks retrieved successfully |  -  |
**404** | Device not found |  -  |
**408** | Operation timeout - device did not respond in time |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device_tasks_async**
> AsyncResponse get_device_tasks_async(serial_number, callback_request, timeout=timeout)

Get device tasks (asynchronous)

Asynchronously retrieves pending tasks for a device

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
    api_instance = openapi_client.TasksApi(api_client)
    serial_number = 'abcdea2332da' # str | Device serial number
    callback_request = openapi_client.CallbackRequest() # CallbackRequest | 
    timeout = 30 # int | Operation timeout in seconds (optional)

    try:
        # Get device tasks (asynchronous)
        api_response = api_instance.get_device_tasks_async(serial_number, callback_request, timeout=timeout)
        print("The response of TasksApi->get_device_tasks_async:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TasksApi->get_device_tasks_async: %s\n" % e)
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

