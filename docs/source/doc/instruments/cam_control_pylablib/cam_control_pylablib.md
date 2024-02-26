# Cam-Control by PyLabLib - Scientific Camera Control

## Install

Install the instrument using the `Manage Instruments` button of NOMAD-CAMELS or by running

```bash
pip install nomad-camels-driver-cam-control-pylablib
```

in the desired Python environment.
The most resent package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-cam-control-pylablib/).

## Basics

The backbone of this driver is the _Cam-Control_ software by [PyLabLib](https://pylablib-cam-control.readthedocs.io/).

```{note}
The _Cam-Control_ software must be running and set up to [allow server communication](https://pylablib-cam-control.readthedocs.io/en/latest/expanding.html#control-server).
CAMELS then connects to the server and sends requests to the server. 
```

You must set up _Cam-Control_ via its own GUI and you can then use CAMELS to actually save images and frames with the settings from the GUI. Some of the GUI settings can be modified with CAMELS.

## Functionality

### Configuration

Under `Manage Instruments` in the `Configure Instruments`-tab you can set:

- `Exposure time`: Exposure time of the camera. You can check the `Overwrite exposure time` checkbox to always overwrite the currently set value with the value given in this field. The value is then set every time a protocol with the device is run. This will overwrite any manual setting of the exposure time of the GUI at protocol startup.
- `Host IP`: Set the host IP address of the cam-control server visible in the GUI at the bottom of the `Plugins`-tab. Format should be `xxx.xxx.xxx.xxx`
- `Port`: Set the correct port of the server, normally `18923`, but can be changed in the `settings.cfg` file of _Cam-Control_.
- `Byte length`: Number of bytes that are read. Usually some large number (>9.000.000) should work fine. A 1920x1080 frame has `1920 * 1080 * 2 = 4.147.200` bytes.

### Channels

- `get_single_frame`: Get a single frame from the buffer and handle it within Python. This allows you to save the frame with all other data to an HDF5 file. A maximum acquisitian speed of 20-25 frames per second is possible in this way.
- `get_background_frame`: Get the current background frame that is subtracted from new frames. You can only get the background frame if the background is valid.
- `path_suffix`: The suffix you want to append to every name of frame that is recorded with the `save_snapshot` or `start_saving` custom function. So if the path in the GUI is `C:/Users/user/Documents/data/frame_name` the saved frame is normally in `C:/Users/user/Documents/data/` called `frame_name.tiff`. If you set a suffix this will be appended, as well as the current time (`time.time()`). So the frame would then be saved in `C:/Users/user/Documents/data/` called `frame_name_<suffix>_<time>.tiff`.
- `frame_average`: Calculates the average pixel value of the latest recorded frame read using `get_single_frame` (uses `np.mean(frame)`). This means you must first read the `get_single_frame` channel and then you can read the `frame_average` channel in a new read loop step.
- `set_roi`: Allows you to set a new region of interest (ROI). Write `[x_min, x_max, y_min, y_max]` into the set channels value field. You must include the braces as you are passing a python list as a value.

### Custom functions

These functions can be used with the loop step type `Call Function`.

- `save_snapshot`: Saves a snapshot of the current frame displayed in the GUI. This includes the already subtracted background and binning. The file is saved locally under the path given in the GUI. It is not saved in the HDF5 file! It is identical to pressing the `Snap` button of the GUI.
- `start_saving`: Starts the continuous saving of frames with the settings configured in the GUI. It is identical to pressing the `Saving` button of the GUI.

```{note}
Take care that the file size can get quite large for small exposure times!
TIFF files have a maximum size of 2 GB! For larger data use 'Raw binary' or 'Big TIFF'.
```

- `stop_saving`: Stops the continuous saving of frames with the settings configured in the GUI. It is identical to pressing the `Saving` button of the GUI again.
- `grab_background`: Grabs a new background with the current settings. It is identical to pressing the `Grab background` button of the GUI.

## Additional Information

You can simply save snapshots locally (already including some processing like background subtraction and binning) and then store the (large) files together with the HDF5 file. For this use the `save_snapshot` function described below. This can be better in some scenarios, as CAMELS does not need to take care of saving the data.

You can also store every frame (`get_single_frame` and `get_background_frame`) in the final HDF5, but this is might be slower than saving the snapshot in some cases.
