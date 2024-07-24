# CAMELS API

The CAMELS API allows you to interact with the opened CAMELS software. You can for example ask for all the current protocols and execute an already defined protocol. This allows you to integrate CAMELS with already existing control software.

CAMELS API uses a web server running on the machines `//localhost:`. You interact with the API by sending http requests to the web server.

## Enabeling the API

You can enable CAMELS API under `File -> Settings`. Check the box `Enable API` and enter a valid port that is not being used by other software on your computer (try something like `5000`). CAMELS will create the API web server as soon as you click `OK` and exit the settings window.

## Creating API Keys

You need to authenticate yourself with an API ke so that the web server accepts most http requests. You can generate such a key in the settings window (`File -> Settings`) by clicking `Generate API Key`. Now make sure to copy and paste this key somewhere and save it.

```{attention}
You can not get back the API key if you do not save it now! Although you can always just create a new API key if you lose an existing one.
```

```{info}
You can have any number of API keys active at the same time.
```

The SHA-256 hashes of the API keys are saved to a database file located in the path you gave for *configuration files* (typically something like `%localappdata%`).

See [here](#deleting-api-keys) for information on how to delete existing API keys.

## Using the API

You can send http requests to the web server to communicate with CAMELS. Documentation on the allowed requests and their logic is displayed on the landing page of the web server `//localhost:<port>/` or  `//localhost:<port>/docs`.

To use any request other than the home path of the web server you need to authenticate your request using the API key.

If you are using a regular browser to access the web server you will be asked to authenticate yourself. Simply enter the API key in the password section. The username can be left empty. This will look something like this
![Example image of the authentication pop up in the browser](images/image.png)

Once logged in the browser will stay authenticated when using further requests until you close the browser.
Following there are descriptions for the most useful commands.

### Get Protocol Names

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

### Running Protocols

You can run an already defined protocol by going to `//localhost:<port>/protocols/{protocol_name}` or using Python:

```python
import requests
api_key = 123 # Enter the actual API you got from CAMELS here
result = requests.get("http://localhost:5000/protocols/TestScript", auth=("", f"{api_key}"))
```

This allows you to programmatically integrate CAMELS in already existing measurement routines. You could for example use CAMELS to control some temperature with its PID controller while still using all the software/code you are already using in your lab.

## Deleting API Keys

You can delete **all** API keys by clicking the red `Delete ALL API keys` button in the settings window. You can not delete individual API keys.

```{attention}
You can not revert deleting the API keys! Any existing software relying on the API keys in the database file will break! You will have to create new API keys afterward and give them to the other software again.
```

It might make sense in some situations to periodically update the API keys to have a clearer understanding of who is using API keys.

