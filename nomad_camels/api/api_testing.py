# %%
import requests
from requests.auth import HTTPBasicAuth
import json

api_key = "fgzT7KuEcCkEbP_Sh9BDHqwBCDCE3MhtpnKpHbUb47PTmS4vaccGJQ"
# %%
protocol_name = "demo"
data = {"variables": {"start_stop": 10, "points": 31}}
# convert data to json
data_json = json.dumps(data)
# %%
# result = requests.post(
#     f"http://127.0.0.1:5000/api/v1/actions/run/protocols/{protocol_name}", auth=("", f"{api_key}"), json=data
# )
# print(result.text)
# %%
protocol_name = "demo"
index = -1
data = {"variables": {"start_stop": 120, "points": 31}}
result = requests.post(
    f"http://127.0.0.1:5000/api/v1/actions/queue/variables/protocols/{protocol_name}_{index}",
    auth=("", f"{api_key}"),
    json=data,
)
# %%
