from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList, RichLog

from spendsmart.controllers import TxnController


class VimOptionList(OptionList):
    def on_key(self, event: events.Key) -> None:
        if event.name == "j":
            self.action_cursor_down()
        elif event.name == "k":
            self.action_cursor_up()


class SpendSmartApp(App):
    def __init__(self, txncontrol: TxnController):
        super().__init__()

        self._txncontrol = txncontrol

    def compose(self) -> ComposeResult:
        txns = self._txncontrol.fetch_txns(10)

        yield Header()
        yield VimOptionList(*[txn.description for txn in txns])
        yield RichLog()
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)
