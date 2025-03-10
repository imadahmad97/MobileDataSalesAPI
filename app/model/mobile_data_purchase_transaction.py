from sqlmodel import SQLModel, Field
import datetime
from app.model.mobile_data_sell_order import CustomerInformation


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
    def build_transaction_from_customer_information(
        cls,
        customer_information: CustomerInformation,
    ) -> "MobileDataPurchaseTransaction":
        """
        This method builds a transaction object from a purchase customer_information and response.
        """
        return cls(
            name=customer_information.name,
            date_of_birth=customer_information.date_of_birth,
            credit_card_number=customer_information.credit_card_number,
            credit_card_expiration_date=customer_information.credit_card_expiration_date,
            credit_card_cvv=customer_information.credit_card_cvv,
            billing_account_number=customer_information.billing_account_number,
            requested_mobile_data=customer_information.requested_mobile_data,
            status=customer_information.status,
            validation_errors=customer_information.validation_errors,
        )
