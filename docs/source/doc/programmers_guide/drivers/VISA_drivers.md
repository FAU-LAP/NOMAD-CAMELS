# VISA instrument-drivers

Just as for EPICS-drivers, CAMELS provides a tool to create simple drivers for instruments that communicate via VISA (virtual instrument software architecture).  
The VISA-driver-builder tool (you can open it from the "Tools" menu in CAMELS) provides the following fields:
* **Name:** This will be the name of your instrument type, as it appears in CAMELS
* **Ophyd-Class-Name:** The name of the instrument's ophyd class. It should best be different than "Name", it is recommended to use only lower case for "Name" and upper case for the first letter of the Ophyd-Class-Name.
* **Default Read-Termination:** The default value for the communication's read-terminator when configuring an instrument.
* **Default Write-Termination:** The default value for the communication's write-terminator when configuring an instrument.
* **Default Baud-Rate:** The default value for the communication's baud rate when configuring an instrument.
* **Search-Tags:** Not of use (yet).
* **Channels** (see below)

## Configuring Channels
The four types of channels vary only a little:
* **Input Channels:** These are used for values that can only be read from the instrument, e.g. a measured resistance.
* **Output Channels:** These channels can output a value defined by the user, e.g. a voltage.
* **Config Channels - Input Only:** These may be used for values that are read from the instrument, but do not change, e.g. the identity, as response from the `*IDN?` command.
* **Config Channels:** These values are set at the beginning of a protocol and are configured in the instrument management. These should be values, that are normally not changed, like whether the instrument is used as a voltage or current source for example.

For configuring these channels, there are several fields:
* **Name:** This will be the name of the channel, as it is also displayed in CAMELS.
* **Query-String:** The string sent to the instrument for querying some value (Input only, examples: `*IDN?`, `VOLT?`).
* **Write-Format-String:** A string that formats the input value so that the instrument understands. The value is given as `{value}`, i.e. for example: `"VOLT {value}"` where "{value}" will be replaced with the input value.
* **Return-Parser:** A regular expression which parses the string returned from the instrument. The first result from the regex will become the value. If this is `None`, for a write-channel, the instrument will only be written to, otherwise a query is performed.
* **Return-Type:** The type to which the returned value from the "Return-Parser" should be converted. Supported are `str`, `float`, `int` and `bool`.
* **Unit:** The physical unit of the channel's measurement / output.
* **Description:** A description for the channel, making it clear in the metadata and for the user, what this channel does.
* **Input-Type:** This determines the input for a config-channel in the config window. Supporter are `str`, `float` (or any number-type) and `bool`.


The driver-files that are created from the input here, can be further modified. Especially for "Query-String", "Write-Format-String" and "Return-Parser", one may also define functions that provide a necessary functionality.

## Modifying the driver-files
The builder creates two file, `<instrument_name>.py` and `<instrument_name>_ophyd.py`.  
In the `<instrument_name>.py` file, further modifications regarding the GUI may be done. If keeping the `Simple_Config` class for the `subclass_config`, one might add comboboxes for config-channels that only take some specific values.  
In the `<instrument_name>_ophyd.py` file further functions may be added for more complicated instruments.
