"""Path and link"""


import os
from pathlib import PurePosixPath


def get_relative_path(current_page: str, link_to: str) -> str:
    current_path = PurePosixPath(current_page)
    current_dir = current_path.parent
    relpath = os.path.relpath(link_to, current_dir)
    if relpath == current_path.name:
        return ""
    return relpath
