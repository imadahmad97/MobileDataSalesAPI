import datetime
import csv
from app.service.binary_parser import parse_binary_text_to_dict, parse_csv_to_dicts


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
        parsed_data = await parse_binary_text_to_dict(await request.body())
        return cls(**parsed_data)

    @classmethod
    def build_from_csv(cls, file_path):
        instances = []
        with open(file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                instances.append(cls(**row))
        return instances
