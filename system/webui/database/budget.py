"""Budget planning API"""
from typing import Any
from ...database import budget, categories, generate_id

class BudgetAPI:
    """BudgetAPI"""

    def _validate(self, data: dict[str, Any]):
        """Validate budget data"""
        required_fields = ["category_id", "amount"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["category_id"], str):
            raise TypeError("Category ID must be a string")

        if not isinstance(data["amount"], (int, float)):
            raise TypeError("Amount must be a number")

        if categories.select_one({'id': data["category_id"]}) is None:
            raise ValueError("Category ID does not exist")

    def add_budget(self, data: dict[str, Any]):
        """Add a budget to the database"""
        self._validate(data)
        budget.insert(
            {
                "id": generate_id(),
                "category_id": data["category_id"],
                "amount": data["amount"],
            }
        )

    def edit_budget(self, data: dict[str, Any]):
        """Edit a budget in the database"""
        self._validate(data)
        budget.update(
            data["id"],
            {
                "category_id": data["category_id"],
                "amount": data["amount"],
            },
        )

    def delete_budget(self, budget_id: str):
        """Delete a budget from the database"""
        budget.delete(budget_id)

    def get_budget(self, budget_id: str):
        """Select a budget"""
        return budget.select_one({"id": budget_id})

    def get_budgets(self):
        """Select all budgets"""
        return budget.select()
