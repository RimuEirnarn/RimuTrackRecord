"""Transactions"""
from time import time as now
from ..database import transaction, generate_id, categories
from .utils import generate_currency, fake

def get_ids():
    '''get ids'''
    base_cid: str = categories.select_one({'name': 'base'}).id
    return {
        'base_cid': base_cid
    }

def push(limit=10):
    """Push several transactions"""
    base_cid = get_ids()['base_cid']
    for _ in range(limit):
        transaction.insert({
            'id': generate_id(),
            'type': 'expense',
            'category_id': base_cid,
            "amount": generate_currency(),
            "time": now(),
            "notes": fake.sentence(9)
        })
