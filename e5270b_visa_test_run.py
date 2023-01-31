# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 18:42:02 2023

@author: fulapuser
"""
import sys
sys.path.append(r"C:\Users\fulapuser\Documents\CAMELS")
sys.path.append(r"C:\Users\fulapuser\Documents\CAMELS\devices\devices_drivers")

import numpy as np
import importlib
import bluesky
import ophyd
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
import bluesky.plan_stubs as bps
import databroker
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from epics import caput
import datetime
from main_classes import plot_widget, list_plot, plot_2D
from utility.databroker_export import broker_to_hdf5, broker_to_dict, broker_to_NX
from utility import theme_changing
from bluesky_handling.evaluation_helper import Evaluator
from bluesky_handling import helper_functions
RE = RunEngine()
darkmode = False
theme = "default"

namespace = {}
all_fits = {}
plots = []



from keysight_e5270b.keysight_e5270b_ophyd import Keysight_E5270B



def Unnamed_Protocol_plan_inner(devs, runEngine=None, stream_name="primary"):
    eva = Evaluator(namespace=namespace)
    runEngine.subscribe(eva)
    """"""
    print("starting loop_step Set Channels (Set_Channels)")
    yield from bps.checkpoint()
    print(f'{devs["keysight_e5270b"].enable1}=')
    yield from bps.abs_set(devs["keysight_e5270b"].enable1, 1, group="A")
    yield from bps.wait("A")
    

    """"""
    print("starting loop_step Read Channels (Read_Channels)")
    yield from bps.checkpoint()
    channels_Read_Channels = [devs["keysight_e5270b"].mesV1,devs["keysight_e5270b"].mesI1]
    yield from bps.trigger_and_read(channels_Read_Channels, name=stream_name)



def Unnamed_Protocol_plan(devs, md=None, runEngine=None, stream_name="primary"):
    yield from bps.open_run(md=md)
    yield from Unnamed_Protocol_plan_inner(devs, runEngine, stream_name)
    yield from helper_functions.get_fit_results(all_fits, namespace, True)
    yield from bps.close_run()

def create_plots(RE, stream="primary"):
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    if darkmode:
        plot_widget.activate_dark_mode()
    theme_changing.change_theme(theme, app)
    subs = []
    return app, plots, subs

def steps_add_main(RE):
    returner = {}
    return returner


def main(dark=False, used_theme="default"):
    global darkmode, theme
    darkmode, theme = dark, used_theme
    bec = BestEffortCallback()
    RE.subscribe(bec)
    catalog = databroker.catalog["CAMELS_CATALOG"]
    RE.subscribe(catalog.v1.insert)
    try:

        devs = {}
        device_config = {}
        """keysight_e5270b (Keysight_E5270B):
        """
        settings = {'use_channels': [1,8] ,'resource_name': 'GPIB0::17::INSTR', 'baud_rate': 9600, 'read_termination': '\r\n', 'write_termination': '\r\n'}
        additional_info = {'description': '', 'device_class_name': 'Keysight_E5270B'}
        keysight_e5270b = Keysight_E5270B("lap019:keysight_e5270b:", name="keysight_e5270b", **settings)
        print("connecting keysight_e5270b")
        keysight_e5270b.wait_for_connection()
        config = { 'currComp1': 0.01, 'voltComp1': 0.2, 'VoutRange1': 0, 'IoutRange1': 0, 'VmeasRange1': 0, 'ImeasRange1': 0, 'setADC1': 1, 'outputFilter1': 0,}
        configs = keysight_e5270b.configure(config)[1]
        device_config["keysight_e5270b"] = {}
        device_config["keysight_e5270b"].update(helper_functions.simplify_configs_dict(configs))
        device_config["keysight_e5270b"].update(settings)
        device_config["keysight_e5270b"].update(additional_info)
        devs.update({"keysight_e5270b": keysight_e5270b})
        print("devices connected")
        md = {"devices": device_config, "description": ""}
        md.update({"versions": {"CAMELS": "0.1", "EPICS": "7.0.6.2", "bluesky": bluesky.__version__, "ophyd": ophyd.__version__}})
        md["protocol_overview"] = "Set Channels - {'Channels': ['keysight_e5270b_enable1', 'keysight_e5270b_setV1'], 'Values': ['1', '0.01']}\nRead Channels - ['keysight_e5270b_mesI1', 'keysight_e5270b_mesV1']\n"
        with open(__file__, "r") as f:
            md["python_script"] = f.read()
        md["variables"] = namespace
        plot_dat = None
        md["user"] = {'Name': 'Alexander Fuchs', 'E-Mail': '', 'Affiliation': '', 'Address (affiliation)': '', 'ORCID': '', 'Phone': ''}
        md["sample"] = {'Name': 'Test', 'Identifier': 'test123', 'Preparation-Info': ''}
        additional_step_data = steps_add_main(RE)
        uids = RE(Unnamed_Protocol_plan(devs, md=md, runEngine=RE))
    finally:
        pass


    runs = catalog[uids]
    broker_to_NX(runs, r"C:\Users\fulapuser\CAMELS_data\databroker\CAMELS_CATALOG\data_new.h5", plot_dat)


    app = QCoreApplication.instance()
    print("protocol finished!")
    if app is not None:
        sys.exit(app.exec_())
    return plot_dat, additional_step_data



if __name__ == "__main__":
    main()
