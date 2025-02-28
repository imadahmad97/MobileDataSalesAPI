"""
This module contains the MobileDataPurchaseRequest class. This class represents a mobile data
purchase request. It contains both the attributes of the request and methods for parsing the request
from a binary file and a binary CSV file.

Methods:
    - parse_date_of_birth
    - parse_credit_card_expiration
    - build_request_from_binary_file
    - build_request_list_from_binary_csv
    - _parse_binary_file
    - _parse_binary_csv
    - _decode_base
"""

import datetime
from typing import Union
from pydantic import BaseModel, field_validator


class CustomerInformation(BaseModel):
    """
    This class represents a mobile data purchase request. It contains both the attributes of the
    request and methods for parsing the request from a binary file and a binary CSV file.
    """

    name: str
    date_of_birth: datetime.datetime
    credit_card_number: str
    credit_card_expiration_date: datetime.datetime
    credit_card_cvv: str
    billing_account_number: str
    requested_mobile_data: str
    status: str
    validation_errors: str

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
    async def construct_customer_information_object_from_list(
        cls, customer_info: list[str]
    ) -> "CustomerInformation":
        return cls(
            name=customer_info[0],
            date_of_birth=customer_info[1],  # type: ignore
            credit_card_number=customer_info[2],
            credit_card_expiration_date=customer_info[3],  # type: ignore
            credit_card_cvv=customer_info[4],
            billing_account_number=customer_info[5],
            requested_mobile_data=customer_info[6],
            status="",
            validation_errors="",
        )

    def update_status(self):
        """
        This method updates the status of the mobile data purchase request based on the presence of
        validation errors.
        """
        if self.validation_errors:
            self.status = "Rejected"
        else:
            self.status = "Approved"
