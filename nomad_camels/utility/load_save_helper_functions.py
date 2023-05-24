from nomad_camels.frontpanels.plot_definer import Plot_Info, Fit_Info


def load_plots(plots:list, plot_data):
    """

    Parameters
    ----------
    plots:list :
        
    plot_data :
        

    Returns
    -------

    """
    plots.clear()
    for plot_dict in plot_data:
        plot = Plot_Info()
        plots.append(plot)
        for k, v in plot_dict.items():
            if k == 'all_fit':
                fit = Fit_Info()
                plot.__dict__[k] = fit
                for k2, v2 in v.items():
                    fit.__dict__[k2] = v2
            elif k == 'fits':
                fits = []
                plot.__dict__[k] = fits
                for fit_dict in v:
                    fit = Fit_Info()
                    fits.append(fit)
                    for k2, v2 in fit_dict.items():
                        fit.__dict__[k2] = v2
            else:
                plot.__dict__[k] = v
    return plots