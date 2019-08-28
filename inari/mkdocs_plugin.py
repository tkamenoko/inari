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

    def on_serve(self, server, config):
        # build docs once.
        self._build(config)
        # add watcher.
        module_path = self.config["module"].replace(".", "/")
        if module_path not in server.watcher._tasks:
            server.watch(module_path, lambda: self._build(config), delay="forever")
        return server

    def on_config(self, config):
        md_ext = config["markdown_extensions"]
        if "attr_list" not in md_ext:
            md_ext.append("attr_list")
        return config

    def on_files(self, files, config):
        # run only on `mkdocs build`
        # TODO: this is workaround.
        args = [x for x in sys.argv if not x.startswith("-")]
        command = args[1]
        if command == "build":
            self._build(config)
        return

    def _build(self, config):
        sys.path.append(os.getcwd())
        out_dir = config["docs_dir"]
        root_name = self.config["module"]
        out_name = self.config["out-name"]
        root_mod = importlib.import_module(root_name)
        mod = ModStruct(root_mod, out_dir, out_name=out_name)
        mod.write()
