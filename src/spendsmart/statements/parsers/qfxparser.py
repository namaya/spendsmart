from datetime import datetime
import logging
from pathlib import Path
import xml.etree.ElementTree as ET

from spendsmart.domainmodels import Statement, Transaction, TransactionType


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

            datestamp = datetime.strptime(txn.find("DTUSER").text, "%Y%m%d%H%M%S.%f")
            date_posted = datetime.strptime(
                txn.find("DTPOSTED").text, "%Y%m%d%H%M%S.%f"
            )

            transactions.append(
                Transaction(
                    datestamp=datestamp,
                    date_posted=date_posted,
                    description=txn.find("NAME").text,
                    amount=int(txn.find("TRNAMT").text.replace(".", "")),
                )
            )

        logger.info(f"Found {len(transactions)} transactions in statement.")

        return Statement(
            account_number=account_number,
            start_date=stmtroot.find("BANKTRANLIST").find("DTSTART").text,
            end_date=stmtroot.find("BANKTRANLIST").find("DTEND").text,
            transactions=transactions,
        )
