# VISA instrument-drivers

CAMELS provides a tool to create simple drivers for instruments that communicate via VISA (virtual instrument software architecture). 

You can use the driver builder to configure the core structure and basic features of your instrument. If you need more complex features you can then open the `*.py` and `*_ophyd.py` files to modify them.\
You could for example easily add a channel that sets a voltage and a current compliance config setting with the **Config Channel**. Then you could then add conditional voltage setting depending on the value of the current compliance string by hand in the files. 

The VISA-driver-builder tool (in the "Tools" menu in CAMELS) provides the following fields:

* **Name:** This will be the name of your instrument type, as it appears in CAMELS in the `Manage Instruments` window. We recommended to use only lower case for `Name`.
* **Ophyd-Class-Name:** The name of the instrument's ophyd class. Best-practice is to have it be different from "Name", it is recommended to use only lower case for "Name" and upper case for the first letter of the Ophyd-Class-Name.
* **Default Read-Termination:** The default value for the communication's read-terminator when configuring an instrument. Typical values are \r\n (CRLF) or \n (LF). 
* **Default Write-Termination:** The default value for the communication's write-terminator when configuring an instrument. Typical values are \r\n (CRLF) or \n (LF). 
* **Default Baud-Rate:** The default value for the communication's baud rate when configuring an instrument. Most commonly a value of 9600 is used. Other possible baud rates are 1200, 2400, 4800, 19200, 38400, 57600, and 115200.
* **Search-Tags:** Not of use (yet). In the future this should help you search for instruments with these tags in some way.
* **Channels** There are four basic channels you can add to an instrument. Read below for more information.

## Configuring Channels
The four types of channels vary only a little:
* **Read Channels:** These are used for values that can only be read from the instrument, e.g. a measured resistance. They can be used in measurements protocols by using a `Read Channels` step.
* **Set Channels:** These channels can set/output a value defined by the user, e.g. a voltage. These channels communicate with the instruments and write to the instrument. If no return parser is set the message is simply written and nothing is read from the instrument. They can be used in measurements protocols by using a `Set Channels` step.
* **Config Channels - Read Only:** These may be used for values that are read only once from the instrument at the beginning of the measurement, but do not change its current state, e.g. the instrument identifier, as response from the `*IDN?` command.\
```{note}
  Config Channels are always run **once** at the beginning of a measurement.
  ```

* **Config Channels:** These values are set at the beginning of a protocol and are configured in the instrument management (`Manage Instruments` window). These should be values, that are normally not changed, like the current and voltage compliance or whether the instrument is used as a voltage or current source for example.\
```{note}
  Config Channels are always run once at the beginning of a measurement. 
```

For configuring these channels, there are several fields:
* **Name:** This will be the name of the channel, as it is also displayed in CAMELS.
* **Query-String: (Only for Read Channels)** The string sent to the instrument for querying some value (Input only, examples: `*IDN?`, `VOLT?`).
* **Write-Format-String: (Only for Set Channels)** A string that formats the input value so that the instrument understands. The value is passed to the string with `{value}`, i.e. for example: `"VOLT {value}"` where "{value}" will be replaced with the input value. So in the end the string that the instrument receives would be for example `"VOLT 1"`.
* **Return-Parser:** A regular expression which parses the string returned from the instrument. The regex must contain a capture group, so parenthesis around the value you want to extract. The first capture group from the regex will become the value. The actual code executed looks like this `re.match(parse, val).group(1)`, where `parse` is the regex string and `val` is the initial string read from the instrument.\
If this is `None`, for a set-channel, the instrument will only be written to, if it is not `None` a query is performed.

* **Return-Type:** The type to which the returned value from the "Return-Parser" should be converted. Supported are `str`, `float`, `int` and `bool`.
* **Unit:** The physical unit of the channel's measurement / output.
* **Description:** A description for the channel, making it clear in the metadata and for the user, what this channel does.
* **Input-Type:** This determines the input for a config-channel in the config window. Supporter are `str`, `float` (or any number-type) and `bool`.


The driver-files that are created from the input here, can be further modified. Especially for "Query-String", "Write-Format-String" and "Return-Parser", one may also define functions that provide a necessary functionality.

## Modifying the driver-files
The builder creates two file, `<instrument_name>.py` and `<instrument_name>_ophyd.py`.  
In the `<instrument_name>.py` file, further modifications regarding the GUI may be done. If keeping the `Simple_Config` class for the `subclass_config`, one might add comboboxes for config-channels that only take some specific values.  
In the `<instrument_name>_ophyd.py` file further functions may be added for more complicated instruments.
