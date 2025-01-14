"""Category API"""

from typing import Any
from ...database import categories, generate_id

class CategoryAPI:
    """CategoryAPI"""

    def _validate(self, data: dict[str, Any]):
        """Validate category data"""
        required_fields = ["name", "type"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["name"], str):
            raise TypeError("Name must be a string")

        if not isinstance(data["type"], str):
            raise TypeError("Type must be a string")

    def add_category(self, data: dict[str, Any]):
        """Add a category to the database"""
        self._validate(data)
        categories.insert(
            {
                "id": generate_id(),
                "name": data["name"],
                "type": data["type"],
            }
        )

    def edit_category(self, data: dict[str, Any]):
        """Edit a category in the database"""
        self._validate(data)
        categories.update(
            data["id"],
            {
                "name": data["name"],
                "type": data["type"],
            },
        )

    def delete_category(self, category_id: str):
        """Delete a category from the database"""
        categories.delete(category_id)

    def get_category(self, category_id: str):
        """Select a category"""
        return categories.select_one({"id": category_id})

    def get_categories(self, limit=0, sort_by='asc'):
        """Select all categories"""
        return categories.select(limit=limit, order=sort_by)
