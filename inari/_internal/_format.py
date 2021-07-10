"""
String formatters for internal use.
"""

import re
from collections.abc import Iterable


def join_fragments(fragments: Iterable[str]) -> str:
    return "\n\n".join([x.strip() for x in fragments if x.strip()])


def modify_attrs(doc: str, attributes: str = "") -> str:
    attr_head = r"^[\-+*]\s+(?P<name>[^\s():`[\]]+)?\s*(?P<type>\(?`[^():`]+`\)?)?\s*"
    attr_tail = r"(?P<tail>:\s*(?P<description>.+))?$"

    def replacer(m: re.Match[str]) -> str:
        name = m.group("name")
        type_ = m.group("type") or ""
        have_tail = m.group("tail")
        description = m.group("description") or ""

        modified_name = f"**{name}**{attributes}" if name else ""
        head = " ".join([x for x in ["-", modified_name, type_] if x])
        tail = f": {description}" if have_tail else ""

        return head + tail

    result = re.sub(
        attr_head + attr_tail,
        replacer,
        doc,
        flags=re.MULTILINE,
    )
    return result
