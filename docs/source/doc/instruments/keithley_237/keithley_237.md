# Keithley 237 - Source Measure Unit (SMU)
## Setup
Basic instructions to add a Keithley 237 SMU to your NOMAD-CAMELS installation.
### Install
Install the instrument using the _Manage Instruments_ button of NOMAD-CAMELS. 

![img.png](k237_img.png)\
Find the instrument under the _Install Instrument_ tab. Then click _Install/Update Selected_ to install the instrument. This uses a pip install internally.

---
### Add Instrument to CAMELS
![img_1.png](k237_img_1.png)\
Then go to the _Configure Instrument_ tab and click the &#10133; icon to add a new Keithley 237 instrument.\
You can add as many of the same instrument type as you want by  clicking the &#10133; additional times if you want to use more than one of the same instruments. 

---
### Configure Instrument Settings
![img_2.png](k237_img_2.png)\
Here you can change the device settings like compliances, averages, integration time, etc.\
**Make sure you set the correct connection type (typically local VISA) and the correct resource name!**\
The communication settings (baud rate, terminators, etc.) can be changed as well and are device dependant.

## Usage
### Source Types
There are **four basic usage types** of the Keithley 237:

1. Source voltage, read current
2. Sweep voltage, read current and voltage ( reads the set value of the voltage, does not actually measure it)
3. Source current, read voltage
4. Sweep current, read voltage and current ( reads the set value of the current, does not actually measure it)

> &#9888; The source type of your Keithley 237 must be set in the device configuration window (see image above)

> &#9888; If `Source Type` in the config window is set to `Voltage` or `Current` then it is NOT possible to read the data created during a sweep in a measurement protocol using the `start_sweep` channel.\
> &#9888; If `Source Type` in the config window is set to `Sweep Voltage` or `Sweep Current` then it is NOT possible to read the data from an individual measurement using the channel `read_DC`.  
 
### Setting and Reading Individual Data Points
To set and read single data points (for example set one voltage and read the corresponding current value in a for-loop) set `Source Type` to `Voltage` or `Current`. When voltage is sourced current is read and when current is sourced then voltage is read.\
This is not very fast as the constant device communication has a lot of overhead. One can achieve at most about 10 measurements per second using this method.

#### Example Protocol
Here is an example protocol for setting and reading individual data points.
##### For-Loop
Settings of the for-loop: it will create 11 values between 0 and 1 including the 1.
![img.png](img.png)
##### Set Channel
Sets the `set_DC` channel to the value of the for-loop.\
&#9888; `set_DC` always sets the source type you selected in the configuration.
![img_1.png](img_1.png) 
##### Read Channel
Reads the `read_DC` channel.\
&#9888; `read_DC` always reads the compliance side of the source type. So it reads voltage when current is sourced and reads current when voltage is sourced.
![img_2.png](img_2.png)

##### Resulting Data
Example data from such a for-loop measurement. From the recorded instrument settings (`keithley_237_Source_Type` entry) it is clear what was measured.

```{image} img_3.png
```

(int_sweeps)=
### Using Internal Sweeps
There are five different types of internal sweeps:
1. Fixed Level (`setSweep_type = 0`)
2. Linear Stair (`setSweep_type = 1`)
3. Logarithmic Stair (`setSweep_type = 2`)
4. Linear Stair Pulsed (`setSweep_type = 3`)
5. Logarithmic Stair Pulsed (`setSweep_type = 4`)

For more details on the exact specifications of these internal sweeps check out the [official manual](https://download.tek.com/manual/236_900_01E.pdf) on pages 3-47 to 3-56.

The type of sweep measurement is set by writing a value (0 to 4) to the  `setSweep_type` channel (see list above).

Each type requires a different set of parameters from this list :\
`level`, `points`, `pulses`, `start`, `step`, `stop`, `t_off` and `t_on`.

#### Setting up the Sweep
##### Sweep Parameters
Before you start the sweep measurement you have to set the required parameters to the desired value in a _'Set Channels step'_. 

E.g. for a linear stair sweep from `start=0` to `stop=1` with `step size=0.1`. `Bias delay` and `range` are set in the instrument config page.\
&#9888; You **MUST set the sweep type** using the `keithley_237_setSweep_Type` channel:\
Here we want the linear sweep so we set the value to `1` as this corresponds to the linear sweep (see list of 5 sweep types [above](int_sweeps))\
![img_4.png](img_4.png)

##### Starting the Sweep

Then you can start the measurement by setting the value of `keithley_237_start_sweep` to `1`
![img_5.png](img_5.png)
and in a different step you have to start the sweep.

Reading the sweep data

To read the measured data simply read the `read_sweep` channel:
![img_6.png](img_6.png)

#### Example Sweep Data

This produces the following data for a voltage sweep using a 15 k&#8486; resistor.
```{image} img_7.png
```

The first column in the data is the set value (in this case the voltage) while the second column is the measured value (current) for that voltage.
The settings of the sweep can be read from the `protocol_overview` entry and the instrument settings.

