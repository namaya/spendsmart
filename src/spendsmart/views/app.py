import locale

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import (
    Header,
    Input,
    Footer,
    ListView,
    ListItem,
    Pretty,
    DataTable,
    RichLog,
)

from spendsmart.controllers import TxnController
from spendsmart.domainmodels import Transaction


locale.setlocale(locale.LC_ALL, "")


# class TxnView(Widget):

#     class Escaped(Message):
#         def __init__(self):
#             super().__init__()

#     def __init__(self):
#         super().__init__()

#         self._pretty = Pretty([])
#         self._merchant_input = Input(placeholder="Merchant")
#         self._category_input = Input(placeholder="Category")

#     def compose(self) -> ComposeResult:
#         with Vertical():
#             yield self._pretty
#             yield ListView(
#                 ListItem(self._merchant_input),
#                 ListItem(self._category_input),
#             )

#     def update(self, txn: Transaction) -> None:
#         self._pretty.update(txn)
#         if txn.merchant != "":
#             self._merchant_input.value = txn.merchant
#         self._category_input.value = txn.description

#     def on_key(self, event: events.Key) -> None:
#         if event.name == "escape":
#             self.post_message(self.Escaped())

#     def focus(self) -> None:
#         self._merchant_input.focus()


class InputModal(Input):
    BINDINGS = [
        ("escape", "unmount", "Unmount modal."),
        ("enter", "unmount", "Unmount modal."),
    ]

    # await def on_unmount(self) -> None:
    #     await self.post_message(self.value)


class TxnListView(DataTable):

    BINDINGS = [
        ("j", "cursor_down", "Move cursor down"),
        ("k", "cursor_up", "Move cursor up"),
        ("m", "edit_merchant", "Edit merchant."),
    ]

    def __init__(self, txns: list[Transaction]):
        super().__init__()

        self._viewable_txns = txns

        self.cursor_type = "row"

    async def on_mount(self) -> None:
        self.add_columns(*["Date", "Description", "Amount", "Merchant", "Category"])

        self.add_rows(
            [
                (
                    txn.datestamp.strftime("%m/%d/%Y"),
                    txn.description,
                    locale.currency(float(txn.amount) / 100, grouping=True),
                    txn.merchant,
                    txn.category,
                )
                for txn in self._viewable_txns
            ]
        )

    async def action_edit_merchant(self) -> None:
        input_widget = InputModal(placeholder="Merchant")

        await self.mount(input_widget)
        input_widget.focus()

    # @on(InputModal.Unmount)


# class TxnWidget(Widget):

#     def __init__(self, txncontrol: TxnController):
#         super().__init__()

#         self._txncontrol = txncontrol
#         self._viewable_txns = txncontrol.fetch_txns(10)

#         self._txnview = TxnView()
#         self._txnlistview = TxnListView(self._viewable_txns)

#     def compose(self) -> ComposeResult:
#         with Horizontal():
#             yield self._txnlistview
#             yield self._txnview

#     @on(TxnListView.RowHighlighted)
#     def view_highlighted_txn(self) -> None:
#         self._txnview.update(self._viewable_txns[self._txnlistview.cursor_row])

#     @on(TxnListView.RowSelected)
#     def focus_txnview(self) -> None:
#         self._txnview.focus()

#     @on(TxnView.Escaped)
#     def focus_txnviewlist(self) -> None:
#         self._txnlistview.focus()


class SpendSmartApp(App):
    CSS_PATH = "styles.tcss"

    def __init__(self, txncontrol: TxnController):
        super().__init__()

        self._txncontrol = txncontrol
        self._viewable_txns = txncontrol.fetch_txns(10)

    def compose(self) -> ComposeResult:
        yield Header()
        yield TxnListView(self._viewable_txns)
        yield RichLog()
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)
