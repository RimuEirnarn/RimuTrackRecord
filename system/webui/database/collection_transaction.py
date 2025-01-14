from typing import Any
from ...database import collection_transaction, generate_id, transaction, collection

class CollectionTransactionAPI:
    """CollectionTransactionAPI class."""

    def _validate(self, data: dict[str, Any]):
        """Validate collection transaction data."""
        required_fields = ["collection_id", "transaction_id"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["collection_id"], str):
            raise TypeError("Collection ID must be a string")

        if not isinstance(data["transaction_id"], str):
            raise TypeError("Transaction ID must be a string")

        if transaction.select_one({'id': data["transaction_id"]}) is None:
            raise ValueError("Transaction ID does not exist")

        if collection.select_one({'id': data["collection_id"]}) is None:
            raise ValueError("Collection ID does not exist")

    def add_collection_transaction(self, data: dict[str, Any]):
        """Add a collection transaction to the database."""
        self._validate(data)
        collection_transaction.insert(
            {
                "id": generate_id(),
                "collection_id": data["collection_id"],
                "transaction_id": data["transaction_id"],
            }
        )

    def edit_collection_transaction(self, data: dict[str, Any]):
        """Edit a collection transaction in the database."""
        self._validate(data)
        collection_transaction.update(
            data["id"],
            {
                "collection_id": data["collection_id"],
                "transaction_id": data["transaction_id"],
            },
        )

    def delete_collection_transaction(self, ct_id: str):
        """Delete a collection transaction from the database."""
        collection_transaction.delete(ct_id)

    def get_collection_transaction(self, ct_id: str):
        """Select a collection transaction."""
        return collection_transaction.select_one({"id": ct_id})

    def get_collection_transactions(self, limit=0, sort_by='asc'):
        """Select all collection transactions."""
        return collection_transaction.select(limit=limit, order=sort_by)

    def get_collection_by_transaction(self, transaction_id: str):
        """Select all collections by transaction."""
        return collection_transaction.select({"transaction_id": transaction_id})

    def get_transactions_by_collection(self, collection_id: str):
        """Select all transactions by collection."""
        return collection_transaction.select({"collection_id": collection_id})
