import requests
import re
from requests.auth import HTTPBasicAuth


def execute_camels_api_call(
    host,
    port,
    api_type,
    post_body,
    authentication_type,
    authentication_string,
    selected_camels_function_index,
    camels_function_parameters,
):
    """
    This function executes the CAMELS API call and returns the results.
    """
    if api_type != "CAMELS":
        raise ValueError(
            "The API type is not CAMELS. This function is only for executing CAMELS API functions."
        )
    # Get all the available functions from the API
    result = requests.get(f"http://{host}:{port}/openapi.json")
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
    # Get the selected function
    selected_function = api_functions[selected_camels_function_index]
    # Check the HTTP method
    if selected_function["method"] == "GET":
        # Check the authentication type
        if authentication_type == "API Key":
            result = requests.get(
                f"http://{host}:{port}{selected_function['formatted_path']}",
                headers={"Authorization": f"Bearer {authentication_string}"},
            )
        elif authentication_type == "HTTP Basic":
            result = requests.get(
                f"http://{host}:{port}{selected_function['formatted_path']}",
                auth=tuple(authentication_string.split(":")),
            )
        elif authentication_type == "None":
            result = requests.get(
                f"http://{host}:{port}{selected_function['formatted_path']}"
            )

    elif selected_function["method"] == "POST":
        # Check the authentication type
        if authentication_type == "API Key":
            result = requests.post(
                f"http://{host}:{port}{selected_function['formatted_path']}",
                headers={"Authorization": f"Bearer {authentication_string}"},
                json=post_body,
            )
        elif authentication_type == "HTTP Basic":
            result = requests.post(
                f"http://{host}:{port}{selected_function['formatted_path']}",
                auth=tuple(authentication_string.split(":")),
                json=post_body,
            )
        elif authentication_type == "None":
            result = requests.post(
                f"http://{host}:{port}{selected_function['formatted_path']}",
                json=post_body,
            )

    return result.json()


def execute_generic_api_call(
    host, port, api_type, post_body, authentication_type, authentication_string
):
    """
    This function executes the generic API call and returns the results.
    """
    # This function is not implemented yet.
    return None


def save_API_response_to_variable(response, namespace):
    """
    This function saves the API response to the namespace.
    """
    # For key value pair in response dictionary save it to the name sapce
    for key, value in response.items():
        namespace[key] = value
    return None


def evaluate_post_body(post_body, eva):
    """
    This function evaluates the values of the post_body items if the value is empty.
    This allows you to use variables and values that are obtained during the script execution.
    """
    # For key value pair in post_body dictionary evaluate the value
    for key, value in post_body["variables"].items():
        if value == "":
            post_body["variables"][key] = eva.eval(key)
    return post_body


def get_available_camels_api_functions(host, port, camels_function_parameters):
    """
    This function gets all the available CAMELS API functions.
    """
    # Get all the available functions from the API
    result = requests.get(f"http://{host}:{port}/openapi.json")
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