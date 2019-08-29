# inari
Write docstrings in Markdown!

[This API documents](./api) are created by `inari` itself.

```shell
# create `inari` documents!
git clone https://github.com/tkamenoko/inari.git
cd inari
poetry install
poetry run mkdocs build
```


## Docstrings Example

```python
# sample.py
"""This is a sample module."""

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
 
## Features

* Minimum configuration.
* No dependencies by default.
* [CLI](./getting-started#use-cli) and [MkDocs Plugin](./getting-started#use-mkdocs-plugin) .
* Cross reference in API documents.


## License

MIT
