from inari.collectors import FunctionCollector
from ward import each, test, using

from .fixtures import _func_expected_doc, target_function, temp_dir


@test("`doc_str` should return correct document.")
@using(out_dir=temp_dir, result=each(_func_expected_doc))
def _(out_dir: str, result: str) -> None:
    collector = FunctionCollector(target_function, {}, out_dir)
    assert collector.doc_str() == result
