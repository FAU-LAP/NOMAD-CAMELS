import os
import sys

import databroker

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from nomad-camels.utility import load_save_functions

def make_yml(datapath, catalog_name='CAMELS_CATALOG'):
    catalog_path = databroker.catalog_search_path()[0]
    if not os.path.isdir(catalog_path):
        os.makedirs(catalog_path)
    fname = f'{catalog_path}/{catalog_name}.yml'
    brokerpath = f'{datapath}/databroker/{catalog_name}'
    with open(fname, 'w') as f:
        f.write('sources:\n'
                f'  {catalog_name}:\n'
                '    driver: "bluesky-msgpack-catalog"\n'
                '    args:\n'
                '      paths:\n'
                f'        - "{brokerpath}/*.msgpack"')
    if not os.path.isdir(brokerpath):
        os.makedirs(brokerpath)


if __name__ == '__main__':
    make_yml(load_save_functions.standard_pref['meas_files_path'])
