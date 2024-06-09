from textual.reactive import reactive
from textual.widgets import Static, Label, Button
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center
from textual.message import Message


class ManagerMenu(Static):
    is_local_manifest_loaded: reactive[bool] = reactive(False)
    is_remote_manifest_loaded: reactive[bool] = reactive(False)
    count_remote_files_only: reactive[int] = reactive(0)
    count_local_files_only: reactive[int] = reactive(0)

    DEFAULT_CSS = """
    ManagerMenu {
        margin-top: 1;
        margin-bottom: 1;
    }

    #manifestmenu-loaded-warning {
        width: auto;
    }

    Vertical {
        height: auto;
    }

    #manifestmenu_container {
        height: auto;
    }

    #menu-middle {
        align: center middle;
    }

    #sync-button {
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="manifestmenu_container"):
            with Vertical(id="menu-middle"):
                with Center():
                    yield Label(
                        "Please Load a Remote and Local Manifest",
                        id="manifestmenu-loaded-warning",
                        classes="highlight-warning",
                    )
                with Center():
                    yield Label(
                        id="local-manifest-outdated-warning", classes="highlight-error"
                    )
                    yield Label(id="all-good-warning", classes="highlight-ok")
                with Center():
                    yield Button("Sync Local", id="sync-button")

    def on_mount(self) -> None:
        outdated_warning = self.query_one("#local-manifest-outdated-warning", Label)
        outdated_warning.display = False

        sync_button = self.query_one("#sync-button", Button)
        sync_button.display = False

        all_good = self.query_one("#all-good-warning", Label)
        all_good.display = False

    def watch_is_local_manifest_loaded(self, new_is_local_manifest_loaded: bool):
        warning_label = self.query_one("#manifestmenu-loaded-warning", Label)
        if new_is_local_manifest_loaded and self.is_remote_manifest_loaded:
            warning_label.display = False
            if self.count_remote_files_only <= 0:
                all_good = self.query_one("#all-good-warning", Label)
                all_good.display = True
                all_good.update("Local Manifest is Up-To-Date with Remote")
        else:
            warning_label.display = True

    def watch_is_remote_manifest_loaded(self, new_is_remote_manifest_loaded: bool):
        warning_label = self.query_one("#manifestmenu-loaded-warning", Label)
        if new_is_remote_manifest_loaded and self.is_local_manifest_loaded:
            warning_label.display = False
            if self.count_remote_files_only <= 0:
                all_good = self.query_one("#all-good-warning", Label)
                all_good.display = True
                all_good.update("Local Manifest is Up-To-Date with Remote")
        else:
            warning_label.display = True

    def watch_count_remote_files_only(self, new_count: int):
        outdated_warning = self.query_one("#local-manifest-outdated-warning", Label)
        sync_button = self.query_one("#sync-button", Button)
        if new_count > 0:
            outdated_warning.update(
                f"Local Manifest is {new_count} Files Behind Remote Manifest"
            )
            outdated_warning.display = True
            sync_button.display = True
        else:
            outdated_warning.display = False
            sync_button.display = False
