# Module inari.structs


## Classes

### BaseStruct {: #BaseStruct }

```python
class BaseStruct(self, abs_path="", name_to_path: dict = None)
```

Base class for collecting objects with docstrings.

**Attributes**

* **name_to_path** (`dict`): Mapping of `{"module.name.class": "module/name#class"}` .
* **doc** (`str`): Docstrings of the object.
* **abs_path** (`str`): Absolute path of the object. Root is `out_dir` .

**Args**

* **abs_path** (`str`): Absolute path of the object.
* **name_to_path** (`dict`): Mapping of name and path.


------

#### Methods {: #BaseStruct-methods }

[**doc_str**](#BaseStruct.doc_str){: #BaseStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

### ClsStruct {: #ClsStruct }

```python
class ClsStruct(self, cls: type, abs_path: str, name_to_path: dict)
```

Class with methods and properties. Attribute docs should be written in class
    docstring like this:

**Attributes**

* **cls** (`type`): Target class.
* **vars** (`List[VarStruct]`): Class properties.
* **methods** (`List[FuncStruct]`): Methods of the class.
* **hash_** (`str`): Used for HTML id.

**Args**

* **cls** (`type`): Class to make documents.
* **abs_path** (`str`): See [`BaseStruct `](./#BaseStruct) .
* **name_to_path** (`str`): See [`BaseStruct `](./#BaseStruct) .


------

#### Methods {: #ClsStruct-methods }

[**doc_str**](#ClsStruct.doc_str){: #ClsStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

[**init_methods**](#ClsStruct.init_methods){: #ClsStruct.init_methods }

```python
def init_methods(self)
```


------

[**init_vars**](#ClsStruct.init_vars){: #ClsStruct.init_vars }

```python
def init_vars(self)
```


------

### FuncStruct {: #FuncStruct }

```python
class FuncStruct(self, f: Callable, name_to_path: dict, abs_path: str)
```

Functions and methods.

**Attributes**

* **func** (`Callable`): Target function.
* **hash_** (`str`): Used for HTML id.

**Args**

* **f** (`Callable`): Target function.
* **abs_path** (`str`): See [`BaseStruct `](./#BaseStruct) .
* **name_to_path** (`str`): See [`BaseStruct `](./#BaseStruct) .


------

#### Methods {: #FuncStruct-methods }

[**doc_str**](#FuncStruct.doc_str){: #FuncStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

### ModStruct {: #ModStruct }

```python
class ModStruct(
    self,
    mod: ModuleType,
    out_dir: Union[str, pathlib.Path],
    name_to_path: dict = None,
    out_name: str = None,)
```

Module docs, submodules, classes, funcs, and variables.

**Attributes**

* **mod** (`ModuleType`): Module to make documents.
* **submods** (`List[ModStruct]`): List of submodules, wrapped by
    [`ModStruct `](./#ModStruct) .
* **vars** (`List[VarStruct]`): List of module-level variables, wrapped by
    [`VarStruct `](./#VarStruct) .
* **classes** (`List[ClsStruct]`): List of public classes, wrapped by
    [`ClsStruct `](./#ClsStruct) .
* **funcs** (`List[FuncStruct]`): List of public functions, wrapped by
    [`FuncStruct `](./#FuncStruct) .
* **out_dir** (`pathlib.Path`): Output directly.
* **filename** (`str`): Output filename, like `index.md` , `submodule.md` .
* **relpaths** (`dict`): Store relational paths. See
    [`make_relpaths `](./#ModStruct.make_relpaths) .

**Args**

* **mod** (`ModuleType`): Module to make documents.
* **out_dir** (`Union[str,Path]`): Output directoly.
* **name_to_path** (`dict`): See [`BaseStruct `](./#BaseStruct) .
* **out_name** (`str`): If given, name of output file/directoly will be orverridden.


------

#### Methods {: #ModStruct-methods }

[**doc_str**](#ModStruct.doc_str){: #ModStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

[**init_classes**](#ModStruct.init_classes){: #ModStruct.init_classes }

```python
def init_classes(self)
```

Find public classes defined in the module.

------

[**init_funcs**](#ModStruct.init_funcs){: #ModStruct.init_funcs }

```python
def init_funcs(self)
```

Find public functions in the module.

------

[**init_vars**](#ModStruct.init_vars){: #ModStruct.init_vars }

```python
def init_vars(self)
```

Find variables having docstrings.

------

[**make_links**](#ModStruct.make_links){: #ModStruct.make_links }

```python
def make_links(self, doc: str) -> str
```

Create internal link on back-quoted name.

To ignore this, append a space like `"foo.bar "` .

------

[**make_relpaths**](#ModStruct.make_relpaths){: #ModStruct.make_relpaths }

```python
def make_relpaths(self)
```

Create mapping between object name to relative path.

~~~markdown

`ful.path.to.mod.cls` -> [`cls`](../../mod#cls)

~~~

------

[**write**](#ModStruct.write){: #ModStruct.write }

```python
def write(self)
```

Write documents to files. Directories are created automatically.

------

### VarStruct {: #VarStruct }

```python
class VarStruct(self, var, name_to_path: dict, abs_path: str, name: str = None, doc: str = None)
```

Module variables and class properties.

**Attributes**

* **var** : Module-level object or class property, not module/class/function.
* **name** (`str`): Name of the object.

**Args**

* **var** : Target object.
* **name_to_path** (`dict`): See [`BaseStruct `](./#BaseStruct) .
* **abs_path** (`str`): See [`BaseStruct `](./#BaseStruct) .
* **name** (`str`): Fallback of `var.__name__` .
* **doc** (`str`): Fallback of `inspect.getdoc(var)` .


------

#### Methods {: #VarStruct-methods }

[**doc_str**](#VarStruct.doc_str){: #VarStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

## Functions

### is_var {: #is_var }

```python
def is_var(obj) -> bool
```

Utility for filtering unexpected objects.
