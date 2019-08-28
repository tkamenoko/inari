# inari
Write docstrings in Markdown!

```python
# sample.py
"""This is sample module."""

variable = 42
"""(`int`):  Docstrings for module-level variables."""

def func(foo: str, bar: int) -> str:
    """
    Docstrings for functions.

    **Args**

    * foo (`str`): First argument.
    * bar (`int`): Second argument.

    **Returns**

    * `str`: Type of return value.

    """
    return foo * bar

class SampleClass:
    """
    Class docstrings.

    **Attributes**

    * baz (`str`): Docstrings for attributes.

    """
    baz: str

    def __init__(self, b: str):
        """
        **Args**

        * b (`str`): Arguments for initializing.

        """

        self.baz = b

    def method(self, bar: int) -> str:
        """
        Method docstrings.

        Cross reference available. `sample.func`

        **Args**

        * bar(`int`)

        **Returns**

        * `str`

        """
        return func(self.baz, bar)

```

```shell
pip install inari
inari sample docs
# Generate `docs/sample.md` .
```

# Features

* Minimum configuration.
* CLI and [MkDocs](https://www.mkdocs.org/) Plugin.
* Cross reference in API documents.


# License

MIT

# TODO
- [] Cleanup out-dir?
- [] Print superclass
- [] Better document structure
