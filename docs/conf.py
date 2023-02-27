# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Dash Tradingview Lightweight Charts Component'
copyright = '2023, Tyson Wu'
author = 'Tyson Wu'

# The full version, including alpha/beta/rc tags
release = 'v0.1.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_context = {
    'default_mode': 'auto'
}

html_theme_options = {
    "source_repository": "https://github.com/tysonwu/dash-tradingview/",
    "source_branch": "master",
    "source_directory": "docs/",
#     "repository_url": "https://github.com/tysonwu/dash-tradingview",
#     "icon_links": [
#         {
#             "name": "PyPI",
#             "url": "https://pypi.org/project/dash-tvlwc/",
#             "icon": "fa-solid fa-box",
#         },
#     ],
#     "use_edit_page_button": True,
#     "use_issues_button": True,
#     "use_repository_button": True,
#     "use_download_button": True,
#     "show_toc_level": 2,
#     # "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
#     # "navbar_center": ["version-switcher", "navbar-nav"],
#     # "navbar_end": ["navbar-icon-links"]
}