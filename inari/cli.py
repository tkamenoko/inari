import argparse
import importlib
import os
import sys

from .structures import ModStruct

parser = argparse.ArgumentParser()
parser.add_argument("module", help="root of your module.")
parser.add_argument("out_dir", help="directory to write documents.", metavar="out-dir")
parser.add_argument(
    "-n",
    "--name",
    help="root directry/file name like `{out-dir}/{name}/{submods}` ."
    + " Default: module name.",
)


def run():
    """CLI entry point."""
    sys.path.append(os.getcwd())
    args = parser.parse_args()
    root_name = args.module
    out_dir = args.out_dir
    out_name = args.name
    root_mod = importlib.import_module(root_name)
    # create docs.
    mod = ModStruct(root_mod, out_dir, out_name=out_name)
    mod.write()
