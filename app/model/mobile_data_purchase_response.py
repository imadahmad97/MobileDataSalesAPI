"""
This module contains the MobileDataPurchaseResponse class. This class is used to store the response
to a mobile data purchase request. It includes the name, credit card number, billing account number,
requested mobile data, status, and validation errors for the request.

Methods:
    - __init__
    - update_status
"""


class MobileDataPurchaseResponse:
    """
    This class represents the response to a mobile data purchase request.
    """

    def __init__(
        self,
        name,
        credit_card_number,
        billing_account_number,
        requested_mobile_data,
        status,
        validation_errors,
    ):
        """
        This method initializes a MobileDataPurchaseResponse object with the provided name, credit
        card number, billing account number, requested mobile data, status, and validation errors.
        """
        self.name = name
        self.credit_card_number = credit_card_number
        self.billing_account_number = billing_account_number
        self.requested_mobile_data = requested_mobile_data
        self.status = status
        self.validation_errors = validation_errors

    def update_status(self):
        """
        This method updates the status of the mobile data purchase request based on the presence of
        validation errors.
        """
        if self.validation_errors:
            self.status = "Rejected"
        else:
            self.status = "Approved"
