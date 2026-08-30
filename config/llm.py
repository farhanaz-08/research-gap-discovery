import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 4096


SYSTEM_PROMPT = """
You are an expert AI research assistant.

Follow these rules:

1. Answer only what is requested.
2. Never invent information.
3. Return valid JSON when requested.
4. Never use markdown code blocks.
5. Never add explanations outside the requested format.
"""