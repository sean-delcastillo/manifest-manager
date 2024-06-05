from typing import Optional
from manifest import ModrinthManifest

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

from widgets import RemoteManifestBox, LocalManifestBox, ManagerMenu, ManifestBox


class ManagerApp(App):
    CSS_PATH = "manifest-manager.tcss"
    local_manifest: Optional[ModrinthManifest] = None
    remote_manifest: Optional[ModrinthManifest] = None

    @on(ManifestBox.ManifestLoaded, "#local")
    def handle_local_manifest_loaded(self, event: LocalManifestBox.ManifestLoaded):
        self.local_manifest = event.manifest
        manager_menu = self.query_one(ManagerMenu)
        manager_menu.is_local_manifest_loaded = True
        if manager_menu.is_remote_manifest_loaded:
            self.scan_manifests()

    @on(ManifestBox.ManifestLoaded, "#remote")
    def handle_remote_manifest_loaded(self, event: RemoteManifestBox.ManifestLoaded):
        self.remote_manifest = event.manifest
        manager_menu = self.query_one(ManagerMenu)
        manager_menu.is_remote_manifest_loaded = True
        if manager_menu.is_local_manifest_loaded:
            self.scan_manifests()

    def scan_manifests(self):
        files_in_remote_only = []
        files_in_local_only = []

        for file_hash, file in self.remote_manifest.files.items():
            if file_hash not in self.local_manifest.files.keys():
                files_in_remote_only.append(file_hash)

        for file_hash, file in self.local_manifest.files.items():
            if file_hash not in self.remote_manifest.files.keys():
                files_in_local_only.append(file_hash)

        remote = self.query_one("#remote", RemoteManifestBox)
        local = self.query_one("#local", LocalManifestBox)

        remote.dispirate_files = files_in_remote_only
        local.dispirate_files = files_in_local_only

        manager_menu = self.query_one(ManagerMenu)
        manager_menu.count_local_files_only = len(files_in_local_only)
        manager_menu.count_remote_files_only = len(files_in_remote_only)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="box"):
            yield ManagerMenu()
            with Horizontal(classes="box"):
                yield RemoteManifestBox(classes="box", id="remote")
                yield LocalManifestBox(classes="box", id="local")
        yield Footer()


if __name__ == "__main__":
    ManagerApp().run()
