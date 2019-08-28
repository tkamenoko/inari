"""
String formatters for internal use. It will be ignored by the module finder of `inari` .
"""

import re


def cleanup(doc: str) -> str:
    return re.sub(r"\n\n\n\n+", "\n\n\n", doc).strip() + "\n"


def modify_attrs(doc: str, h="") -> str:
    # more readable args, attrs and returns.
    result = re.sub(
        r"^\*\s+([^\s():`[\]]+)\s*(\()?(`.+`)?(\))?\s*(:.+)?(?=\n|$)",
        r"* **\1**" + h + r" \2\3\4\5",
        doc,
        flags=re.MULTILINE,
    )
    return result
