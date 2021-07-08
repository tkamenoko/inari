from inspect import cleandoc

from inari.collectors import FunctionCollector
from ward import fixture, test, using

from .fixtures import temp_dir


def target_function(
    foo: str, bar: int, /, baz: bool, spam: str = "foobar", *, egg: bytes = b""
) -> dict[str, str]:
    """
    This function is a test fixture.

    **Args**

    * foo (`str`): Lorem ipsum.
    * bar (`int`): *italic*
    * baz (`bool`): **emphasize**
    * spam (`str`): Multiline description
        should be indented.
    * egg (`bytes`): `backtick`

    **Returns**

    * `dict[str, str]`: Return type.

    """
    return {"return": "dict"}


@fixture
def expected_doc() -> str:
    doc = """
    ### target_function {: #target_function }

    ```python
    def target_function(
        foo: str, bar: int, /, baz: bool, spam: str = "foobar", *, egg: bytes = b""
    ) -> dict[str, str]
    ```

    This function is a test fixture.

    **Args**

    * **foo** (`str`): Lorem ipsum.
    * **bar** (`int`): *italic*
    * **baz** (`bool`): **emphasize**
    * **spam** (`str`): Multiline description
        should be indented.
    * **egg** (`bytes`): `backtick`

    **Returns**

    * `dict[str, str]`: Return type.
    """
    return cleandoc(doc)


@test("`doc_str` should return correct document.")
@using(out_dir=temp_dir, result=expected_doc)
def _(out_dir: str, result: str) -> None:
    collector = FunctionCollector(target_function, {}, out_dir)
    assert collector.doc_str() == result
