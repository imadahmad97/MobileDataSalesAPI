from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
from app.interface.validation_interface import validate_purchase_request


async def process_mobile_data_purchase_request(mobile_data_purchase_request):
    # Prep Step: Initialize a new mobile data purchase request object:
    purchase_request = await MobileDataPurchaseRequest.from_binary_data(
        mobile_data_purchase_request
    )

    # Prep Step: Initialize a new mobile data purchase response object:
    purchase_response = MobileDataPurchaseResponse(
        name=purchase_request.name,
        credit_card_number=purchase_request.credit_card_number,
        billing_account_number=purchase_request.billing_account_number,
        requested_mobile_data=purchase_request.requested_mobile_data,
        status="",
        validation_errors=[],
    )

    # Step 1: Validate the purchase request and append any validation errors to the response object
    purchase_response.validation_errors.append(
        validate_purchase_request(
            purchase_request.date_of_birth,
            purchase_request.credit_card_number,
            purchase_request.credit_card_expiration_date,
        )
    )

    # Step 2: Save the purchase request to the database

    # Step 3: Generate a PDF invoice for the purchase request

    # Return extracted values
    # return {
    #     "name": purchase_request.name,
    #     "date_of_birth": purchase_request.date_of_birth,
    #     "credit_card_number": purchase_request.credit_card_number,
    #     "credit_card_expiration_date": purchase_request.credit_card_expiration_date,
    #     "credit_card_cvv": purchase_request.credit_card_cvv,
    #     "billing_account_number": purchase_request.billing_account_number,
    #     "requested_mobile_data": purchase_request.requested_mobile_data,
    # }

    return purchase_response.validation_errors
