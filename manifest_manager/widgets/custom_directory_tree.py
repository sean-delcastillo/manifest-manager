from pathlib import Path
from typing import Iterable
from textual.widgets import DirectoryTree


class CustomDirectoryTree(DirectoryTree):
    def __init__(
        self,
        path: str | Path,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(path, name=name, id=id, classes=classes, disabled=disabled)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if path.is_dir() or path.suffix == ".mrpack"]
