from textual.app import ComposeResult
from textual.widgets import Label, Static
from textual.containers import Horizontal
from textual.reactive import reactive


class ManifestFileBox(Static):
    file_name: reactive[str] = reactive("")
    version: reactive[str] = reactive("")

    DEFAULT_CSS = """
    #filebox-title {
        width: 4fr;
    }

    #filebox-version {
        width: 1fr;
        text-align: right;
    }

    #dispirate-symbol {
        text-align: right;
        margin-left: 1;
    }
    """

    def __init__(self, file_name: str, version: str, id: str) -> None:
        super().__init__(id=id)
        self.file_name = file_name
        self.version = version

    def compose(self) -> ComposeResult:
        with Horizontal(classes="box"):
            yield Label(self.file_name, id="filebox-title")
            yield Label(self.version, id="filebox-version")
            yield Label(id="dispirate-symbol")

    def mark_dispirate(self, symbol: str = ""):
        symbol_label = self.query_one("#dispirate-symbol", Label)
        symbol_label.update(symbol)
