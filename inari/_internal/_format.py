"""
String formatters for internal use.
"""

import re


def cleanup(doc: str) -> str:
    return re.sub(r"\n\n\n\n+", "\n\n\n", doc).strip() + "\n"


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
