# Cam-Control by PyLabLib - Scientific Camera Control

## Install
Install the instrument using the `Manage Instruments` button of NOMAD-CAMELS or by running 
```
pip install nomad-camels-driver-cam-control-pylablib
```
in the desired Python environment.
The most resent PyPi package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-cam-control-pylablib/).

## Basics
The backbone of this driver is the cam-control software by [PyLabLib](https://pylablib-cam-control.readthedocs.io/). The software must be running and set up to [allow server communication](https://pylablib-cam-control.readthedocs.io/en/latest/expanding.html#control-server).
CAMELS then connects to the server and sends requests to the server. 

You must set up cam-control via its own GUI and you can then use CAMELS to actually save images with the exact settings from the GUI.

## Best Practices
It is currently best (fastest measurements) to simply save snapshots locally (already including some processing like background subtraction and binning) and to then store the (large) files together with the HDF5 file. For this use the `save_snapshot` function described below.

You can also store every frame (`get_single_frame` and `get_background_frame`) in the final HDF5, but this is (much) slower than saving the snapshot. 

## Functionality
### Configuration
Under `Manage Instruments` in the `Configure Instruments`-tab you can set:
- `Exposure time`: Exposure time of the camera. Changes value of the GUI every time a protocol with the device is run. Take care to always consider this as it will overwrite any manual setting of the exposure time at protocol startup. You can manually change the exposure time while the protocol is running but this might cause the protocol to fail as the read timing might be wrong (e.g. protocol expects an exposure time of 100 ms, but you set it manually to 10s &#8594; read timeout error.)
- `Host IP`: Set the host IP adress of the cam-control server visible in the GUI at the bottom of the `Plugins`-tab. Format should be `xxx.xxx.xxx.xxx`
- `Port`: Set the correct port of the server, normally `18923`, but can be changed in the `settings.cfg` file of cam-control.
- `Wait for frame`: Time that is waited before reading data after a frame request by `get_single_frame` or `get_background_frame`. This is done to prevent errors as the server is not very fast. Typical value is about 1000 ms if you quickly loop over images, can be reduced if you perform many actions and therefore have more time between getting frames.

### Channels
- `get_single_frame`: Get a single frame from the buffer and handle it within Python. This allows you to save the frame with all other data to an HDF5 file. Not very fast. Time between getting frames should be around 1 second. Waits for the time specified in `Wait for frame` between requests and actually reading the frame data.
- `get_background_frame`: Get the current background frame that is subtracted from new frames. You can only get the background frame if the background is valid. Time between getting background frames should be around 1 second. Waits for the time specified in `Wait for frame` between requests and actually reading the frame data.
### Custom functions
These functions can be used with the loop step type `Call Function`.
- `save_snapshot`: Saves a snapshot of the current frame displayed in the GUI. This includes the already subtracted background and binning. The file is saved locally under the path given in the GUI. It is not saved in the HDF5 file! It is identical to pressing the `Snap` button of the GUI. 
- `start_saving`: Starts the continuous saving of frames with the settings configured in the GUI. It is identical to pressing the `Saving` button of the GUI. 
  > Take care that the file size can get quite large for small exposure times!

  > TIFF files have a maximum size of 2 GB! For larger data use 'Raw binary' or 'Big TIFF'.
- `stop_saving`: Stops the continuous saving of frames with the settings configured in the GUI. It is identical to pressing the `Saving` button of the GUI again. 








