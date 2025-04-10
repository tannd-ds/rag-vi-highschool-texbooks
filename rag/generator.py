import os
from google import genai
from dotenv import load_dotenv


def format_prompt(contexts, question):
    context_str = "\n".join([f"Context {i+1}: {c}" for i, c in enumerate(contexts)])
    return f"You are a helpful assistant. Use the following context to answer the question.\n\n{context_str}\n\nQuestion: {question}"

class GeminiClient:
    def __init__(self):
        load_dotenv()
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
        self.client = genai.Client(api_key=gemini_api_key)

    def generate_answer(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text