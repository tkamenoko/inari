from ward import test, using, each

from inari._internal import _path


@test("Relative link from `{page}` to `{link_to}` should be `{result}` .")
@using(
    page="/inari/foo/bar",
    link_to=each("/inari/foo/baz", "/inari/foo/bar", "/inari/baz/spam", "/inari/baz"),
    result=each("baz", "", "../baz/spam", "../baz"),
)
def _(page: str, link_to: str, result: str) -> None:
    assert _path.get_relative_path(page, link_to) == result
