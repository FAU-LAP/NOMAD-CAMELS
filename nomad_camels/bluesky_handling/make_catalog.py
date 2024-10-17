""""""

import os
import pathlib

import databroker

from nomad_camels.utility import load_save_functions, update_camels
from nomad_camels.ui_widgets.warn_popup import WarnPopup


def make_yml(datapath, catalog_name="CAMELS_CATALOG", ask_restart=False):
    """
    Creates the yml file for the databroker (where it is looking for them) to
    configure a simple catalog for measurements with CAMELS.

    Parameters
    ----------
    datapath : str, path
        The path where the measurement data of the catalog should be saved to.
    catalog_name : str
         (Default value = 'CAMELS_CATALOG')
         The name, the catalog should have.
    """
    catalog_path = databroker.catalog_search_path()[0]
    if not isinstance(datapath, pathlib.Path):
        datapath = pathlib.Path(datapath)
    if not isinstance(catalog_path, pathlib.Path):
        catalog_path = pathlib.Path(catalog_path)
    if not os.path.isdir(catalog_path):
        os.makedirs(catalog_path)
    fname = (catalog_path / catalog_name).with_suffix(".yml")
    brokerpath = datapath / "databroker" / catalog_name
    if not os.path.isdir(brokerpath):
        os.makedirs(brokerpath)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(
            "sources:\n"
            f"  {catalog_name}:\n"
            '    driver: "bluesky-msgpack-catalog"\n'
            "    args:\n"
            "      paths:\n"
            f'        - "{brokerpath.as_posix()}/*.msgpack"'
        )
    if catalog_name not in list(databroker.catalog):
        databroker.catalog.force_reload()
    if ask_restart and catalog_name not in list(databroker.catalog):
        WarnPopup(
            text="Could not load the databroker catalog, you might have to restart CAMELS",
            title="Databroker catalog not loaded",
        )
        update_camels.restart_camels(ask_restart=True)
