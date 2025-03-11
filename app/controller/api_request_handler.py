"""
This module contains the function that handles a mobile data purchase request. It takes a request as
input, processes the request into multiple sets of customer information, validates the customer
information, records the transaction in the database, generates a PDF invoice, and returns a JSON
response with the status and BAN of each request.
"""

import io
import csv
import logging
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.service.db_service import DataBaseService
from app.model.mobile_data_sell_order import MobileDataSellOrder
from app.service.invoice_generation_service import generate_pdf_invoices
from app.service.validation_service import validate_mobile_data_sell_orders

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def handle_mobile_data_purchase_request(
    api_request: Request, db_session: Session
) -> JSONResponse:
    """
    This function handles a mobile data purchase request. It takes a request as input, processes the
    request into multiple sets of customer information, validates the customer information, records
    the transaction in the database, generates a PDF invoice, and returns a JSON response with the
    status and BAN of each request.
    """

    # Prep Step: Parse the CSV content into a list of MobileDataSellOrder objects
    mobile_data_sell_orders: list[MobileDataSellOrder] = await parse_csv_content(
        await api_request.body()
    )

    # Step 1: Validate the mobile data sell orders
    validate_mobile_data_sell_orders(mobile_data_sell_orders)

    # Step 2: Record the transaction in the database
    DataBaseService.record_transactions(mobile_data_sell_orders, db_session)

    # Step 3: Generate PDF invoices
    generate_pdf_invoices(mobile_data_sell_orders)

    # Step 4: Get the responses
    responses: dict = await get_responses(mobile_data_sell_orders)

    return JSONResponse(content=responses)


async def parse_csv_content(content: bytes) -> list[MobileDataSellOrder]:

    csv_text: io.StringIO = io.StringIO(content.decode("utf-8"))
    reader: csv.reader = csv.reader(csv_text)
    parsed_rows: list[list[str]] = list(reader)

    mobile_data_sell_orders: list[MobileDataSellOrder] = []

    for row in parsed_rows:
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
        mobile_data_sell_orders.append(mobile_data_sell_order)

    return mobile_data_sell_orders


async def get_responses(mobile_data_sell_orders: list[MobileDataSellOrder]) -> dict:
    """
    This function returns a dictionary containing the status and BAN of each mobile data sell order.
    """
    responses: dict = {}

    for mobile_data_sell_order in mobile_data_sell_orders:
        responses[f"Status for BAN {mobile_data_sell_order.billing_account_number}"] = (
            mobile_data_sell_order.status
        )

    return responses
