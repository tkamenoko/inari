from typing import NamedTuple

from inari._internal import _format
from ward import each, test, using


class Fixtures(NamedTuple):
    raw_description: str
    attributes: str
    result: str


simple = Fixtures(
    raw_description="- var (`object`): Target object.",
    attributes="",
    result="- **var** (`object`): Target object.",
)
attr_and_emphasize = Fixtures(
    raw_description="* variables (`list[VariableCollector]`):"
    + " Class properties. **IMPORTANT!**",
    attributes="{: #ClassItself }",
    result="- **variables**{: #ClassItself } (`list[VariableCollector]`): Class "
    + "properties. **IMPORTANT!**",
)
multiline = Fixtures(
    raw_description="* var (`object`): Target object.\n"
    + "+ var (`object`): `backtick`\n\n"
    + "**Returns**\n"
    + "* `str`: Return type.\n",
    attributes="",
    result="- **var** (`object`): Target object.\n"
    + "- **var** (`object`): `backtick`\n\n"
    + "**Returns**\n"
    + "- `str`: Return type.\n",
)
no_description = Fixtures(
    raw_description="* no_description(`str`)",
    attributes="",
    result="- **no_description** (`str`)",
)


@test(
    "Description `` {raw_description} `` with `` {attributes} `` should be modified "
    + "into `` {result} `` ."
)
@using(
    raw_description=each(
        simple.raw_description,
        attr_and_emphasize.raw_description,
        multiline.raw_description,
        no_description.raw_description,
    ),
    attributes=each(
        simple.attributes,
        attr_and_emphasize.attributes,
        multiline.attributes,
        no_description.attributes,
    ),
    result=each(
        simple.result,
        attr_and_emphasize.result,
        multiline.result,
        no_description.result,
    ),
)
def _(raw_description: str, attributes: str, result: str) -> None:
    assert _format.modify_attrs(raw_description, attributes) == result
