# %%
import requests
from requests.auth import HTTPBasicAuth
import json

api_key = "4hdB9w9_CHHkZH6f3pHCT6l7rLKvoNPRlhP62o7q7LM6L_6GhGhIDQ"
# %%
data = {'variables': {'start_stop': 10, 'points': 31}}
# convert data to json
data_json = json.dumps(data)
# %%
result = requests.post(
    "http://127.0.0.1:5000/api/v1/actions/run/protocols/demo", auth=("", f"{api_key}"), json=data
)
print(result.text)
