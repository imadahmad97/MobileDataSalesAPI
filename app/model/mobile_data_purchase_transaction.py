from sqlmodel import SQLModel, Field
import datetime
from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest


class MobileDataPurchaseTransaction(SQLModel, table=True):
    name: str = Field()
    date_of_birth: datetime.datetime = Field()
    credit_card_number: str = Field(primary_key=True)
    credit_card_expiration_date: datetime.datetime = Field()
    credit_card_cvv: str = Field()
    billing_account_number: str = Field()
    requested_mobile_data: str = Field()
    status: str = Field()
    validation_errors: str = Field()

    @classmethod
    def build_transaction_from_request_and_response(
        cls,
        request: MobileDataPurchaseRequest,
        status: str,
        validation_errors: str,
    ) -> "MobileDataPurchaseTransaction":
        """
        This method builds a transaction object from a purchase request and response.
        """
        return cls(
            name=request.name,
            date_of_birth=request.date_of_birth,
            credit_card_number=request.credit_card_number,
            credit_card_expiration_date=request.credit_card_expiration_date,
            credit_card_cvv=request.credit_card_cvv,
            billing_account_number=request.billing_account_number,
            requested_mobile_data=request.requested_mobile_data,
            status=status,
            validation_errors=validation_errors,
        )
