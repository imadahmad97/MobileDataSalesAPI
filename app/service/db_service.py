from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from app.model.mobile_data_purchase_transaction import MobileDataPurchaseTransaction
from sqlmodel import Session, SQLModel, create_engine


class DataBaseService:
    sqlite_file_name = "/appdata/database/mobile_data_sales_api.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    def __init__(self):
        self.engine = create_engine(
            self.__class__.sqlite_url, connect_args={"check_same_thread": False}
        )

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_db_session(self):
        with Session(self.engine) as session:
            yield session

    @staticmethod
    def record_transaction(
        purchase_request: MobileDataPurchaseRequest,
        status: str,
        validation_errors: str,
        session: Session,
    ) -> MobileDataPurchaseTransaction:
        transaction = (
            MobileDataPurchaseTransaction.build_transaction_from_request_and_response(
                purchase_request, status, validation_errors
            )
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
