"""Transactions"""
from time import time as now
from ..database import transaction, generate_id, categories
from .utils import generate_currency, fake

BASE_CID: str = categories.select_one({'name': 'base'}).id

def push(limit=10):
    """Push several transactions"""
    for _ in range(limit):
        transaction.insert({
            'id': generate_id(),
            'type': 'expense',
            'category_id': BASE_CID,
            "amount": generate_currency(),
            "time": now(),
            "notes": fake.sentence(9)
        })
