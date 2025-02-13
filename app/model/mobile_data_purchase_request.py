import datetime


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
    async def from_binary_data(cls, request):
        contents = await request.body()
        decoded_text = contents.decode("utf-8")

        parsed_data = cls._parse_text(decoded_text)

        return cls(**parsed_data)

    @staticmethod
    def _parse_text(text: str):
        data = {}
        for line in text.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                formatted_key = key.lower().replace(" ", "_")
                data[formatted_key] = value.strip()
        return data
