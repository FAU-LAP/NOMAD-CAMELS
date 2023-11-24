In this tutorial we want to guide you through the process of creating a new driver for an instrument you have in your lab.

The instrument we want to implement is a _Keithley Series 2400 SourceMeter_.
The instrument is connected to our computer via serial connection (RS232, GPIB, ...).

# 1. Create the Core Structure
To create the core structure use the _driver builder_. Open `CAMELS` and navigate to `Tools > Driver builder`.

![img_1.png](img_1.png)

# 2. Name Instrument
1. Fill out the `Name` field to name the instrument.\
   The name should be all lower-case and should make clear what instrument this driver is for. The name should start with an alphabetical letter [a-z], as the name entered here will become a Python variable.\
   In our case we will use `keithley_2400_smu`.
2. The `Ophyd-Class-Name` should be the same as `Name` but with the first letter in uppercase. This is best-practice, in general you can use any class name you want.\
   So here we choose `Keithley_2400_smu`.
   In later versions the ophyd-class-name is given automatically.

# 3. Select VISA Connection
Now you must choose if the instrument uses a serial connection like GPIB, RS232, ... and can be communicated with via the VISA protocol.\
Check or uncheck the `VISA connection` box accordingly. 

As our Keithley instrument is connected using a GPIB-USB adapter we check the `VISA connection` box.

The driver builder sohuld now look like this

![img_2.png](img_2.png)

# 4. Set Serial Connection Parameters (OPTIONAL)
If you use a instrument with serial communication you should now set the terminators and the baud rate. Make sure this matches the instrument setting of the physical hardware device. 

Our instrument uses the default settings, so we can just leave this. You can always change these values later on in the instrument manager when actually adding the instrument. 
# 5. Adding Channels
The core part of the drivers are the channels you define for each instrument. Each channel corresponds to one action or value (this can be a single value or something more complex like an n-dimensional array) you want to set or read.

Think of the actions you want to perform with your instrument and then add a channel for each. 

We want to add the functionality to read and set voltages, as well as currents.
We also want to be able to configure some instrument settings such as the compliance (maximum allowed output) and the ranges for voltage and current.

We will start with the reading and setting of voltages and currents. 

# 5.1 Reading and Setting - VISA
As we want to actually communicate with the instrument when setting and reading it, we add these as
- `Read Channels - VISA`: reading the voltage/current values measured by the instrument 
- `Set Channels - VISA`: sets voltage/current on the instrument.

```{important}
`VISA` channels **always** send a string to the instrument. If you do not want to send a string every time the channel is set or read, use the custom Channel on the left! There you can customize exactly waht is done when the channel is read and set.
```

# 5.2 Reading Channels - VISA
We now add two `Read Channels - VISA` by clicking the &#10133;Symbol.
The Keithley 2400 only as a `READ?` command which reads voltage or current depending on the measurement type selected by the command `:CONF:<VOLT/CURR>` so we can not send a genereic read command to the instrument. Therefore, we leave the `Query-string`field empty. We will add the functionality to actually read values from the instrument after the driver has been built by adding a few lines of Python code to the driver.

As we know how the read data looks like we can add a return parser that takes the answer from the instrument and uses regex matching to extract the exact value we are looking for. The regular expression we use to parse the response:

```regexp
Voltage:
^([+-].*),[+-].*,[+-].*,[+-].*,[+-].*$
Current:
^[+-].*,([+-].*),[+-].*,[+-].*,[+-].*$
```
the braces are the actual value that is taken. (1. match group of the expression)

We want the voltage and current to be read in as a float, so we select `float`in the `Return-Type` field.

For a detailed description of the possible fields see  [here](../../programmers_guide/drivers/writing_drivers.md#channel-fields).

As unit we set `V` and `A` respectively. 

You can add a `Description` if you like. This will make it easier for people to understand what this channel does and how to use it in a measurement protocol. Descriptions appear when overing over a channel in the measurement protocol. 

Your instrument should look something like this now.
![img_3.png](img_3.png)

# 5.3 Set Channels - VISA
We now add two `Set Channels - VISA` by clicking the &#10133;Symbol. 

The Keithley 2400 can only set voltages/currents if the source function is set to voltage/current. This means we can not send a generic command to simply set the voltage/current of the output but we have to check if it in the right source mode first. Therefore, we do not add any `Write-Format-String` but we will add the functionality later on in the Python code of the driver.

We add units and descriptions. You should have something like this now
![img_4.png](img_4.png)

# 5.4 Instrument Settings
Now we want to add channels that will define the instrument settings, so things that typically do not change for an instrument during a single measurement. These channels are execuFor the Keithley 2400 this is:
- Voltage/current compliance
- Voltage/current range

These