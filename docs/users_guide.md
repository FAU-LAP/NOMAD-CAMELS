---
layout: default
title: User's Guide
has_children: true
nav_order: 3
---

# User's Guide
## Reading HDF5 files from CAMELS
You can use this simple script to read your HDF5 recursively and convert it to a nested dictionary.

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

Then simply access the relevant data by navigating through the dictionary.

<p style="text-align:left;">
  <span style="color: grey;">
  <a href="quick_start.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="programmers_guide.html">Next &rarr;</a><br>
  </span>
</p>