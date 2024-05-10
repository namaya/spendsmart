from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList

from spendsmart.controllers import TxnController


class SpendSmartApp(App):
    def __init__(self, txncontrol: TxnController):
        super().__init__()

        self._txncontrol = txncontrol

    def compose(self) -> ComposeResult:
        txns = self._txncontrol.list(10)
        yield Header()
        yield OptionList(*[txn.description for txn in txns])
        yield Footer()
