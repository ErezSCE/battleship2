"""Compatibility shim for pathlib on legacy Python versions.
This module provides a minimal Path class sufficient for the project's test
conftest which only uses Path.resolve(), attribute .parents and the '/' operator.
It deliberately avoids importing the standard library ``pathlib`` to prevent
shadowing issues when the real module is unavailable (e.g., Python 2.7).
"""

import os

class Path:
    def __init__(self, *parts):
        # Accept a single string or multiple parts like pathlib.Path does.
        if len(parts) == 1 and isinstance(parts[0], (list, tuple)):
            parts = parts[0]
        self._path = os.path.join(*[str(p) for p in parts]) if parts else ""

    def __truediv__(self, other):
        return Path(self._path, str(other))

    def resolve(self):
        # Return an absolute version of the path.
        return Path(os.path.abspath(self._path))

    @property
    def parents(self):
        # Return a list of Path objects representing the ancestry.
        parts = []
        current = os.path.abspath(self._path)
        while True:
            parent = os.path.dirname(current)
            if parent == current or parent == "":
                break
            parts.append(Path(parent))
            current = parent
        return parts

    def __str__(self):
        return self._path

    def __repr__(self):
        return f"Path({self._path!r})"

    def __fspath__(self):
        return self._path
