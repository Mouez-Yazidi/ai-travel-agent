"""
LLM client (Groq) for the travel agent.
"""
from langchain_groq import ChatGroq

from config import require_groq_key

llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=require_groq_key(),
    temperature=0,
)
