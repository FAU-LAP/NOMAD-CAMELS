import importlib.metadata
import os.path
import json
import sys

import databroker
import h5py
from datetime import datetime as dt

import numpy as np
import xarray


def recourse_entry_dict(entry, metadata):
    """Recoursively makes the metadata to a dictionary.

    Parameters
    ----------
    entry :
        
    metadata :
        

    Returns
    -------

    """
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
    metadata and the dataset.

    Parameters
    ----------
    runs :
        
    filename :
        
    additional_data :
         (Default value = None)

    Returns
    -------

    """
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
                stream_meta = run[stream].metadata
                for col in dataset:
                    group[col] = dataset[col]
                if 'descriptors' in stream_meta:
                    dat = stream_meta['descriptors'][0]['data_keys']
                    for key, val in dat.items():
                        if isinstance(val, dict):
                            for k, v in val.items():
                                group[key].attrs[k] = v


def export_run(filename, run_number=-1, plot_data=None, additional_data=None,
               session_name='', export_to_csv=False, export_to_json=False,
               catalog_name='CAMELS_CATALOG'):
    """ TODO """
    catalog = databroker.catalog[catalog_name]
    run = catalog[run_number]
    broker_to_NX([run], filename, plot_data, additional_data,
                 session_name, export_to_csv, export_to_json)


def broker_to_NX(runs, filename, plot_data=None, additional_data=None,
                 session_name='', export_to_csv=False, export_to_json=False):
    """

    Parameters
    ----------
    runs :
        
    filename :
        
    plot_data :
         (Default value = None)
    additional_data :
         (Default value = None)
    session_name :
         (Default value = '')
    export_to_csv :
         (Default value = False)
    export_to_json :
         (Default value = False)

    Returns
    -------

    """
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    if not isinstance(runs, list):
        runs = [runs]
    for run in runs:
        metadata = run.metadata
        meta_start = dict(metadata['start'])
        meta_stop = dict(metadata['stop'])
        st_time = meta_start.pop('time')
        start_time = timestamp_to_ISO8601(st_time)
        end_time = timestamp_to_ISO8601(meta_stop.pop('time'))
        entry_name = f'{session_name}_{start_time}' if session_name else start_time
        entry_name_non_iso = f'{session_name}_{st_time}' if session_name else st_time
        if export_to_json:
            if not os.path.isdir(filename.split(".")[0]):
                os.makedirs(filename.split(".")[0])
            with open(f'{filename.split(".")[0]}/{entry_name_non_iso}_metadata.json', 'w', encoding='utf-8') as json_file:
                json.dump(meta_start, json_file, indent=2)
        with h5py.File(filename, 'a') as file:
            entry = file.create_group(entry_name)
            entry.attrs['NX_class'] = 'NXentry'
            entry['definition'] = 'NXsensor_scan'
            entry['start_time'] = start_time
            entry['end_time'] = end_time
            if 'description' in meta_start:
                desc = meta_start.pop('description')
                entry['experiment_description'] = desc
            if 'identifier' in meta_start:
                ident = meta_start.pop('identifier')
                entry['experiment_identifier'] = ident
            proc = entry.create_group('process')
            proc.attrs['NX_class'] = 'NXprocess'
            proc['program'] = 'NOMAD-CAMELS'
            proc['program'].attrs['version'] = '0.1'
            proc['program'].attrs['program_url'] = 'https://github.com/FAU-LAP/NOMAD-CAMELS'
            version_dict = meta_start.pop('versions')
            vers_group = proc.create_group('versions')
            py_environment = proc.create_group('python_environment')
            py_environment.attrs['python_version'] = sys.version
            d = importlib.metadata.distributions()
            for x in importlib.metadata.distributions():
                name = x.metadata['Name']
                if name not in py_environment.keys():
                    py_environment[x.metadata['Name']] = x.version
                # except Exception as e:
                #     print(e, x.metadata['Name'])
            recourse_entry_dict(vers_group, version_dict)
            user = entry.create_group('user')
            user.attrs['NX_class'] = 'NXuser'
            recourse_entry_dict(user, meta_start.pop('user'))
            sample = entry.create_group('sample')
            sample.attrs['NX_class'] = 'NXsample'
            recourse_entry_dict(sample, meta_start.pop('sample'))

            instr = entry.create_group('instrument')
            instr.attrs['NX_class'] = 'NXinstrument'
            environ = instr.create_group('environment')
            environ.attrs['NX_class'] = 'NXenvironment'
            for dev, dat in meta_start.pop('devices').items():
                dev_group = environ.create_group(dev)
                if 'idn' in dat:
                    dev_group['model'] = dat.pop('idn')
                else:
                    dev_group['model'] = dat['device_class_name']
                dev_group['name'] = dat.pop('device_class_name')
                dev_group['short_name'] = dev
                settings = dev_group.create_group('settings')
                recourse_entry_dict(settings, dat)

            recourse_entry_dict(entry, meta_start)

            data_entry = entry.create_group('data')
            data_entry.attrs['NX_class'] = 'NXdata'
            for stream in run:
                if '_fits_readying_' in stream:
                    continue
                dataset = run[stream].read()
                if export_to_csv:
                    if not os.path.isdir(f'{filename.split(".")[0]}/{entry_name_non_iso}'):
                        os.makedirs(f'{filename.split(".")[0]}/{entry_name_non_iso}')
                    try:
                        dataset.to_pandas().to_csv(f'{filename.split(".")[0]}/{entry_name_non_iso}/{stream}.csv')
                    except Exception as e:
                        raise print(e)
                if stream == 'primary':
                    group = data_entry
                else:
                    group = data_entry.create_group(stream)
                    group.attrs['NX_class'] = 'NXdata'
                for coord in dataset.coords:
                    if coord == 'time':
                        isos = []
                        for t in dataset[coord].values:
                            isos.append(timestamp_to_ISO8601(t))
                        since = dataset[coord].to_numpy()
                        since -= st_time
                        group['time_since_start'] = since
                        group['time'] = isos
                    else:
                        group[coord] = dataset[coord]
                stream_meta = run[stream].metadata
                for col in dataset:
                    # Enables CAMELS to read strings from channels
                    if str(dataset[col].dtype).startswith('<U'):
                        group[col] = dataset[col].astype(bytes)
                    else:
                        group[col] = dataset[col]
                if 'descriptors' in stream_meta:
                    dat = stream_meta['descriptors'][0]['data_keys']
                    for key, val in dat.items():
                        if isinstance(val, dict):
                            for k, v in val.items():
                                try:
                                    group[key].attrs[k] = v
                                except Exception as e:
                                    print(f"could not add value {v} to metadata with name {k}\n{e}")
                if not plot_data:
                    continue
                axes = []
                signals = []
                for plot in plot_data:
                    if plot.stream_name == stream and hasattr(plot, 'x_name'):
                        if plot.x_name not in axes:
                            axes.append(plot.x_name)
                        if hasattr(plot, 'z_name'):
                            if plot.y_name not in axes:
                                axes.append(plot.y_name)
                            if plot.z_name not in signals:
                                signals.append(plot.z_name)
                        else:
                            for y in plot.y_names:
                                if y not in signals:
                                    signals.append(y)
                        if not hasattr(plot, 'liveFits') or not plot.liveFits:
                            continue
                        fit_group = group.require_group('fits')
                        for fit in plot.liveFits:
                            if not fit.results:
                                continue
                            fg = fit_group.require_group(fit.name)
                            param_names = []
                            param_values = []
                            covars = []
                            timestamps = []
                            for t, res in fit.results.items():
                                timestamps.append(float(t))
                                if res.covar is None:
                                    covar = np.ones((len(res.best_values), len(res.best_values)))
                                    covar *= np.nan
                                else:
                                    covar = res.covar
                                covars.append(covar)
                                if not param_names:
                                    param_names = res.model.param_names
                                param_values.append(res.params)
                            fg.attrs['param_names'] = param_names
                            timestamps, covars, param_values = sort_by_list(timestamps, [covars, param_values])
                            isos = []
                            for t in timestamps:
                                isos.append(timestamp_to_ISO8601(t))
                            fg['time'] = isos
                            since = np.array(timestamps)
                            since -= st_time
                            fg['time_since_start'] = since
                            fg['covariance'] = covars
                            fg['covariance'].attrs['parameters'] = param_names[:len(covars[0])]
                            param_values = get_param_dict(param_values)
                            for p, v in param_values.items():
                                fg[p] = v
                            for name, val in fit.additional_data.items():
                                fg[name] = val
                if signals:
                    group.attrs['signal'] = signals[0]
                    if len(signals) > 1:
                        group.attrs['auxiliary_signals'] = signals[1:]
                group.attrs['axes'] = axes
                group.attrs['NX_class'] = 'NXdata'
    # print('Successfully saved protocol data!')


def get_param_dict(param_values):
    """

    Parameters
    ----------
    param_values :
        

    Returns
    -------

    """
    p_s = {}
    for vals in param_values:
        for k in vals:
            if k in p_s:
                p_s[k].append(vals[k].value)
            else:
                p_s[k] = [vals[k].value]
    return p_s


def sort_by_list(sort_list, other_lists):
    """

    Parameters
    ----------
    sort_list :
        
    other_lists :
        

    Returns
    -------

    """
    s_list = sorted(zip(sort_list, *other_lists), key=lambda x: x[0])
    return zip(*s_list)




def broker_to_dict(runs, to_iso_time=True):
    """Puts the runs into a dictionary.

    Parameters
    ----------
    runs :
        
    to_iso_time :
         (Default value = True)

    Returns
    -------

    """
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
    """

    Parameters
    ----------
    timestamp :
        

    Returns
    -------

    """
    from_stamp = dt.fromtimestamp(timestamp)
    return from_stamp.astimezone().isoformat()
