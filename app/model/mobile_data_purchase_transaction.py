from sqlmodel import SQLModel, Field
from typing import Optional
import datetime
import uuid


class MobileDataPurchaseTransaction(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    name: str = Field()
    date_of_birth: datetime.datetime = Field()
    credit_card_number: str = Field(primary_key=True)
    credit_card_expiration_date: datetime.datetime = Field()
    credit_card_cvv: str = Field()
    billing_account_number: str = Field()
    requested_mobile_data: str = Field()
    status: str = Field()
    validation_errors: str = Field()
