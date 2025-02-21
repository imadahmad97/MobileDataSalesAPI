import datetime
import csv
import base64
from typing import Union, Type
from fastapi import Request
from pydantic import BaseModel, field_validator
import logging


class MobileDataPurchaseRequest(BaseModel):

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
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%m/%d/%Y")
        return value

    @field_validator("credit_card_expiration_date", mode="before")
    @classmethod
    def parse_credit_card_expiration(
        cls, value: Union[str, datetime.datetime]
    ) -> datetime.datetime:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%m/%y")
        return value

    @classmethod
    async def build_request_from_binary_file(
        cls: Type["MobileDataPurchaseRequest"], request: Request
    ) -> "MobileDataPurchaseRequest":
        parsed_data: dict = await cls._decode_binary_file(await request.body())
        return cls(**parsed_data)

    @classmethod
    def build_request_list_from_binary_csv(
        cls: Type["MobileDataPurchaseRequest"], file_path: str
    ) -> list["MobileDataPurchaseRequest"]:
        decoded_data: list = cls._decode_binary_csv(file_path)
        return [cls(**row) for row in decoded_data]

    @staticmethod
    async def _decode_binary_file(contents: bytes) -> dict:
        base64_string = contents.decode("utf-8")
        text = base64.b64decode(base64_string).decode("utf-8")
        data = {}
        for line in text.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                data[key.lower().replace(" ", "_")] = value.strip()
        return data

    @staticmethod
    def _decode_binary_csv(file_path: str) -> list[dict]:
        """Decodes a Base64-encoded CSV file and returns a list of dictionaries."""
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            headers = [
                base64.b64decode(header).decode("utf-8") for header in next(csv_reader)
            ]
            data = [
                {
                    headers[i]: base64.b64decode(cell).decode("utf-8")
                    for i, cell in enumerate(row)
                }
                for row in csv_reader
            ]
        return data
