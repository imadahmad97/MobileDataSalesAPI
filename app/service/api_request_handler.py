from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.service.mobile_data_purchase_processor import (
    process_mobile_data_purchase_request,
)


async def handle_single_mobile_data_purchase_request(
    binary_purchase_request, db_service
):
    purchase_request = await MobileDataPurchaseRequest.build_from_binary_file(
        binary_purchase_request
    )
    return await process_mobile_data_purchase_request(purchase_request, db_service)


async def handle_bulk_mobile_upload_purchase_request(csv_path, db_service):
    for row in MobileDataPurchaseRequest.build_from_binary_csv(csv_path):
        await process_mobile_data_purchase_request(row, db_service)
