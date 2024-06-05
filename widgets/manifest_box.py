import json
from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from manifest import ModrinthManifest, read_remote

from .custom_directory_tree import CustomDirectoryTree
from .manifest_menu import ManifestMenu
from .manifest_file_box import ManifestFileBox

from textual.widgets import DirectoryTree, Static, Button, Label, Input
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.dom import DOMNode


class ManifestBox(Static):
    class ManifestLoaded(Message):
        _control: Optional[DOMNode] = None

        @property
        def control(self):
            return self._control

        @control.setter
        def control(self, value):
            self._control = value

        def __init__(self, manifest: ModrinthManifest, control: DOMNode | None):
            self.manifest = manifest
            self.control = control
            super().__init__()

    dispirate_files: reactive[list] = reactive([])
    dispirate_file_symbol: str = ""

    DEFAULT_CSS = """
    .dispirate {
        background: red 20%;
    }
    """

    def watch_dispirate_files(self, new_dispirate_files: list):
        if new_dispirate_files == []:
            return

        manifest_menu = self.query_one(ManifestMenu)
        hash: str
        for hash in new_dispirate_files:
            file_box = manifest_menu.query_one(f"#_{hash}", ManifestFileBox)
            file_box.mark_dispirate(self.dispirate_file_symbol)
            file_box.add_class("dispirate")


class LocalManifestBox(ManifestBox):
    local_manifest_path: reactive[Path] = reactive(Path.home())
    is_directory_tree_open = False
    dispirate_file_symbol = "<<"

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.local_manifest_path = event.path
        self.is_directory_tree_open = False
        self.get_child_by_id("dir_tree").remove()

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        directory_tree = self.query_one(DirectoryTree)
        if event.path == directory_tree.path:
            directory_tree.path = event.path.parent
        else:
            directory_tree.path = event.path

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "local_file_select" and self.is_directory_tree_open == False:
            self.is_directory_tree_open = True
            directory_tree = CustomDirectoryTree(Path.home(), id="dir_tree")
            self.mount(directory_tree)
        elif button_id == "local_file_select":
            self.is_directory_tree_open = False
            self.get_child_by_id("dir_tree").remove()

    def add_manifest_menu(self) -> None:
        if self.local_manifest_path == Path.home():
            return
        with ZipFile(self.local_manifest_path, "r") as local_pack:
            with local_pack.open("modrinth.index.json") as local_manifest:
                manifest_json = json.loads(local_manifest.read())
                manifest_menu = ManifestMenu(manifest_json=manifest_json)
                self.mount(manifest_menu)

                self.post_message(self.ManifestLoaded(manifest_menu.manifest, self))

    def watch_local_manifest_path(self, new_manifest_path: str) -> None:
        try:
            path_input = self.query_one("#local_path_input", Input)
            if str(new_manifest_path) != ".":
                path_input.value = str(new_manifest_path)
        except:
            pass
        self.add_manifest_menu()

    def compose(self) -> ComposeResult:
        yield Label("Local Manifest")
        with Horizontal(classes="box"):
            yield Input(
                type="text",
                disabled=True,
                value=str(self.local_manifest_path),
                id="local_path_input",
            )
            yield Button("Select File", id="local_file_select")


class RemoteManifestBox(ManifestBox):
    is_manifest_loaded: reactive[bool] = reactive(False)
    dispirate_file_symbol = ">>"

    def toggle_is_manifest_loaded(self) -> None:
        self.is_manifest_loaded = not self.is_manifest_loaded
        if self.is_manifest_loaded:
            manifest_menu = self.query_one(ManifestMenu)
            self.post_message(self.ManifestLoaded(manifest_menu.manifest, self))

    def add_manifest_menu(self) -> None:
        manifest_json = read_remote(self.query_one("#remote_url_input", Input).value)
        manifest_menu = ManifestMenu(manifest_json=manifest_json)
        self.mount(manifest_menu)

    def remove_manifest_menu(self) -> None:
        self.query_one(ManifestMenu).remove()

    def relabel_load_button(self, label: str) -> None:
        button: Button = self.query_one("#load_remote_button", Button)
        button.label = label

    def watch_is_manifest_loaded(self, is_manifest_loaded: bool):
        if is_manifest_loaded:
            self.add_manifest_menu()
            self.relabel_load_button("Unload Remote")
            self.query_one("#remote_url_input").disabled = True
        else:
            try:
                self.remove_manifest_menu()
                self.relabel_load_button("Load Remote")
                self.query_one("#remote_url_input").disabled = False
            except:
                pass

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "load_remote_button":
            self.toggle_is_manifest_loaded()

    def compose(self) -> ComposeResult:
        yield Label("Remote Manifest")
        with Horizontal(classes="box"):
            yield Input(
                type="text", value=ModrinthManifest.remote_url, id="remote_url_input"
            )
            yield Button("Load Remote", id="load_remote_button")
