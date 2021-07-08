from tempfile import TemporaryDirectory
from typing import Iterator, Type

from ward import fixture


@fixture
def temp_dir() -> Iterator[str]:
    with TemporaryDirectory() as directory:
        yield directory


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


@fixture
def target_class() -> Type[TargetClass]:
    return TargetClass
