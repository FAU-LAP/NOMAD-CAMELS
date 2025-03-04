# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys


sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../../"))
sys.path.insert(0, os.path.abspath("../../nomad_camels"))

exclude_patterns = []
print(os.getenv("EXCLUDE_CODE_DIR"))
if os.getenv("EXCLUDE_CODE_DIR") != "true":
    import suitcase.nomad_camels_hdf5

    sys.path.insert(0, suitcase.nomad_camels_hdf5.__path__[0])

project = "NOMAD-CAMELS"
# copyright = '2021, FAIRmat'
author = "FAIRmat"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]

source_suffix = [".rst", ".md"]

master_doc = "index"

html_favicon = "assets/CAMELS.ico"

html_show_copyright = False

html_logo = "assets/camels_horizontal.png"
# html_theme_options = {
#     'logo_only': True
# }

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 5,
                      "collapse_navigation": False}
html_static_path = ["_static"]

html_css_files = {"css/custom.css"}
html_js_files = ["js/custom.js"]
