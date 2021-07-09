"""
String formatters for internal use.
"""

import re
from typing import Iterable


def join_fragments(fragments: Iterable[str]) -> str:
    return "\n\n".join([x.strip() for x in fragments if x.strip()])


def modify_attrs(doc: str, attributes: str = "") -> str:
    attr_head = r"^\*\s+(?P<name>[^\s():`[\]]+)\s*(?P<type>\(`[^():`]+`\))?\s*"
    attr_tail = r"(?P<tail>:\s*(?P<description>.+))?$"

    def replacer(m: re.Match[str]) -> str:
        name = m.group("name")
        type_ = m.group("type")
        have_tail = m.group("tail")
        description = m.group("description")

        if not have_tail:
            return f"* **{name}**{attributes} {type_}"

        return f"* **{name}**{attributes} {type_}: {description}"

    result = re.sub(
        attr_head + attr_tail,
        replacer,
        doc,
        flags=re.MULTILINE,
    )
    return result
