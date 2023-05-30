# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../nomad_camels'))

project = 'NOMAD-CAMELS'
# copyright = '2021, FAIRmat'
author = 'jl'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'myst_parser', 'sphinx_copybutton']

templates_path = ['_templates']
exclude_patterns = []

source_suffix = ['.rst', '.md']

master_doc = 'index'

html_favicon = 'assets/CAMELS.ico'

html_logo = 'assets/camels_horizontal.png'
# html_theme_options = {
#     'logo_only': True
# }

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 5
}
html_static_path = ['_static']

html_css_files = {
    'css/custom.css'
}
