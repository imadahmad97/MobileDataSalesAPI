from app.model.mobile_data_sell_order import MobileDataSellOrder
from app.model.mobile_data_purchase_transaction import MobileDataPurchaseTransaction
from app.service.db_service import DataBaseService
from sqlalchemy import inspect
from unittest.mock import MagicMock


def test_create_db_and_tables(db_service):
    inspector = inspect(db_service.engine)
    table_names = inspector.get_table_names()
    assert "mobiledatapurchasetransaction" in table_names


def test_close_db_connection():
    db_service = DataBaseService("sqlite:///:memory:")
    db_service.engine.dispose = MagicMock()
    db_service.close_db_connection()
    db_service.engine.dispose.assert_called_once()


def test_get_db_session(db_service):
    session_gen = db_service.get_db_session()
    session = next(session_gen)
    assert session is not None
    assert session.bind == db_service.engine


def test_record_transactions(db_service):
    sample_orders = [
        MobileDataSellOrder(
            name="John Doe",
            date_of_birth="01/01/1990",
            credit_card_number="1234567890123456",
            credit_card_expiration_date="12/25",
            credit_card_cvv="123",
            billing_account_number="9876543210",
            requested_mobile_data="10GB",
            status="approved",
            validation_errors=[],
        ),
        MobileDataSellOrder(
            name="Jane Doe",
            date_of_birth="02/02/1992",
            credit_card_number="6543210987654321",
            credit_card_expiration_date="11/24",
            credit_card_cvv="456",
            billing_account_number="0123456789",
            requested_mobile_data="20GB",
            status="approved",
            validation_errors=["Invalid credit card number"],
        ),
    ]

    session = next(db_service.get_db_session())
    DataBaseService.record_transactions(sample_orders, session)

    result = session.query(MobileDataPurchaseTransaction).all()
    assert len(result) == len(sample_orders)
    assert result[0].name == sample_orders[0].name
    assert result[1].name == sample_orders[1].name
    assert result[0].billing_account_number == sample_orders[0].billing_account_number
    assert result[1].billing_account_number == sample_orders[1].billing_account_number
    assert result[0].requested_mobile_data == sample_orders[0].requested_mobile_data
    assert result[1].requested_mobile_data == sample_orders[1].requested_mobile_data
    assert result[0].status == sample_orders[0].status
    assert result[1].status == sample_orders[1].status
    assert result[0].validation_errors == ""
    assert result[1].validation_errors == "Invalid credit card number"
    assert result[0].credit_card_number == sample_orders[0].credit_card_number
