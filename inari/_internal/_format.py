"""
String formatters for internal use.
"""

import re


def cleanup(doc: str) -> str:
    return re.sub(r"\n\n\n\n+", "\n\n\n", doc).strip() + "\n"


def modify_attrs(doc: str, attributes: str = "") -> str:
    result = re.sub(
        r"^\*\s+([^\s():`[\]]+)\s*(\()?(`.+`)?(\))?\s*(:.*)?(?=\n|$)",
        r"* **\1**" + attributes + r" \2\3\4\5",
        doc,
        flags=re.MULTILINE,
    )
    return result
