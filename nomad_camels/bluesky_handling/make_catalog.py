import os
import pathlib

import databroker

from nomad_camels.utility import load_save_functions

def make_yml(datapath, catalog_name='CAMELS_CATALOG', restart_fail=False):
    """

    Parameters
    ----------
    datapath :
        
    catalog_name :
         (Default value = 'CAMELS_CATALOG')

    restart_fail :
        (Default value = False)

    Returns
    -------

    """
    catalog_path = databroker.catalog_search_path()[0]
    if not isinstance(datapath, pathlib.Path):
        datapath = pathlib.Path(datapath)
    if not isinstance(catalog_path, pathlib.Path):
        catalog_path = pathlib.Path(catalog_path)
    if not os.path.isdir(catalog_path):
        os.makedirs(catalog_path)
    fname = (catalog_path / catalog_name).with_suffix('.yml')
    brokerpath = datapath / 'databroker' / catalog_name
    if not os.path.isdir(brokerpath):
        os.makedirs(brokerpath)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('sources:\n'
                f'  {catalog_name}:\n'
                '    driver: "bluesky-msgpack-catalog"\n'
                '    args:\n'
                '      paths:\n'
                f'        - "{brokerpath.as_posix()}/*.msgpack"')
    if catalog_name not in list(databroker.catalog):
        databroker.catalog.force_reload()
    if catalog_name not in list(databroker.catalog) and restart_fail:
        from nomad_camels.utility import update_camels
        update_camels.restart_camels(ask_restart=False)


if __name__ == '__main__':
    make_yml(load_save_functions.standard_pref['meas_files_path'], 'test')
