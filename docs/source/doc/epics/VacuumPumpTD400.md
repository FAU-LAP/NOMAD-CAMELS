# How the IOC for the Vacuum Pump TurboDrive 400 works

For the following documentation, each PV name has a prefix, currently set to be `tvsl80:`. For conciseness, this prefix
is ommited.

## Read Parameters

To read out parameters, the following PV names are available:

1. `g1pres`
    * read the pressure of gauge 1 in milliBar
2. `g2pres`
    * read the pressure of gauge 2 in milliBar
3. `freq`
    * read pump frequency in Hertz
4. `current`
    * read actual input current in Ampere
5. `power`
    * read actual input power in Watt
6. `bearingTemp`
    * read actual bearing temperature in °C
7. `motorTemp`
    * read actual motor temperature in °C

They return a value in their respective Unit
<br>

To read out settings, the following PV names are available (and should be self-explanatory):

0. `getPumpStatus`
1. `getStandbyStatus`
2. `getFanStatus`
3. `getPurgeStatus`
4. `getVentStatus`
5. `getFVPStatus`

The return value is either `Off`, representing a `0`, or `On`, representing a `1`.

## Set Parameters

The settings listed just above can be set. To do this, the PV `toggleParameters` has to be used. It works by writing the
number of the setting that has to be toggled on/off into it. So to for example toggle the pump, `toggleParameters` has
to be set to `0`, so for example via `caput tvsl80:toggleParameters 0`.
<br>
It is not possible to just toggle on. With the same `caput tvsl80:toggleParameters 0`, a running pump will shut off and
a standing pump will turn on.
So, before wanting to turn on the pump, first check the pump status via for example `caget tvsl80:getPumpStatus` and
then only send the command if the pump actually was off.
<br>
Be aware that setting a parameter takes around one second for the pump to process.

## Extra records
The records `LOGIN` and `CHANGE` are used by `toggleParameters` and should not be used on their own.
<br>
The record `REFRESH` checks for changes to the settings every second, for example if they got changed via the Web Interface.

