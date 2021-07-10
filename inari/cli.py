import argparse
import importlib
import os
import sys

from .collectors import ModuleCollector

parser = argparse.ArgumentParser()
parser.add_argument("module", help="root of your module.")
parser.add_argument("out_dir", help="directory to write documents.", metavar="out-dir")
parser.add_argument(
    "-n",
    "--name",
    help="root directory/file name like `{out-dir}/{name}/{submods}` ."
    + " Default: module name.",
)
parser.add_argument(
    "-y",
    "--enable-yaml-header",
    help="deciding whether to include yaml header. Default: `False`.",
    action="store_true",
)


def run() -> None:
    """CLI entry point."""
    sys.path.append(os.getcwd())
    args = parser.parse_args()
    root_name = args.module
    out_dir = args.out_dir
    out_name = args.name
    enable_yaml_header = args.enable_yaml_header
    root_mod = importlib.import_module(root_name)
    # create docs.
    mod = ModuleCollector(
        root_mod, out_dir, out_name=out_name, enable_yaml_header=enable_yaml_header
    )
    mod.write()
