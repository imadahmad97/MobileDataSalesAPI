"""
This module contains the CustomerInformation class, which represents a customer's information for a
mobile data purchase request. It contains both the attributes of the request and methods for
validating, constructing, and updating the request.
"""

import datetime
from typing import Union
from pydantic import BaseModel, field_validator


class MobileDataSellOrder(BaseModel):
    """
    This class represents a customer's information for a mobile data purchase request. It contains
    both the attributes of the request and methods for validating, constructing, and updating the
    request.
    """

    name: str
    date_of_birth: datetime.datetime
    credit_card_number: str
    credit_card_expiration_date: datetime.datetime
    credit_card_cvv: str
    billing_account_number: str
    requested_mobile_data: str
    status: str
    validation_errors: list[str]

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def parse_date_of_birth(
        cls, value: Union[str, datetime.datetime]
    ) -> datetime.datetime:
        """
        This method converts the date of birth attribute to a datetime object.
        """
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%m/%d/%Y")
        return value

    @field_validator("credit_card_expiration_date", mode="before")
    @classmethod
    def parse_credit_card_expiration(
        cls, value: Union[str, datetime.datetime]
    ) -> datetime.datetime:
        """
        This method converts the credit card expiration date attribute to a datetime object.
        """
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%m/%y")
        return value

    @classmethod
    async def build_mobile_data_sell_order_from_list(
        cls, customer_info: list[str]
    ) -> "MobileDataSellOrder":
        """
        This method constructs a customer information object from a list of customer information.
        """
        return cls(
            name=customer_info[0],
            date_of_birth=customer_info[1],  # type: ignore
            credit_card_number=customer_info[2],
            credit_card_expiration_date=customer_info[3],  # type: ignore
            credit_card_cvv=customer_info[4],
            billing_account_number=customer_info[5],
            requested_mobile_data=customer_info[6],
            status="Approved",
            validation_errors=[],
        )
