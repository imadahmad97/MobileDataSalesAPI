import datetime
import csv
import base64
from typing import Union, Type
from fastapi import Request


class MobileDataPurchaseRequest:
    def __init__(
        self,
        name: str,
        date_of_birth: Union[str, datetime.datetime],
        credit_card_number: str,
        credit_card_expiration_date: Union[str, datetime.datetime],
        credit_card_cvv: str,
        billing_account_number: str,
        requested_mobile_data: str,
    ):
        self.name: str = name
        self.date_of_birth: Union[str, datetime.datetime] = date_of_birth
        self.credit_card_number: str = credit_card_number
        self.credit_card_expiration_date: Union[str, datetime.datetime] = (
            credit_card_expiration_date
        )
        self.credit_card_cvv: str = credit_card_cvv
        self.billing_account_number: str = billing_account_number
        self.requested_mobile_data: str = requested_mobile_data

        self._convert_dates_to_datetime()

    def _convert_dates_to_datetime(self: "MobileDataPurchaseRequest") -> None:
        self.date_of_birth: datetime.datetime = datetime.datetime.strptime(self.date_of_birth, "%m/%d/%Y")  # type: ignore
        self.credit_card_expiration_date: (  # type: ignore
            datetime.datetime
        ) = datetime.datetime.strptime(
            self.credit_card_expiration_date, "%m/%y"  # type: ignore
        )

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
