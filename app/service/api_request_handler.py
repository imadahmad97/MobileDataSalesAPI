from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
from app.interface.mobile_data_purchase_processor_interface import (
    process_mobile_data_purchase_request,
)
from fastapi.responses import JSONResponse
from fastapi import Request
from app.service.db_service import DatabaseService


async def handle_single_mobile_data_purchase_request(
    binary_purchase_request: Request, db_service: DatabaseService
) -> JSONResponse:

    purchase_request: MobileDataPurchaseRequest = (
        await MobileDataPurchaseRequest.build_request_from_binary_file(
            binary_purchase_request
        )
    )

    purchase_response: MobileDataPurchaseResponse = (
        await process_mobile_data_purchase_request(purchase_request, db_service)
    )

    return JSONResponse(
        content={
            f"status for BAN {purchase_response.billing_account_number}": purchase_response.status
        }
    )


async def handle_bulk_mobile_upload_purchase_request(
    csv_path: str, db_service: DatabaseService
) -> JSONResponse:

    responses: list[MobileDataPurchaseResponse] = []

    async for row in MobileDataPurchaseRequest.build_request_list_from_binary_csv(
        csv_path
    ):
        responses.append(await process_mobile_data_purchase_request(row, db_service))

    return JSONResponse(
        content={
            f"status for BAN {response.billing_account_number}": response.status
            for response in responses
        }
    )
