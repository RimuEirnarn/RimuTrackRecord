"""Transaction"""

from typing import Any, Literal

from sqlite_database import Row
from sqlite_database.operators import le, ge
from ...database import transaction, generate_id, database


class TransactionAPI:
    """Transaction"""

    def _validate(self, data: dict[str, Any]):
        """Validate transaction data"""
        required_fields = ["type", "category_id", "amount", "date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["type"], str):
            raise TypeError("Type must be a string")

        if not isinstance(data["category_id"], str):
            raise TypeError("Category ID must be a string")

        if not isinstance(data["amount"], (int, float)):
            raise TypeError("Amount must be a number")

        if not isinstance(data['time'], float):
            raise TypeError("Time must be a float")

        if "notes" in data and not isinstance(data["notes"], str):
            raise TypeError("Notes must be a string")

    def add_transaction(self, data: dict[str, Any]):
        """Add a transaction to the database"""
        self._validate(data)
        transaction.insert(
            {
                "id": generate_id(),
                "type": data["type"],
                "category_id": data["category_id"],
                "amount": data["amount"],
                "time": data["time"],
                "notes": data.get("notes", "<no note>"),
            }
        )

    def edit_transaction(self, data: dict[str, Any]):
        """Edit a transaction in the database"""
        self._validate(data)
        transaction.update(
            data["id"],
            {
                "type": data["type"],
                "category_id": data["category_id"],
                "amount": data["amount"],
                "time": data["time"],
                "notes": data.get("notes", "<no note>"),
            },
        )

    def delete_transaction(self, transaction_id: str):
        """Delete a transaction from the database"""
        transaction.delete(transaction_id)

    def get_transaction(self, transaction_id: str):
        """Get a transaction from the database"""
        return transaction.select_one({"id": transaction_id})

    def get_transactions(self, limit=0):
        """Get all transactions from the database"""
        return transaction.select(limit=limit)

    def get_transactions_by_category(self, category_id: str, limit=0):
        """Get all transactions for a given category"""
        return transaction.select({"category_id": category_id}, limit=limit)

    def get_transactions_by_time(self, date: float, state: Literal["newer", "older"], limit=0):
        """Get all transactions for a given time"""
        return transaction.select(
            [le("time", date) if state == "older" else ge("time", date)],
            limit=limit
        )

    def get_transactions_by_type(self, tr_type: str, limit=0) -> list[Row]:
        """Get all transactions for a given type"""
        return transaction.select({"type": tr_type}, limit=limit)

    def get_transactions_by_amount(self, amount: float, state: Literal["greater", "less"], limit):
        """Get all transactions for a given amount"""
        return transaction.select(
            [ge("amount", amount) if state == "greater" else le("amount", amount)],
            limit=limit
        )

    def get_ungrouped_transactions(self) -> list[Row]:
        """Get all ungrouped transactions"""
        query = '''
                SELECT t.*
                FROM transaction_tbl t
                LEFT JOIN collection_transaction ct ON t.id = ct.transaction_id
                WHERE ct.transaction_id IS NULL
            '''
        return database.sql.execute(query).fetchall()
