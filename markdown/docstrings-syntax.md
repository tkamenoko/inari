# Docstrings Syntax

You can use any Markdown syntax supported by `MkDocs` , and `inari` provides some additional features.

## List Arguments/Attributes

To list arguments or attributes, use `*`. `inari` emphasises these name automatically.

Example:
```python

def func(alpha: str, bata: str) -> str:
    """
    Sample function.

    **Args**

    * alpha (`str`): Explain `alpha` .
    * bata (`str`): Explain `bata` .

    **Returns**

    * `str`: Return type.

    """

    return alpha + bata

```

That will be converted to this:

~~~markdown
## Functions

### func {: #func }
```python
def func(alpha: str, bata: str) -> str:
```

Sample function.

**Args**

* **alpha** (`str`): Explain `alpha` .
* **bata** (`str`): Explain `bata` .

**Returns**

* `str`: Return type.

~~~

## Cross Reference

`inari` generates cross reference in API documents. `module.submodule.function` will be converted to appropriate relative link like ``[`function`](../submodule#function)`` .

Example:
```python
# `module/submodule.py`
def func(alpha: str, bata: str) -> str:
    """
    Link to some method like `module.anothermodule.SampleClass.some_method`
    """

    return alpha + bata

# `module/anothermodule.py`
class SampleClass:
    """
    Make reference like `module.submodule.func`
    """
    def some_method(self):
        pass

```

`inari` make hyperlink like this:
```markdown
<!-- module/submodule.md -->
Link to some method like [`some_method`](../anothermodule#SampleClass.some_method)

<!-- module/anothermodule.md -->
Make reference like [`func`](../submodule#func)

```
