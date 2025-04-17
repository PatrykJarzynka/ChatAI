from llama_index.llms.openai import OpenAI
from typing import List

class OpenAIHelper():
    def __init__(self):
        self.support_llm = OpenAI('gpt-4o-mini')
        pass

    def get_state_assigned_to_city(self, city: str, states: List[str]) -> str:
            prompt = f"""Pick only one state from the list: {','.join(states)}, that is in your opinion assigned to the given city: {city}. Answer with just the name of the state, one word."""

            response = self.support_llm.complete(prompt)
            return response.text.strip()