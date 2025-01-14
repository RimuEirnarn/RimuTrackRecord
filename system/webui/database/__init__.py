"""Database"""

from .budget import BudgetAPI
from .category import CategoryAPI
from .transaction import TransactionAPI
from .collection_transaction import CollectionTransactionAPI
from .collection import CollectionAPI


class DatabaseAPI:
    """DatabaseAPI"""

    budget = BudgetAPI()
    category = CategoryAPI()
    transaction = TransactionAPI()
    collection_transaction = CollectionTransactionAPI()
    collection = CollectionAPI()
