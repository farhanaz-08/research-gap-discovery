import json
import time

from google import genai

from config.llm import (
    GEMINI_API_KEY,
    MODEL_NAME
)


class LLMWrapper:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = MODEL_NAME

    def clean_json_response(
        self,
        text: str
    ):

        text = text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()

    def parse_json(
        self,
        text: str
    ):

        cleaned = self.clean_json_response(text)

        return json.loads(cleaned)

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str
    ):

        full_prompt = f"""

{system_prompt}

------------------------

{user_prompt}

"""

        start = time.perf_counter()

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt
        )

        execution_time = time.perf_counter() - start

        return {

            "response": response.text,

            "execution_time": execution_time

        }

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_retries: int = 3
    ):

        full_prompt = f"""

{system_prompt}

------------------------

{user_prompt}

Return ONLY valid JSON.

"""

        for attempt in range(max_retries):

            try:

                start = time.perf_counter()

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt
                )

                execution_time = time.perf_counter() - start

                return {

                    "response": self.parse_json(
                        response.text
                    ),

                    "execution_time": execution_time

                }

            except json.JSONDecodeError:

                if attempt == max_retries - 1:

                    raise RuntimeError(
                        "LLM returned invalid JSON after multiple attempts."
                    )

                time.sleep(1)