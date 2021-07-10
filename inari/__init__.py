"""inari - Write docstrings in Markdown!"""


from .collectors import (
    ModuleCollector,
    VariableCollector,
    FunctionCollector,
    ClassCollector,
)

__all__ = [
    "ModuleCollector",
    "VariableCollector",
    "FunctionCollector",
    "ClassCollector",
]
