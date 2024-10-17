import importlib.metadata
import os.path
import json
import sys

import databroker
import h5py
from datetime import datetime as dt

import numpy as np
import xarray

from PySide6.QtWidgets import (
    QDialog,
    QComboBox,
    QPushButton,
    QGridLayout,
    QLabel,
    QCheckBox,
)


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
        if isinstance(val, databroker.core.Start) or isinstance(
            val, databroker.core.Stop
        ):
            val = dict(val)
            stamp = val["time"]
            val["time"] = timestamp_to_ISO8601(stamp)
            # stamp = rundict['metadata_stop']['time']
            # rundict['metadata_stop']['time'] = timestamp_to_ISO8601(stamp)
        if type(val) is dict:
            if key == "start":
                sub_entry = entry
            else:
                sub_entry = entry.create_group(key)
            recourse_entry_dict(sub_entry, val)
        elif type(val) is list:
            no_dict = False
            for i, value in enumerate(val):
                if isinstance(value, dict):
                    sub_entry = entry.create_group(f"{key}_{i}")
                    recourse_entry_dict(sub_entry, value)
                # else:
                #     # entry.attrs[f'{key}_{i}'] = val
                else:
                    no_dict = True
                    break
            if no_dict:
                if any(isinstance(item, str) for item in val):
                    entry[key] = np.array(val).astype("S")
                else:
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
        start_time = timestamp_to_ISO8601(metadata["start"]["time"])
        with h5py.File(filename, "a") as file:
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
                    if coord == "time":
                        isos = []
                        for t in dataset[coord].values:
                            isos.append(timestamp_to_ISO8601(t))
                        since = dataset[coord].to_numpy()
                        since -= metadata["start"]["time"]
                        group["time_since_start"] = since
                        group["time"] = isos
                    else:
                        group[coord] = dataset[coord]
                stream_meta = run[stream].metadata
                for col in dataset:
                    group[col] = dataset[col]
                if "descriptors" in stream_meta:
                    dat = stream_meta["descriptors"][0]["data_keys"]
                    for key, val in dat.items():
                        if isinstance(val, dict):
                            for k, v in val.items():
                                group[key].attrs[k] = v


def export_run(
    filename,
    run_number=-1,
    plot_data=None,
    additional_data=None,
    session_name="",
    export_to_csv=False,
    export_to_json=False,
    catalog_name="CAMELS_CATALOG",
    new_file_each_run=False,
):
    """TODO"""
    catalog = databroker.catalog[catalog_name]
    run = catalog[run_number]
    from nomad_camels.bluesky_handling.helper_functions import export_function

    export_function(
        [run],
        filename,
        True,
        new_file_each_run,
        export_to_csv,
        export_to_json,
        plot_data,
    )
    # broker_to_NX(
    #     [run],
    #     filename,
    #     plot_data,
    #     additional_data,
    #     session_name,
    #     export_to_csv,
    #     export_to_json,
    #     new_file_each_run,
    # )


def broker_to_NX(
    runs,
    filename,
    plot_data=None,
    additional_data=None,
    session_name="",
    export_to_csv=False,
    export_to_json=False,
    new_file_each_run=False,
):
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
        meta_start = dict(metadata["start"])
        meta_stop = {"time": None}
        if "stop" in metadata and metadata["stop"]:
            meta_stop = dict(metadata["stop"])
        st_time = meta_start.pop("time")
        start_time = timestamp_to_ISO8601(st_time)
        end_time = timestamp_to_ISO8601(meta_stop.pop("time"))
        entry_name = f"{session_name}_{start_time}" if session_name else start_time
        entry_name_non_iso = clean_filename(entry_name)
        # check if the filename already exists, if yes, add entry_name to filename
        if new_file_each_run and os.path.isfile(filename):
            filename = os.path.splitext(filename)[0] + f"_{entry_name_non_iso}.nxs"
        filename = os.path.join(
            os.path.abspath(os.path.dirname(filename)),
            os.path.normpath(
                f"{clean_filename(os.path.splitext(os.path.basename(filename))[0])}.nxs"
            ),
        )
        if export_to_json:
            if not os.path.isdir(filename.split(".")[0]):
                os.makedirs(filename.split(".")[0])
            with open(
                f'{filename.split(".")[0]}/{entry_name_non_iso}_metadata.json',
                "w",
                encoding="utf-8",
            ) as json_file:
                json.dump(meta_start, json_file, indent=2)
        with h5py.File(filename, "a") as file:
            entry = file.create_group(entry_name)
            entry.attrs["NX_class"] = "NXentry"
            entry["definition"] = "NXsensor_scan"
            entry["start_time"] = start_time
            entry["end_time"] = end_time
            if "description" in meta_start:
                desc = meta_start.pop("description")
                entry["experiment_description"] = desc
            if "identifier" in meta_start:
                ident = meta_start.pop("identifier")
                entry["experiment_identifier"] = ident
            proc = entry.create_group("process")
            proc.attrs["NX_class"] = "NXprocess"
            proc["program"] = "NOMAD CAMELS"
            proc["program"].attrs["version"] = "0.1"
            proc["program"].attrs[
                "program_url"
            ] = "https://github.com/FAU-LAP/NOMAD-CAMELS"
            version_dict = meta_start.pop("versions")
            vers_group = proc.create_group("versions")
            py_environment = proc.create_group("python_environment")
            py_environment.attrs["python_version"] = sys.version
            for x in importlib.metadata.distributions():
                name = x.metadata["Name"]
                if name not in py_environment.keys():
                    py_environment[x.metadata["Name"]] = x.version
                # except Exception as e:
                #     print(e, x.metadata['Name'])
            recourse_entry_dict(vers_group, version_dict)
            user = entry.create_group("user")
            user.attrs["NX_class"] = "NXuser"
            recourse_entry_dict(user, meta_start.pop("user"))
            sample = entry.create_group("sample")
            sample.attrs["NX_class"] = "NXsample"
            recourse_entry_dict(sample, meta_start.pop("sample"))

            instr = entry.create_group("instrument")
            instr.attrs["NX_class"] = "NXinstrument"
            for dev, dat in meta_start.pop("devices").items():
                dev_group = instr.create_group(dev)
                dev_group.attrs["NX_class"] = "NXsensor"
                if "idn" in dat:
                    dev_group["model"] = dat.pop("idn")
                else:
                    dev_group["model"] = dat["device_class_name"]
                dev_group["name"] = dat.pop("device_class_name")
                dev_group["short_name"] = dev
                settings = dev_group.create_group("settings")
                recourse_entry_dict(settings, dat)

            recourse_entry_dict(entry, meta_start)

            data_entry = entry.create_group("data")
            data_entry.attrs["NX_class"] = "NXdata"
            for stream in run:
                if "_fits_readying_" in stream:
                    continue
                dataset = run[stream].read()
                if export_to_csv:
                    if not os.path.isdir(
                        f'{filename.split(".")[0]}/{entry_name_non_iso}'
                    ):
                        os.makedirs(f'{filename.split(".")[0]}/{entry_name_non_iso}')
                    try:
                        df = dataset.to_dataframe()
                        df.to_csv(
                            f'{filename.split(".")[0]}/{entry_name_non_iso}/{stream}.csv',
                            sep=";",
                        )
                    except Exception as e:
                        print(e)
                if stream == "primary":
                    group = data_entry
                else:
                    group = data_entry.create_group(stream)
                    group.attrs["NX_class"] = "NXdata"
                for coord in dataset.coords:
                    if coord == "time":
                        isos = []
                        for t in dataset[coord].values:
                            isos.append(timestamp_to_ISO8601(t))
                        since = dataset[coord].to_numpy()
                        since -= st_time
                        group["time_since_start"] = since
                        group["time"] = isos
                    else:
                        group[coord] = dataset[coord]
                stream_meta = run[stream].metadata
                for col in dataset:
                    # Enables CAMELS to read strings from channels
                    if str(dataset[col].dtype).startswith("<U"):
                        group[col] = dataset[col].astype(bytes)
                    else:
                        group[col] = dataset[col]
                if "descriptors" in stream_meta:
                    dat = stream_meta["descriptors"][0]["data_keys"]
                    for key, val in dat.items():
                        if isinstance(val, dict):
                            for k, v in val.items():
                                try:
                                    group[key].attrs[k] = v
                                except Exception as e:
                                    print(
                                        f"could not add value {v} to metadata with name {k}\n{e}"
                                    )
                if not plot_data:
                    continue
                axes = []
                signals = []
                for plot in plot_data:
                    if plot.stream_name == stream and hasattr(plot, "x_name"):
                        if plot.x_name not in axes:
                            axes.append(plot.x_name)
                        if hasattr(plot, "z_name"):
                            if plot.y_name not in axes:
                                axes.append(plot.y_name)
                            if plot.z_name not in signals:
                                signals.append(plot.z_name)
                        else:
                            for y in plot.y_names:
                                if y not in signals:
                                    signals.append(y)
                        if not hasattr(plot, "liveFits") or not plot.liveFits:
                            continue
                        fit_group = group.require_group("fits")
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
                                    covar = np.ones(
                                        (len(res.best_values), len(res.best_values))
                                    )
                                    covar *= np.nan
                                else:
                                    covar = res.covar
                                covars.append(covar)
                                if not param_names:
                                    param_names = res.model.param_names
                                param_values.append(res.params)
                            fg.attrs["param_names"] = param_names
                            timestamps, covars, param_values = sort_by_list(
                                timestamps, [covars, param_values]
                            )
                            isos = []
                            for t in timestamps:
                                isos.append(timestamp_to_ISO8601(t))
                            fg["time"] = isos
                            since = np.array(timestamps)
                            since -= st_time
                            fg["time_since_start"] = since
                            fg["covariance"] = covars
                            fg["covariance"].attrs["parameters"] = param_names[
                                : len(covars[0])
                            ]
                            param_values = get_param_dict(param_values)
                            for p, v in param_values.items():
                                fg[p] = v
                            for name, val in fit.additional_data.items():
                                fg[name] = val
                if signals:
                    group.attrs["signal"] = signals[0]
                    if len(signals) > 1:
                        group.attrs["auxiliary_signals"] = signals[1:]
                group.attrs["axes"] = axes
                group.attrs["NX_class"] = "NXdata"
    # print('Successfully saved protocol data!')
    return filename


def export_h5_to_csv_json(
    filename, entry_name=None, export_data=True, export_metadata=True, export_path=None
):
    # read the h5 file and list the entries

    with h5py.File(filename, "r") as file:
        entries = list(file.keys())
    if entry_name is not None and entry_name in entries:
        entries = [entry_name]
    if export_path is None:
        fpath = os.path.join(
            os.path.dirname(filename), os.path.basename(filename).split(".")[0]
        )
    else:
        fpath = export_path
    for entry_name in entries:
        with h5py.File(filename, "r") as file:
            entry = file[entry_name]
            entry_name_non_iso = clean_filename(entry_name)
            if export_metadata:
                metadata = h5_group_to_dict(entry)
                fname = os.path.join(fpath, f"{entry_name_non_iso}_metadata.json")
                if not os.path.isdir(os.path.dirname(fname)):
                    os.makedirs(os.path.dirname(fname))
                with open(fname, "w", encoding="utf-8") as json_file:
                    json.dump(metadata, json_file, cls=NumpyEncoder, indent=2)
            if export_data:
                if "data" not in entry:
                    continue
                data = entry["data"]
                export_h5_group_to_csv(
                    data, os.path.join(fpath, entry_name_non_iso, "primary.csv")
                )


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, bytes):
            import base64

            return base64.b64encode(obj).decode("utf-8")
        else:
            return super(NumpyEncoder, self).default(obj)


def h5_group_to_dict(group):
    """

    Parameters
    ----------
    group :


    Returns
    -------

    """
    data = {}
    for k in group.keys():
        if k == "data":
            continue
        if isinstance(group[k], h5py.Group):
            data[k] = h5_group_to_dict(group[k])
        else:
            # read dataset and handle scalar data
            if len(group[k].shape) == 0:
                data[k] = group[k][()]
            else:
                data[k] = group[k][:].tolist()
            # if data[k] is of type bytes, convert it to string
            if isinstance(data[k], bytes):
                data[k] = data[k].decode("utf-8")
    return data


def export_h5_group_to_csv(group, filename):
    import pandas as pd

    arrs = {}
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    for k in group.keys():
        if isinstance(group[k], h5py.Group):
            export_h5_group_to_csv(group[k], f'{filename.split(".")[0]}_{k}.csv')
        elif isinstance(group[k], h5py.Dataset):
            # convert the dataset to a numpy array
            arr = group[k][:]
            # if the array is 2D save it as a dataframe
            if len(arr.shape) == 2:
                df = pd.DataFrame(arr)
                df.to_csv(f'{filename.split(".")[0]}_{k}.csv', sep=",")
            elif len(arr.shape) > 2:
                # Create a MultiIndex for an unknown number of dimensions
                index = pd.MultiIndex.from_product(
                    [range(i) for i in arr.shape],
                    names=[f"dim{i}" for i in range(len(arr.shape))],
                )
                # Flatten the array and create a DataFrame
                arr_flat = arr.flatten()
                df = pd.DataFrame(arr_flat, index=index)
                df.to_csv(f'{filename.split(".")[0]}_{k}.csv', sep=",")
            else:
                arrs[k] = arr
    if arrs:
        try:
            df = pd.DataFrame(arrs)
        except Exception as e:
            print(e)
            return
        df.to_csv(filename, sep=",")


class ExportH5_dialog(QDialog):
    def __init__(self, parent=None):
        from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit

        super().__init__(parent)
        self.setWindowTitle("Export H5 - NOMAD CAMELS")
        layout = QGridLayout()
        self.setLayout(layout)

        self.filename = Path_Button_Edit()
        self.filename.path_changed.connect(self.update_entries)

        label_entry = QLabel("Entry")
        self.entry_name = QComboBox()
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.accept)

        self.checkbox_all_entries = QCheckBox("export all entries")
        self.checkbox_all_entries.stateChanged.connect(self.all_entries)

        self.checkbox_export_to_dir = QCheckBox("export to directory of hdf5 file")
        self.export_path = Path_Button_Edit(select_directory=True)
        self.export_path.setEnabled(False)
        self.checkbox_export_to_dir.stateChanged.connect(self.export_path.setDisabled)
        self.checkbox_export_to_dir.setChecked(True)

        self.checkbox_data = QCheckBox("export data")
        self.checkbox_data.setChecked(True)
        self.checkbox_metadata = QCheckBox("export metadata")
        self.checkbox_metadata.setChecked(True)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(QLabel("hdf5 file"), 0, 0)
        layout.addWidget(self.filename, 0, 1)
        layout.addWidget(label_entry, 1, 0)
        layout.addWidget(self.entry_name, 1, 1)
        layout.addWidget(self.checkbox_all_entries, 2, 0, 1, 2)
        layout.addWidget(self.checkbox_data, 3, 0)
        layout.addWidget(self.checkbox_metadata, 3, 1)
        layout.addWidget(self.checkbox_export_to_dir, 5, 0)
        layout.addWidget(self.export_path, 5, 1)
        layout.addWidget(self.export_button, 10, 0)
        layout.addWidget(self.cancel_button, 10, 1)

        self.show()
        self.adjustSize()

    def all_entries(self):
        if self.checkbox_all_entries.isChecked():
            self.entry_name.setEnabled(False)
        else:
            self.entry_name.setEnabled(True)

    def update_entries(self):
        self.entry_name.clear()
        if not self.filename.get_path():
            return
        with h5py.File(self.filename.get_path(), "r") as file:
            entries = list(file.keys())
        self.entry_name.addItems(entries)

    def accept(self):
        if not self.filename.get_path():
            return
        if self.checkbox_all_entries.isChecked():
            entry = None
        else:
            entry = self.entry_name.currentText()
        export_data = self.checkbox_data.isChecked()
        export_metadata = self.checkbox_metadata.isChecked()
        export_path = (
            self.export_path.get_path()
            if not self.checkbox_export_to_dir.isChecked()
            else None
        )
        export_h5_to_csv_json(
            self.filename.get_path(),
            entry_name=entry,
            export_data=export_data,
            export_metadata=export_metadata,
            export_path=export_path,
        )
        from nomad_camels.ui_widgets.warn_popup import WarnPopup

        WarnPopup(
            text="Successfully exported data to csv and json",
            title="Export successful",
            info_icon=True,
        )
        super().accept()


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
        rundict = {
            "metadata_start": dict(run.metadata["start"]),
            "metadata_stop": dict(run.metadata["stop"]),
            "data": data,
        }
        if to_iso_time:
            stamp = rundict["metadata_start"]["time"]
            rundict["metadata_start"]["time"] = timestamp_to_ISO8601(stamp)
            stamp = rundict["metadata_stop"]["time"]
            rundict["metadata_stop"]["time"] = timestamp_to_ISO8601(stamp)
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
    if timestamp is None:
        return "None"
    from_stamp = dt.fromtimestamp(timestamp)
    return from_stamp.astimezone().isoformat()


def clean_filename(filename):
    """
    cleans the filename from characters that are not allowed

    Parameters
    ----------
    filename : str
        The filename to clean.
    """
    filename = filename.replace(" ", "_")
    filename = filename.replace(".", "_")
    filename = filename.replace(":", "-")
    filename = filename.replace("/", "-")
    filename = filename.replace("\\", "-")
    filename = filename.replace("?", "_")
    filename = filename.replace("*", "_")
    filename = filename.replace("<", "_smaller_")
    filename = filename.replace(">", "_greater_")
    filename = filename.replace("|", "-")
    filename = filename.replace('"', "_quote_")
    return filename
