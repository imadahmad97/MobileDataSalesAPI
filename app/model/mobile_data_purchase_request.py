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
import csv
import base64
from typing import Union, Type
from fastapi import Request, HTTPException
from pydantic import BaseModel, field_validator


class MobileDataPurchaseRequest(BaseModel):
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
    async def build_request_from_binary_file(
        cls: Type["MobileDataPurchaseRequest"], request: Request
    ) -> "MobileDataPurchaseRequest":
        """
        This method builds a mobile data purchase request from a binary file.
        """
        parsed_data: dict = await cls._parse_binary_file(await request.body())

        return cls(**parsed_data)

    @classmethod
    def build_request_list_from_binary_csv(
        cls: Type["MobileDataPurchaseRequest"], file_path: str
    ) -> list["MobileDataPurchaseRequest"]:
        """
        This method builds a list of mobile data purchase requests from a binary CSV file.
        """
        decoded_data: list = cls._parse_binary_csv(file_path)

        return [cls(**row) for row in decoded_data]

    @staticmethod
    async def _parse_binary_file(contents: bytes) -> dict:
        """
        Parses the contents of a binary file and returns the data as a dictionary.
        This method only extracts data; validation is handled separately.
        """
        decoded_text = MobileDataPurchaseRequest._decode_base64_text(contents)

        parsed_data = {}

        for line_number, line in enumerate(decoded_text.split("\n"), start=1):
            if not line.strip():
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.lower().replace(" ", "_").strip()
            value = value.strip()

            parsed_data[key] = value

        errors = MobileDataPurchaseRequest._validate_parsed_data(parsed_data)

        if errors:
            raise HTTPException(status_code=400, detail={"errors": errors})

        return parsed_data

    @staticmethod
    def _parse_binary_csv(file_path: str) -> list[dict]:
        """
        This method parses the contents of a binary CSV file and returns the data as a list of
        dictionaries.
        """
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)

            headers = []
            for header in next(csv_reader):
                headers.append(MobileDataPurchaseRequest._decode_base64_text(header))  # type: ignore

            parsed_data = []
            for row in csv_reader:
                parsed_data.append(
                    {
                        headers[i]: MobileDataPurchaseRequest._decode_base64_text(cell)  # type: ignore
                        for i, cell in enumerate(row)
                    }
                )

        return parsed_data

    @staticmethod
    def _validate_parsed_data(parsed_data: dict) -> list[str]:
        """
        Validates parsed data to ensure all required fields are present and correctly formatted.
        Returns a list of error messages if validation fails.
        """
        errors = []
        expected_keys = {
            "name",
            "date_of_birth",
            "credit_card_number",
            "credit_card_expiration_date",
            "credit_card_cvv",
            "billing_account_number",
            "requested_mobile_data",
        }

        missing_keys = expected_keys - parsed_data.keys()
        if missing_keys:
            errors.append(f"Missing keys: {', '.join(missing_keys)}")

        if "date_of_birth" in parsed_data:
            try:
                datetime.datetime.strptime(parsed_data["date_of_birth"], "%m/%d/%Y")
            except ValueError:
                errors.append(
                    "Invalid date format for 'date_of_birth'. Expected MM/DD/YYYY."
                )

        if "credit_card_expiration_date" in parsed_data:
            try:
                datetime.datetime.strptime(
                    parsed_data["credit_card_expiration_date"], "%m/%y"
                )
            except ValueError:
                errors.append(
                    "Invalid date format for 'credit_card_expiration_date'. Expected MM/YY."
                )

        return errors

    @staticmethod
    def _decode_base64_text(encoded_data: bytes) -> str:
        """
        This method decodes a base64 encoded string and returns the decoded text.
        """
        return base64.b64decode(encoded_data).decode("utf-8")
