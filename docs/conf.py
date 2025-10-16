# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "somerandomapi.py"
copyright = "2023-2025, Soheab_"
author = "Soheab_"
release = "0.1.3"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
from typing import Any


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "enum_tools.autoenum",
]


templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# These folders are copied to the documentation's HTML output
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "css/custom.css",
]

autodoc_default_options = {
    "members": True,
    #'undoc-members': False,
    #'inherited-members': True,
    "special-members": False,
    "exclude-members": "from_dict, to_dict, construct, __init__, _data, _http, __http, http",
}
# Links used for cross-referencing stuff in other documentation
intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "aio": ("https://docs.aiohttp.org/en/stable/", None),
}

extlinks = {
    "apidocs": ("https://some-random-api.com/docs/%s", None),
}


viewcode_follow_imported_members = True
autoclass_signature = "separated"
autodoc_typehints_format = "short"
autodoc_member_order = "alphabetical"
autoclass_content = "class"
autodoc_typehints_description_target = "documented_params"
always_document_param_types = False
sphinx_autodoc_typehints = True
typehints_use_signature_return = False
napoleon_use_param = True
autodoc_typehints = "none"
autodoc_class_signature = "separated"
typehints_use_signature = False

# kept getting the following warnings:
# WARNING: py:class reference target not found: _io.BytesIO
# WARNING: py:class reference target not found: somerandomapi.models.image.FileLike
# somerandomapi.errors.TypingError:15: WARNING: py:class reference target not found: Attribute [ref.class]
# and these two lines seemed to fix it.
nitpicky = True
# fmt: off
nitpick_ignore = [
    ("py:class", "_io.BytesIO"),
    ("py:class", "somerandomapi.models.image.FileLike"),
    ("py:class", "Attribute")
]
# fmt: on

def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation) -> tuple[Any, Any]:
    if obj.__class__.__name__ == "Attribute":
        # hides the "= <object xxxx Attribute>" part from the signature, that's only used internally.
        options["no-value"] = True
        return "", return_annotation
    return signature, return_annotation


def setup(app):
    app.connect("autodoc-process-signature", autodoc_process_signature)