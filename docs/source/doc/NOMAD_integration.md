# NOMAD Integration

NOMAD CAMELS provides direct integration with [NOMAD](nomad-lab.eu).

## Logging In
To log in to NOMAD with CAMELS:
Select _NOMAD user_ instead of _local user_. A window will open, that asks you for credentials:
- You can select either the [central NOMAD](https://nomad-lab.eu/prod/v1/) server or a [NOMAD Oasis](https://nomad-lab.eu/nomad-lab/nomad-oasis.html).
- For an Oasis, you need to provide the URL of the oasis. For example the FAIRmat example Oasis `https://nomad-lab.eu/prod/v1/oasis/api/v1`. Just copying the link from your browser should work.
- The login is done via NOMAD's App token. The button in the login-window directs you to NOMAD's (or your Oasis') site where you can copy the token.

```{note}
If the login to the Oasis does not work, you might need to adjust the URL. Although we tried to catch all cases, it may help if the URL ends with `api/v1`.
```

```{hint}
For security reasons, CAMELS does not store your token in a file. When you close CAMELS or log out, your token is deleted from memory and you will need to log in again.
```

## Connecting the Sample to NOMAD
When you are logged in, instead of entering the sample infos, you can also select a sample from any ELN entry in NOMAD.

Check the box `use NOMAD sample` and click on `select NOMAD sample`. A dialog that asks you to select an entry opens. Several sorting options for the entries exist:
- *Entry Scope* is either _user_ or _shared_, this means whether only your uploads / entries are shown, or also those that are shared with you by other users.
- *Upload* is the upload in NOMAD.
- *Entry Type* is for example BasicEln. The entries are filtered by the entry type.
All these settings filter from top to bottom, i.e. only those entry types are shown, that exist in the specified upload.

On the right side of the window, a preview of the contents of the selected entry is given.

After clicking `OK`, the button `select NOMAD sample` will instead display the name of the selected sample. Clicking it again lets you change the sample.

## Connecting Instruments with NOMAD
In the _Manage Instruments_ view, each of the instruments has a field `ID`. Next to it is a button, that lets you select an entry of NOMAD, similar to the [sample selection](#connecting-the-sample-to-nomad). The metadata of the instrument will the contain the information of the NOMAD entry. The `ID` itself is used for the connection between the data files and the instrument in NOMAD's ELN (see [below](#camels-data-in-the-nomad-eln)).

## Automatic Data Upload
Once you are logged in, a new box appears on the top right of CAMELS' main window for how to handle uploading a measurement to NOMAD. If you select "ask after run", a window appears when a protocol is finished, where you can select the Upload where the files should be uploaded to. If you select "auot upload", a second box where you can select the Upload and the data will be uploaded there once the protocol is finished.


## CAMELS Data in the NOMAD ELN
In NOMAD, you can use the "CAMELS App", to easily search and filter your data that you produced with CAMELS. See the [Example Oasis](https://nomad-lab.eu/prod/v1/oasis/gui/search/myapp) for a look at the CAMELS App.

You can filter your data by sample, time and many other things.

Additionally to the search capabilities, the entry in NOMAD that belongs to the data of a CAMELS file is derictly connected to the instruments and sample, as well as the user.

