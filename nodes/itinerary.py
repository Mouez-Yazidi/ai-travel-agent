"""
Node: create a 1-day itinerary from attractions and weather summary.
"""
from langchain_core.prompts import ChatPromptTemplate

from llm import llm
from state import State


def create_itinerary(state: State) -> dict:
    """Generate a short 1-day itinerary based on attractions and weather."""
    prompt = ChatPromptTemplate.from_messages([
        (
            "human",
            "Create a 1-day itinerary for visiting {city} based on these attractions: "
            "{attractions} and the following weather: {weather}. "
            "Summarize it in 3-4 sentences."
        ),
    ])
    attractions_str = ", ".join(state.get("attractions") or [])
    messages = prompt.format_messages(
        city=state["city"],
        attractions=attractions_str,
        weather=state.get("weather", ""),
    )
    response = llm.invoke(messages)
    itinerary = (response.content or "").strip()
    return {"itinerary": itinerary}
