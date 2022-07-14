import os.path

import databroker
import h5py
from datetime import datetime as dt

import xarray


def recourse_entry_dict(entry, metadata):
    """Recoursively makes the metadata to a dictionary."""
    # TODO check if actually necessary
    for key, val in metadata.items():
        if isinstance(val, databroker.core.Start) or isinstance(val, databroker.core.Stop):
            val = dict(val)
        if type(val) is dict:
            sub_entry = entry.create_group(key)
            recourse_entry_dict(sub_entry, val)
        elif type(val) is list:
            for i, value in enumerate(val):
                if isinstance(value, dict):
                    sub_entry = entry.create_group(f'{key}_{i}')
                    recourse_entry_dict(sub_entry, value)
                else:
                    entry.attrs[f'{key}_{i}'] = val
        elif val is None:
            continue
        else:
            entry.attrs[key] = val

def broker_to_hdf5(runs, filename, additional_data=None):
    """Puts the given `runs` into `filename`, containing the run's
    metadata and the dataset."""
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    if not isinstance(runs, list):
        runs = [runs]
    for run in runs:
        metadata = run.metadata
        with h5py.File(filename, 'a') as file:
            entry = file.create_group(run.name)
            for stream in run:
                dataset = run[stream].read()
                group = entry.create_group(stream)
                for col in dataset:
                    group[col] = dataset[col]
                for coord in dataset.coords:
                    group[coord] = dataset[coord]
            recourse_entry_dict(entry, metadata)
            additional_data = additional_data or {}
            recourse_entry_dict(entry, additional_data)



def broker_to_dict(runs, to_iso_time=False):
    """Puts the runs into a dictionary."""
    dicts = []
    if not isinstance(runs, list):
        runs = [runs]
    for run in runs:
        data = {}
        for stream in run:
            data = run[stream].read()
            if isinstance(data, xarray.Dataset):
                data = data.to_array()
        rundict = {'metadata_start': dict(run.metadata['start']),
                   'metadata_stop': dict(run.metadata['stop']),
                   'data': data}
        if to_iso_time:
            stamp = rundict['metadata_start']['time']
            rundict['metadata_start']['time'] = timestamp_to_ISO8601(stamp)
            stamp = rundict['metadata_stop']['time']
            rundict['metadata_stop']['time'] = timestamp_to_ISO8601(stamp)
        dicts.append(rundict)
    return dicts


def timestamp_to_ISO8601(timestamp):
    from_stamp = dt.fromtimestamp(timestamp)
    return from_stamp.astimezone().isoformat()
