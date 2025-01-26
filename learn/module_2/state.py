from pydantic import BaseModel, field_validator, ValidationError
from typing import Literal, TypedDict


class State(BaseModel):
    name: str
    mood: Literal["happy", "sad", "neutral"]
    graph_state: str = ""  # Add default empty string

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, value):
        if value not in ["happy", "sad", "neutral"]:
            raise ValidationError(
                "Mood cannot be anything other than happy, sad, or neutral"
            )
        return value


try:
    state = State(name="John", mood="sad")
except ValidationError as e:
    print("Validation error occurred", e)


class OverallState(TypedDict):
    question: str
    answer: str
    notes: str
