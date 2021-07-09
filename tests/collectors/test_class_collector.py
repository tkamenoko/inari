from inspect import cleandoc

from inari.collectors import ClassCollector
from ward import each, test, using

from .fixtures import TargetClass, temp_dir


@test("`doc_str` should return correct document.")
@using(cls=each(TargetClass), out_dir=temp_dir)
def _(cls: type, out_dir: str) -> None:
    collector = ClassCollector(cls, out_dir, {})
    assert collector.doc_str() == cleandoc(getattr(cls, "_expected_doc"))
