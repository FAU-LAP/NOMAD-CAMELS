# NOMAD CAMELS toolbox

To assist with the evaluation of data, we provide the package [`nomad_camels_toolbox`](https://pypi.org/project/nomad-camels-toolbox/).

Currently, it only helps with reading the data from the hdf5 file. More functionality is planned for the future.

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
If there is only one entry in the hdf5 file, it will automatically read the main dataset with this code.

```{note}
For more information, see the [code reference](https://fau-lap.github.io/NOMAD-CAMELS/code/nomad_camels_toolbox.html).
```

Your data will then be in a pandas DataFrame and can be accessed like:
```python
detector_data = data['demo_instrument_detectorComm']
motorx_data = data['demo_instrument_motorX']
motory_data = data['demo_instrument_motorY']
```
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
The data viewer can be used for more functionalities than the h5-viewer can provide.
To start the viewer, run:
```python
import nomad_camels_toolbox as nct

figures = nct.run_viewer()
```
To open your file, you can drag and drop it into the viewer window, once it is running.
