"""
Shared state schema for the travel agent workflow.
"""
from typing import List, TypedDict


class State(TypedDict, total=False):
    """State passed between workflow nodes."""

    city: str
    attractions: List[str]
    weather: str
    itinerary: str
