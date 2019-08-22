# Module inari.structs


## Classes

### BaseStruct {: #BaseStruct }

```python
class BaseStruct(self, abs_path="", name_to_path: dict = None)
```

Base class for collecting docstrings.

Initialize self.  See help(type(self)) for accurate signature.


------

#### Methods {: #BaseStruct-methods }

**doc_str**{: #BaseStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

### ClsStruct {: #ClsStruct }

```python
class ClsStruct(self, cls, abs_path: str, name_to_path: dict)
```

Class with methods and properties. Attribute docs should be written in class
    docstring like this:

**Attributes**

* **cls** (`type`): object class.
* **vars** 
* **methods** 
* hash_

Initialize self.  See help(type(self)) for accurate signature.


------

#### Methods {: #ClsStruct-methods }

**doc_str**{: #ClsStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

**init_methods**{: #ClsStruct.init_methods }

```python
def init_methods(self)
```


------

**init_vars**{: #ClsStruct.init_vars }

```python
def init_vars(self)
```


------

### FuncStruct {: #FuncStruct }

```python
class FuncStruct(self, f: Callable, name_to_path: dict, abs_path: str)
```

Functions and methods.

Initialize self.  See help(type(self)) for accurate signature.


------

#### Methods {: #FuncStruct-methods }

**doc_str**{: #FuncStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

### ModStruct {: #ModStruct }

```python
class ModStruct(
        self, mod: ModuleType, out_dir, name_to_path=None, out_name: str = None)
```

Module docs, submodules, classes, funcs, and variables..

Initialize self.  See help(type(self)) for accurate signature.


------

#### Methods {: #ModStruct-methods }

**doc_str**{: #ModStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

------

**init_classes**{: #ModStruct.init_classes }

```python
def init_classes(self)
```

Find public classes defined in the module.

------

**init_funcs**{: #ModStruct.init_funcs }

```python
def init_funcs(self)
```

Find public functions in the module.

------

**init_vars**{: #ModStruct.init_vars }

```python
def init_vars(self)
```

Find variables having docstrings.

------

**make_links**{: #ModStruct.make_links }

```python
def make_links(self, doc: str) -> str
```

Create internal link on back-quoted name.

------

**make_relpaths**{: #ModStruct.make_relpaths }

```python
def make_relpaths(self)
```

Create mapping between object name to relative path.

~~~markdown

`ful.path.to.mod.cls` -> [`cls`](../../mod/cls)

~~~

------

**write**{: #ModStruct.write }

```python
def write(self)
```

Write documents to files. Directories are created automatically.

------

### VarStruct {: #VarStruct }

```python
class VarStruct(
        self, var, name_to_path: dict, abs_path: str, name: str = None, doc: str = None)
```

Module variables and class properties.

Initialize self.  See help(type(self)) for accurate signature.


------

#### Methods {: #VarStruct-methods }

**doc_str**{: #VarStruct.doc_str }

```python
def doc_str(self) -> str
```

Create documents from its contents.

## Functions

### is_var {: #is_var }

```python
def is_var(obj) -> bool
```
