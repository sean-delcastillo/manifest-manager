from typing import Optional
from textual.reactive import reactive
from textual.widgets import Static, Label
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical


class ManagerMenu(Static):
    is_local_manifest_loaded: reactive[bool] = reactive(False)
    is_remote_manifest_loaded: reactive[bool] = reactive(False)
    count_remote_files_only: reactive[int] = reactive(0)
    count_local_files_only: reactive[int] = reactive(0)

    DEFAULT_CSS = """
    #manifestmenu-remote-label {
        width: 1fr;
        margin-left: 1;
        margin-right: 1;
    }

    #manifestmenu-local-label {
        width: 1fr;
        margin-left: 1;
        margin-right: 1;
        text-align: right;
    }

    #manifestmenu-loaded-warning {
        background: orange 50%;
        width: auto;
        margin-left: 1;
        margin-right: 1;
        padding-left: 1;
        padding-right: 1;
    }

    #manifestmenu-remote-count {
        width: 1fr;
        margin-left: 1;
        margin-right: 1;
    }

    #manifestmenu-local-count {
        width: 1fr;
        margin-left: 1;
        margin-right: 1;
        text-align: right;
    }

    .label_highlight {
        color: red 90%;
    }

    Vertical {
        height: auto;
    }    
    """

    def compose(self) -> ComposeResult:
        with Horizontal(classes="box"):
            with Vertical(id="manifestmenu-remote-group"):
                yield Label("Remote Manifest Loaded", id="manifestmenu-remote-label")
                yield Label(id="manifestmenu-remote-count")
            yield Label(
                "Please Load a Remote and Local Manifest",
                id="manifestmenu-loaded-warning",
            )
            with Vertical(id="manifestmenu-local-group"):
                yield Label("Local Manifest Loaded", id="manifestmenu-local-label")
                yield Label(id="manifestmenu-local-count")

    def on_mount(self) -> None:
        remote_label = self.query_one("#manifestmenu-remote-label", Label)
        remote_label.display = False

        local_label = self.query_one("#manifestmenu-local-label", Label)
        local_label.display = False

        remote_count = self.query_one("#manifestmenu-remote-count", Label)
        remote_count.display = False

        local_count = self.query_one("#manifestmenu-local-count", Label)
        local_count.display = False

    def watch_is_local_manifest_loaded(self, new_is_local_manifest_loaded: bool):
        local_label = self.query_one("#manifestmenu-local-label", Label)
        warning_label = self.query_one("#manifestmenu-loaded-warning", Label)
        if new_is_local_manifest_loaded:
            local_label.display = True
        else:
            local_label.display = False
        if new_is_local_manifest_loaded and self.is_remote_manifest_loaded:
            warning_label.display = False
        else:
            warning_label.display = True

    def watch_is_remote_manifest_loaded(self, new_is_remote_manifest_loaded: bool):
        remote_label = self.query_one("#manifestmenu-remote-label", Label)
        warning_label = self.query_one("#manifestmenu-loaded-warning", Label)
        if new_is_remote_manifest_loaded:
            remote_label.display = True
        else:
            remote_label.display = False
        if new_is_remote_manifest_loaded and self.is_local_manifest_loaded:
            warning_label.display = False
        else:
            warning_label.display = True

    def watch_count_remote_files_only(self, new_count: int):
        remote_count = self.query_one("#manifestmenu-remote-count", Label)
        if new_count > 0:
            remote_count.display = True
            remote_count.add_class("label_highlight")
        remote_count.update(f"{new_count} >>")

    def watch_count_local_files_only(self, new_count: int):
        local_count = self.query_one("#manifestmenu-local-count", Label)
        if new_count > 0:
            local_count.display = True
            local_count.add_class("label_highlight")
        local_count.update(f"<< {new_count}")
