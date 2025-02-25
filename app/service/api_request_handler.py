"""
This module contains functions that handle API requests. The functions in this module are called by
the FastAPI routes defined in main.py. The functions in this module build a request from a binary
file, process the request, and return a JSON response with the status and BAN of the request.

Dependencies:
    - app.model.mobile_data_purchase_request.MobileDataPurchaseRequest
    - app.model.mobile_data_purchase_response.MobileDataPurchaseResponse
    - app.interface.mobile_data_purchase_processor_interface.process_mobile_data_purchase_request
    - fastapi.responses.JSONResponse
    - fastapi.Request
    - app.service.db_service.DataBaseService
    - logging

Methods:
    - handle_single_mobile_data_purchase_request
    - handle_bulk_mobile_upload_purchase_request
"""

import logging
from fastapi.responses import JSONResponse
from fastapi import Request
from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
from app.interface.mobile_data_purchase_processor_interface import (
    process_mobile_data_purchase_request,
)
from fastapi import HTTPException
from sqlalchemy.orm import Session


async def handle_single_mobile_data_purchase_request(
    binary_purchase_request: Request, db_service: Session
) -> JSONResponse:
    """
    This function handles a single mobile data purchase request. It builds a request from a
    binary file, processes the request, and returns a JSON response with the status and BAN of the
    request.
    """
    try:
        logging.info("Building a mobile data purchase request from a binary file")

        purchase_request: MobileDataPurchaseRequest = (
            await MobileDataPurchaseRequest.build_request_from_binary_file(
                binary_purchase_request
            )
        )

        logging.info("Processing the mobile data purchase request")

        purchase_response: MobileDataPurchaseResponse = (
            await process_mobile_data_purchase_request(purchase_request, db_service)
        )

        logging.info("Successfully processed the mobile data purchase request")

        return JSONResponse(
            content={
                f"status for BAN {purchase_response.billing_account_number}": purchase_response.status
            }
        )
    except Exception:
        logging.error("Failed to process the mobile data purchase request")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to process the mobile data purchase request",
        )


async def handle_bulk_mobile_upload_purchase_request(
    csv_path: str, db_service: Session
) -> JSONResponse:
    """
    This function handles a bulk mobile data purchase request. It builds a list of requests from a
    binary csv file, processes the requests, and returns a JSON response with the status and BAN
    of each request.
    """
    try:
        logging.info(
            "Building a list of mobile data purchase requests from a binary CSV file"
        )

        responses: list[MobileDataPurchaseResponse] = []

        logging.info("Processing the mobile data purchase requests")

        for row in MobileDataPurchaseRequest.build_request_list_from_binary_csv(  # type: ignore
            csv_path
        ):
            responses.append(
                await process_mobile_data_purchase_request(row, db_service)
            )

            logging.info(
                "Successfully processed a mobile data purchase request, BAN: %s",
                row.billing_account_number,
            )

        logging.info("Successfully processed the bulk mobile data purchase requests")

        return JSONResponse(
            content={
                f"status for BAN {response.billing_account_number}": response.status
                for response in responses
            }
        )
    except Exception:
        logging.error("Failed to process the bulk mobile data purchase requests")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to process the bulk mobile data purchase requests",
        )
