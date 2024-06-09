from typing import Optional
from textual.app import ComposeResult
from textual.widgets import Label, Static
from textual.containers import Horizontal
from textual.reactive import reactive


class ManifestFileBox(Static):
    file_name: reactive[str] = reactive("")
    version: reactive[str] = reactive("")
    is_dispirate: reactive[bool] = reactive(False)
    dispirate_file_symbol: reactive[str] = reactive("")

    DEFAULT_CSS = """
    #filebox-title {
        width: 3fr;
    }

    #filebox-version {
        width: 2fr;
        text-align: right;
    }

    #dispirate-symbol {
        color: red 90%;
        text-align: right;
        margin-left: 1;
    }

    Horizontal {
        height: auto;
        margin: 1;
    }
    """

    def __init__(
        self, file_name: str, version: str, id: str, classes: Optional[str] = None
    ) -> None:
        super().__init__(id=id, classes=classes)
        self.file_name = file_name
        self.version = version

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self.file_name, id="filebox-title")
            yield Label(self.version, id="filebox-version")
            yield Label(id="dispirate-symbol")

    def mark_dispirate(self):
        self.is_dispirate = True
        symbol_label = self.query_one("#dispirate-symbol", Label)
        symbol_label.update(self.dispirate_file_symbol)

    def update_symbol(self):
        if not self.is_dispirate:
            return
        symbol_label = self.query_one("#dispirate-symbol", Label)
        symbol_label.update(self.dispirate_file_symbol)
