import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

def check_models():
    try:
        models = genai.list_models()
        print("Models available for your API key:\n")
        for model in models:
            print(f"🔹 Model: {model.name}")
            print(f"   ➤ Supports: {model.supported_generation_methods}")
            print()
    except Exception as e:
        print(" Error fetching models:", e)

if __name__ == "__main__":
    check_models()
