"""
Templates of document components.
"""

import inspect


def build_yaml_header(**kw: str) -> str:
    headers = [f"{key}: {value}" for key, value in kw.items()]
    yaml_header = "\n".join(["---", *headers, "---"])
    return inspect.cleandoc(yaml_header)
