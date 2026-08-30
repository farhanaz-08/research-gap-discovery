from config.llm import SYSTEM_PROMPT
from app.llm.llm_wrapper import LLMWrapper

llm = LLMWrapper()

result = llm.generate_json(
    system_prompt=SYSTEM_PROMPT,
    user_prompt="""
Extract:

1. Research intent
2. Keywords

Research Topic:

Shared-memory Multi-Agent Systems
"""
)

print(result["response"])
print(f"\nExecution Time: {result['execution_time']:.2f} seconds")