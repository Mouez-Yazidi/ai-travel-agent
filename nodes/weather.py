"""
Node: fetch weather for the city and summarize it for travelers.
"""
from langchain_core.prompts import ChatPromptTemplate

from llm import llm
from state import State
from tools.weather import get_weather


def check_weather(state: State) -> dict:
    """Fetch live weather and produce a short traveler-oriented summary."""
    city = state["city"]
    weather_data = get_weather.invoke({"city": city})

    prompt = ChatPromptTemplate.from_messages([
        (
            "human",
            "Here is the weather data for {city}:\n\n{weather}\n\n"
            "Write a short weekend weather summary for travelers."
        ),
    ])
    messages = prompt.format_messages(city=city, weather=weather_data)
    response = llm.invoke(messages)
    summary = (response.content or "").strip()
    return {"weather": summary}
