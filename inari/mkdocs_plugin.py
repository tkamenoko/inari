import importlib
import os
import sys
from typing import Any, Callable, Optional

from mkdocs.config import Config, config_options
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin

from .collectors import ModuleCollector


class Plugin(BasePlugin):
    """
    MkDocs Plugin class.
    """

    _root_module: Optional[ModuleCollector] = None

    # out-dir is config["docs_dir"]
    config_scheme = (
        ("module", config_options.Type(str, required=True)),
        ("out-name", config_options.Type(str, default=None)),
    )

    def root_module(self, config: Config) -> ModuleCollector:
        if not self._root_module:
            out_dir = config["docs_dir"]
            out_name = self.config["out-name"]
            root_name = self.config["module"]
            _root_module = importlib.import_module(root_name)
            self._root_module = ModuleCollector(
                _root_module, out_dir, out_name=out_name, enable_yaml_header=True
            )

        return self._root_module

    def on_config(self, config: Config, **kw: Any) -> Config:
        md_ext = config.get("markdown_extensions", [])
        if "attr_list" not in md_ext:
            md_ext.append("attr_list")
        if "meta" not in md_ext:
            md_ext.append("meta")
        config["markdown_extantions"] = md_ext
        return config

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

    def on_pre_build(self, config: Config) -> None:
        """Build markdown docs from python modules."""
        self._build(config)

    def _build(self, config: Config) -> None:
        cwd = os.getcwd()
        if cwd not in sys.path:
            sys.path.append(cwd)

        # create docs.
        self.root_module(config).write()
