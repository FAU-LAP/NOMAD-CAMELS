# Call API - Protocol Step

This step allows you to call any API that is hosted on a server. It uses HTTP requests so you can communicate with any API that answers to something like

```bash
<host>:<port>/path/to/api
```

## Passing and Using Variables

You can pass all variables used in the protocol to the body of the HTTP requests.

The returned data (a dictionary) is converted to variables where the key name of the dictionary becomes the variable name prefixed by the *API Call* step name. You can use these variables in the following protocol steps.

> [!WARNING]
> As CAMELS can not know what variables it will be getting, it will display all uses of the new variables in red. You can simply ignore this visual warning.

## API Options

You can chose between two general API types to communicate with:

1. `CAMELS`
2. `Generic`

### API Type - CAMELS

This step is used to execute the functions offered by the CAMELS API.

#### Available Functions

If you select this API type you will get a drop down menu of all available API requests offered by the CAMELS API. This list is created dynamically every time you click the drop down menu. For this to work you must enter a working `host` and `port` address of a running CAMELS API instance.

#### Parameters

Some CAMELS API requests require the user to enter parameters such as the protocol name you want to run or the index of the queue item you want to remove. For each function selection you can enter values for these parameters.

For `POST` requests you can pass a message body. This is done to modify the variables of protocols.

### API Type - Generic

This options allows you to address any API that accepts HTTP requests to a specific URL.



For `POST`, `PUT` and `PATCH` requests you can pass a message body. This is done to modify the variables of protocols.
