"""
This module contains the functions that parse a CSV file into a list of MobileDataSellOrder objects.
"""

from app.model.mobile_data_sell_order import MobileDataSellOrder
import io
import csv


async def parse_csv_content(content: bytes) -> list[MobileDataSellOrder]:
    """
    This function parses the content of a CSV file into a list of MobileDataSellOrder objects
    """

    parsed_rows: list[list[str]] = await parse_text_from_csv(content)

    mobile_data_sell_orders: list[MobileDataSellOrder] = []

    for row in parsed_rows:
        mobile_data_sell_order = await build_mobile_data_sell_order(row)
        mobile_data_sell_orders.append(mobile_data_sell_order)

    return mobile_data_sell_orders


async def parse_text_from_csv(content: bytes) -> list[list[str]]:
    """
    This function parses the content of a CSV file into a list of lists of strings
    """
    csv_text: io.StringIO = io.StringIO(content.decode("utf-8"))
    reader: csv.reader = csv.reader(csv_text)  # type: ignore
    parsed_rows: list[list[str]] = list(reader)

    return parsed_rows


async def build_mobile_data_sell_order(row: list[str]) -> MobileDataSellOrder:
    """
    This function builds a MobileDataSellOrder object from a list of strings
    """
    mobile_data_sell_order = MobileDataSellOrder(
        name=row[0],
        date_of_birth=row[1],  # type: ignore
        credit_card_number=row[2],
        credit_card_expiration_date=row[3],  # type: ignore
        credit_card_cvv=row[4],
        billing_account_number=row[5],
        requested_mobile_data=row[6],
        status="Approved",
        validation_errors=[],
    )

    return mobile_data_sell_order
