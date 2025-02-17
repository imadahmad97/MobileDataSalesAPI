import sqlite3


class DatabaseService:
    def __init__(self):
        # Allow the SQLite connection to be used across threads
        self.con = sqlite3.connect(
            "appdata/database/mobile_data_sales_api.db", check_same_thread=False
        )
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS 
            transactions (name TEXT, date_of_birth TEXT, credit_card_number TEXT,
            credit_card_expiration_date TEXT, credit_card_cvv TEXT, billing_account_number TEXT, 
            requested_mobile_data TEXT, status TEXT, validation_errors TEXT)"""
        )
        self.con.commit()

    def record_transaction(
        self,
        purchase_request,
        status,
        validation_errors,
    ):
        self.cur.execute(
            """INSERT INTO transactions (name, date_of_birth, credit_card_number, credit_card_expiration_date, 
            credit_card_cvv, billing_account_number, requested_mobile_data, status, validation_errors) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                purchase_request.name,
                purchase_request.date_of_birth,
                purchase_request.credit_card_number,
                purchase_request.credit_card_expiration_date,
                purchase_request.credit_card_cvv,
                purchase_request.billing_account_number,
                purchase_request.requested_mobile_data,
                status,
                validation_errors,
            ),
        )
        self.con.commit()

    def close(self):
        """Close database connection."""
        self.cur.close()
        self.con.close()

    @staticmethod
    def get_db_service():
        """Create a new DatabaseService instance for each request and ensure it is closed after use."""
        db_service = DatabaseService()
        try:
            yield db_service
        finally:
            db_service.close()
