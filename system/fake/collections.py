"""Collections"""

import time
from ..database import (
    transaction,
    generate_id,
    categories,
    collection,
    collection_transaction,
)

def get_ids():
    """Get ids"""
    base_cid: str = categories.select_one({"name": "base"}).id
    electronics_cid: str = categories.select_one({"name": "electronics"}).id
    first_ten = transaction.select(limit=10)
    return {
        'base_cid': base_cid,
        'electronics_cid': electronics_cid,
        'first_ten': first_ten
    }


def push():
    """Push several collections"""
    cl_name = ["Computer Setup", "Groceries Essentials"]
    collection.insert_many([{"id": generate_id(), "name": name, 'time': time.time(), 'notes': 'a'} for name in cl_name])


def mtm_collections():
    """Many-to-many collections-transactions"""
    base: str = collection.select_one({"name": "Computer Setup"}).id
    electronics_cid = get_ids()['electronics_cid']
    ids = [generate_id() for _ in range(4)]
    transaction.insert_many(
        [
            {
                "id": ids[0],
                "type": "expense",
                "category_id": electronics_cid,
                "amount": 16_000_000,
                "time": time.time(),
                "notes": "RAM 8GB 4x",
            },
            {
                "id": ids[1],
                "type": "expense",
                "category_id": electronics_cid,
                "amount": 5_500_000,
                "time": time.time(),
                "notes": "Monitor",
            },
            {
                "id": ids[2],
                "type": "expense",
                "category_id": electronics_cid,
                "amount": 23_000_000,
                "time": time.time(),
                "notes": "SSD 2.5TB",
            },
            {
                "id": ids[3],
                "type": "expense",
                "category_id": electronics_cid,
                "amount": 12_000_000,
                "time": time.time(),
                "notes": "HDD 16TB",
            },
        ]
    )

    collection_transaction.insert_many(
        [{"id": generate_id(), "collection_id": base, "transaction_id": id_} for id_ in ids]
    )
