import copy

standard_plot_string = '\tapp = QCoreApplication.instance()\n'
standard_plot_string += '\tif app is None:\n'
standard_plot_string += '\t\tapp = QApplication(sys.argv)\n'
# standard_plot_string += '\tapp.aboutToQuit.connect(wait_for_workers_to_quit)\n'
standard_plot_string += '\tif "--darkmode" in sys.argv:\n'
standard_plot_string += '\t\tplot_widget.activate_dark_mode()\n'
standard_plot_string += '\t\timport qdarkstyle\n'
standard_plot_string += '\t\tapp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())\n'
standard_plot_string += '\t\tapp.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))\n'
standard_plot_string += '\tplots = []\n'

def plot_creator(plot_data, func_name='create_plots'):
    plot_string = f'\ndef {func_name}(RE, stream="primary"):\n'
    plot_string += standard_plot_string
    plot_string += '\tsubs = []\n'
    plotting = False
    for i, plot in enumerate(plot_data):
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
        plot_string += f'\tplot_{i} = plot_widget.PlotWidget(x_name="{plot.x_axis or "time"}", y_names={plot.y_axes["formula"]}, ylabel="{plot.ylabel}", xlabel="{plot.xlabel}", title="{plot.title}", stream_name=stream, namespace=namespace, fits=fits)\n'
        plot_string += f'\tplots.append(plot_{i})\n'
        plot_string += f'\tplot_{i}.show()\n'
        plot_string += f'\tsubs.append(RE.subscribe(plot_{i}.livePlot))\n'
        # plot_string += f'\tfor lfp in plot_{i}.liveFitPlots:\n'
        # plot_string += f'\t\tsubs.append(RE.subscribe(lfp))\n'
    plot_string += '\treturn app, plots, subs\n\n'
    return plot_string, plotting