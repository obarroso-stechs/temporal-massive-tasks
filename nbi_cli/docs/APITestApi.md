# openapi_client.APITestApi

All URIs are relative to *https://demo1.lab2.local.stechs.io/acs/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_error_codes**](APITestApi.md#get_error_codes) | **GET** /errorCodes | List available error codes
[**test_ws**](APITestApi.md#test_ws) | **GET** /testws | API health check


# **get_error_codes**
> Dict[str, GetErrorCodes200ResponseValue] get_error_codes()

List available error codes

Returns all available error codes and their descriptions used by the API

### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.get_error_codes200_response_value import GetErrorCodes200ResponseValue
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
    api_instance = openapi_client.APITestApi(api_client)

    try:
        # List available error codes
        api_response = api_instance.get_error_codes()
        print("The response of APITestApi->get_error_codes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APITestApi->get_error_codes: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Dict[str, GetErrorCodes200ResponseValue]**](GetErrorCodes200ResponseValue.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Error codes list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_ws**
> TestWs200Response test_ws()

API health check

Tests if the API is running and checks Celery job queue connectivity.
Returns OK if both the API and job queuing system are operational.


### Example

* Basic Authentication (basicAuth):

```python
import openapi_client
from openapi_client.models.test_ws200_response import TestWs200Response
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
    api_instance = openapi_client.APITestApi(api_client)

    try:
        # API health check
        api_response = api_instance.test_ws()
        print("The response of APITestApi->test_ws:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APITestApi->test_ws: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TestWs200Response**](TestWs200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API status response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

