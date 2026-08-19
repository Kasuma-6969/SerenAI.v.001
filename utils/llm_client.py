# utils/llm_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.cliente = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.modelo = "llama-3.1-8b-instant"
    
    def generar(self, sistema, usuario, temperatura=0.7):
        respuesta = self.cliente.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario}
            ],
            temperature=temperatura
        )
        return respuesta.choices[0].message.content