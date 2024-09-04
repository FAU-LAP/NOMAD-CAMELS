# %%
import requests
from requests.auth import HTTPBasicAuth
import json

api_key = "fgzT7KuEcCkEbP_Sh9BDHqwBCDCE3MhtpnKpHbUb47PTmS4vaccGJQ"
# %%
# protocol_name = "demo"
# data = {"variables": {"start_stop": 10, "points": 31}}
# # convert data to json
# data_json = json.dumps(data)
# %%
# result = requests.post(
#     f"http://127.0.0.1:5000/api/v1/actions/run/protocols/{protocol_name}", auth=("", f"{api_key}"), json=data
# )
# print(result.text)
# %%
protocol_name = "demo"
index = -1
data = {"variables": {"start_stop": 120, "points": 31}}
result = requests.get(f"http://127.0.0.1:8088/openapi.json")
# %%
# Parse the JSON response
openapi_schema = json.loads(result.text)
paths = openapi_schema.get("paths", {})
# Extract the function names and descriptions
api_functions = []
for path, methods in paths.items():
    for method, details in methods.items():
        summary = details.get("summary", "No summary available")
        operation_id = details.get("operationId", "Unnamed function")
        description = details.get("description", "No description available")
        parameters = details.get("parameters", [])
        print(parameters)
        api_functions.append(
            {
                "summary": summary,
                "method": method.upper(),
                "path": path,
                "operation_id": operation_id,
                "description": description,
                "parameters": parameters,
            }
        )
# Print the extracted information
# for func in api_functions:
#     print(
#         f"Method: {func['method']}, Path: {func['path']}, Summary: {func['summary']}, Function: {func['operation_id']}, Description: {func['description']}"
#     )
