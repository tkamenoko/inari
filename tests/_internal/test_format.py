from ward import test, using, each

from inari._internal import _format


@test(
    "Description `` {raw_description} `` with `` {attributes} `` should be modified "
    + "into `` {result} `` ."
)
@using(
    raw_description=each(
        "* var (`object`): Target object.",
        "* variables (`list[VariableCollector]`): Class properties. **IMPORTANT!**",
    ),
    attributes=each("", "{: #ClassItself }"),
    result=each(
        "* **var** (`object`): Target object.",
        "* **variables**{: #ClassItself } (`list[VariableCollector]`): Class "
        + "properties. **IMPORTANT!**",
    ),
)
def _(raw_description: str, attributes: str, result: str) -> None:
    assert _format.modify_attrs(raw_description, attributes) == result
