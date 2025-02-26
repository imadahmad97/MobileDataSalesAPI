from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.model.mobile_data_purchase_transaction import MobileDataPurchaseTransaction
from sqlmodel import Session, SQLModel, create_engine
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DataBaseService:
    sqlite_file_name = BASE_DIR / "appdata" / "database" / "mobile_data_sales_api.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    def __init__(self):
        logger.info("Initializing the database service")
        self.engine = create_engine(
            self.__class__.sqlite_url, connect_args={"check_same_thread": False}
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
    def record_transaction(
        purchase_request: MobileDataPurchaseRequest,
        status: str,
        validation_errors: str,
        session: Session,
    ) -> MobileDataPurchaseTransaction:
        """
        This method records a transaction to the database. It is called by the
        process_mobile_data_purchase_request function after the request has been validated and
        processed.
        """
        transaction = (
            MobileDataPurchaseTransaction.build_transaction_from_request_and_response(
                purchase_request, status, validation_errors
            )
        )
        logger.info("Committing the transaction to the database")
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
