import copy

standard_plot_string = '\tapp = QCoreApplication.instance()\n'
standard_plot_string += '\tif app is None:\n'
standard_plot_string += '\t\tapp = QApplication(sys.argv)\n'
# standard_plot_string += '\tapp.aboutToQuit.connect(wait_for_workers_to_quit)\n'
standard_plot_string += '\tif darkmode:\n'
standard_plot_string += '\t\tplot_widget.activate_dark_mode()\n'
# standard_plot_string += '\ttheme_changing.change_theme(theme, app)\n'
# standard_plot_string += '\t\timport qdarkstyle\n'
# standard_plot_string += '\t\tapp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())\n'
# standard_plot_string += '\t\tapp.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))\n'


def get_plot_add_string(name, stream, subprotocol=False):
    """

    Parameters
    ----------
    name :
        
    stream :
        
    subprotocol :
         (Default value = False)

    Returns
    -------

    """
    add_main_string = '\tif "subs" not in returner:\n'
    add_main_string += '\t\treturner["subs"] = []\n'
    add_main_string += '\tif "plots" not in returner:\n'
    add_main_string += '\t\treturner["plots"] = []\n'
    if subprotocol:
        add_main_string += f'\tplots, subs, _ = {name}_mod.create_plots(RE, {stream})\n'
    else:
        add_main_string += f'\tplots, subs, _ = create_plots_{name}(RE, {stream})\n'
    add_main_string += '\treturner["subs"] += subs\n'
    add_main_string += '\treturner["plots"] += plots\n'
    return add_main_string



def plot_creator(plot_data, func_name='create_plots', multi_stream=False):
    """

    Parameters
    ----------
    plot_data :
        
    func_name :
         (Default value = 'create_plots')
    multi_stream :
         (Default value = False)

    Returns
    -------

    """
    plot_string = f'\ndef {func_name}(RE, stream="primary"):\n'
    plot_string += standard_plot_string
    plot_string += '\tsubs = []\n'
    plotting = False
    for i, plot in enumerate(plot_data):
        if plot.plt_type == 'X-Y plot':
            plotting = True
            fits = []
            if plot.same_fit:
                if plot.all_fit and plot.all_fit.do_fit:
                    for y in plot.y_axes['formula']:
                        fit = copy.deepcopy(plot.all_fit)
                        fit.y = y
                        fits.append(fit)
            else:
                for fit in plot.fits:
                    if fit.do_fit:
                        fits.append(fit)
            plot_string += '\tfits = []\n'
            for fit in fits:
                plot_string += f'\tfits.append({fit.__dict__})\n'
            plot_string += f'\tplot_{i} = plot_widget.PlotWidget(x_name="{plot.x_axis or "time"}", y_names={plot.y_axes["formula"]}, ylabel="{plot.ylabel}", xlabel="{plot.xlabel}", title="{plot.title}", stream_name=stream, namespace=namespace, fits=fits, multi_stream={multi_stream})\n'
            plot_string += f'\tplots.append(plot_{i})\n'
            plot_string += f'\tplot_{i}.show()\n'
            plot_string += f'\tsubs.append(RE.subscribe(plot_{i}.livePlot))\n'
            plot_string += f'\tfor fit in plot_{i}.liveFits:\n'
            plot_string += '\t\tall_fits[fit.name] = fit\n'
            # plot_string += f'\tfor lfp in plot_{i}.liveFitPlots:\n'
            # plot_string += f'\t\tsubs.append(RE.subscribe(lfp))\n'
        elif plot.plt_type == 'Value-List':
            plotting = True
            plot_string += f'\tplot_{i} = list_plot.Values_List_Plot({plot.y_axes["formula"]}, title="{plot.title}", stream_name=stream, namespace=namespace)\n'
            plot_string += f'\tplots.append(plot_{i})\n'
            plot_string += f'\tplot_{i}.show()\n'
            plot_string += f'\tsubs.append(RE.subscribe(plot_{i}))\n'
        elif plot.plt_type == '2D plot':
            plotting = True
            plot_string += f'\tplot_{i} = plot_2D.PlotWidget_2D("{plot.x_axis}", "{plot.y_axes["formula"][0]}", "{plot.z_axis}", xlabel="{plot.xlabel}", ylabel="{plot.ylabel}", zlabel="{plot.zlabel}", title="{plot.title}", stream_name=stream, namespace=namespace)\n'
            plot_string += f'\tplots.append(plot_{i})\n'
            plot_string += f'\tplot_{i}.show()\n'
            plot_string += f'\tsubs.append(RE.subscribe(plot_{i}.livePlot))\n'
    plot_string += '\treturn plots, subs, app\n\n'
    return plot_string, plotting