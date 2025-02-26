"""
This module provides functions that are often used when building a protocol.
It is not inside the `protocol_builder` module, since these functions are also
called by the classes of the single protocol-steps.
"""

import copy
from nomad_camels.loop_steps.read_channels import get_channel_string

standard_plot_string = "\tglobal app\n"
standard_plot_string += "\tapp = QCoreApplication.instance()\n"
standard_plot_string += "\tif app is None:\n"
standard_plot_string += "\t\tapp = QApplication(sys.argv)\n"
# standard_plot_string += '\tapp.aboutToQuit.connect(wait_for_workers_to_quit)\n'
standard_plot_string += (
    "\tfrom nomad_camels.main_classes import plot_pyqtgraph, list_plot\n"
)
standard_plot_string += "\tif darkmode:\n"
standard_plot_string += "\t\tplot_pyqtgraph.activate_dark_mode()\n"
# standard_plot_string += '\ttheme_changing.change_theme(theme, app)\n'
# standard_plot_string += '\t\timport qdarkstyle\n'
# standard_plot_string += '\t\tapp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())\n'
# standard_plot_string += '\t\tapp.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))\n'


def get_plot_add_string(name, stream, subprotocol=False, n_tabs=1):
    """
    This function generates the necessary lines for the "steps_add_main"
    function in the protocol-script to open the plots of a sub-step of the
    protocol.

    Parameters
    ----------
    name : str
        The name of the calling protocol-step.

    stream : str
        The bluesky-stream on which the plots should react.

    subprotocol :
         (Default value = False)
         If True, the create_plots function will be called from the
         subprotocol's module.

    Returns
    -------
    add_main_string
        The string to be added.

    """
    tabs = "\t" * n_tabs
    add_main_string = f'{tabs}if "subs" not in returner:\n'
    add_main_string += f'{tabs}\treturner["subs"] = []\n'
    add_main_string += f'{tabs}if "plots" not in returner:\n'
    add_main_string += f'{tabs}\treturner["plots"] = []\n'
    if subprotocol:
        add_main_string += (
            f"{tabs}plots, subs, _, _ = {name}_mod.create_plots(RE, {stream})\n"
        )
    else:
        add_main_string += (
            f"{tabs}plots, subs, _, _ = create_plots_{name}(RE, {stream})\n"
        )
    add_main_string += f'{tabs}returner["subs"] += subs\n'
    add_main_string += f'{tabs}returner["plots"] += plots\n'
    return add_main_string


def flyer_creator(flyer_data, func_name="create_flyers"):
    """
    Creates the `create_flyers` function for the protocol if asynchronous acquisition is used.

    Parameters
    ----------
    flyer_data : list[dict]
        A list of dictionaries with all information for the flyers.

    func_name : str
         (Default value = 'create_flyers')
         The name of the function in the protocol-script.

    Returns
    -------
    flyer_string
        The string containing the function for the protocol-script.

    """
    flyer_string = f"\ndef {func_name}(devs):\n"
    if not flyer_data:
        flyer_string += "\treturn []\n\n"
        return flyer_string
    flyer_string += (
        "\tfrom nomad_camels.bluesky_handling.flyer_interface import CAMELS_Flyer\n"
    )
    for i, flyer in enumerate(flyer_data):
        detectors = []
        for c in flyer["channels"]["channel"]:
            detectors.append(get_channel_string(c))
        flyer_string += f'\tflyer_{i} = CAMELS_Flyer(name="{flyer["name"]}", read_time={flyer["read_rate"]}, detectors=['
        for j, det in enumerate(detectors):
            flyer_string += f"{det}"
        flyer_string += "], "
        flyer_string += f"can_fail={flyer['channels']['ignore failed']})\n"
        flyer_string += f"\tflyers.append(flyer_{i})\n"
    flyer_string += "\treturn flyers\n\n"
    return flyer_string


def plot_creator(
    plot_data,
    func_name="create_plots",
    multi_stream=False,
    plot_is_box=False,
    box_names="",
    skip_box=True,
):
    """
    Creates the `create_plots` function for the protocol.

    Parameters
    ----------
    plot_data : list[Plot_Info]
        A list of Plot_Info objects with all information for the plots.

    func_name : str
         (Default value = 'create_plots')
         The name of the function in the protocol-script.

    multi_stream :
         (Default value = False)
         Passes the multi_stream keyword to the plot-widgets. This is used if
         the plot should not only react to the stream that's specified exactly.

    Returns
    -------
    plot_string
        The string containing the function for the protocol-script.

    plotting
        True if there actually was a plot. Otherwise the function will not be
        created in the script at all.


    """
    plot_string = f'\ndef {func_name}(RE, stream="primary"):\n'
    if not plot_data:
        plot_string += "\treturn [], [], None, None\n\n"
        return plot_string, False
    plot_string += standard_plot_string
    plot_string += "\tplot_evaluator=eva\n"
    plot_string += "\tsubs = []\n"
    plotting = False
    for i, plot in enumerate(plot_data):
        if (
            plot.checkbox_show_in_browser
            and "from nomad_camels.main_classes import plot_plotly" not in plot_string
        ):
            plot_string += "\tfrom nomad_camels.main_classes import plot_plotly\n"
        if plot.plt_type == "X-Y plot":
            plotting = True
            fits = []
            if plot.same_fit:
                if plot.all_fit and plot.all_fit.do_fit:
                    for y in plot.y_axes["formula"]:
                        fit = copy.deepcopy(plot.all_fit)
                        fit.y = y
                        fits.append(fit)
            else:
                for fit in plot.fits:
                    if fit.do_fit:
                        fits.append(fit)
            plot_string += "\tfits = []\n"
            for fit in fits:
                plot_string += f"\tfits.append({fit.__dict__})\n"
            y_axes = {}
            ylabel2 = plot.ylabel2 if plot.ylabel2 else ""
            for j, f in enumerate(plot.y_axes["formula"]):
                y_axes[f] = 2 if plot.y_axes["axis"][j] == "right" else 1
                if not ylabel2 and y_axes[f] == 2:
                    ylabel2 = f
            xlabel = plot.xlabel if plot.xlabel else plot.x_axis or "time"
            ylabel = plot.ylabel if plot.ylabel else plot.y_axes["formula"][0]
            plot_string += f'\tplot_info = dict(x_name="{plot.x_axis or "time"}", y_names={plot.y_axes["formula"]}, ylabel="{ylabel}", xlabel="{xlabel}", title="{plot.title}", stream_name=stream, evaluator=plot_evaluator, fits=fits, multi_stream={multi_stream}, y_axes={y_axes}, ylabel2="{ylabel2}", logX={plot.logX}, logY={plot.logY}, logY2={plot.logY2}, maxlen="{plot.maxlen}", manual_plot_position={plot.checkbox_manual_plot_position}, top_left_x="{plot.top_left_x}", top_left_y="{plot.top_left_y}", plot_width="{plot.plot_width}", plot_height="{plot.plot_height}", show_in_browser="{plot.checkbox_show_in_browser}", web_port={plot.browser_port})\n'
            plot_string += f"\tplot_{i} = plot_pyqtgraph.PlotWidget(**plot_info)\n"
            plot_string += f"\tplots.append(plot_{i})\n"
            # plot_string += f"\tplot_data.append(plot_info)\n"
            plot_string += f"\tplot_{i}.show()\n"
            plot_string += f"\tsubs.append(RE.subscribe(plot_{i}.livePlot))\n"
            if plot.checkbox_show_in_browser:
                plot_string += f"\tplot_info_dash_{i}=plot_info\n"
                plot_string += (
                    f"\tplot_info_dash_{i}['web_port'] = {plot.browser_port}\n"
                )
                plot_string += f"\tplot_plotly_{i} = plot_plotly.PlotlyLiveCallback(**plot_info_dash_{i})\n"
                plot_string += f"\tplots_plotly.append(plot_plotly_{i})\n"
                plot_string += f"\tsubs.append(RE.subscribe(plot_plotly_{i}))\n"
            plot_string += f"\tfor fit in plot_{i}.liveFits:\n"
            plot_string += "\t\tall_fits[fit.name] = fit\n"
            # plot_string += f'\tfor lfp in plot_{i}.liveFitPlots:\n'
            # plot_string += f'\t\tsubs.append(RE.subscribe(lfp))\n'
        elif plot.plt_type == "Value-List":
            plotting = True
            plot_string += f'\tplot_{i} = list_plot.Values_List_Plot({plot.y_axes["formula"]}, title="{plot.title}", stream_name=stream, namespace=namespace, plot_all_available={plot.plot_all_available}, top_left_x="{plot.top_left_x}", top_left_y="{plot.top_left_y}", plot_width="{plot.plot_width}", plot_height="{plot.plot_height}")\n'
            plot_string += f"\tplots.append(plot_{i})\n"
            plot_string += f"\tplot_{i}.show()\n"
            plot_string += f"\tsubs.append(RE.subscribe(plot_{i}.livePlot))\n"
        elif plot.plt_type == "2D plot":
            plotting = True
            plot_string += f'\tplot_{i} = plot_pyqtgraph.PlotWidget_2D("{plot.x_axis}", "{plot.y_axes["formula"][0]}", "{plot.z_axis}", xlabel="{plot.xlabel}", ylabel="{plot.ylabel}", zlabel="{plot.zlabel}", title="{plot.title}", maxlen="{plot.maxlen}", stream_name=stream, evaluator=eva, manual_plot_position={plot.checkbox_manual_plot_position}, top_left_x="{plot.top_left_x}", top_left_y="{plot.top_left_y}", plot_width="{plot.plot_width}", plot_height="{plot.plot_height}")\n'
            plot_string += f"\tplots.append(plot_{i})\n"
            plot_string += f"\tplot_{i}.show()\n"
            plot_string += f"\tsubs.append(RE.subscribe(plot_{i}.livePlot))\n"
            if plot.checkbox_show_in_browser:
                plot_string += f'\tplot_plotly_{i} = plot_plotly.PlotlyLiveCallback_2d(x_name="{plot.x_axis}", y_name="{plot.y_axes["formula"][0]}", z_name="{plot.z_axis}", xlabel="{plot.xlabel}", ylabel="{plot.ylabel}", zlabel="{plot.zlabel}", web_port={plot.browser_port}, evaluator=eva, title="{plot.title}", maxlen="{plot.maxlen}", stream_name=stream, namespace=namespace, top_left_x="{plot.top_left_x}", top_left_y="{plot.top_left_y}", plot_width="{plot.plot_width}", plot_height="{plot.plot_height}")\n'
                plot_string += f"\tplots_plotly.append(plot_plotly_{i})\n"
                plot_string += f"\tsubs.append(RE.subscribe(plot_plotly_{i}))\n"
        if plot_is_box:
            plot_string += f"\tboxes['{box_names}_{i}'] = helper_functions.Waiting_Bar(title='{plot.title}', skipable={skip_box}, display_bar=False, plot=plot_{i})\n"
    plot_string += "\treturn plots, subs, app, plots_plotly\n\n"
    return plot_string, plotting
