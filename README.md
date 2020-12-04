# inari

Write docstrings in Markdown!

# Features

- Minimum configuration.
- No dependencies by default(but [MkDocs](https://www.mkdocs.org/) is recommended!).
- CLI and MkDocs Plugin.
- Cross reference in API documents.

# Install

```shell
pip install inari[mkdocs]
```

# Example

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
inari sample docs
```

`inari` makes this Markdown file:

````markdown
<!-- docs/sample-py.md -->

# Module sample

This is a sample module.

## Variables

- **variable**{: #variable } (`int`): Docstrings for module-level variables.

## Classes

### SampleClass {: #SampleClass }

```python
class SampleClass(self, b: str)
```

Class docstrings.

**Attributes**

- **baz** (`str`): Docstrings for attributes.

**Args**

- **b** (`str`): Arguments for initializing.

---

#### Methods {: #SampleClass-methods }

[**method**](#SampleClass.method){: #SampleClass.method }

```python
def method(self, bar: int) -> str
```

Method docstrings.

Cross reference available. [`func `](./#func)

**Args**

- **bar** (`int`)
  **Returns**

- `str`

## Functions

### func {: #func }

```python
def func(foo: str, bar: int) -> str
```

Docstrings for functions.

**Args**

- **foo** (`str`): First argument.
- **bar** (`int`): Second argument.

**Returns**

- `str`: Type of return value.
````

# License

MIT
