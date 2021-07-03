import importlib
import os
import sys
from typing import Any, Callable

from mkdocs.config import Config, config_options
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin

from .structures import ModStruct


class Plugin(BasePlugin):
    """
    MkDocs Plugin class.
    """

    # out-dir is config["docs_dir"]
    config_scheme = (
        ("module", config_options.Type(str, required=True)),
        ("out-name", config_options.Type(str, default=None)),
    )

    def on_serve(
        self,
        server: LiveReloadServer,
        config: Config,
        builder: Callable[[], None],
        **kw: Any
    ) -> LiveReloadServer:
        self._build(config)
        # add watching path.
        module_path = self.config["module"].replace(".", "/")
        server.watch(module_path)
        return server

    def on_config(self, config: Config, **kw: Any) -> Config:
        md_ext = config["markdown_extensions"]
        if "attr_list" not in md_ext:
            md_ext.append("attr_list")
        return config

    def on_pre_build(self, config: Config) -> None:
        self._build(config)

    def _build(self, config: Config) -> None:
        cwd = os.getcwd()
        if cwd not in sys.path:
            sys.path.append(cwd)
        out_dir = config["docs_dir"]
        root_name = self.config["module"]
        out_name = self.config["out-name"]
        root_mod = importlib.import_module(root_name)
        root_mod = importlib.reload(root_mod)
        # create docs.
        mod = ModStruct(root_mod, out_dir, out_name=out_name)
        mod.write()
