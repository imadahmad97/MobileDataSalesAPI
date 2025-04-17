"""
This module contains the functions that parse a CSV file into a list of MobileDataSellOrder objects.
"""

from app.model.mobile_data_sell_order import MobileDataSellOrder
import io
import csv


def parse_csv_content(content: bytes) -> list[MobileDataSellOrder]:
    """
    This function parses the content of a CSV file into a list of MobileDataSellOrder objects

    Args:
        content (bytes): The content of the CSV file as bytes.
    """

    parsed_rows: list[list[str]] = parse_text_from_binary(content)

    mobile_data_sell_orders: list[MobileDataSellOrder] = []

    for row in parsed_rows:
        mobile_data_sell_order = (
            MobileDataSellOrder.build_mobile_data_sell_order_from_list(row)
        )
        mobile_data_sell_orders.append(mobile_data_sell_order)

    return mobile_data_sell_orders


def parse_text_from_binary(content: bytes) -> list[list[str]]:
    """
    This function parses the content of a CSV file into a list of lists of strings

    Args:
        content (bytes): The content of the CSV file as bytes.
    """
    csv_text: io.StringIO = io.StringIO(content.decode("utf-8"))
    reader: csv.reader = csv.reader(csv_text)  # type: ignore
    parsed_rows: list[list[str]] = list(reader)

    return parsed_rows
