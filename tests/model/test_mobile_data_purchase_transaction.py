from app.model.mobile_data_purchase_transaction import MobileDataPurchaseTransaction
from app.model.mobile_data_sell_order import MobileDataSellOrder
import datetime


def test_build_transaction_from_sell_order():
    sell_order = MobileDataSellOrder(
        name="John Doe",
        date_of_birth="01/01/1990",
        credit_card_number="1234567890123456",
        credit_card_expiration_date="12/25",
        credit_card_cvv="123",
        billing_account_number="9876543210",
        requested_mobile_data="5GB",
        status="Approved",
        validation_errors=[],
    )

    expected_transaction = MobileDataPurchaseTransaction(
        name="John Doe",
        date_of_birth=datetime.datetime(1990, 1, 1),
        credit_card_number="1234567890123456",
        credit_card_expiration_date=datetime.datetime(2025, 12, 1),
        credit_card_cvv="123",
        billing_account_number="9876543210",
        requested_mobile_data="5GB",
        status="Approved",
        validation_errors="",
    )

    transaction = MobileDataPurchaseTransaction.build_transaction_from_sell_order(
        sell_order
    )

    assert transaction == expected_transaction


def test_build_transaction_from_sell_order_missing_name():
    sell_order = MobileDataSellOrder(
        name="",
        date_of_birth="01/01/1990",
        credit_card_number="1234567890123456",
        credit_card_expiration_date="12/25",
        credit_card_cvv="123",
        billing_account_number="9876543210",
        requested_mobile_data="5GB",
        status="Approved",
        validation_errors=[],
    )

    expected_transaction = MobileDataPurchaseTransaction(
        name="",
        date_of_birth=datetime.datetime(1990, 1, 1),
        credit_card_number="1234567890123456",
        credit_card_expiration_date=datetime.datetime(2025, 12, 1),
        credit_card_cvv="123",
        billing_account_number="9876543210",
        requested_mobile_data="5GB",
        status="Approved",
        validation_errors="",
    )

    transaction = MobileDataPurchaseTransaction.build_transaction_from_sell_order(
        sell_order
    )
    assert transaction == expected_transaction
