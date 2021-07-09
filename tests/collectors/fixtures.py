from inspect import cleandoc
from tempfile import TemporaryDirectory
from typing import Iterator

from ward import fixture


@fixture
def _temp_dir() -> Iterator[str]:
    with TemporaryDirectory() as directory:
        yield directory


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


_func_expected_doc = """
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
_func_expected_doc = cleandoc(_func_expected_doc)


class TargetClass(object):
    """
    Document for this class.

    **Attributes**

    * num (`int`): number.
    * foo (`str`): string.

    """

    num: int
    foo: str

    _expected_doc = """
    ### TargetClass {: #TargetClass }

    ```python
    class TargetClass(self, num: int, foo: str)
    ```

    Document for this class.

    **Attributes**

    * **num** (`int`): number.
    * **foo** (`str`): string.

    **Args**

    * **num** (`int`): number.
    * **foo** (`str`): string.

    ------

    #### Instance attributes {: #TargetClass-attrs }

    * **instance_attr**{: #TargetClass.instance_attr } (`str`): Should be documented.

    ------

    #### Methods {: #TargetClass-methods }

    [**method1**](#TargetClass.method1){: #TargetClass.method1 }

    ```python
    def method1(self, *args: str) -> list[str]
    ```

    Method documents.

    **Args**

    * **args** (`str`): Variadic arguments.

    **Returns**

    * `list[str]`: Return given args.
    """.strip()

    def __init__(self, num: int, foo: str) -> None:
        """
        **Args**

        * num (`int`): number.
        * foo (`str`): string.

        """
        self.num = num
        self.foo = foo

    @property
    def instance_attr(self) -> str:
        """
        (`str`): Should be documented.
        """
        return ""

    def method1(self, *args: str) -> list[str]:
        """
        Method documents.

        **Args**

        * args (`str`): Variadic arguments.

        **Returns**

        * `list[str]`: Return given args.
        """
        return [*args]

    def _should_be_ignored(self) -> None:
        """
        This document should be ignored.
        """
        return


"""(`str`): variable docs."""
target_variable = "lorem"

_var_doc = """(`str`): variable docs."""
_var_expected_docs = (
    "* **target_variable**{: #target_variable } (`str`): variable docs."
)
