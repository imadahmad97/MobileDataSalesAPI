"""
This module contains the DatabaseService class, which provides a service for interacting with the
SQLite database.

Dependencies:
    - sqlite3
    - app.model.mobile_data_purchase_request.MobileDataPurchaseRequest
    - typing.Generator
    
Methods:
    - __init__
    - record_transaction
    - close
    - get_db_service
"""

import sqlite3
from typing import Generator
from app.model.mobile_data_purchase_request import MobileDataPurchaseRequest
from fastapi import HTTPException
import logging


class DatabaseService:
    """
    This class provides a service for interacting with the SQLite database."""

    def __init__(self) -> None:
        """
        This method initializes the DatabaseService class by creating a connection to the SQLite
        database and creating a table to store transactions if it does not already exist.
        """
        try:
            self.con: sqlite3.Connection = sqlite3.connect(
                "appdata/database/mobile_data_sales_api.db", check_same_thread=False
            )
            self.cur: sqlite3.Cursor = self.con.cursor()
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS 
                transactions (name TEXT, date_of_birth TEXT, credit_card_number TEXT,
                credit_card_expiration_date TEXT, credit_card_cvv TEXT, billing_account_number TEXT, 
                requested_mobile_data TEXT, status TEXT, validation_errors TEXT)"""
            )
            self.con.commit()
        except Exception:
            logging.error("Failed to connect to the database")
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error: Failed to connect to the database",
            )

    def record_transaction(
        self: "DatabaseService",
        purchase_request: "MobileDataPurchaseRequest",
        status: str,
        validation_errors: str,
    ) -> None:
        """
        This method records a transaction in the database with the provided purchase request, status
        and validation errors.
        """
        try:
            self.cur.execute(
                """INSERT INTO transactions (name, date_of_birth, credit_card_number, 
                credit_card_expiration_date, credit_card_cvv, billing_account_number, 
                requested_mobile_data, status, validation_errors) 
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

        except Exception:
            logging.error("Failed to record the transaction")
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error: Failed to record the transaction",
            )

    def close(self: "DatabaseService") -> None:
        """
        This method closes the connection to the SQLite database.
        """
        try:
            self.cur.close()
            self.con.close()
        except Exception:
            logging.error("Failed to close the database connection")
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error: Failed to close the database connection",
            )

    @staticmethod
    def get_db_service() -> Generator["DatabaseService", None, None]:
        """
        This method is a generator function that yields a DatabaseService object and closes the
        connection to the SQLite database when the generator is finished.
        """
        db_service: DatabaseService = DatabaseService()
        try:
            yield db_service
        finally:
            db_service.close()
