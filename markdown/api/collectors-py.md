---
module_digest: 98b0e2f9aa6aefc59ebd8687cb9c046b
---

# Module inari.collectors

collectors -  Store module members, and build markdown documents from docstrings.


## Classes

### BaseCollector {: #BaseCollector }

```python
class BaseCollector(self, abs_path: str = "", name_to_path: Optional[dict[str, str]] = None)
```

Base class for collecting objects with docstrings.

**Attributes**

* **name_to_path** (`dict[str, str]`):
    Mapping of `{"module.name.class": "module/name#class"}` .
* **doc** (`str`): Docstrings of the object.
* **abs_path** (`str`): Absolute path of the object. Root is `out_dir` .

**Args**

* **abs_path** (`str`): Absolute path of the object.
* **name_to_path** (`dict[str, str]`): Mapping of name and path.


------

#### Methods {: #BaseCollector-methods }

[**doc_str**](#BaseCollector.doc_str){: #BaseCollector.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

### ClassCollector {: #ClassCollector }

```python
class ClassCollector(self, cls: type, abs_path: str, name_to_path: dict[str, str])
```

Class with methods and properties. Attribute docs should be written in class
    docstring like this:

**Attributes**

* **cls** (`type`): Target class.
* **variables** (`list[VariableCollector]`): Class properties.
* **methods** (`list[FunctionCollector]`): Methods of the class.
* **hash_** (`str`): Used for HTML id.

**Args**

* **cls** (`type`): Class to make documents.
* **abs_path** (`str`): See [`BaseCollector `](./#BaseCollector) .
* **name_to_path** (`dict[str, str]`): See [`BaseCollector `](./#BaseCollector) .


------

#### Base classes {: #ClassCollector-bases }

* [`BaseCollector `](./#BaseCollector)


------

#### Methods {: #ClassCollector-methods }

[**doc_str**](#ClassCollector.doc_str){: #ClassCollector.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

[**init_methods**](#ClassCollector.init_methods){: #ClassCollector.init_methods }

```python
def init_methods(self) -> None
```


------

[**init_variables**](#ClassCollector.init_variables){: #ClassCollector.init_variables }

```python
def init_variables(self) -> None
```


------

### FunctionCollector {: #FunctionCollector }

```python
class FunctionCollector(self, f: Callable[..., Any], name_to_path: dict[str, str], abs_path: str)
```

Functions and methods.

**Attributes**

* **function** (`Callable[..., Any]`): Target function.
* **hash_** (`str`): Used for HTML id.

**Args**

* **f** (`Callable[..., Any]`): Target function.
* **abs_path** (`str`): See [`BaseCollector `](./#BaseCollector) .
* **name_to_path** (`dict[str, str]`): See [`BaseCollector `](./#BaseCollector) .


------

#### Base classes {: #FunctionCollector-bases }

* [`BaseCollector `](./#BaseCollector)


------

#### Methods {: #FunctionCollector-methods }

[**doc_str**](#FunctionCollector.doc_str){: #FunctionCollector.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

### ModuleCollector {: #ModuleCollector }

```python
class ModuleCollector(
    self,
    mod: ModuleType,
    out_dir: os.PathLike[str],
    name_to_path: Optional[dict[str, str]] = None,
    out_name: Optional[str] = None,
    enable_yaml_header: bool = False,)
```

Module docs, submodules, classes, functions, and variables.

test: [`run `](../cli-py#run)

**Attributes**

* **mod** (`ModuleType`): Module to make documents.
* **submodules** (`dict[str, ModuleCollector]`): key-value pair of paths and submodules,
    wrapped by [`ModuleCollector `](./#ModuleCollector) .
* **variables** (`list[VariableCollector]`): list of module-level variables, wrapped by
    [`VariableCollector `](./#VariableCollector) .
* **classes** (`list[ClassCollector]`): list of public classes, wrapped by
    [`ClassCollector `](./#ClassCollector) .
* **functions** (`list[FunctionCollector]`): list of public functions, wrapped by
    [`FunctionCollector `](./#FunctionCollector) .
* **out_dir** (`pathlib.Path`): Output directly.
* **filename** (`str`): Output filename, like `index.md` , `submodule.md` .
* **relpaths** (`dict[str, tuple[str, str]]`): Store relational paths. See
    `inari.collectors.ModuleCollector.make_relpaths` .
* **enable_yaml_header** (`bool`): a flag for deciding whether to include yaml header.

**Args**

* **mod** (`ModuleType`): Module to make documents.
* **out_dir** (`Union[str,Path]`): Output directory.
* **name_to_path** (`dict`): See [`BaseCollector `](./#BaseCollector) .
* **out_name** (`str`): Output file name.
* **enable_yaml_header** (`bool`): a flag for deciding whether to include
    yaml header.


------

#### Base classes {: #ModuleCollector-bases }

* [`BaseCollector `](./#BaseCollector)


------

#### Methods {: #ModuleCollector-methods }

[**doc_str**](#ModuleCollector.doc_str){: #ModuleCollector.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

[**init_classes**](#ModuleCollector.init_classes){: #ModuleCollector.init_classes }

```python
def init_classes(self) -> None
```

Find public classes defined in the module.

------

[**init_functions**](#ModuleCollector.init_functions){: #ModuleCollector.init_functions }

```python
def init_functions(self) -> None
```

Find public functions in the module.

------

[**init_submodules**](#ModuleCollector.init_submodules){: #ModuleCollector.init_submodules }

```python
def init_submodules(self) -> None
```

Find submodules.

------

[**init_vars**](#ModuleCollector.init_vars){: #ModuleCollector.init_vars }

```python
def init_vars(self) -> None
```

Find variables having docstrings.

------

[**make_links**](#ModuleCollector.make_links){: #ModuleCollector.make_links }

```python
def make_links(self, doc: str) -> str
```

Create internal link on back-quoted name.

To ignore this, append a space like `"foo.bar "` .

------

[**make_relpaths**](#ModuleCollector.make_relpaths){: #ModuleCollector.make_relpaths }

```python
def make_relpaths(self) -> None
```

Create mapping between object name to relative path.

~~~markdown

`ful.path.to.mod.cls` -> [`cls`](../../mod#cls)

~~~

------

[**make_yaml_header**](#ModuleCollector.make_yaml_header){: #ModuleCollector.make_yaml_header }

```python
def make_yaml_header(self) -> str
```

Make yaml header from given values.

------

[**remove_old_submodules**](#ModuleCollector.remove_old_submodules){: #ModuleCollector.remove_old_submodules }

```python
def remove_old_submodules(self) -> None
```

Remove documents and collectors of deleted modules.

------

[**write**](#ModuleCollector.write){: #ModuleCollector.write }

```python
def write(self) -> None
```

Write documents to files. Directories are created automatically.

------

### VariableCollector {: #VariableCollector }

```python
class VariableCollector(
    self,
    var: object,
    name_to_path: dict[str, str],
    abs_path: str,
    name: Optional[str] = None,
    doc: Optional[str] = None,)
```

Module variables and class properties.

**Attributes**

* **var** : Module-level object or class property, not module/class/function.
* **name** (`str`): Name of the object.

**Args**

* **var** (`object`): Target object.
* **name_to_path** (`dict[str, str]`): See [`BaseCollector `](./#BaseCollector) .
* **abs_path** (`str`): See [`BaseCollector `](./#BaseCollector) .
* **name** (`str`): Fallback of `var.__name__` .
* **doc** (`str`): Fallback of `inspect.getdoc(var)` .


------

#### Base classes {: #VariableCollector-bases }

* [`BaseCollector `](./#BaseCollector)


------

#### Methods {: #VariableCollector-methods }

[**doc_str**](#VariableCollector.doc_str){: #VariableCollector.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

## Functions

### is_var {: #is_var }

```python
def is_var(obj: object) -> bool
```

Utility for filtering unexpected objects.
