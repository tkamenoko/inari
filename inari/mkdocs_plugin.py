import importlib
import os
import shutil
import sys

from mkdocs.config import config_options
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

    def on_serve(self, server, config):
        def hook():
            self._clean(config)
            self._build(config)

        # build docs once.
        hook()
        # add watcher.
        module_path = self.config["module"].replace(".", "/")
        if module_path not in server.watcher._tasks:
            server.watch(module_path, hook, delay="forever")
        return server

    def on_config(self, config):
        md_ext = config["markdown_extensions"]
        if "attr_list" not in md_ext:
            md_ext.append("attr_list")
        return config

    def on_pre_build(self, config):
        # run only on `mkdocs build`
        # TODO: this is workaround.
        args = [x for x in sys.argv if not x.startswith("-")]
        command = args[1]
        if command == "build":
            self._clean(config)
            self._build(config)

    def _clean(self, config):
        # clean old docs.
        out_dir = config["docs_dir"]
        root_name = self.config["module"]
        out_name = self.config["out-name"]
        old_file = os.path.join(out_dir, (out_name or root_name + "-py") + ".md")
        if os.path.exists(old_file):
            os.remove(old_file)
        old_dir = os.path.join(out_dir, (out_name or root_name))
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir)

    def _build(self, config):
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
