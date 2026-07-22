"""
models.py
---------
Single place where the LLM is configured.
If you ever want to switch model / provider, this is the only file you touch.

Currently using Groq (https://console.groq.com) because it has a genuinely
free tier — no credit card required — and runs open models like Llama 3.3
very fast.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load variables from .env into the environment
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.3"))

if not API_KEY or API_KEY == "your_api_key_here":
    raise ValueError(
        "GROQ_API_KEY is missing. Open the .env file and paste your real API key "
        "(get a free one at https://console.groq.com/keys)."
    )


def get_llm() -> ChatGroq:
    """
    Returns a ready-to-use LangChain chat model.
    Used by both the Planner and Executor agents so behavior stays consistent.
    """
    return ChatGroq(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        api_key=API_KEY,
    )
