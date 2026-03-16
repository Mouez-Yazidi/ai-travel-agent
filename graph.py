"""
LangGraph workflow: attractions -> weather -> itinerary.
"""
from langgraph.graph import END, StateGraph

from nodes import check_weather, create_itinerary, suggest_attractions
from state import State

workflow = StateGraph(State)

workflow.add_node("attractions_node", suggest_attractions)
workflow.add_node("weather_node", check_weather)
workflow.add_node("itinerary_node", create_itinerary)

workflow.set_entry_point("attractions_node")
workflow.add_edge("attractions_node", "weather_node")
workflow.add_edge("weather_node", "itinerary_node")
workflow.add_edge("itinerary_node", END)

app = workflow.compile()
