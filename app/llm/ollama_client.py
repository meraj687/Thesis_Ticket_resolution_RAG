"""
Ollama Client
"""

import ollama


class OllamaClient:
    """
    Handles communication with the local Ollama model.
    """

    def __init__(self, model="llama3.2"):

        self.model = model

    def generate(self, prompt: str):

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response["message"]["content"]