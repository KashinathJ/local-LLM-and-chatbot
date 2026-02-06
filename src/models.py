"""
Pydantic v2 schema for Recipe Intelligence Chatbot.
Ensures structured JSON output from the LLM.
"""

from pydantic import BaseModel, Field


class Recipe(BaseModel):
    """Structured recipe output schema."""

    name: str = Field(description="Name of the dish or recipe")
    ingredients: list[str] = Field(
        description="List of ingredients with quantities (e.g., '2 eggs', '1 cup onions')"
    )
    steps: list[str] = Field(
        description="Numbered cooking steps in order"
    )
    prep_time_minutes: int = Field(
        ge=1,
        le=480,
        description="Total preparation and cooking time in minutes"
    )
    calories: int = Field(
        ge=0,
        le=5000,
        description="Estimated calories per serving"
    )
