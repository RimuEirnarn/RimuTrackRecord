"""Collection"""

from typing import Any
from ...database import collection, generate_id

class CollectionAPI:
    """CollectionAPI"""

    def _validate(self, data: dict[str, Any]):
        """Validate collection data"""
        required_fields = ["name", "notes", "time"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["name"], str):
            raise TypeError("Name must be a string")

        if not isinstance(data["time"], float):
            raise TypeError("Time must be a float")

        if "notes" in data and not isinstance(data["notes"], str):
            raise TypeError("Notes must be a string")

    def add_collection(self, data: dict[str, Any]):
        """Add a collection to the database"""
        self._validate(data)
        collection.insert(
            {
                "id": generate_id(),
                "name": data["name"],
                "time": data["time"],
                "notes": data.get("notes", "<no note>"),
            }
        )

    def edit_collection(self, data: dict[str, Any]):
        """Edit a collection in the database"""
        self._validate(data)
        collection.update(
            data["id"],
            {
                "name": data["name"],
                "time": data["time"],
                "notes": data.get("notes", "<no note>"),
            },
        )

    def delete_collection(self, collection_id: str):
        """Delete a collection from the database"""
        collection.delete(collection_id)

    def get_collection(self, collection_id: str):
        """Get a collection from the database"""
        return collection.select_one({"id": collection_id})

    def get_collections(self, limit=0, sort_by='asc'):
        """Get all collections from the database"""
        return collection.select(limit=limit, order=sort_by)

    def get_collections_by_date(self, date: float):
        """Get all collections from the database by date"""
        return collection.select({"time": date})
