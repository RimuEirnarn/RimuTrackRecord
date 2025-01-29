"""Database"""

from sys import exit as sys_exit
from traceback import format_exception
from uuid import uuid4
from sqlite3 import OperationalError
from sqlite_database import Database, Table, integer, real, text
from sqlite_database.errors import DatabaseExistsError
import system.log
from .config import DB_PATH

database = Database(DB_PATH)
_tables_d: dict[str, Table] = {}
_initialized = False # pylint: disable=invalid-name

CONFIG_SCHEMA = [text("name").unique(), text("value")]
SYSTEM_CONFIG = [text("name").unique(), text("value")]

def commit():
    """Commit whatever in database"""
    database.commit()

TRANSACTION_SCHEMA = [
    text("id").primary(),
    text("type"),
    text("category_id").foreign("category/id"),
    real("amount"),
    real("time"),
    text("notes").default("<no note>"),
]

CATEGORIES_SCHEMA = [text("id").primary(), text("name")]

BUDGET_SCHEMA = [
    text("id").primary(),
    text('name'),
    text("category_id").foreign("category/id").on_delete("null"),
    real("amount"),
    real("start_time"),
    real("end_time"),
    integer("recurrable").default(0),
    text('collection_id').foreign("collection/id").on_delete("cascade"),
]

COLLECTION_SCHEMA = [
    text("id").primary(),
    text("name"),
    real("time"),
    text("notes").default("<no note>"),
]

COLLECTION_TRANSACTION_SCHEMA = [
    text("id").primary(),
    text("collection_id").foreign("collection/id").on_delete("cascade"),
    text("transaction_id").foreign("transaction_tbl/id").on_delete("cascade"),
]


def generate_id():
    """Generate a new ID"""
    return str(uuid4())


def reset(use_config=False):
    """Reset specific tables"""
    tables_d = [
        "transaction_tbl",
        "category",
        "budget",
        "collection",
        "collection_transaction",
    ]
    schemas = [
        TRANSACTION_SCHEMA,
        CATEGORIES_SCHEMA,
        BUDGET_SCHEMA,
        COLLECTION_SCHEMA,
        COLLECTION_TRANSACTION_SCHEMA,
    ]
    if use_config:
        tables_d.extend(("config", "system_config"))
        schemas.extend(CONFIG_SCHEMA, SYSTEM_CONFIG)
    for table, schema in zip(tables_d, schemas, strict=True):
        database.reset_table(table, schema)


def init():
    """Initialize database"""
    global _initialized, _tables_d # pylint: disable=global-statement
    tables_d = [
        "transaction_tbl",
        "category",
        "budget",
        "collection",
        "collection_transaction",
        "config",
        "system_config",
    ]
    schemas = [
        TRANSACTION_SCHEMA,
        CATEGORIES_SCHEMA,
        BUDGET_SCHEMA,
        COLLECTION_SCHEMA,
        COLLECTION_TRANSACTION_SCHEMA,
        CONFIG_SCHEMA,
        SYSTEM_CONFIG,
    ]
    try:
        if database.table("config").select_one() and not _initialized:
            _tables_d = {tbl: database.table(tbl) for tbl in tables_d}
            _initialized = True
            return _tables_d
    except OperationalError:
        pass

    try:
        for table, schema in zip(tables_d, schemas):
            _tables_d[table] = database.create_table(table, schema)
            system.log.info("Table %s created", table)
        database.commit()
        system.log.info("Comitted")
        return _tables_d
    except DatabaseExistsError as exc:
        system.log.debug("Database exists? %s", str(exc))
        system.log.debug("\n".join(exc.__notes__)) # pylint: disable=no-member
    except OperationalError as exc:
        system.log.critical("Unable to continue creating database")
        system.log.critical("\n %s", "".join(format_exception(exc)))
        sys_exit(1)

    if _initialized:
        return _tables_d

    _tables = _tables_d = {tbl: database.table(tbl) for tbl in tables_d}
    _initialized = True
    return _tables


# Initialize tables at import time for convenience
tables = init()

# Export individual tables for easy imports
transaction = tables["transaction_tbl"]
categories = tables["category"]
budget = tables["budget"]
collection = tables["collection"]
collection_transaction = tables["collection_transaction"]
config = tables["config"]
system_config = tables["system_config"]
