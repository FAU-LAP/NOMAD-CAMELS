
```
 _  _   ___   __  __  ___  ___           ___  ___  __  __  ___  _     ___ 
| \| | / _ \ |  \/  |/   \|   \   ___   / __|/   \|  \/  || __|| |   / __|
| .  || (_) || |\/| || - || |) | |___| | (__ | - || |\/| || _| | |__ \__ \
|_|\_| \___/ |_|  |_||_|_||___/         \___||_|_||_|  |_||___||____||___/
```
# NOMAD-CAMELS
## Configurable Application for Measurements, Experiments and Laboratory-Systems  

NOMAD-CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS will allow to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication. The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary devices if necessary. Even large-scale, distributed systems can be implemented. CAMELS is well suited to generate FAIR-compliant output data. Nexus standards, immediate NOMAD integration and hence a FAIRmat compliant data pipeline can be readily implemented.


## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/).

# Changelog

## 0.2.4 (in Progress)

Features:

Changes:

Fixes:


## 0.2.3 (in Progress)
Features:
- driver builder now not only for VISA, includes custom functions

Changes:
- changed order of channels to be above variables in context menu
- changed marker style to 'pixel' for 2D-plots

Fixes:
- fixed error when changing the sweep channel in the ND sweep step 

## 0.2.2
Features:
- Reading/Saving of variables ad Read_Channels is now possible, appears as an array in the data
- added a class for a waiting bar during protocols
- added support for NOMAD's new app token feature

Fixes:
- unwanted printing of packages in instrument-management fixed
- plots of sweeps or subprotocols of subprotocols should now also be added to the main-plot list, enabling closing on closing of CAMELS or via button
- error of screen object already being deleted should be fixed
- databroker export to csv improved for non simple 2D data
- time weight of sub protocols now handled correctly
- use abs for y axis should now be possible (again)
- color settings for material theme are now remembered when opening the settings

## 0.2.1
Minor features:
- callable functions for manual move of stage control
- now showing readme and license of drivers

Quality of life:
- waiting cursor during reference drive of stage control
- names of steps now appear in protocol overview

Fixes:
- Fixed bug for showing non-number values / channels in list-plot
- fixed repeated firing of keyPress/ReleaseEvent in manual control of stage
- fixed all 3 axes being called when clicking "go-to" in stage control, even if not available
- fixed that Read_Channels steps could not be renamed

## 0.2.0
Major new feature:
- Callable functions of instruments, that are not channels

Minor features:
- Reference drive and stop of stage control are now callable functions

Quality of life:
- startup speed increased, but first run of protocol now slowed down
- added plot all available channels as possibility for List-Plot
- improved layout of set-panel

Fixes:
- Can now set log scale when using only one y-axis
- now using settings of log-scale from definition window at startup of plot

## 0.1.9
New features:
- Retry on error for VISA-devices
- Set_Panel added as a new manual control, this may be used to easily control channels that often have to be set to certain values in preparation of an experiment

Quality of life:
- waiting cursor when adding instrument and it takes some time

Fixes:
- Now the For-Loop (and children of it) display the "start - min - max - stop" preview correctly
- import of instruments should now work correctly when running protocol outside the UI
- int in instrument config is now saved as int
- pyvisa added to requirements to support local drivers

## 0.1.8
Fixes:
- finalize steps of instruments are now being called
- fixed issue with handing variables to subprotocol
- fixed update function for Windows, function for Unix/Mac not tested

## 0.1.7
Added functionalities:
- Added functionality to import protocols

Fixes:
- Fixed error message appearing when closing List-Plot
- Fixed login for central NOMAD
- fixed comment/uncomment of steps being saved correctly

## 0.1.6
Added functionalities:
- Added capabilities to interact with NOMAD (Oasis), uploading files, getting user information and using a NOMAD entry as sample
- Functionality to comment / uncomment steps in a protocol for testing / quickly changing a protocol

Fixes:
- CAMELS should not crash completely anymore when an instrument cannot be initialised
- Variables should mostly be refreshed for step configs without clicking around
- add_metadata removed from Custom_Function_Signal
- search in channels-tables not case sensitive anymore
- fixed that protocol without plots starts QApplication when run outside CAMELS

## 0.1.5
- Fixed the 'Update CAMELS' tool.\
- Renamed input and output to read and set in the 'Update CAMELS' tool.\
- Small fix to the VISA device builder.

## 0.1.4
- Added a timeout setting to all VISA instruments. Setting the timeout determines how long the instrument waits after sending a command before raising a timeout exception

## 0.1.3
- First stable and working release

## 0.1.0 to 0.1.2 
- &#9888; Broken releases due to minor bugs that were fixed in 0.1.3
