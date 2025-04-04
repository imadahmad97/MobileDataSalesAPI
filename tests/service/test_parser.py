from app.service.parser import parse_csv_content, parse_text_from_binary
from app.model.mobile_data_sell_order import MobileDataSellOrder


test_csv = b"John Doe,05/14/1990,406583246170089012345678,08/25,123,987654321,5GB\r\nDean Lawrence,11/7/1976,374245455400126,12/22,456,12349,1GB\r\nJane Doe,02/28/1985,374245455400126,08/25,123,988769,5GB\r\nJared Stevens,09/30/1982,374245455400126,12/25,456,432345,1GB\r\nRay Lopez,03/15/1995,406583246170089012345678,08/25,123,987654321,5GB\r\n"


def test_parse_text_from_binary_bare_csv():
    bare_csv_content = b"header1,header2\nvalue1,value2\n"
    bare_csv_expected_result = [["header1", "header2"], ["value1", "value2"]]
    bare_csv_actual_result = parse_text_from_binary(bare_csv_content)
    assert bare_csv_actual_result == bare_csv_expected_result


def test_parse_text_from_binary_csv_test_csv():
    test_csv_expected_result = [
        [
            "John Doe",
            "05/14/1990",
            "406583246170089012345678",
            "08/25",
            "123",
            "987654321",
            "5GB",
        ],
        [
            "Dean Lawrence",
            "11/7/1976",
            "374245455400126",
            "12/22",
            "456",
            "12349",
            "1GB",
        ],
        [
            "Jane Doe",
            "02/28/1985",
            "374245455400126",
            "08/25",
            "123",
            "988769",
            "5GB",
        ],
        [
            "Jared Stevens",
            "09/30/1982",
            "374245455400126",
            "12/25",
            "456",
            "432345",
            "1GB",
        ],
        [
            "Ray Lopez",
            "03/15/1995",
            "406583246170089012345678",
            "08/25",
            "123",
            "987654321",
            "5GB",
        ],
    ]

    test_csv_actual_result = parse_text_from_binary(test_csv)
    assert test_csv_actual_result == test_csv_expected_result


def test_parse_csv_content():
    test_csv_expected_result = [
        MobileDataSellOrder(
            name="John Doe",
            date_of_birth="05/14/1990",
            credit_card_number="406583246170089012345678",
            credit_card_expiration_date="08/25",
            credit_card_cvv="123",
            billing_account_number="987654321",
            requested_mobile_data="5GB",
            status="Approved",
            validation_errors=[],
        ),
        MobileDataSellOrder(
            name="Dean Lawrence",
            date_of_birth="11/7/1976",
            credit_card_number="374245455400126",
            credit_card_expiration_date="12/22",
            credit_card_cvv="456",
            billing_account_number="12349",
            requested_mobile_data="1GB",
            status="Approved",
            validation_errors=[],
        ),
        MobileDataSellOrder(
            name="Jane Doe",
            date_of_birth="02/28/1985",
            credit_card_number="374245455400126",
            credit_card_expiration_date="08/25",
            credit_card_cvv="123",
            billing_account_number="988769",
            requested_mobile_data="5GB",
            status="Approved",
            validation_errors=[],
        ),
        MobileDataSellOrder(
            name="Jared Stevens",
            date_of_birth="09/30/1982",
            credit_card_number="374245455400126",
            credit_card_expiration_date="12/25",
            credit_card_cvv="456",
            billing_account_number="432345",
            requested_mobile_data="1GB",
            status="Approved",
            validation_errors=[],
        ),
        MobileDataSellOrder(
            name="Ray Lopez",
            date_of_birth="03/15/1995",
            credit_card_number="406583246170089012345678",
            credit_card_expiration_date="08/25",
            credit_card_cvv="123",
            billing_account_number="987654321",
            requested_mobile_data="5GB",
            status="Approved",
            validation_errors=[],
        ),
    ]

    test_csv_actual_result = parse_csv_content(test_csv)
    assert test_csv_actual_result == test_csv_expected_result
