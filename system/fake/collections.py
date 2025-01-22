"""Collections"""

import time
from ..database import (
    transaction,
    generate_id,
    categories,
    collection,
    collection_transaction,
)

BASE_CID: str = categories.select_one({"name": "base"}).id
ELECTRONICS_CID: str = categories.select_one({"name": "electronics"}).id
FIRST_TEN = transaction.select(limit=10)


def push():
    """Push several collections"""
    cl_name = ["Computer Setup", "Groceries Essentials"]
    collection.insert_many([{"id": generate_id(), "name": name} for name in cl_name])


def mtm_collections():
    """Many-to-many collections-transactions"""
    base: str = collection.select_one({"name": "Computer Setup"}).id
    ids = [generate_id() for _ in range(4)]
    transaction.insert_many(
        [
            {
                "id": ids[0],
                "type": "expense",
                "category_id": ELECTRONICS_CID,
                "amount": 16_000_000,
                "time": time.time(),
                "notes": "RAM 8GB 4x",
            },
            {
                "id": ids[1],
                "type": "expense",
                "category_id": ELECTRONICS_CID,
                "amount": 5_500_000,
                "time": time.time(),
                "notes": "Monitor",
            },
            {
                "id": ids[2],
                "type": "expense",
                "category_id": ELECTRONICS_CID,
                "amount": 23_000_000,
                "time": time.time(),
                "notes": "SSD 2.5TB",
            },
            {
                "id": ids[3],
                "type": "expense",
                "category_id": ELECTRONICS_CID,
                "amount": 12_000_000,
                "time": time.time(),
                "notes": "HDD 16TB",
            },
        ]
    )

    collection_transaction.insert_many(
        [{"id": generate_id(), "collection_id": base, "transaction_id": ids[0]}]
    )
