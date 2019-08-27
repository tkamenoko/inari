import importlib
import os
import sys

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from .structs import ModStruct


class Plugin(BasePlugin):
    """
    MkDocs Plugin class.
    """

    # out-dir is config["docs_dir"]
    config_scheme = (
        ("module", config_options.Type(str, required=True)),
        ("out-name", config_options.Type(str, default=None)),
    )

    def on_config(self, config):
        md_ext = config["markdown_extensions"]
        if "attr_list" not in md_ext:
            md_ext.append("attr_list")

    def on_files(self, files, config):
        sys.path.append(os.getcwd())
        out_dir = config["docs_dir"]
        root_name = self.config["module"]
        out_name = self.config["out-name"]
        root_mod = importlib.import_module(root_name)
        mod = ModStruct(root_mod, out_dir, out_name=out_name)
        mod.write()
