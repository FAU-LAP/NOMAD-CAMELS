<img src="https://fau-lap.github.io/NOMAD-CAMELS/_images/camels-horizontal.svg" alt="NOMAD CAMELS" width="300"/>

## Configurable Application for Measurements, Experiments and Laboratory Systems  

NOMAD CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS allows to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication. The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary instruments if necessary. Even large-scale distributed systems can be implemented. CAMELS generates FAIR-compliant data including rich metadata. NeXus standards, immediate NOMAD integration and hence a FAIRmat-compliant data pipeline can be readily implemented.


## Documentation

For more information and documentation visit [the documentation](https://fau-lap.github.io/NOMAD-CAMELS/).


## Publication

Please also see our publication in the Journal of Open Source Software (JOSS):

[![DOI](https://joss.theoj.org/papers/10.21105/joss.06371/status.svg)](https://doi.org/10.21105/joss.06371)

# Changelog

### 1.8.2
UI-Improvements:
- Notification when log in to NOMAD was (not) successful
- Added a maximum height and scrollbar for description of protocol steps
- Added more tooltips in the UI
- modernized tooltip style
- increased startup size of instrument management, to decrease number of resize-events
- driver-builder now pre-creates the finalize-steps method
- table with channels can now be sorted
- read channels of gradient-descent step now same table type as for all other steps

Fixes:
- instrument do not change anymore when "cancel" clicked in manage instruments
- if default file association for .py is running python, protocols are not run anymore right away when opening externally, but instead revealed in os-file explorer
- sometimes breaking for-loops or sweeps when point distance could not be calculated after copying or reloading should be fixed
- ignore failed readings in simple sweep now actually doing something

### 1.8.1 Fixed broken Plots in Loops

UI-Improvements:
- Tabs now have an "x" button to close them (right-click still works)

Fixed:
- Fixed plots in subprotocols not updating when called from loops (`For Loop`, `Simple Sweep`).
- Error message now only appears once when trying to plot and fit something that is not being read
- When adding a new protocol, the view does not jump back to the first tab anymore
- Fixed broken export to csv files and prevent overwriting of existing csv files.
- Deleting tabs now works again


## 1.8.0 Parallel Async Reading and New Plot Backend

Features:
- can now asynchronously read channels during a running protocol

Changes:
- Plots now use a different backend. Should make the run engine faster and more stable. Plots now run in their own threads and should not interefere as much with the main protocol execution.
- Now saves data files with an `.h5` file extension if no NeXus output was enabled. Only uses `.nxs` file extension if NeXus output is saved to the file. Should clarify that the standard CAMELS data files do **NOT** follow rigid NeXus standards.
- Subprotocols always create a new data stream and entry in the data file

Fixed:
- You can now run the same subprotocol multiple times. Each subprotocol execution creates it own data stream. This means the datafile has separate entires for each subprotocol run
- When dragging / dropping a step in the protocol sequence, the moved step is now selected afterwards
- Cannot drop a step in a simple sweep anymore
- Manual controls could not work with channels that need to call trigger, now fixed
- Made aborting a protocol more stable
- Generic set and read manual control now closes its thread more stably
- Fixed expression evaluation for subprotocols
- Protocol and device description field is now max 130px high. After that it becomes scrollable.

### 1.7.2

Features:
- Can now break loops in the if-step
- Can now play a sound effect (select checkbox in settings) when protocol is doen

UI:
- Simple_Config of instruments now supports tool tips for config channels
- Layout of Simple_Config now scrollable and can support more / less columns
- Stage control manual control with ctrl + arrow keys now also if some part of the control is selected

Fixed:
- Changing plot color now does not always affect the first item anymore
- Setting a number of plot points in the definition window now works again
- Progress bar in wait sometimes crashed, now fixed
- Updated custom function signal to better support list / tuple ... setting-types by handling kwargs from bluesky
- Made plotting much more robust. You can now define multiple plots and read at multiple points in your protocol. The plots are only updated if data concerning the y-axis of your plot is actually read.
- Updating instrument never worked, only installing, now fixed
- Update all instruments now skips local drivers
- Users and samples are now saved in a more robust way

### 1.7.1

Fixed:
- Automatic upload to NOMAD fixed when also exporting to CSV

## 1.7.0 Browser plots and improved install

Features:
- Can now show plots in the browser
- Support of Python 3.9 is back!
- Live comments now come with timestamps

Changes:
- Cleaned up the protocol builder to only import modules when necessary
- When selecting an upload for automatic upload to NOMAD, the *Uploads* drop-down list is now automatically updated.
- Added warning and option to install flask, dash and plotly when selecting "Show plot in browser"
- Installation and dependency management now via poetry to keep dependencies clean

Fixed:
- Fits now have at least the number of data points in the plot view
- Could insert variables at channel names in set channels and similar, now only possible for the value
- Improved exception handling for instrument (un-)install



## 1.6.0 Ignore failed read, new manual control

Features:
- Can ignore failed readings of specific channels now, so the protocol does not break if some sensor fails once
- New manual control to generically set / read any kind of channel
- Can now manually adjust size and position of plots in protocol configuration

Changes:
- Order of steps in menu now alphabetically
- Default value of read variables in "Read Channels" now True
- In the Set Value Popup, now a messagebox asks, whether the user is sure if they click on "cancel"

Fixed:
- Changelog is now actually shown
- Waiting bars could crash if executed in a fast loop, now fixed

### 1.5.3 Less Confusion!

Changes:
- No more confusion when opening a protocol configuration, cannot open the same twice anymore, but raises the already opened window to the front

Fixed:
- ElapsedTime for List and 2D plots fixed
- Not necessary to read channels when waiting for condition anymore (condition might be due to variable for example)
- Driver builder does not create read-functions for set-channels anymore
- List-plot can now display other types than numbers and bool again
- Throwing an error when trying to execute python file without specifying a file
- Variables in protocols run by a watchdog should now work
- Replace with menu now looks as the others, cannot replace step with same type anymore

### 1.5.2 The team of NOMAD CAMELS wishes you a measuring christmas and bug-free new year!

Features:
- Now showing the changelog after an update

Changes:
- The log-window now has a maximum number of lines (default for the moment at 10000)
- Menu of steps renamed from "Additional" to "Advanced"

Fixed:
- Manage instruments could not be opened without internet connection, now fixed
- Instruments that depend on others sometimes were closed in the wrong order, should now be fixed (example: first de-instantiate the PID, then its read / set channels)
- Fixed a bug where in some Qt versions the window could not be loaded anymore by changing requirement of PySide6, fixed warning that happened in versions where it worked
- Wrong movement of stage manual control when using buttons after keyboard move fixed
- Read only config data (e.g. IDN for some instruments) were not read if they had a default value, now fixed

### 1.5.1

Features:
- Can now live-control the variables of a protocol while it is running
- Can now skip some datapoints in plotting, useful for long measurements to free up some memory or improve speed

Changes:
- Added a button to the API settings that redirects you to the API documentation
- Session now also creates a sub-folder

Fixed:
- Opening the data path opened several windows in some cases, now fixed
- Samples can now be deleted again
- "Channels" or "Variables" do not appear in set value popup anymore if None of these are set
- Tree of protocol sequence not scrolling back to the top anymore on every click
- The button for adding a step now displays the same menu as a right click in the sequence
- Folder with python files might have been missing on first start, now fixed

## 1.5.0 metadata structuring

Features:
There is a new data output structure, making it clearer to understand, mostly consistent with old versions.
The data / metadata are not saved in a rigid NeXus shape anymore. However, it is possible (turned on by default) to add the NX structure as an additional entry in the hdf5. If doing this, the data is not duplicated, everything is done by soft-links in the hdf5.

Fixed:
- Can now paste again with ctrl+v in most outer part of protocol
- Fixed throwing errors when entering bad values in variable-boxes
- Removed additional appearance of plot_data in metadata

---

### 1.4.3

Features:
- Can now make a protocol stop on an if condition

Changes in UI:
- Steps now grouped in menu
- Renamed plots button

Fixed:
- Removed bad version numbers from metadata
- Fixed an issue with the databroker catalog not being set
- Channel-metadata is now consistent over several measurements (metadata was lost because of mutable datatype)
- Plots from sub-steps are now in the data
- Databroker should now load correclty again
- Added export of bytes into json
- Not always focusing the new box in tables anymore

### 1.4.2

Changes:
- Improved the NOMAD identifier for samples, user and instruments

Fixed:
- Fixed error from empty 2D plot
- Fixed several issues with how the NOMAD Oasis URL is handled
- Fixed session name not being used in data file

### 1.4.1 2D plot features

Features:
- Clear plot now possible for 2D plots
- 2D plot now has maximum number of data points
- 
Fixed:
- Fixed compatibility of 2D plot with newer numpy versions (np.ptp(x) instead of x.ptp())

## 1.4.0 API improvements, clean protocol exit, more metadata

Features:
- Added a **new** protocol step called `API Call`. This step allows you the user to call other APIs via HTTP requests. There is native support for CAMELS API calls. Results returned by the API calls can then be used in the following steps.
- CAMELS API server now accessible from network. (Changed host setting to `0.0.0.0`)
- CAMELS API now lets you get a JSON string containing the protocol and all its settings
- CAMELS API now lets you get a JSON string containing the current CAMELS settings.
- A protocol to execute at the end of a protocol, no matter wether it finishes correctly or breaks can now be added
- Instruments can now get metadata from ELNs

Changes:
- Renamed `comment / uncomment` to `enable / disable` for protocol steps to make it more clear
- Data passing from the Execute Python Script step was changed. Now should be more stable, as it looks for the Data between the `###Start Data` und `###End Data` strings. See our [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/protocol_steps/step_Execute_Python_File.html#returning-results) for more details.
- Refactored the way metadata is saved in instruments

Fixed:
- Fixed a bug where a protocol would show multiple times
- Installed version should now be found correctly when searching for updates
- Removing / moving of buttons in tabs fixed
- Requirement updated to camels suitcase 0.2.2, fixing datasets in instruments
- Some raised exceptions now provide additional traceback
- Errors raised by plots now only raised once, not for each datapoint
- Number of datapoints set in plot definition now correctly taken over to plot
- Fixed a bug that would stop users from logging in to the central NOMAD
- Logging used a bad file handler that would stop logs, now corrected

---

### 1.3.1

Features:
- API: Now adds a UUID to all protocol executions performed via API. Allows you to track and retrieve the results of each protocol run.
- Set Value Popup step now allows to define comboboxes
- Can allow prompt step to abort protocol now

Changes:
- Resetting positions for plots at each run, hoping to keep plots visible for remote-sessions
- Allowed for stopping a protocol during instrument instantiation

Fixed:
- Removed unnecessary import in protocols
- Having quotation marks in a prompt or a step description could break the protocol, now fixed
- Fixed tabs on first startup of CAMELS
- Fixed naming of empty tabs
- Packages that could not be loaded might have hindered opening the instrument manager, now fixed
- Making new preset now actually loads said one and does not overwrite the old one
- API: Fixed changing variables of protocols already added to the queue
- API: You can now use negative index in the API calls
- Evaluator does not break on non-string inputs, but simply returns them
- Fixed different read-channel steps when using a subprotocol
- Fixed subprotocol evaluator not updating
- Fixed usage of quotation marks for advanced instrument config step
- When switching the preset, the tabs now load correctly
- Tab order is now remembered
- Log plots might not show correctly, now they have a minimum size
- Quotation mark problems with protocol overview fixed
- Links now open correctly on unix and mac
- Ctrl+v now works in container-steps
- Should now correctly handle /gui urls for NOMAD oasis
- ElapsedTime now displays correctly in plots
- Adding while-loop counter earlier to namespace so it can be part of the while condition
- Fixed a bug where a short queued protocol would be run endlessly
- When the most recent preset was no viable json, it might break camels, now the second newest will be loaded instead of breaking

## 1.3.0 API and Watchdogs

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

Fixed:
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

---

### 1.2.2

Features:
- Included the protocol's json used by the configuration in CAMELS into the data file
- Added functionality to replace loopsteps (instead of delete + add a new one)
- Included exception handling for manual control threads and allow for restarting them on error
- Added a progress bar functionality for the wait-step
- Added conditional waiting to the wait-step
- More info on python file step in protocol overview

Fixed:
- Cannot move protocols or manual controls to empty tab containing the "+" button anymore
- If instrument instantiation fails, only the actual error should now be raised
- Improved thread stability of stage control
- Plots that were once closed now behave correctly, not throwing an error on closing again and can be closed by the close plots button
- Read Channels with the same channels but different state of reading variables now work
- Search bar of menu of editable boxes now appears at the top instead of bottom
- Cannot display empty menus for insert-variables anymore --> search does not break menu anymore

### 1.2.1

Features:
- Added NOMAD metadata to NOMAD samples

Fixed:
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
- Start-min-max-stop sweeps in a for loop now behave differently, the number of points is now the total number of points, not the number between min and max

Fixed:
- Description fields now change their size dynamically.
- Filtering the channels by name does not break if no matches were found.
- Filtering Set Channels now does not reset the value if the channel does not match the query.
- Fixed the hide/show information when installing instruments

---

### 1.1.2

Fixed:

- Removed empty fit parameters, which would cause an error before
- Fixed requirement of pyepics, version 3.5.3 seems broken on windows, going back to version 3.5.2

### 1.1.1

Features:
- parsing now understands physical constants with `const.<constant_name>` by using `scipy.constants` as `const`

Changes:
- Now displaying errors together with fit values

Fixed:
- Too little characters were allowed in plot labels, now most characters are allowed again
- Failed fits do not throw an error that crashes the protocol anymore
- Title and icon of plot windows

## 1.1.0
Features:
- Protocols and manual controls are now sortable into tabs!
- Protocols can now be run in a queue
- Added possibility to force sequential on/off for single channels
- Plots are now done with pyqtgraph, improving interactivity and performance

Fixed:
- Plots being placed somewhere should now not kill the program anymore

---

### 1.0.6

Features:
- Added an "owner" field to the samples, it is automatically populated when a new sample is created. This should stop cluttering the samples for all users. Only the current user's samples will show in the comboBox, or those without owner.
- Added possibility to use instruments that generate their channels at runtime. 
- Added SequentialDevice that forces every call to the instrument to wait for the previous one to finish.
- Added the `*.py` and `*_ophyd.py` file contents as metadata to each instrument in the final measurement file. 

Fixed:
- "Hide info" button in instrument installer now working

### 1.0.5

Changes:
- Driver versions now have a separate branch on CAMELS_drivers to improve keeping them up to date
- Same for extensions
- Now checking filenames of protocols for invalid characters
- Improved speed of looking for updates

Fixed:
- Fixed checking for currently used version
- Extensions can now actually be downloaded

### 1.0.4

Fixed:
- NOMAD upload now uses the correct file if new file for every run
- Dependency updated to python>=3.11.3

### 1.0.3

Changes:
- Removed "environment" from saved hdf5 files, moved instrument information up on step in hirarchy
- changed file extension to .nxs for better NOMAD integration

Fixed:
- Fixed bug that prevented set panels from starting
- Fixed issue with uploads to NOMAD if an unnamed upload exists
- Fixed trigger for Custom_Function_SignalRO
- Fixed parameters for custom function in fits

### 1.0.2

Features:
- Added functionality to select path for exporting hdf5 to csv/json

Fixed:
- You can now use new lines and special characters in the protocol description field.
- If exporting hdf5 to csv/json and not specifying the path for the export, the path of the hdf5 should now be selected correctly


### 1.0.1

Features:
- Now asking for the path, where to save measurement data when starting up CAMELS for the first time (or there is no preferences.json)
- Added "Quit" button to file menu

Changes:
- Changed the default configuration files path for linux and mac; now the user is asked at the first startup where to put configuration files and can set the path in the settings
- Improved usability of moving steps in sequence

# 1.0.0

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
- The imports needed at a later time are now running in another thread after starting the main app to improve speed
- Changed displayed window titles to show "NOMAD CAMELS" last
- Changed displayed name to "NOMAD CAMELS" wherever found
- Removed checkbox whether to plot an xy-plot, it is now always plotted
- Added color to GUI buttons for better usability

Fixed:
- Fixed export from databroker if the run failed such that no "stop" is in metadata
- Plot widget now shows the table to change linestyle and markerstyle
- Refactor file paths for cross-platform compatibility in device_driver_builder.py
- Fix issue of stage control not updating set_channel when moving manually


### 0.2.3

Features:

- Driver builder now not only for VISA, includes custom functions
- Now allowing for non-string configs (e.g. other instruments)

Changes:

- Changed order of channels to be above variables in context menu
- Changed marker style to 'pixel' for 2D-plots
- Changed driver information window, you can now toggle it on and off with the button in the instrument management

Fixed:

- Fixed error when changing the sweep channel in the ND sweep step 


### 0.2.2

Features:
- Reading/Saving of variables ad Read_Channels is now possible, appears as an array in the data
- Added a class for a waiting bar during protocols
- Added support for NOMAD's new app token feature

Fixed:
- Unwanted printing of packages in instrument-management fixed
- Plots of sweeps or subprotocols of subprotocols should now also be added to the main-plot list, enabling closing on closing of CAMELS or via button
- Error of screen object already being deleted should be fixed
- Databroker export to csv improved for non simple 2D data
- Time weight of sub protocols now handled correctly
- Use abs for y axis should now be possible (again)
- Color settings for material theme are now remembered when opening the settings

### 0.2.1

Minor features:
- Callable functions for manual move of stage control
- Now showing readme and license of drivers

Quality of life:
- Waiting cursor during reference drive of stage control
- Names of steps now appear in protocol overview

Fixed:
- Fixed bug for showing non-number values / channels in list-plot
- Fixed repeated firing of keyPress/ReleaseEvent in manual control of stage
- Fixed all 3 axes being called when clicking "go-to" in stage control, even if not available
- Fixed that Read_Channels steps could not be renamed

## 0.2.0

Major new feature:
- Callable functions of instruments, that are not channels

Minor features:
- Reference drive and stop of stage control are now callable functions

Quality of life:
- Startup speed increased, but first run of protocol now slowed down
- Added plot all available channels as possibility for List-Plot
- Improved layout of set-panel

Fixed:
- Can now set log scale when using only one y-axis
- Now using settings of log-scale from definition window at startup of plot

### 0.1.9

New features:
- Retry on error for VISA-devices
- Set_Panel added as a new manual control, this may be used to easily control channels that often have to be set to certain values in preparation of an experiment

Quality of life:
- Waiting cursor when adding instrument and it takes some time

Fixed:
- Now the For-Loop (and children of it) display the "start - min - max - stop" preview correctly
- Import of instruments should now work correctly when running protocol outside the UI
- Int in instrument config is now saved as int
- Pyvisa added to requirements to support local drivers

### 0.1.8

Fixed:
- Finalize steps of instruments are now being called
- Fixed issue with handing variables to subprotocol
- Fixed update function for Windows, function for Unix/Mac not tested

### 0.1.7

Added functionalities:
- Added functionality to import protocols

Fixed:
- Fixed error message appearing when closing List-Plot
- Fixed login for central NOMAD
- fixed comment/uncomment of steps being saved correctly

### 0.1.6

Added functionalities:
- Added capabilities to interact with NOMAD (Oasis), uploading files, getting user information and using a NOMAD entry as sample
- Functionality to comment / uncomment steps in a protocol for testing / quickly changing a protocol

Fixed:
- CAMELS should not crash completely anymore when an instrument cannot be initialised
- Variables should mostly be refreshed for step configs without clicking around
- *add_metadata* removed from Custom_Function_Signal
- Search in channels-tables not case sensitive anymore
- Fixed that protocol without plots starts QApplication when run outside CAMELS

### 0.1.5

- Fixed the 'Update CAMELS' tool.\
- Renamed input and output to read and set in the 'Update CAMELS' tool.\
- Small fix to the VISA device builder.

### 0.1.4

- Added a timeout setting to all VISA instruments. Setting the timeout determines how long the instrument waits after sending a command before raising a timeout exception

### 0.1.3

- First stable and working release

### 0.1.0 to 0.1.2 

- &#9888; Broken releases due to minor bugs that were fixed in 0.1.3
