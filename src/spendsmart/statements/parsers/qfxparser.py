import logging
from pathlib import Path
import xml.etree.ElementTree as ET

from spendsmart.statements.dataclasses import Statement, Transaction, TransactionType


logger = logging.getLogger(__name__)


class QfxParser:
    def parse(self, stmtpath: Path) -> Statement:
        logger.info(f"Parsing QFX file '{stmtpath}'.")

        with stmtpath.open("r") as f:
            xml_tree = ET.parse(f)

        ofxroot = xml_tree.getroot()
        stmtroot = (
            ofxroot.find("CREDITCARDMSGSRSV1").find("CCSTMTTRNRS").find("CCSTMTRS")
        )

        currency = stmtroot.find("CURDEF").text
        account_number = stmtroot.find("CCACCTFROM").find("ACCTID").text
        ledger_balance = float(stmtroot.find("LEDGERBAL").find("BALAMT").text)
        available_balance = float(stmtroot.find("AVAILBAL").find("BALAMT").text)

        transactions = []

        for txn in stmtroot.find("BANKTRANLIST").findall("STMTTRN"):
            txn_type = txn.find("TRNTYPE").text

            transactions.append(
                Transaction(
                    type=(
                        TransactionType.CREDIT
                        if txn_type == "CREDIT"
                        else TransactionType.DEBIT
                    ),
                    date_posted=txn.find("DTPOSTED").text,
                    description=txn.find("NAME").text,
                    amount=float(txn.find("TRNAMT").text),
                    balance=0,
                )
            )

        logger.info(f"Found {len(transactions)} transactions in statement.")

        return Statement(
            account_number=account_number,
            start_date=stmtroot.find("BANKTRANLIST").find("DTSTART").text,
            end_date=stmtroot.find("BANKTRANLIST").find("DTEND").text,
            transactions=transactions,
        )
