import locale

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Pretty, DataTable, RichLog

from spendsmart.controllers import TxnController
from spendsmart.domainmodels import Transaction


class TxnList(DataTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cursor_type = "row"

    def on_key(self, event: events.Key) -> None:
        if event.name == "j":
            self.action_cursor_down()
        elif event.name == "k":
            self.action_cursor_up()


class TxnView:
    def __init__(self, txn: Transaction):
        self._txn_details = txn

    def to_datatable_row(self) -> tuple:
        locale.setlocale(locale.LC_ALL, "")
        return (
            self._txn_details.datestamp.strftime("%m/%d/%Y"),
            self._txn_details.description,
            locale.currency(float(self._txn_details.amount) / 100, grouping=True),
        )


class SpendSmartApp(App):
    CSS_PATH = "styles.tcss"

    def __init__(self, txncontrol: TxnController):
        super().__init__()

        self._txncontrol = txncontrol
        self._txns = self._txncontrol.fetch_txns(10)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield TxnList()
            yield Pretty([])
        yield RichLog()
        yield Footer()

    def on_mount(self) -> None:
        txnlist = self.query_one(TxnList)

        txnlist.add_columns(*["Date", "Description", "Amount"])
        txnlist.add_rows([TxnView(txn).to_datatable_row() for txn in self._txns])

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)

    @on(TxnList.RowHighlighted)
    def update_highlighted_view(self) -> None:
        index = self.query_one(TxnList).cursor_row
        self.query_one(Pretty).update(self._txns[index])
