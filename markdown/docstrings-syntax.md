# Docstrings Syntax

You can use any Markdown syntax, and `inari` provides some additional features.

## List Arguments/Attributes

To list arguments or attributes, use `*`. `inari` emphasizes these name automatically.

Example:

```python

def func(alpha: str, beta: str) -> str:
    """
    Sample function.

    **Args**

    * alpha (`str`): Explain `alpha` .
    * beta (`str`): Explain `beta` .

    **Returns**

    * `str`: Return type.

    """

    return alpha + beta

```

That will be converted to this:

````markdown
## Functions

### func

```python
def func(alpha: str, beta: str) -> str
```

Sample function.

**Args**

- **alpha** (`str`): Explain `alpha` .
- **beta** (`str`): Explain `beta` .

**Returns**

- `str`: Return type.
````

## Cross Reference

`inari` generates cross reference in API documents. `module.submodule.function` will be converted to appropriate relative link like `` [`function `](../submodule#function) `` .

!!! note
If you installed `inari` without `MkDocs` , you have to install [`Python-Markdown`](https://python-markdown.github.io/) and enable [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/) extension to create hash anchors.

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

`inari` makes hyperlink like this:

````markdown
<!-- docs/module/submodule-py.md -->

# Module module.submodule

## Functions

### func {: #func }

```python
def func(alpha: str, bata: str) -> str
```

Link to some method like [`SampleClass.some_method `](../anothermodule-py#SampleClass.some_method)

<!-- docs/module/anothermodule-py.md -->

# Module module.anothermodule

## Classes

### SampleClass {: #SampleClass }

```python
class SampleClass()
```

Make reference like [`func `](../submodule-py#func)

---

#### Methods {: #SampleClass-methods }

[**some_method**](#SampleClass.some_method){: #SampleClass.some_method }

```python
def some_method(self)
```
````
