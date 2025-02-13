class MobileDataPurchaseResponse:
    def __init__(
        self,
        name,
        credit_card_number,
        billing_account_number,
        requested_mobile_data,
        status,
        validation_errors,
    ):
        self.name = name
        self.credit_card_number = credit_card_number
        self.billing_account_number = billing_account_number
        self.requested_mobile_data = requested_mobile_data
        self.status = status
        self.validation_errors = validation_errors
