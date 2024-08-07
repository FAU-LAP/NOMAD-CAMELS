
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


## Publication

Please also see our publication in the Journal of Open Source Software (JOSS):

[![DOI](https://joss.theoj.org/papers/10.21105/joss.06371/status.svg)](https://doi.org/10.21105/joss.06371)

# Changelog


## 1.3.0

Major Features:

- Added an API web server. The homepage `http:\\localhost:<PORT>` gives you an overview of the available API calls and how to use them. You need to create an API key in the settings to be able to use most of the API calls. You can get a list of the available protocols you can execute with `GET /protocols` and run a specific protocol by using `POST /protocols/{protocol_name}` For more information check the documentation.
- Added a Watchdog feature to monitor certain values and execute operations when their condition is met.

Features:
- The `Execute Python Files` step passes the current value of variables passed to the script if no value is entered in the `value` field.
- "Shared" scope now possible in NOMAD sample selection
- Added more metadata to instruments in the data

Changes:
- Variable signal is now saved as group instead of dataset
- Can now read variables also without channels
- moved databroker catalog loading to import thread, should speed up starting

Fixes:
- Can now save variables with non-scalar size
- x-y plot now working with array-data again
- Multiple occurances of same protocol in tab-dictionary in save-json removed
- Pause would trigger unsubscribe of run-router for live data saving, now moved so it does not happen
- List-plot now shows again on new data
- Fixed a bug that would not allow extension-users to show up in data
- Fixed bug where a custom function signal that does not use force-sequential would not work
- Fixed bug that prevented fits from being displayed if the fit had many variables
- Number of databroker files setting never did anything, now it does
- Would upload wrong file to NOMAD if always new file

## 1.2.2
Features:
- Included the protocol's json used by the configuration in CAMELS into the data file
- Added functionality to replace loopsteps (instead of delete + add a new one)
- Included exception handling for manual control threads and allow for restarting them on error
- Added a progress bar functionality for the wait-step
- Added conditional waiting to the wait-step
- More info on python file step in protocol overview

Fixes:
- Cannot move protocols or manual controls to empty tab containing the "+" button anymore
- If instrument instantiation fails, only the actual error should now be raised
- Improved thread stability of stage control
- plots that were once closed now behave correctly, not throwing an error on closing again and can be closed by the close plots button
- Read Channels with the same channels but different state of reading variables now work
- Search bar of menu of editable boxes now appears at the top instead of bottom
- cannot display empty menus for insert-variables anymore --> search does not break menu anymore

## 1.2.1
Features:
- added NOMAD metadata to NOMAD samples

Fixes:
- For loop for which no distance was ever defined was broken, now fixed
- Fixed bug that prevented the app from starting when no tabs were used before
- Fixed issue with dots in paths

## 1.2.0

Features:
- Data can now be exported to hdf5 during the measurement. This should remove long waiting times after running protocols with lots of data.
- Added a filter functionality to the right-click menu when setting channels or variables. This filters all available channels, variables or functions by the string that is entered.
- Added the `Execute Python File` loop step. This allows the user to specify a Python file and a Python environment to run the file with. The environment can either be the same as the one running CAMELS (default), a different already existing one, or is created dynamically by giving it the required packages and versions. The Python file can return (realized by printing) a dictionary with key value pairs. To read these, give the name of the key in the `Values returned by the Python file` list.
- Added a tab that allows you to add new tabs simply by clicking it.
- Point Distance can now be used for For-loops.

Changes:
- Running a protocol with a subprotocol also builds the subprotocol now. This makes it easier to change sub-protocols for more complex measurement routines.
- start-min-max-stop sweeps in a for loop now behave differently, the number of points is now the total number of points, not the number between min and max

Fixes:
- Description fields now change their size dynamically.
- Filtering the channels by name does not break if no matches were found.
- Filtering Set Channels now does not reset the value if the channel does not match the query.
- Fixed the hide/show information when installing instruments


## 1.1.2

Fixes:

- Removed empty fit parameters, which would cause an error before
- Fixed requirement of pyepics, version 3.5.3 seems broken on windows, going back to version 3.5.2

## 1.1.1
Features:
- parsing now understands physical constants with `const.<constant_name>` by using `scipy.constants` as `const`

Changes:
- Now displaying errors together with fit values

Fixes:
- Too little characters were allowed in plot labels, now most characters are allowed again
- Failed fits do not throw an error that crashes the protocol anymore
- Title and icon of plot windows

## 1.1.0
Features:
- Protocols and manual controls are now sortable into tabs!
- Protocols can now be run in a queue
- added possibility to force sequential on/off for single channels
- Plots are now done with pyqtgraph, improving interactivity and performance

Fixes:
- Plots being placed somewhere should now not kill the program anymore


## 1.0.6
Features:
- Added an "owner" field to the samples, it is automatically populated when a new sample is created. This should stop cluttering the samples for all users. Only the current user's samples will show in the comboBox, or those without owner.
- Added possibility to use instruments that generate their channels at runtime. 
- Added SequentialDevice that forces every call to the instrument to wait for the previous one to finish.
- Added the `*.py` and `*_ophyd.py` file contents as metadata to each instrument in the final measurement file. 

Fixes:
- "Hide info" button in instrument installer now working

## 1.0.5
Changes:
- Driver versions now have a separate branch on CAMELS_drivers to improve keeping them up to date
- Same for extensions
- Now checking filenames of protocols for invalid characters
- Improved speed of looking for updates

Fixes:
- Fixed checking for currently used version
- Extensions can now actually be downloaded

## 1.0.4
Fixes:
- NOMAD upload now uses the correct file if new file for every run
- Dependency updated to python>=3.11.3

## 1.0.3
Changes:
- Removed "environment" from saved hdf5 files, moved instrument information up on step in hirarchy
- changed file extension to .nxs for better NOMAD integration

Fixes:
- fixed bug that prevented set panels from starting
- fixed issue with uploads to NOMAD if an unnamed upload exists
- fixed trigger for Custom_Function_SignalRO
- fixed parameters for custom function in fits

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
