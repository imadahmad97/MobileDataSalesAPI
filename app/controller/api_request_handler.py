"""
This module contains the function that handles a mobile data purchase request. It takes a request as
input, processes the request into multiple sets of customer information, validates the customer
information, records the transaction in the database, generates a PDF invoice, and returns a JSON
response with the status and BAN of each request.
"""

import logging
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import JSONResponse
from app.service.db_service import DataBaseService
from app.service.parser import parse_csv_content
from app.model.mobile_data_sell_order import MobileDataSellOrder
from app.service.invoice_generator import generate_pdf_invoices
from app.validation.validation_interface import validate_mobile_data_sell_orders

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def handle_mobile_data_sell_request(
    api_request: Request, db_session: Session
) -> JSONResponse:
    """
    This function handles a mobile data sell request. It takes a request as input, validates,
    records, generates PDF invoices, and returns a JSON response with the status and BAN of each
    request.
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
