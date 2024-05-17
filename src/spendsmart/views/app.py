import locale

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Header, Input, Footer, Pretty, DataTable, RichLog

from spendsmart.controllers import TxnController
from spendsmart.domainmodels import Transaction


class TxnListView(DataTable):
    def __init__(self, txns: list[Transaction]):
        super().__init__()

        self._viewable_txns = txns

        self.cursor_type = "row"

    def on_key(self, event: events.Key) -> None:
        if event.name == "j":
            self.action_cursor_down()
        elif event.name == "k":
            self.action_cursor_up()
        elif event.name == "l":
            self.focus()

    def on_mount(self) -> None:
        self.add_columns(*["Date", "Description", "Amount"])
        self.add_rows([TxnView(txn).to_datatable_row() for txn in self._viewable_txns])

    # def update_highlighted_view(self) -> None:
    #     self.query_one(Pretty).update(self._txns[index])


class TxnWidget(Widget):
    def __init__(self, txncontrol: TxnController):
        super().__init__()

        self._txncontrol = txncontrol
        self._viewable_txns = txncontrol.fetch_txns(10)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield TxnListView(self._viewable_txns)
            with Vertical():
                yield Pretty([])
                yield Input(placeholder="Merchant")
                yield Input(placeholder="Category")

    @on(TxnListView.RowHighlighted)
    def view_highlighted_txn(self) -> None:
        txnlist = self.query_one(TxnListView)
        idx = txnlist.cursor_row

        self.query_one(Pretty).update(self._viewable_txns[idx])


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

    def compose(self) -> ComposeResult:
        yield Header()
        yield TxnWidget(self._txncontrol)
        yield RichLog()
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)
