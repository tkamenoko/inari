import sys
import os
import importlib

from .structs import ModStruct


def run():
    sys.path.append(os.getcwd())
    root_name, out_dir, *out_name = sys.argv[1:]
    if out_name:
        name = out_name[-1]
    else:
        name = ""
    root_mod = importlib.import_module(root_name)
    mod = ModStruct(root_mod, out_dir, out_name=name)
    mod.write()


if __name__ == "__main__":
    run()
