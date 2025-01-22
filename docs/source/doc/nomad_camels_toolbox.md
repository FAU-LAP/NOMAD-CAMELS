# NOMAD CAMELS toolbox

To assist with the evaluation of data, we provide the package [`nomad_camels_toolbox`](https://pypi.org/project/nomad-camels-toolbox/).

Currently, it only helps with reading the data from the hdf5 file. More functionality is planned for the future.

Instead of using this toolbox, you could also read the data directly. You find how to do this and more information about hdf5-files in general under [Handling HDF5 files](handling_hdf5.md#users-guide)

## Installation

To use the NOMAD CAMELS toolbox, you need to run
```
pip install nomad-camels-toolbox[pandas]
```
in the Python environment you use for your evaluation.
This installs `pandas` as a powerful package for data evaluation along with the toolbox, so the data can be read directly as a [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

```{note}
If you do not want to install the functionalities that come along with pandas, you can run `pip install nomad-camels-toolbox` instead. However, we recommend using pandas.
```

## Reading Data
The main usage is to read the data from files produced by CAMELS. To read the file at `file_path`, you can run:
```python
import nomad_camels_toolbox as ntc

data = ntc.read_camels_file(file_path)
```
If there is only one entry in the hdf5 file, it will automatically read the main dataset with this code. For more information, see the [code reference](../code/nomad_camels_toolbox.html#nomad_camels_toolbox.data_reader.read_camels_file).


