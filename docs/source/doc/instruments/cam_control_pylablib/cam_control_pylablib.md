# Cam-Control by PyLabLib - Scientific Camera Control

## Install
Install the instrument using the `Manage Instruments` button of NOMAD-CAMELS or by running 
```
pip install nomad-camels-driver-cam-control-pylablib
```
in the desired Python environment.
The most resent package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-cam-control-pylablib/).

## Basics
The backbone of this driver is the _Cam-Control_ software by [PyLabLib](https://pylablib-cam-control.readthedocs.io/). 
> The software must be running and set up to [allow server communication](https://pylablib-cam-control.readthedocs.io/en/latest/expanding.html#control-server).
CAMELS then connects to the server and sends requests to the server. 

You must set up cam-control via its own GUI and you can then use CAMELS to actually save images with the exact settings from the GUI.




## Functionality
### Configuration
Under `Manage Instruments` in the `Configure Instruments`-tab you can set:
- `Exposure time`: Exposure time of the camera. Changes value of the GUI every time a protocol with the device is run. Take care to always consider this as it will overwrite any manual setting of the exposure time at protocol startup. You can manually change the exposure time while the protocol is running but this might cause the protocol to fail as the read timing might be wrong (e.g. protocol expects an exposure time of 100 ms, but you set it manually to 10s &#8594; read timeout error.)
- `Host IP`: Set the host IP adress of the cam-control server visible in the GUI at the bottom of the `Plugins`-tab. Format should be `xxx.xxx.xxx.xxx`
- `Port`: Set the correct port of the server, normally `18923`, but can be changed in the `settings.cfg` file of cam-control.
- `Byte length`: Number of bytes that are read. Usually some large number (>9.000.000) should work fine. A 1920x1080 frame has `1920 * 1080 * 2 = 4.147.200` bytes.


### Channels
- `get_single_frame`: Get a single frame from the buffer and handle it within Python. This allows you to save the frame with all other data to an HDF5 file. Not very fast. Time between getting frames should be around 1 second. Waits for the time specified in `Wait for frame` between requests and actually reading the frame data.
- `get_background_frame`: Get the current background frame that is subtracted from new frames. You can only get the background frame if the background is valid. Time between getting background frames should be around 1 second. Waits for the time specified in `Wait for frame` between requests and actually reading the frame data.
- `path_suffix`: The suffix you want to append to every name of frame that is recorded with the `save_snapshot` or `start_saving` custom function. So if the path in the GUI is `C:/Users/user/Documents/data/frame_name` the saved frame is normally in `C:/Users/user/Documents/data/` called `frame_name.tiff`. If you set a suffix this will be appended, as well as the current time (`time.time()`). So the frame would then be saved in `C:/Users/user/Documents/data/` called `frame_name_<suffix>_<time>.tiff`.
- `frame_average`: Calculates the average pixel value of the latest recorded frame read using `get_single_frame` (uses `np.mean(frame)`). This means you must first read the `get_single_frame` channel and then you can read the `frame_average` channel in a new read loop step.
- `set_roi`: Allows you to set a new region of interest (ROI). Write `[x_min, x_max, y_min, y_max]` into the set channels value field. You must include the braces as you are passing a python list as a value.
### Custom functions
These functions can be used with the loop step type `Call Function`.
- `save_snapshot`: Saves a snapshot of the current frame displayed in the GUI. This includes the already subtracted background and binning. The file is saved locally under the path given in the GUI. It is not saved in the HDF5 file! It is identical to pressing the `Snap` button of the GUI. 
- `start_saving`: Starts the continuous saving of frames with the settings configured in the GUI. It is identical to pressing the `Saving` button of the GUI. 
  > Take care that the file size can get quite large for small exposure times!

  > TIFF files have a maximum size of 2 GB! For larger data use 'Raw binary' or 'Big TIFF'.
- `stop_saving`: Stops the continuous saving of frames with the settings configured in the GUI. It is identical to pressing the `Saving` button of the GUI again. 
- `grab_background`: Grabs a new background with the current settings. It is identical to pressing the `Grab background` button of the GUI. 

## Additional Information
You can simply save snapshots locally (already including some processing like background subtraction and binning) and then store the (large) files together with the HDF5 file. For this use the `save_snapshot` function described below. This can be better in some scenarios, as CAMELS does not need to take care of saving the data. 

You can also store every frame (`get_single_frame` and `get_background_frame`) in the final HDF5, but this is might be slower than saving the snapshot in some cases. 






