"""Database"""

from uuid import uuid4
from sqlite3 import OperationalError
from sqlite_database import Database, real, text
from sqlite_database.errors import DatabaseExistsError
from .config import DB_PATH

database = Database(DB_PATH)

CONFIG_SCHEMA = [text("name").unique(), text("value")]
SYSTEM_CONFIG = [text('name').unique(), text('value')]

TRANSACTION_SCHEMA = [
    text("id").primary(),
    text("type"),
    text("category_id").foreign("category/id"),
    real("amount"),
    real('time'),
    text("notes").default("<no note>"),
]

CATEGORIES_SCHEMA = [text("id").primary(), text("name")]

BUDGET_SCHEMA = [
    text("id").primary(),
    text("category_id").foreign("category/id"),
    real("amount"),
]

COLLECTION_SCHEMA = [
    text("id").primary(),
    text("name"),
    real("time"),
    text("notes").default("<no note>"),
]

COLLECTION_TRANSACTION_SCHEMA = [
    text("id").primary(),
    text("collection_id").foreign("collection/id").on_delete('cascade'),
    text("transaction_id").foreign("transaction/id").on_delete('cascade'),
]

def generate_id():
    """Generate a new ID"""
    return str(uuid4())


def init():
    """Initialize database"""
    # print('this')
    try:
        if database.table("config").select_one():
            return (
                database.table("config"),
                database.table("transaction_tbl"),
                database.table("categories"),
                database.table("budget"),
                database.table("collection"),
                database.table("collection_transaction"),
                database.table('system_config')
            )
    except OperationalError:
        pass

    try:
        # print('that')
        _config = database.create_table("config", CONFIG_SCHEMA)
        _transaction = database.create_table("transaction_tbl", TRANSACTION_SCHEMA)
        _categories = database.create_table("categories", CATEGORIES_SCHEMA)
        _budget = database.create_table("budget", BUDGET_SCHEMA)
        _collection = (database.create_table("collection", COLLECTION_SCHEMA),)
        _collection_transaction = database.create_table(
            "collection_transaction", COLLECTION_TRANSACTION_SCHEMA
        )
        _system = database.create_table("system_config", SYSTEM_CONFIG)
        database.commit()
        return (
            _config,
            _transaction,
            _categories,
            _budget,
            _collection,
            _collection_transaction,
            _system
        )
    except DatabaseExistsError:
        # print('these', exc)
        return (
            database.table("config"),
            database.table("transaction_tbl"),
            database.table("categories"),
            database.table("budget"),
            database.table("collection"),
            database.table("collection_transaction"),
            database.table('system_config')
        )


# pylint: disable-next=unbalanced-tuple-unpacking
config, transaction, categories, budget, collection, collection_transaction, system_tbl = init()
