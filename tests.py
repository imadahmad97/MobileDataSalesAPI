import unittest
from app.interface import validation_interface
import datetime


class TestValidationInterface(unittest.TestCase):
    def test_is_customer_of_legal_age(self):
        self.assertEqual(
            validation_interface.is_customer_of_legal_age(
                datetime.datetime(1990, 10, 1), 18
            ),
            "",
        )
        self.assertEqual(
            validation_interface.is_customer_of_legal_age(
                datetime.datetime(2010, 1, 1), 18
            ),
            "Customer is not of legal age. ",
        )

    def test_is_credit_card_number_length_valid(self):
        self.assertEqual(
            validation_interface.is_credit_card_number_length_valid(
                "1234567890123456", 16, 16
            ),
            "",
        )
        self.assertEqual(
            validation_interface.is_credit_card_number_length_valid(
                "1234567890123456", 15, 15
            ),
            "Credit card number is invalid. ",
        )

    def test_is_credit_card_number_valid(self):
        self.assertEqual(
            validation_interface.is_credit_card_number_valid("4111111111111111"),
            "",
        )
        self.assertEqual(
            validation_interface.is_credit_card_number_valid("4111111111111112"),
            "Credit card number is invalid. ",
        )

    def test_is_cvv_valid(self):
        self.assertEqual(
            validation_interface.is_cvv_valid("123", 3, 3),
            "",
        )
        self.assertEqual(
            validation_interface.is_cvv_valid("123", 4, 4),
            "CVV is invalid. ",
        )

    def test_is_credit_card_expired(self):
        self.assertEqual(
            validation_interface.is_credit_card_expired(datetime.datetime(2026, 1, 1)),
            "",
        )
        self.assertEqual(
            validation_interface.is_credit_card_expired(datetime.datetime(2020, 1, 1)),
            "Credit card is expired. ",
        )

    def test_validate_purchase_request(self):
        self.assertEqual(
            validation_interface.validate_purchase_request(
                datetime.datetime(1990, 10, 1),
                "4111111111111111",
                datetime.datetime(2026, 1, 1),
                "123",
            ),
            "",
        )
        self.assertEqual(
            validation_interface.validate_purchase_request(
                datetime.datetime(2010, 1, 1),
                "4111111111111111",
                datetime.datetime(2020, 1, 1),
                "123",
            ),
            "Customer is not of legal age. Credit card is expired. ",
        )

        self.assertEqual(
            validation_interface.validate_purchase_request(
                datetime.datetime(1990, 10, 1),
                "4111111111111112",
                datetime.datetime(2026, 1, 1),
                "123",
            ),
            "Credit card number is invalid. ",
        )

        self.assertEqual(
            validation_interface.validate_purchase_request(
                datetime.datetime(1990, 10, 1),
                "4111111111111111",
                datetime.datetime(2026, 1, 1),
                "123456",
            ),
            "CVV is invalid. ",
        )

        self.assertEqual(
            validation_interface.validate_purchase_request(
                datetime.datetime(1990, 10, 1),
                "4111111111111111",
                datetime.datetime(2020, 1, 1),
                "123",
            ),
            "Credit card is expired. ",
        )

        self.assertEqual(
            validation_interface.validate_purchase_request(
                datetime.datetime(2010, 1, 1),
                "4111111111111112",
                datetime.datetime(2020, 1, 1),
                "123456",
            ),
            "Customer is not of legal age. Credit card number is invalid. CVV is invalid. Credit card is expired. ",
        )


if __name__ == "__main__":
    unittest.main()
