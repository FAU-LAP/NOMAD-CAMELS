# Creating API Keys

You need to authenticate yourself with an API ke so that the web server accepts most http requests. You can generate such a key in the settings window (`File -> Settings`) by clicking `Generate API Key`. Now make sure to copy and paste this key somewhere and save it.

```{attention}
You can not get back the API key if you do not save it now! Although you can always just create a new API key if you lose an existing one.
```

```{info}
You can have any number of API keys active at the same time.
```

The SHA-256 hashes of the API keys are saved to a database file located in the path you gave for *configuration files* (typically something like `%localappdata%`).

See [here](Deleting_API_Keys.md) for information on how to delete existing API keys.