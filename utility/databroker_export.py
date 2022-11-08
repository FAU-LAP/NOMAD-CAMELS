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
            stamp = val['time']
            val['time'] = timestamp_to_ISO8601(stamp)
            # stamp = rundict['metadata_stop']['time']
            # rundict['metadata_stop']['time'] = timestamp_to_ISO8601(stamp)
        if type(val) is dict:
            if key == 'start':
                sub_entry = entry
            else:
                sub_entry = entry.create_group(key)
            recourse_entry_dict(sub_entry, val)
        elif type(val) is list:
            no_dict = False
            for i, value in enumerate(val):
                if isinstance(value, dict):
                    sub_entry = entry.create_group(f'{key}_{i}')
                    recourse_entry_dict(sub_entry, value)
                # else:
                #     # entry.attrs[f'{key}_{i}'] = val
                else:
                    no_dict = True
                    break
            if no_dict:
                entry[key] = val
        elif val is None:
            continue
        else:
            # entry.attrs[key] = val
            entry[key] = val

def broker_to_hdf5(runs, filename, additional_data=None):
    """Puts the given `runs` into `filename`, containing the run's
    metadata and the dataset."""
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    if not isinstance(runs, list):
        runs = [runs]
    for run in runs:
        metadata = run.metadata
        start_time = timestamp_to_ISO8601(metadata['start']['time'])
        with h5py.File(filename, 'a') as file:
            entry = file.create_group(start_time)
            recourse_entry_dict(entry, metadata)
            additional_data = additional_data or {}
            recourse_entry_dict(entry, additional_data)
            for stream in run:
                dataset = run[stream].read()
                # entry[stream] = dataset.to_pandas()
                # return
                group = entry.create_group(stream)
                for coord in dataset.coords:
                    if coord == 'time':
                        isos = []
                        for t in dataset[coord].values:
                            isos.append(timestamp_to_ISO8601(t))
                        since = dataset[coord].to_numpy()
                        since -= metadata['start']['time']
                        group['time_since_start'] = since
                        group['time'] = isos
                    else:
                        group[coord] = dataset[coord]
                for col in dataset:
                    group[col] = dataset[col]



def broker_to_dict(runs, to_iso_time=True):
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
