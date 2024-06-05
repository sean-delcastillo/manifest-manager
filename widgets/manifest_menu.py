from typing import cast
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

    def __init__(self, manifest_json) -> None:
        super().__init__()

        self.manifest = ModrinthManifest(manifest_json=manifest_json)

        self.manifest_name = str(self.manifest.name)
        self.format_version = str(self.manifest.format_version)
        self.version_id = str(self.manifest.version_id)

    def compose(self) -> ComposeResult:
        with Vertical(classes="box"):
            yield Label(f"Modpack: {self.name}")
            yield Label(f"Format Version: {self.format_version}")
            yield Label(f"Modpack Version: {self.version_id}")
            yield Label(f"Mod Count: {len(self.manifest.files)}")
        with VerticalScroll():
            for hash, file in self.manifest.files.items():
                yield ManifestFileBox(
                    file_name=cast(ModrinthProject, file.project).title,
                    version=cast(ModrinthVersionFile, file.version_file).version_number,
                    id=f"_{hash}",
                )

    def watch_reorder_file_list(self, new_bool):
        if new_bool:
            self.reorder_file_list = False
        # TODO: Write the function to order dispirate files on top
