from inari._internal import _format
from ward import each, test, using


@test(
    "Description `` {raw_description} `` with `` {attributes} `` should be modified "
    + "into `` {result} `` ."
)
@using(
    raw_description=each(
        "* var (`object`): Target object.",
        "* variables (`list[VariableCollector]`): Class properties. **IMPORTANT!**",
        "* var (`object`): Target object.\n"
        + "* var (`object`): `backtick`\n\n"
        + "**Returns**\n"
        + "* `str`: Return type.\n",
        "* no_description(`str`)",
    ),
    attributes=each("", "{: #ClassItself }", "", ""),
    result=each(
        "* **var** (`object`): Target object.",
        "* **variables**{: #ClassItself } (`list[VariableCollector]`): Class "
        + "properties. **IMPORTANT!**",
        "* **var** (`object`): Target object.\n"
        + "* **var** (`object`): `backtick`\n\n"
        + "**Returns**\n"
        + "* `str`: Return type.\n",
        "* **no_description** (`str`)",
    ),
)
def _(raw_description: str, attributes: str, result: str) -> None:
    assert _format.modify_attrs(raw_description, attributes) == result
