import requests
api_key = "123abc" # Enter the actual API key you got from CAMELS here
protocol_name = 'demo' # Change this to the name of the protocol you are using
data = {'variables': {'npoints': 7,}}
# Create the headers with the Bearer token
headers = {
    "Authorization": f"Bearer {api_key}"
}
port = 5000 # Change this to the port you are acutally using
result = requests.post(
    f"http://127.0.0.1:{port}/api/v1/actions/run/protocols/{protocol_name}",
    headers=headers,
    json=data
)
print(result.json())