from .category import push_categories
from .collections import push as push_collections, mtm_collections
from .transaction import push as push_transactions
from ..database import commit, init

def seeder():
    """Seeder"""
    init()
    push_categories()
    push_collections()
    push_transactions()
    mtm_collections()
    commit()
