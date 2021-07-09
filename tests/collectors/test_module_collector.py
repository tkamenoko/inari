from types import ModuleType

from inari.collectors import ModuleCollector
from ward import each, test, using

from . import fixtures as target_module


@test("`doc_str` should return correct document.")
@using(
    module=each(target_module),
    result=each(target_module._mod_expected_docs),
    out_dir=target_module._temp_dir,
)
def _(module: ModuleType, result: str, out_dir: str) -> None:
    collector = ModuleCollector(module, out_dir, {})
    assert collector.doc_str() == result
