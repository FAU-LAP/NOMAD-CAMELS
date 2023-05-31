# User's Guide
## Display HDF5 File
You can  display the HDF5 file you obtained from CAMELS by dragging-and-dropping it into the following [webpage](https://h5web.panosc.eu/h5wasm) or any other HDF5-viewer.
## Reading HDF5 Files from CAMELS
You can use this Python script to read your HDF5 recursively and convert it to a nested dictionary.\
> This is not necessary as the HDF5 file can be used like a dictionary in Python but might be useful in some situations.

```python
import h5py


def h5_to_dict(h5file):
    def h5_to_dict_rec(h5group):
        d = {}
        for key, item in h5group.items():
            if isinstance(item, h5py.Dataset):
                d[key] = item[()]
            elif isinstance(item, h5py.Group):
                d[key] = h5_to_dict_rec(item)
        return d
    with h5py.File(h5file, 'r') as f:
        return h5_to_dict_rec(f)


# Example usage:
data = h5_to_dict(r'C:\Users\file.h5')
```

Then  access the relevant data by navigating through the dictionary.
