from typing import NamedTuple

from inari._internal import _path
from ward import each, test, using


class Fixtures(NamedTuple):
    page: str
    link_to: str
    result: str


current_dir = Fixtures(page="/inari/foo/bar", link_to="/inari/foo/baz", result="baz")
link_self = Fixtures(page="/inari/foo/bar", link_to="/inari/foo/bar", result="")
another_dir = Fixtures(page="/inari/foo/bar", link_to="/inari/baz", result="../baz")
another_dir_child = Fixtures(
    page="/inari/foo/bar", link_to="/inari/baz/spam", result="../baz/spam"
)


@test("Relative link from `{page}` to `{link_to}` should be `{result}` .")
@using(
    page=each(
        current_dir.page, link_self.page, another_dir.page, another_dir_child.page
    ),
    link_to=each(
        current_dir.link_to,
        link_self.link_to,
        another_dir.link_to,
        another_dir_child.link_to,
    ),
    result=each(
        current_dir.result,
        link_self.result,
        another_dir.result,
        another_dir_child.result,
    ),
)
def _(page: str, link_to: str, result: str) -> None:
    assert _path.get_relative_path(page, link_to) == result
