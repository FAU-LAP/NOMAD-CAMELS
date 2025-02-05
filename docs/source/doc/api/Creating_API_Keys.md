# Creating API Keys

The CAMELS API uses the HTTP "Bearer" token authentication. You need to authenticate yourself with an API key (bearer token) so that the web server accepts most http requests.

You can generate such an API key in the settings window (`File -> Settings`) by clicking `Generate API Key`. Now make sure to copy and paste this key somewhere and save it. You could either save it in a text file or in something more secure like a password manager.

```{warning}
You can not get back the API key if you do not save it now! Although you can always just create a new API key if you lose an existing one.
```

```{note}
You can have any number of API keys active at the same time.
```

The HTTP "Bearer" authentication does NOT allow you to simply open up a browser window with the url. You will either need to use the `//localhost:<port>/docs` overview or a script based request to the HTTP server including the bearer token/API key.

The SHA-256 hashes of the API keys are saved to a database file located in the path you gave for *configuration files* (typically something like `%localappdata%`).

See [here](Deleting_API_Keys.md) for information on how to delete existing API keys.

