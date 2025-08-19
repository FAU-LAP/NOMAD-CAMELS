# NOMAD CAMELS toolbox

To assist with the evaluation of data, we provide the package [`nomad_camels_toolbox`](https://pypi.org/project/nomad-camels-toolbox/).

Currently, it only helps with reading the data from the hdf5 file. More functionality is planned for the future.

```{hint}
For more information on how to use the toolbox, see the [code reference](https://fau-lap.github.io/NOMAD-CAMELS/code/nomad_camels_toolbox.html).
```

## Installation

To install the NOMAD CAMELS toolbox, run
```
pip install nomad-camels-toolbox[all]
```
in the Python environment you use for your evaluation. This installs all optional dependencies to use the full functionality. The following options are all included when using `all`.

Single installation options can be installed by using `pip install nomad-camels-toolbox[option-name]` ([see pip install documentation](https://pip.pypa.io/en/stable/cli/pip_install/)). The options are:
- `pandas`: This installs `pandas` as a powerful package for data evaluation along with the toolbox, so the data can be read directly as a [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). Also see [reading data](#reading-data).
- `plotly`: Installs [plotly](https://pypi.org/project/plotly/), [lmfit](https://pypi.org/project/lmfit/) and [pandas](https://pypi.org/project/pandas/). It enables to automatically recreate the plots made in CAMELS, using plotly figures. See [recreating plots](#recreating-plots)
- `qt`: Installs [PySide6](https://pypi.org/project/PySide6/) and [pyqtgraph](https://pypi.org/project/pyqtgraph/). This is used to provide a GUI, to quickly investigate data from CAMELS, see [data viewer](#data-viewer).

## Reading Data
The main usage is to read the data from files produced by CAMELS. To read the file at `file_path`, you can run:
```python
import nomad_camels_toolbox as nct

data = nct.read_camels_file(your_file_path)
```
If there is only one entry in the hdf5 file, it will automatically read the main dataset (if there is no other dataset, otherwise you will be asked to select one).

```{hint}
For more information on how to use the toolbox, see the [code reference](https://fau-lap.github.io/NOMAD-CAMELS/code/nomad_camels_toolbox.html).
```

Your data will then be in a pandas DataFrame and can be accessed like:
```python
detector_data = data['demo_instrument_detectorComm']
motorx_data = data['demo_instrument_motorX']
motory_data = data['demo_instrument_motorY']
```

If you want to read the data from a sub-dataset, like a Simple Sweep (in this example named "Simple_Sweep"), one possibility is:
```python
data = nct.read_camels_file(your_file_path, data_set_key="Simple_Sweep")
```
Another way is to read all datasets and then select the one you want to investigate further:
```python
data = nct.read_camels_file(your_file_path, read_all_datasets=True)
primary_data = data["primary"]
simple_sweep_data = data["Simple_Sweep"]
```
Here `data` is a dictionary of dataframes with all your data.


You can find more examples for data evaluation in the [documentation part regarding h5py](handling_hdf5.md#using-h5py).


## Recreating Plots
The toolbox provides a function that allows to quickly recreate all plots that were defined within CAMELS, using plotly. You can run it with:
```python
import nomad_camels_toolbox as nct

figures = nct.recreate_plots(your_file_path)
```
This way it will create all the plots, including those of sub-steps and return the corresponding figures as a dictionary.

For more information see the [code reference](https://fau-lap.github.io/NOMAD-CAMELS/code/nomad_camels_toolbox.html).


## Data Viewer
This tool is for a quick look at data plots. Besides simple x-y plots, it also provides functionalities for 2D plots and filtering. It is possible to plot expressions of the data.

To start the viewer, run one of the following in your command line:

`camels-viewer` or `python -m nomad_camels_toolbox`.

Alternatively, you can run it from inside python:
```python
import nomad_camels_toolbox as nct

nct.run_viewer()
```
To open your file, you can drag and drop it into the viewer window (on the right part), once it is running.

The UI is split into the configuration on the left, and the plot on the right. You can drag the line in the middle.

On the left side, you can select which datasets to plot, and how they should look. You can add a second plot by loading another file. If you want to compare two values from the same file, just load it again.


### Multi-Dimensional Data

If you select as "x" and "y" two datasets with dimension 2, more selection possibilities appear at the bottom. (For example wavelength and intensity of optical spectra.)
You can select an "image X" and "image Y" axis of the remaining values of the dataset (for example x and y values of a spacial scan). If the data can be processed, an image appears, and you can select for which pixel of the image the x-y data is plotted by dragging the red box.

At the top image, two red lines will appear. Dragging those will change the color of the image below. It is color-coded by the integrated intensity between these lines.

Selecting "None" for "image Y", you can also just plot the integrated intensity over one value, if it has no duplicates.



