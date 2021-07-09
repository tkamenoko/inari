from inari.collectors import VariableCollector
from ward import test, using

from .fixtures import target_variable, _var_expected_docs, temp_dir, _var_doc


@test("`doc_str` should return correct document.")
@using(
    variable=target_variable, docs=_var_doc, result=_var_expected_docs, out_dir=temp_dir
)
def _(variable: str, docs: str, result: str, out_dir: str) -> None:
    # No way to set docstrings to variables.
    collector = VariableCollector(
        variable, {}, out_dir, doc=docs, name="target_variable"
    )
    assert collector.doc_str() == result
