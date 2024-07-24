# %%
import requests
from requests.auth import HTTPBasicAuth
import json

api_key = "5rCMKfU4JJV6SjOy_z237lk0-OoxdQIM_MjOPu2P2BGLENG60jY1eA"
# %%
# result_no_key = requests.get("http://127.0.0.1:5000/get_protocols")
# print(result_no_key.text)
# %%

result = requests.get("http://localhost:5000/protocols", auth=("", f"{api_key}"))
print(result.text)
