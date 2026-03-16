"""
Node: suggest must-see attractions for a city using the LLM.
"""
from langchain_core.prompts import ChatPromptTemplate

from llm import llm
from state import State


def suggest_attractions(state: State) -> dict:
    """Generate a list of 5 must-see attractions for the given city."""
    prompt = ChatPromptTemplate.from_messages([
        ("human", "List 5 must-see attractions in {city}. Reply with one attraction per line, no numbering or extra text.")
    ])
    messages = prompt.format_messages(city=state["city"])
    response = llm.invoke(messages)
    text = (response.content or "").strip()
    attractions = [line.strip() for line in text.split("\n") if line.strip()]

    return {"attractions": attractions}
