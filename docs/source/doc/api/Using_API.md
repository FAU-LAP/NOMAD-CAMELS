# Using the API

You can send http requests to the web server to communicate with CAMELS. Documentation on the allowed requests and their logic is displayed on the landing page of the web server `//localhost:<port>/` or  `//localhost:<port>/docs`.

To use any request other than the home path of the web server you need to authenticate your request using the API key.

If you are using a regular browser to access the web server you will be asked to authenticate yourself. Simply enter the API key in the password section. The username can be left empty. This will look something like this
![Example image of the authentication pop up in the browser](images/image.png)

Once logged in the browser will stay authenticated when using further requests until you close the browser.
Following there are descriptions for the most useful commands.

## Get Protocol Names

You can get all protocol names that are currently defined in CAMELS by going to `//localhost:<port>/protocols`. 

You can also use Python to perform the http request. This could look something like:

```python
import requests
api_key = 123 # Enter the actual API key you got from CAMELS here
result = requests.get("http://localhost:5000/protocols", auth=("", f"{api_key}"))
```

The API will return a JSON string of the form:

```JSON
{"Protocols":["ProtocolXYZ","DefaultProtocol","..."]}
```

## Running Protocols

You can run an already defined protocol by going to `//localhost:<port>/protocols/{protocol_name}` or using Python:

```python
import requests
api_key = 123 # Enter the actual API you got from CAMELS here
result = requests.get("http://localhost:5000/protocols/TestScript", auth=("", f"{api_key}"))
```

This allows you to programmatically integrate CAMELS in already existing measurement routines. You could for example use CAMELS to control some temperature with its PID controller while still using all the software/code you are already using in your lab.