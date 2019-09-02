"""
Store module structures, members, and docstrings.
"""

import inspect
import os
import pathlib
import re
import shutil
from functools import reduce
from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType
from typing import Any, Callable, List, Union

from ._format import cleanup, modify_attrs

try:
    import markdown
except ImportError:
    markdown = None


def is_var(obj) -> bool:
    """Utility for filtering unexpected objects."""

    return not any(
        [
            inspect.ismodule(obj),
            inspect.isclass(obj),
            inspect.ismethod(obj),
            inspect.isfunction(obj),
        ]
    )


class BaseStruct:
    """
    Base class for collecting objects with docstrings.

    **Attributes**

    * name_to_path (`dict`): Mapping of `{"module.name.class": "module/name#class"}` .
    * doc (`str`): Docstrings of the object.
    * abs_path (`str`): Absolute path of the object. Root is `out_dir` .

    """

    name_to_path: dict
    doc: str
    abs_path: str

    def __init__(self, abs_path="", name_to_path: dict = None):
        """
        **Args**

        * abs_path (`str`): Absolute path of the object.
        * name_to_path (`dict`): Mapping of name and path.

        """
        if name_to_path is None:
            name_to_path = {}
        self.name_to_path = name_to_path
        self.abs_path = abs_path

    def doc_str(self) -> str:
        """Create documents from its contents."""
        raise NotImplementedError


class ModStruct(BaseStruct):
    """
    Module docs, submodules, classes, funcs, and variables.

    test: `inari.cli.run`

    **Attributes**

    * mod (`ModuleType`): Module to make documents.
    * submods (`List[ModStruct]`): List of submodules, wrapped by
        `inari.structs.ModStruct` .
    * vars (`List[VarStruct]`): List of module-level variables, wrapped by
        `inari.structs.VarStruct` .
    * classes (`List[ClsStruct]`): List of public classes, wrapped by
        `inari.structs.ClsStruct` .
    * funcs (`List[FuncStruct]`): List of public functions, wrapped by
        `inari.structs.FuncStruct` .
    * out_dir (`pathlib.Path`): Output directly.
    * filename (`str`): Output filename, like `index.md` , `submodule.md` .
    * relpaths (`dict`): Store relational paths. See
        `inari.structs.ModStruct.make_relpaths` .

    """

    mod: ModuleType

    submods: List["ModStruct"]
    vars: List["VarStruct"]
    classes: List["ClsStruct"]
    funcs: List["FuncStruct"]

    out_dir: pathlib.Path
    filename: str
    relpaths: dict

    def __init__(
        self,
        mod: ModuleType,
        out_dir: Union[str, pathlib.Path],
        name_to_path: dict = None,
        out_name: str = None,
    ):
        """
        **Args**

        * mod (`ModuleType`): Module to make documents.
        * out_dir (`Union[str,Path]`): Output directoly.
        * name_to_path (`dict`): See `inari.structs.BaseStruct` .
        * out_name (`str`): If given, name of output file/directoly will be orverridden.

        """
        self.mod = mod
        abs_path = "/" + mod.__name__.replace(".", "/")
        super().__init__(abs_path=abs_path, name_to_path=name_to_path)
        self.relpaths = {}

        mod_path = inspect.getfile(mod)
        if mod_path.endswith("__init__.py"):
            self.name_to_path[mod.__name__] = self.abs_path
            # output names.
            self.out_dir = pathlib.Path(out_dir) / (
                out_name or (mod.__name__.rsplit(".", 1)[-1])
            )
            self.filename = "index.md"
            # clean old docs.
            if os.path.exists(self.out_dir):
                shutil.rmtree(self.out_dir)
            # get submodules.
            submods = [
                import_module(f"{mod.__name__}.{x.name}")
                for x in walk_packages(mod.__path__)
                if not x.name.startswith("_")
            ]
            self.submods = [
                ModStruct(submod, self.out_dir, self.name_to_path) for submod in submods
            ]

        else:
            self.out_dir = pathlib.Path(out_dir)
            if out_name:
                name = out_name
                self.name_to_path[mod.__name__] = self.abs_path
            else:
                # workaround for "index.py" .
                name = mod.__name__.rsplit(".", 1)[-1] + "-py"
                self.abs_path += "-py"
                self.name_to_path[mod.__name__] = self.abs_path
            self.filename = f"{name}.md"
            # no submodules.
            self.submods = []

        self.doc = inspect.getdoc(self.mod) or ""

        self.init_vars()
        self.init_classes()
        self.init_funcs()

    def init_classes(self):
        """Find public classes defined in the module."""
        mod_classes = [
            x[1]
            for x in inspect.getmembers(self.mod, inspect.isclass)
            if (not x[0].startswith("_")) and (inspect.getmodule(x[1]) == self.mod)
        ]
        self.classes = [
            ClsStruct(c, name_to_path=self.name_to_path, abs_path=self.abs_path)
            for c in mod_classes
        ]

    def init_vars(self):
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

        self.vars = [
            VarStruct(
                v["value"],
                name_to_path=self.name_to_path,
                abs_path=self.abs_path,
                name=v["name"],
                doc=v["doc"],
            )
            for v in mod_vars
        ]

    def init_funcs(self):
        """Find public functions in the module."""
        mod_funcs = [
            x[1]
            for x in inspect.getmembers(
                self.mod,
                lambda f: (inspect.isroutine(f) and (inspect.getmodule(f) is self.mod)),
            )
            if (not x[0].startswith("_"))
        ]
        self.funcs = [
            FuncStruct(m, name_to_path=self.name_to_path, abs_path=self.abs_path)
            for m in mod_funcs
        ]

    def doc_str(self) -> str:
        self.make_relpaths()
        mod_head = f"# Module {self.mod.__name__}"
        mod_ds = self.doc

        def submod_to_link(sub_name: str) -> str:
            rel_path = self.relpaths[sub_name][0]
            return f"[{sub_name}]({rel_path})"

        submodules_head = "## Submodules"
        submodules = [submod_to_link(x.mod.__name__) for x in self.submods]
        submodules_list = "\n\n".join(submodules)
        if not submodules:
            submodules_head = ""

        vars_head = "## Variables"
        vars_ = [x.doc_str() for x in self.vars]
        vars_list = "\n\n".join(vars_)
        if not vars_:
            vars_head = ""

        classes_head = "## Classes"
        classes = [x.doc_str() for x in self.classes]
        classes_list = "\n\n------\n\n".join(classes)
        if not classes:
            classes_head = ""

        funcs_head = "## Functions"
        funcs = [x.doc_str() for x in self.funcs]
        funcs_list = "\n\n------\n\n".join(funcs)
        if not funcs:
            funcs_head = ""

        doc = "\n\n".join(
            [
                mod_head,
                mod_ds,
                submodules_head,
                submodules_list,
                vars_head,
                vars_list,
                classes_head,
                classes_list,
                funcs_head,
                funcs_list,
            ]
        )

        doc = self.make_links(doc)
        return cleanup(doc)

    def make_relpaths(self):
        """
        Create mapping between object name to relative path.

        ~~~markdown

        `ful.path.to.mod.cls` -> [`cls`](../../mod#cls)

        ~~~

        """
        for name, path in self.name_to_path.items():
            if "#" in path:
                relpath, hash_ = path.split("#")
                hash_ = "#" + hash_
            else:
                relpath, hash_ = path, ""
            relpath = os.path.relpath(relpath, self.abs_path)
            if relpath.endswith("."):
                relpath = relpath + "/"
            self.relpaths[name] = (relpath, hash_)

    def make_links(self, doc: str) -> str:
        """
        Create internal link on back-quoted name.

        To ignore this, append a space like `"foo.bar "` .

        """
        for long_name, rel_hash in self.relpaths.items():
            if rel_hash[1]:
                short_name = rel_hash[1][1:]
            else:
                short_name = long_name.rsplit(".", 1)[-1]
            # append a space after short_name because of avoiding unexpected replacing.
            doc = doc.replace(
                f"`{long_name}`", f"[`{short_name} `]({''.join(rel_hash)})"
            )
        return doc

    def write(self):
        """Write documents to files. Directories are created automatically."""
        # create dir.
        os.makedirs(self.out_dir, exist_ok=True)
        # write self.
        with open(
            self.out_dir / self.filename, mode="w", newline="\n", encoding="utf-8"
        ) as index:
            index.write(self.doc_str())
        # write submodules.
        for submod in self.submods:
            submod.write()


class VarStruct(BaseStruct):
    """
    Module variables and class properties.

    **Attributes**

    * var: Module-level object or class property, not module/class/function.
    * name (`str`): Name of the object.

    """

    var: Any

    name: str
    hash_: str

    def __init__(
        self, var, name_to_path: dict, abs_path: str, name: str = None, doc: str = None
    ):
        """
        **Args**

        * var: Target object.
        * name_to_path (`dict`): See `inari.structs.BaseStruct` .
        * abs_path (`str`): See `inari.structs.BaseStruct` .
        * name (`str`): Fallback of `var.__name__` .
        * doc (`str`): Fallback of `inspect.getdoc(var)` .

        """
        super().__init__(name_to_path=name_to_path)
        self.var = var
        self.doc = doc or inspect.getdoc(var) or ""
        name = name or var.__name__
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
        h = ""
        if markdown:
            h = f"{{: {self.hash_} }}"
        if self.doc:
            doc = f"* {self.name} {self.doc}"
        else:
            doc = f"* {self.name}"
        return modify_attrs(doc, h)


class ClsStruct(BaseStruct):
    """
    Class with methods and properties. Attribute docs should be written in class
        docstring like this:

    **Attributes**

    * cls (`type`): Target class.
    * vars (`List[VarStruct]`): Class properties.
    * methods (`List[FuncStruct]`): Methods of the class.
    * hash_ (`str`): Used for HTML id.

    """

    # TODO: get ancestor
    cls: type

    vars: List[VarStruct]
    methods: List["FuncStruct"]

    hash_: str

    def __init__(self, cls: type, abs_path: str, name_to_path: dict):
        """
        **Args**

        * cls (`type`): Class to make documents.
        * abs_path (`str`): See `inari.structs.BaseStruct` .
        * name_to_path (`str`): See `inari.structs.BaseStruct` .

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

        self.init_vars()
        self.init_methods()

    def init_vars(self):
        cls_vars = [
            x
            for x in inspect.getmembers(self.cls, lambda v: v.__class__ is property)
            if (not x[0].startswith("_"))
        ]
        self.vars = [
            VarStruct(
                v[1], name=v[0], name_to_path=self.name_to_path, abs_path=self.abs_path
            )
            for v in cls_vars
        ]

    def init_methods(self):
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
            FuncStruct(m, name_to_path=self.name_to_path, abs_path=self.abs_path)
            for m in methods
        ]

    def doc_str(self) -> str:
        # class {classname}{signature}
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
            init_doc = inspect.getdoc(init)
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
        vars_ = [x.doc_str() for x in self.vars]
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


class FuncStruct(BaseStruct):
    """
    Functions and methods.

    **Attributes**

    * func (`Callable`): Target function.
    * hash_ (`str`): Used for HTML id.

    """

    func: Callable
    hash_: str

    def __init__(self, f: Callable, name_to_path: dict, abs_path: str):
        """
        **Args**

        * f (`Callable`): Target function.
        * abs_path (`str`): See `inari.structs.BaseStruct` .
        * name_to_path (`str`): See `inari.structs.BaseStruct` .

        """
        self.func = f
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
        if self.hash_ != "#" + self.func.__name__:
            head = f"[**{self.func.__name__}**]({self.hash_}){h}"
        else:
            head = f"### {self.func.__name__} {h}"
        full_source = inspect.getsource(self.func)
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
