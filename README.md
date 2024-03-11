
```
 _  _   ___   __  __  ___  ___        ___  ___  __  __  ___  _     ___ 
| \| | / _ \ |  \/  |/   \|   \      / __|/   \|  \/  || __|| |   / __|
| .  || (_) || |\/| || - || |) |    | (__ | - || |\/| || _| | |__ \__ \
|_|\_| \___/ |_|  |_||_|_||___/      \___||_|_||_|  |_||___||____||___/
```
# NOMAD CAMELS
## Configurable Application for Measurements, Experiments and Laboratory Systems  

NOMAD CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS allows to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication. The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary instruments if necessary. Even large-scale distributed systems can be implemented. CAMELS generates FAIR-compliant data including rich metadata. NeXus standards, immediate NOMAD integration and hence a FAIRmat-compliant data pipeline can be readily implemented.


## Documentation

For more information and documentation visit [the documentation](https://fau-lap.github.io/NOMAD-CAMELS/).

# Changelog
## 1.0.3
Fixes:
- fixed bug that prevented set panels from starting

## 1.0.2
Features:
- Added functionality to select path for exporting hdf5 to csv/json

Fixes:
- You can now use new lines and special characters in the protocol description field.
- If exporting hdf5 to csv/json and not specifying the path for the export, the path of the hdf5 should now be selected correctly


## 1.0.1
Features:
- Now asking for the path, where to save measurement data when starting up CAMELS for the first time (or there is no preferences.json)
- Added "Quit" button to file menu

Changes:
- changed the default configuration files path for linux and mac; now the user is asked at the first startup where to put configuration files and can set the path in the settings
- improved usability of moving steps in sequence

## 1.0.0
Features:
- Fit values can now be displayed directly in the plot
- Refactor device instantiation to be handled in another thread to keep the UI responsive, this might cause some problems with instrument-specific manual controls that are not yet updated accordingly
- Added the plot point number to the definition already
- It is now possible to not configure instruments when starting a protocol, this feature has to be used with caution!
- Number of backuped preset files can now be curated. Possibilities are to keep all, only a certain number or "smart" way: all backups of the last 7 days, one for each of the last 30 days, one for each of the last 12 months and one for each year.
- Old databroker files may now be removed.
- Password protection may be enabled for changing settings or presets. May be useful if the responsible person does not want users to change anything, or for lab courses.
- There is now an extension feature, the first extension provides a compatibility with eLabFTW
- Can now save each run in its own file.
- Can now open the save file path when right-clicking on a protocol.
- Added a tool to export CAMELS hdf5 files to csv / json
- Can now run from command line using "nomad-camels"

Changes:
- the imports needed at a later time are now running in another thread after starting the main app to improve speed
- Changed displayed window titles to show "NOMAD CAMELS" last
- Changed displayed name to "NOMAD CAMELS" wherever found
- Removed checkbox whether to plot an xy-plot, it is now always plotted
- Added color to GUI buttons for better usability

Fixes:
- fixed export from databroker if the run failed such that no "stop" is in metadata
- plot widget now shows the table to change linestyle and markerstyle
- Refactor file paths for cross-platform compatibility in device_driver_builder.py
- Fix issue of stage control not updating set_channel when moving manually


## 0.2.3

Features:

- driver builder now not only for VISA, includes custom functions
- now allowing for non-string configs (e.g. other instruments)

Changes:

- changed order of channels to be above variables in context menu
- changed marker style to 'pixel' for 2D-plots
- changed driver information window, you can now toggle it on and off with the button in the instrument management

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
