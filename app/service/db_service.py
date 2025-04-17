"""
This module contains the database service class. The class is responsible for creating the database
and tables, closing the database connection, and providing a database session for interacting with
the database.
"""

from app.model.mobile_data_sell_order import MobileDataSellOrder
from app.model.mobile_data_purchase_transaction import MobileDataPurchaseTransaction
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm.session import Session
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DataBaseService:

    def __init__(self, path_to_db_file: str):
        logger.info("Connecting to the database")
        self.engine = create_engine(
            path_to_db_file, connect_args={"check_same_thread": False}
        )

    def create_db_and_tables(self):
        """
        This method creates the database and tables if they do not exist. It is called when the
        FastAPI application is started.
        """
        logger.info("Creating the database and tables")
        SQLModel.metadata.create_all(self.engine)

    def close_db_connection(self):
        """
        This method closes the database connection. It is called when the FastAPI application is
        stopped.
        """
        logger.info("Closing the database connection")
        self.engine.dispose()

    def get_db_session(self):
        """
        This method returns a database session. The session is used to interact with the database.
        """
        with Session(self.engine) as session:
            yield session

    @staticmethod
    def record_transactions(
        sell_orders: list[MobileDataSellOrder],
        session: Session,
    ) -> None:
        """
        This method records multiple transactions to the database. It is called by the
        process_mobile_data_purchase_request function after the request has been validated and
        processed.

        Args:
            sell_orders (list[MobileDataSellOrder]): A list of MobileDataSellOrder objects to be
                recorded in the database.
            session (Session): The database session to be used for the transaction.
        """

        for sell_order in sell_orders:
            transaction = MobileDataPurchaseTransaction(
                name=sell_order.name,
                date_of_birth=sell_order.date_of_birth,
                credit_card_number=sell_order.credit_card_number,
                credit_card_expiration_date=sell_order.credit_card_expiration_date,
                credit_card_cvv=sell_order.credit_card_cvv,
                billing_account_number=sell_order.billing_account_number,
                requested_mobile_data=sell_order.requested_mobile_data,
                status=sell_order.status,
                validation_errors=", ".join(sell_order.validation_errors),
            )
            logger.info(
                f"Committing the transaction for BAN {sell_order.billing_account_number} to the database"
            )
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
