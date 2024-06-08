from typing import Optional, cast
from modrinth_api import ModrinthProject, ModrinthVersionFile
from .manifest_file_box import ManifestFileBox

from manifest import ModrinthManifest

from textual.widgets import Static, Label
from textual.containers import Vertical, VerticalScroll
from textual.reactive import reactive
from textual.app import ComposeResult


class ManifestMenu(Static):
    manifest_name: reactive[str] = reactive("")
    format_version: reactive[str] = reactive("")
    version_id: reactive[str] = reactive("")
    reorder_file_list: reactive[bool] = reactive(False)
    dispirate_file_symbol: reactive[str] = reactive("")

    DEFAULT_CSS = """
    Vertical Label {
        width: 100%;
    }

    Vertical {
        margin-top: 1;
        margin-bottom: 1;
        height: auto;
    }
    """

    def __init__(
        self, manifest_json, dispirate_file_symbol: Optional[str] = None
    ) -> None:
        super().__init__()

        self.manifest = ModrinthManifest(manifest_json=manifest_json)

        self.manifest_name = str(self.manifest.name)
        self.format_version = str(self.manifest.format_version)
        self.version_id = str(self.manifest.version_id)
        self.dispirate_file_symbol = str(dispirate_file_symbol)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(f"{self.manifest_name} {self.version_id}")
            yield Label(f"{len(self.manifest.files)} Files")
        with VerticalScroll(id="filebox-list"):
            for hash, file in self.manifest.files.items():
                yield ManifestFileBox(
                    file_name=cast(ModrinthProject, file.project).title,
                    version=cast(ModrinthVersionFile, file.version_file).version_number,
                    id=f"_{hash}",
                )

    def watch_reorder_file_list(self, new_bool):
        if new_bool:
            self.reorder_file_list = False
        else:
            return

        fileboxes = self.query_one("#filebox-list", VerticalScroll)

        new_file_list = []

        for filebox in fileboxes.query(ManifestFileBox):
            new_file_list.append(
                {
                    "file_name": filebox.file_name,
                    "version": filebox.version,
                    "hash": filebox.id,
                    "is_dispirate": filebox.is_dispirate,
                }
            )

        fileboxes.remove_children()

        # Sorting file list to make sure dispirate files are on top
        new_file_list = sorted(
            new_file_list,
            key=lambda file: not bool(file["is_dispirate"]),
        )

        for file in new_file_list:
            new_filebox = ManifestFileBox(
                file_name=file["file_name"],
                version=file["version"],
                id=file["hash"],
                classes="dispirate" if file["is_dispirate"] else None,
            )
            fileboxes.mount(new_filebox)
            new_filebox.update_symbol()
