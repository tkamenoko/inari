import sys
import os
import importlib
import argparse

from .structs import ModStruct

parser = argparse.ArgumentParser()
parser.add_argument("module", help="root of your module.")
parser.add_argument("out_dir", help="directory to write documents.", metavar="out-dir")
parser.add_argument(
    "-n",
    "--name",
    help="name of root directry, like `{out-dir}/{name}/{submods}` ."
    + " Default: module name.",
)


def run():
    sys.path.append(os.getcwd())
    args = parser.parse_args()
    root_name = args.module
    out_dir = args.out_dir
    out_name = args.name
    root_mod = importlib.import_module(root_name)
    mod = ModStruct(root_mod, out_dir, out_name=out_name)
    mod.write()


if __name__ == "__main__":
    run()
