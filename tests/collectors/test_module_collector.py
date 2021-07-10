import pathlib
from os.path import isfile
from types import ModuleType

from inari.collectors import ModuleCollector
from ward import each, test, using

from . import blank_module
from . import fixtures as target_module


@test("`doc_str` should return correct document.")
@using(
    module=each(target_module, blank_module),
    result=each(
        target_module._mod_expected_docs, "# Module tests.collectors.blank_module"
    ),
    out_dir=target_module._temp_dir,
)
def _(module: ModuleType, result: str, out_dir: str) -> None:
    collector = ModuleCollector(module, out_dir, {})
    assert collector.doc_str() == result


@test("`write` should write docs on expected paths.")
@using(
    module=each(target_module, blank_module),
    out_dir=target_module._temp_dir,
    out_name=each("fixtures-py.md", "blank_module/index.md"),
)
def _(module: ModuleType, out_dir: str, out_name: str) -> None:
    collector = ModuleCollector(module, out_dir, {})
    collector.write()
    expected_path = pathlib.PurePath(out_dir, out_name)
    assert isfile(expected_path)
