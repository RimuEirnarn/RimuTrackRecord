"""Categories database seeder"""
from ..database import categories, generate_id
CATEGORIES = [
    "electronics",
    "accessories",
    "utilities",
    "groceries",
    "rent",
    "base"
]

def push_categories():
    """Push categories"""
    categories.insert_many([{'id': generate_id(), 'name': name} for name in CATEGORIES])
