import datetime
import csv
import base64


class MobileDataPurchaseRequest:
    def __init__(
        self,
        name: str,
        date_of_birth: str,
        credit_card_number: str,
        credit_card_expiration_date: str,
        credit_card_cvv: str,
        billing_account_number: str,
        requested_mobile_data: str,
    ):
        self.name = name
        self.date_of_birth = date_of_birth
        self.credit_card_number = credit_card_number
        self.credit_card_expiration_date = credit_card_expiration_date
        self.credit_card_cvv = credit_card_cvv
        self.billing_account_number = billing_account_number
        self.requested_mobile_data = requested_mobile_data

        self._convert_dates_to_datetime()

    def _convert_dates_to_datetime(self):
        self.date_of_birth = datetime.datetime.strptime(self.date_of_birth, "%m/%d/%Y")
        self.credit_card_expiration_date = datetime.datetime.strptime(
            self.credit_card_expiration_date, "%m/%y"
        )

    @classmethod
    async def build_from_binary_file(cls, request):
        parsed_data = await cls._decode_binary_file(await request.body())
        return cls(**parsed_data)

    @classmethod
    def build_from_binary_csv(cls, file_path):
        decoded_data = cls._decode_binary_csv(file_path)
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
