import requests
import re
from requests.auth import HTTPBasicAuth


def execute_camels_api_call(
    host: str,
    port: str,
    api_type: str,
    message_body: dict,
    authentication_type: str,
    authentication_string: str,
    selected_camels_function_index: int,
    camels_function_parameters: dict,
):
    """
    This function executes the CAMELS API call and returns the results.
    """
    # Make sure there is HTTP schema in the host
    if not host.startswith("http"):
        host = f"http://{host}"
    # Use port 80 for http and 443 for https if no port is provided
    if port == "":
        if host.startswith("https"):
            port = "443"
        else:
            port = "80"
    if api_type != "CAMELS":
        raise ValueError(
            "The API type is not CAMELS. This function is only for executing CAMELS API functions."
        )
    api_functions = get_available_camels_api_functions(
        host, port, camels_function_parameters
    )
    # Get the selected function
    selected_function = api_functions[selected_camels_function_index]
    # Check the HTTP method
    if selected_function["method"] == "GET":
        # Check the authentication type
        if authentication_type == "Bearer Token":
            result = requests.get(
                f"{host}:{port}{selected_function['formatted_path']}",
                headers={"Authorization": f"Bearer {authentication_string}"},
            )
        elif authentication_type == "HTTP Basic":
            raise ValueError(
                "HTTP Basic authentication is not supported for CAMELS requests."
            )
        elif authentication_type == "None":
            raise ValueError("No authentication is not supported for CAMELS requests.")

    elif selected_function["method"] == "POST":
        # Check the authentication type
        if authentication_type == "Bearer Token":
            result = requests.post(
                f"{host}:{port}{selected_function['formatted_path']}",
                headers={"Authorization": f"Bearer {authentication_string}"},
                json=message_body,
            )
        elif authentication_type == "HTTP Basic":
            raise ValueError(
                "HTTP Basic authentication is not supported for CAMELS requests."
            )
        elif authentication_type == "None":
            raise ValueError("No authentication is not supported for CAMELS requests.")

    return result.json()


def execute_generic_api_call(
    host: str,
    port: str,
    api_type: str,
    api_url: str,
    http_method: str,
    message_body: dict,
    authentication_type: str,
    authentication_string: str,
    http_parameters: dict,

):
    """
    This function executes the generic API call and returns the results.
    """
    # Make sure there is HTTP schema in the host
    if not host.startswith("http"):
        host = f"http://{host}"
    # Use port 80 for http and 443 for https if no port is provided
    if port == "":
        if host.startswith("https"):
            port = "443"
        else:
            port = "80"
    if api_type != "Generic":
        raise ValueError(
            "The API type is not Generic. This function is only for executing Generic API functions."
        )
    
    # Add the http_parameters to the api_url
    if http_parameters:
        print(http_parameters)
        api_url = api_url + "?"
        parameters = http_parameters['Parameter']
        values = http_parameters['Value']
        for param, value in zip(parameters, values):
            api_url = api_url + f"{param}={value}&"
        api_url = api_url[:-1]
        print(api_url)
        print('_'   * 50)
    
    
    # Check the HTTP method
    if http_method == "GET":
        # Check the authentication type
        if authentication_type == "Bearer Token":
            result = requests.get(
                f"{host}:{port}{api_url}",
                headers={"Authorization": f"Bearer {authentication_string}"},
            )
        elif authentication_type == "HTTP Basic":
            result = requests.get(
                f"{host}:{port}{api_url}",
                auth=HTTPBasicAuth(*authentication_string.split(":")),
            )
        elif authentication_type == "None":
            result = requests.get(f"{host}:{port}{api_url}")

    elif http_method == "POST":
        # Check the authentication type
        if authentication_type == "Bearer Token":
            result = requests.post(
                f"{host}:{port}{api_url}",
                headers={"Authorization": f"Bearer {authentication_string}"},
                json=message_body,
            )
        elif authentication_type == "HTTP Basic":
            result = requests.post(
                f"{host}:{port}{api_url}",
                auth=HTTPBasicAuth(*authentication_string.split(":")),
                json=message_body,
            )
        elif authentication_type == "None":
            result = requests.post(
                f"{host}:{port}{api_url}",
                json=message_body,
            )
    elif http_method == "DELETE":
        # Check the authentication type
        if authentication_type == "Bearer Token":
            result = requests.delete(
                f"{host}:{port}{api_url}",
                headers={"Authorization": f"Bearer {authentication_string}"},
            )
        elif authentication_type == "HTTP Basic":
            result = requests.delete(
                f"{host}:{port}{api_url}",
                auth=HTTPBasicAuth(*authentication_string.split(":")),
            )
        elif authentication_type == "None":
            result = requests.delete(f"{host}:{port}{api_url}")

        elif http_method == "PATCH":
            # Check the authentication type
            if authentication_type == "Bearer Token":
                result = requests.patch(
                    f"{host}:{port}{api_url}",
                    headers={"Authorization": f"Bearer {authentication_string}"},
                    json=message_body,
                )
            elif authentication_type == "HTTP Basic":
                result = requests.patch(
                    f"{host}:{port}{api_url}",
                    auth=HTTPBasicAuth(*authentication_string.split(":")),
                    json=message_body,
                )
            elif authentication_type == "None":
                result = requests.patch(
                    f"{host}:{port}{api_url}",
                    json=message_body,
                )

            elif http_method == "PUT":
                # Check the authentication type
                if authentication_type == "Bearer Token":
                    result = requests.put(
                        f"{host}:{port}{api_url}",
                        headers={"Authorization": f"Bearer {authentication_string}"},
                        json=message_body,
                    )
                elif authentication_type == "HTTP Basic":
                    result = requests.put(
                        f"{host}:{port}{api_url}",
                        auth=HTTPBasicAuth(*authentication_string.split(":")),
                        json=message_body,
                    )
                elif authentication_type == "None":
                    result = requests.put(
                        f"{host}:{port}{api_url}",
                        json=message_body,
                    )
    if result.status_code == 403:
        raise ValueError("The authentication failed. Please check your credentials.")
    return result.json()


def save_API_response_to_variable(response, namespace, protocol_step_name):
    """
    This function saves the API response to the namespace. This allows you to use the response values in the script and following protocol steps.
    """
    # For key value pair in response dictionary save it to the namesapce
    for key, value in response.items():
        namespace[f"{protocol_step_name}_{key}"] = value
    return None


def evaluate_message_body(message_body, eva):
    """
    This function evaluates the values of the message_body items if the value is empty.
    This allows you to use variables and values that are obtained during the script execution.
    """
    # For key value pair in message_body dictionary evaluate the value
    for key, value in message_body["variables"].items():
        if value == "":
            message_body["variables"][key] = eva.eval(key)
    return message_body


def get_available_camels_api_functions(host, port, camels_function_parameters):
    """
    This function gets all the available CAMELS API functions.
    """
    # Get all the available functions from the API
    result = requests.get(f"{host}:{port}/openapi.json")
    # Parse the JSON response
    openapi_schema = result.json()
    paths = openapi_schema.get("paths", {})
    # Create the formatted path
    # Extract the function names and descriptions
    api_functions = []
    for path, methods in paths.items():
        # Extract variables from the path
        path_variables = re.findall(r"\{(\w+)\}", path)

        # Check if all variables are in the parameters dictionary
        if all(var in camels_function_parameters for var in path_variables):
            formatted_path = path.format(**camels_function_parameters)
        else:
            formatted_path = "Not modified"  # or handle it accordingly
        for method, details in methods.items():
            summary = details.get("summary", "No summary available")
            operation_id = details.get("operationId", "Unnamed function")
            description = details.get("description", "No description available")
            parameters = details.get("parameters", [])
            api_functions.append(
                {
                    "summary": summary,
                    "method": method.upper(),
                    "path": path,
                    "operation_id": operation_id,
                    "description": description,
                    "parameters": parameters,
                    "formatted_path": formatted_path,
                }
            )
    return api_functions
