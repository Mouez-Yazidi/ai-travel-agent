import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Add it to .env or your environment.")

# Initialize the ChatGroq instance
llm = ChatGroq(model="qwen/qwen3-32b", api_key=api_key, temperature=0.0)

# Test the setup
response = llm.invoke("Provide a short weather summary for Tunis this weekend.")
print(response.content)