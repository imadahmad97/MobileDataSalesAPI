from sqlmodel import SQLModel, Field
import datetime


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
