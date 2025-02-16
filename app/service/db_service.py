import sqlite3


class DatabaseService:
    def __init__(self):
        # Allow the SQLite connection to be used across threads
        self.con = sqlite3.connect(
            "appdata/mobile_data_sales_api.db", check_same_thread=False
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
        name,
        date_of_birth,
        credit_card_number,
        credit_card_expiration_date,
        credit_card_cvv,
        billing_account_number,
        requested_mobile_data,
        status,
        validation_errors,
    ):
        self.cur.execute(
            """INSERT INTO transactions (name, date_of_birth, credit_card_number, credit_card_expiration_date, 
            credit_card_cvv, billing_account_number, requested_mobile_data, status, validation_errors) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                name,
                date_of_birth,
                credit_card_number,
                credit_card_expiration_date,
                credit_card_cvv,
                billing_account_number,
                requested_mobile_data,
                status,
                validation_errors,
            ),
        )
        self.con.commit()

    def close(self):
        """Close database connection."""
        self.cur.close()
        self.con.close()

    def get_db_service():
        """Create a new DatabaseService instance for each request and ensure it is closed after use."""
        db_service = DatabaseService()
        try:
            yield db_service
        finally:
            db_service.close()
