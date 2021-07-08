"""
collectors -  Store module members, and build markdown documents from docstrings.
"""

import hashlib
import importlib
import inspect
import os
import pathlib
import re
from functools import reduce
from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType
from typing import Any, Callable, Optional

from ._internal._format import cleanup, modify_attrs
from ._internal._path import get_relative_path
from ._internal._templates import build_yaml_header

try:
    import markdown
except ImportError:
    markdown = None


def is_var(obj: object) -> bool:
    """Utility for filtering unexpected objects."""

    return not any(
        [
            inspect.ismodule(obj),
            inspect.isclass(obj),
            inspect.ismethod(obj),
            inspect.isfunction(obj),
        ]
    )


class BaseCollector:
    """
    Base class for collecting objects with docstrings.

    **Attributes**

    * name_to_path (`dict[str, str]`):
        Mapping of `{"module.name.class": "module/name#class"}` .
    * doc (`str`): Docstrings of the object.
    * abs_path (`str`): Absolute path of the object. Root is `out_dir` .

    """

    name_to_path: dict[str, str]
    doc: str
    abs_path: str

    def __init__(
        self, abs_path: str = "", name_to_path: Optional[dict[str, str]] = None
    ):
        """
        **Args**

        * abs_path (`str`): Absolute path of the object.
        * name_to_path (`dict[str, str]`): Mapping of name and path.

        """
        self.name_to_path = name_to_path or {}
        self.abs_path = abs_path

    def doc_str(self) -> str:
        """
        Create documents from its contents.

        **Returns**

        * `str`: Created from docstrings and annotations.

        """
        raise NotImplementedError


class ModuleCollector(BaseCollector):
    """
    Module docs, submodules, classes, functions, and variables.

    **Attributes**

    * mod (`ModuleType`): Module to make documents.
    * submodules (`dict[str, ModuleCollector]`): key-value pair of paths and submodules,
        wrapped by `inari.collectors.ModuleCollector` .
    * variables (`list[VariableCollector]`): list of module-level variables, wrapped by
        `inari.collectors.VariableCollector` .
    * classes (`list[ClassCollector]`): list of public classes, wrapped by
        `inari.collectors.ClassCollector` .
    * functions (`list[FunctionCollector]`): list of public functions, wrapped by
        `inari.collectors.FunctionCollector` .
    * out_dir (`pathlib.Path`): Output directly.
    * filename (`str`): Output filename, like `index.md` , `submodule.md` .
    * relpaths (`dict[str, tuple[str, str]]`): Store relational paths. See
        `inari.collectors.ModuleCollector.make_relpaths` .
    * enable_yaml_header (`bool`): a flag for deciding whether to include yaml header.

    """

    mod: ModuleType

    submodules: dict[str, "ModuleCollector"]
    variables: list["VariableCollector"]
    classes: list["ClassCollector"]
    functions: list["FunctionCollector"]

    out_dir: pathlib.Path
    filename: str
    relpaths: dict[str, tuple[str, str]]
    enable_yaml_header: bool

    _has_submodules: bool
    _module_digest: str

    def __init__(
        self,
        mod: ModuleType,
        out_dir: os.PathLike[str],
        name_to_path: Optional[dict[str, str]] = None,
        out_name: Optional[str] = None,
        enable_yaml_header: bool = False,
    ):
        """
        **Args**

        * mod (`ModuleType`): Module to make documents.
        * out_dir (`Union[str,Path]`): Output directory.
        * name_to_path (`dict`): See `inari.collectors.BaseCollector` .
        * out_name (`str`): Output file name.
        * enable_yaml_header (`bool`): a flag for deciding whether to include
            yaml header.

        """
        self.mod = mod
        self.submodules = {}
        abs_path = "/" + mod.__name__.replace(".", "/")
        super().__init__(abs_path=abs_path, name_to_path=name_to_path)
        self.relpaths = {}
        self.enable_yaml_header = enable_yaml_header

        mod_path = inspect.getfile(mod)
        if mod_path.endswith("__init__.py"):
            self.name_to_path[mod.__name__] = self.abs_path
            # output names.
            self.out_dir = pathlib.Path(out_dir) / (
                out_name or (mod.__name__.rsplit(".", 1)[-1])
            )
            self.filename = "index.md"
            self._has_submodules = True

        else:
            self.out_dir = pathlib.Path(out_dir)
            self._has_submodules = False
            if out_name:
                name = out_name
                self.name_to_path[mod.__name__] = self.abs_path
            else:
                # workaround for "index.py" .
                name = mod.__name__.rsplit(".", 1)[-1] + "-py"
                self.abs_path += "-py"
                self.name_to_path[mod.__name__] = self.abs_path
            self.filename = f"{name}.md"

        self.doc = inspect.getdoc(self.mod) or ""

    def init_submodules(self) -> None:
        """
        Find submodules.
        """

        if self._has_submodules:
            # get submodules.
            module_path = getattr(self.mod, "__path__", [])
            submods = [
                import_module(f"{self.mod.__name__}.{x.name}")
                for x in walk_packages(module_path)
                if not x.name.startswith("_")
            ]
            for submod in submods:
                key = inspect.getfile(submod)
                self.submodules.setdefault(
                    key,
                    ModuleCollector(
                        submod,
                        self.out_dir,
                        self.name_to_path,
                        enable_yaml_header=self.enable_yaml_header,
                    ),
                )

        else:
            # no submodules.
            self.submodules = {}

    def init_classes(self) -> None:
        """Find public classes defined in the module."""
        mod_classes = [
            x[1]
            for x in inspect.getmembers(self.mod, inspect.isclass)
            if (not x[0].startswith("_")) and (inspect.getmodule(x[1]) == self.mod)
        ]
        self.classes = [
            ClassCollector(c, name_to_path=self.name_to_path, abs_path=self.abs_path)
            for c in mod_classes
        ]

    def init_vars(self) -> None:
        """Find variables having docstrings."""
        try:
            src = inspect.getsource(self.mod)
        except OSError:
            # `__init__.py` is empty.
            src = ""
        var_docs = {
            x[0].split("=")[0].strip(): inspect.cleandoc(x[1])
            for x in re.findall(r'(.*)\n"""(.*(?!""")(?<!""").*)"""\n', src)
        }

        mod_vars = [
            {"name": x[0], "value": x[1], "doc": var_docs[x[0]]}
            for x in inspect.getmembers(self.mod, is_var)
            if (not x[0].startswith("_")) and (x[0] in var_docs)
        ]

        self.variables = [
            VariableCollector(
                v["value"],
                name_to_path=self.name_to_path,
                abs_path=self.abs_path,
                name=v["name"],
                doc=v["doc"],
            )
            for v in mod_vars
        ]

    def init_functions(self) -> None:
        """Find public functions in the module."""
        mod_functions = [
            x[1]
            for x in inspect.getmembers(
                self.mod,
                lambda f: (inspect.isroutine(f) and (inspect.getmodule(f) is self.mod)),
            )
            if (not x[0].startswith("_"))
        ]
        self.functions = [
            FunctionCollector(m, name_to_path=self.name_to_path, abs_path=self.abs_path)
            for m in mod_functions
        ]

    def doc_str(self) -> str:
        self.init_vars()
        self.init_classes()
        self.init_functions()
        self.make_relpaths()

        yaml_header = self.make_yaml_header()

        mod_head = f"# Module {self.mod.__name__}"
        mod_ds = self.doc

        def submod_to_link(sub_name: str) -> str:
            rel_path = self.relpaths[sub_name][0]
            return f"[{sub_name}]({rel_path})"

        submodules_head = "## Submodules"
        submodules = [submod_to_link(x.mod.__name__) for x in self.submodules.values()]
        submodules_list = "\n\n".join(submodules)
        if not submodules:
            submodules_head = ""

        vars_head = "## Variables"
        vars_ = [x.doc_str() for x in self.variables]
        vars_list = "\n\n".join(vars_)
        if not vars_:
            vars_head = ""

        classes_head = "## Classes"
        classes = [x.doc_str() for x in self.classes]
        classes_list = "\n\n------\n\n".join(classes)
        if not classes:
            classes_head = ""

        functions_head = "## Functions"
        functions = [x.doc_str() for x in self.functions]
        functions_list = "\n\n------\n\n".join(functions)
        if not functions:
            functions_head = ""

        doc = "\n\n".join(
            [
                yaml_header,
                mod_head,
                mod_ds,
                submodules_head,
                submodules_list,
                vars_head,
                vars_list,
                classes_head,
                classes_list,
                functions_head,
                functions_list,
            ]
        )

        doc = self.make_links(doc)
        return cleanup(doc)

    def make_relpaths(self) -> None:
        """
        Create mapping between object name to relative path.

        ~~~markdown

        `ful.path.to.mod.cls` -> [`cls`](../../mod.md#cls)

        ~~~

        """
        for name, path in self.name_to_path.items():
            if "#" in path:
                relpath, hash_ = path.split("#")
                hash_ = "#" + hash_
            else:
                relpath, hash_ = path, ""
            if not relpath.endswith("-py"):
                relpath = f"{relpath}/index".replace("//", "/")

            relpath = get_relative_path(self.abs_path, relpath)

            if relpath:
                relpath = relpath + ".md"

            self.relpaths[name] = (relpath, hash_)

    def make_links(self, doc: str) -> str:
        """
        Create internal link on back-quoted name.

        To ignore this, append a space like `"foo.bar "` .

        """

        for long_name, rel_hash in self.relpaths.items():
            _, hash_id = rel_hash
            if hash_id:
                short_name = hash_id.removeprefix("#")
            else:
                short_name = long_name.rsplit(".", 1)[-1]
            # append a space after short_name because of avoiding unexpected replacing.
            doc = doc.replace(
                f"`{long_name}`", f"[`{short_name} `]({''.join(rel_hash)})"
            )
        return doc

    def make_yaml_header(self) -> str:
        """
        Make yaml header from given values.
        """
        if not self.enable_yaml_header:
            return ""

        header = build_yaml_header(
            title=self.mod.__name__, module_digest=self._module_digest
        )
        return header

    def remove_old_submodules(self) -> None:
        """
        Remove documents and collectors of deleted modules.
        """
        if not self._has_submodules:
            return

        new_modules: dict[str, ModuleCollector] = {
            path: submodule
            for path, submodule in self.submodules.items()
            if os.path.isfile(path)
        }

        filenames = [
            f for f in os.listdir(self.out_dir) if os.path.isfile(self.out_dir / f)
        ]

        submodule_filenames = [x.filename for x in new_modules.values()]

        def is_not_used(s: str) -> bool:
            path = pathlib.PurePath(s)
            filename = path.name
            if filename == "index.md":
                return False
            return filename not in submodule_filenames

        unused_filenames = filter(is_not_used, filenames)

        for unused_filename in unused_filenames:
            os.remove(self.out_dir / unused_filename)
        self.submodules = new_modules

    def write(self) -> None:
        """Write documents to files. Directories are created automatically."""
        importlib.reload(self.mod)
        self.init_submodules()
        os.makedirs(self.out_dir, exist_ok=True)
        self.remove_old_submodules()
        current_digest = hashlib.md5(
            inspect.getsource(self.mod).encode("utf-8")
        ).hexdigest()

        if os.path.isfile(self.out_dir / self.filename):
            with open(
                self.out_dir / self.filename, mode="r", newline="\n", encoding="utf-8"
            ) as index:
                content = index.read()
                matched = re.match(
                    r"^---\n(.+)\n---\n", content, re.MULTILINE | re.DOTALL
                )
                headers = matched.group(0) if matched else ""
        else:
            headers = ""

        modified = current_digest not in headers

        if modified:
            self._module_digest = current_digest
            # write self.
            with open(
                self.out_dir / self.filename, mode="w", newline="\n", encoding="utf-8"
            ) as index:
                index.write(self.doc_str())
        # write submodules.
        for submod in self.submodules.values():
            submod.write()


class VariableCollector(BaseCollector):
    """
    Module variables and class properties.

    **Attributes**

    * var: Module-level object or class property, not module/class/function.
    * name (`str`): Name of the object.

    """

    var: object

    name: str
    hash_: str

    _should_skip = False

    def __init__(
        self,
        var: object,
        name_to_path: dict[str, str],
        abs_path: str,
        name: Optional[str] = None,
        doc: Optional[str] = None,
    ) -> None:
        """
        **Args**

        * var (`object`): Target object.
        * name_to_path (`dict[str, str]`): See `inari.collectors.BaseCollector` .
        * abs_path (`str`): See `inari.collectors.BaseCollector` .
        * name (`str`): Fallback of `var.__name__` .
        * doc (`str`): Fallback of `inspect.getdoc(var)` .

        """
        super().__init__(name_to_path=name_to_path)
        self.var = var
        self.doc = doc or inspect.getdoc(var) or ""
        name = name or getattr(var, "__name__", None)
        if not name:
            self._should_skip = True
            return
        self.name = name.rsplit(".")[-1]
        module_name = ".".join([n for n in abs_path.split("/") if n]).replace("-py", "")

        if "#" in abs_path:
            abs_path = f"{abs_path}.{self.name}"
            long_name = module_name.replace("#", ".") + "." + self.name
        else:
            abs_path = f"{abs_path}#{self.name}"
            long_name = module_name + "." + self.name
        self.name_to_path[long_name] = abs_path
        self.hash_ = "#" + abs_path.rsplit("#", 1)[-1]

    def doc_str(self) -> str:
        if self._should_skip:
            return ""
        attributes = ""
        if markdown:
            attributes = f"{{: {self.hash_} }}"
        if self.doc:
            doc = f"* {self.name} {self.doc}"
        else:
            doc = f"* {self.name}"
        return modify_attrs(doc, attributes)


class ClassCollector(BaseCollector):
    """
    Class with methods and properties. Attribute docs should be written in class
        docstring like this:

    **Attributes**

    * cls (`type`): Target class.
    * variables (`list[VariableCollector]`): Class properties.
    * methods (`list[FunctionCollector]`): Methods of the class.
    * hash_ (`str`): Used for HTML id.

    """

    cls: type

    variables: list[VariableCollector]
    methods: list["FunctionCollector"]

    hash_: str

    def __init__(self, cls: type, abs_path: str, name_to_path: dict[str, str]):
        """
        **Args**

        * cls (`type`): Class to make documents.
        * abs_path (`str`): See `inari.collectors.BaseCollector` .
        * name_to_path (`dict[str, str]`): See `inari.collectors.BaseCollector` .

        """
        self.cls = cls
        self.doc = inspect.getdoc(cls) or ""
        self.doc = modify_attrs(self.doc)

        module_name = ".".join([n for n in abs_path.split("/") if n]).replace("-py", "")
        long_name = module_name + "." + self.cls.__qualname__
        self.hash_ = "#" + self.cls.__qualname__
        abs_path = abs_path + self.hash_
        super().__init__(abs_path=abs_path, name_to_path=name_to_path)
        self.name_to_path[long_name] = self.abs_path

    def init_variables(self) -> None:
        cls_variables = [
            x
            for x in inspect.getmembers(self.cls, lambda v: v.__class__ is property)
            if (not x[0].startswith("_"))
        ]
        self.variables = [
            VariableCollector(
                v[1], name=v[0], name_to_path=self.name_to_path, abs_path=self.abs_path
            )
            for v in cls_variables
        ]

    def init_methods(self) -> None:
        methods = [
            x[1]
            for x in inspect.getmembers(
                self.cls,
                lambda f: (
                    inspect.isroutine(f)
                    and (f.__class__ is not property)
                    and f.__qualname__.startswith(self.cls.__qualname__)
                    and not inspect.isbuiltin(f)
                ),
            )
            if (not x[0].startswith("_"))
        ]
        self.methods = [
            FunctionCollector(m, name_to_path=self.name_to_path, abs_path=self.abs_path)
            for m in methods
        ]

    def doc_str(self) -> str:
        self.init_variables()
        self.init_methods()
        name = self.cls.__name__.rsplit(".")[-1]
        h = ""
        if markdown:
            h = f"{{: {self.hash_} }}"
        head = f"### {name} {h}"
        try:
            pos = inspect.getsource(self.cls).find("def __init__(")
            def_args = inspect.getsource(self.cls)[pos:]
            def_args = (
                re.sub(r"\) *( *-> *None *)?: *(#.*)?\n", r"):\n", def_args)
                .split(":\n", 1)[0]
                .rsplit(")", 1)[0]
            )
            args = (def_args.replace("def", "", 1).replace("__init__(", "", 1)).strip()
            if not args:
                raise ValueError
            if "\n    " in args:
                args = "\n    " + args
                args = re.sub(r"\n(    )+", "\n    ", args)
            source = f"class {name}({args})"
            defs = f"```python\n{source}\n```"
        except (OSError, ValueError):
            try:
                args_ = str(inspect.signature(self.cls))
            except ValueError:
                args_ = "(self, *args, **kwargs)"
            defs = f"```python\nclass {name}{args_}\n```".replace(" -> None", "")
        init = self.cls.__init__
        if init.__qualname__.startswith(self.cls.__qualname__):
            init_doc = inspect.getdoc(init) or ""
        else:
            init_doc = ""
        init_doc = modify_attrs(init_doc)
        cls_doc = "\n\n".join([defs, self.doc, init_doc])
        # base classes
        bases_doc = ""
        bases = [set(c.mro()) for c in self.cls.mro() if c is not self.cls]
        if len(bases) > 1:
            h = ""
            if markdown:
                h = f"{{: {self.hash_}-bases }}"
            bases_head = f"\n\n------\n\n#### Base classes {h}\n\n"
            # get direct bases
            base_set = reduce(lambda x, y: x | y, bases)
            base_list = reduce(lambda x, y: x + y, [list(s) for s in bases])
            parents = [x for x in base_set if base_list.count(x) == 1]
            base_names = []
            root = inspect.getmodule(self.cls).__name__.split(".", 1)[0]
            for p in parents:
                mod_name = inspect.getmodule(p).__name__
                mod_root = mod_name.split(".", 1)[0]
                if mod_root == root:
                    base_name = f"* `{mod_name}.{p.__name__}`"
                else:
                    base_name = f"* `{mod_root}.{p.__name__}`"
                base_names.append(base_name)
            bases_doc = bases_head + "\n".join(base_names)
        # class vars
        h = ""
        if markdown:
            h = f"{{: {self.hash_}-attrs }}"
        vars_head = f"\n\n------\n\n#### Instance attributes {h}\n"
        vars_ = [x.doc_str() for x in self.variables]
        vars_list = "\n\n".join(vars_)
        if not vars_:
            vars_head = ""
        vars_doc = vars_head + "\n" + vars_list
        # methods
        h = ""
        if markdown:
            h = f"{{: {self.hash_}-methods }}"
        methods_head = f"\n\n------\n\n#### Methods {h}\n"
        methods = [x.doc_str() for x in self.methods]
        methods_list = "\n\n------\n\n".join(methods)
        if not methods:
            methods_head = ""
        methods_doc = methods_head + "\n" + methods_list

        return "\n\n".join([head, cls_doc, bases_doc, vars_doc, methods_doc])


class FunctionCollector(BaseCollector):
    """
    Functions and methods.

    **Attributes**

    * function (`Callable[..., Any]`): Target function.
    * hash_ (`str`): Used for HTML id.

    """

    function: Callable[..., Any]
    hash_: str

    def __init__(
        self, f: Callable[..., Any], name_to_path: dict[str, str], abs_path: str
    ):
        """
        **Args**

        * f (`Callable[..., Any]`): Target function.
        * abs_path (`str`): See `inari.collectors.BaseCollector` .
        * name_to_path (`dict[str, str]`): See `inari.collectors.BaseCollector` .

        """
        self.function = f
        self.doc = inspect.getdoc(f) or ""
        self.doc = modify_attrs(self.doc)

        module_name = ".".join([n for n in abs_path.split("/") if n]).replace("-py", "")
        if "#" in abs_path:
            abs_path = f"{abs_path}.{f.__name__}"
            long_name = module_name.replace("#", ".") + "." + f.__name__
        else:
            abs_path = f"{abs_path}#{f.__name__}"
            long_name = module_name + "." + f.__name__

        self.hash_ = "#" + abs_path.split("#")[-1]
        super().__init__(abs_path=abs_path, name_to_path=name_to_path)

        self.name_to_path[long_name] = self.abs_path

    def doc_str(self) -> str:
        # is method?
        h = ""
        if markdown:
            h = f"{{: {self.hash_} }}"
        if self.hash_ != "#" + self.function.__name__:
            head = f"[**{self.function.__name__}**]({self.hash_}){h}"
        else:
            head = f"### {self.function.__name__} {h}"
        full_source = inspect.getsource(self.function)
        no_decolators = re.sub(r"^\s*@.+$", "", full_source, flags=re.MULTILINE)
        no_comments = re.sub(r"\) *(-> *.+)? *: *(#.*)?\n", r") \1 :\n", no_decolators)
        sig = no_comments.split(":\n", 1)[0]
        args, returns = sig.rsplit(")", 1)
        if "\n    " in args:
            args = re.sub(r"\n(    )+", "\n    ", args)
        source = f"{args}){returns}".strip()
        defs = f"```python\n{source}\n```"
        docs = "\n\n".join([head, defs, self.doc])
        return docs
