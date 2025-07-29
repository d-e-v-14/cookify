import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Gemini-pro model
model = genai.GenerativeModel(model_name="gemini-2.0-pro-exp")

def generate_recipe(ingredients, preference=""):
    prompt = (
        f"Ingredients: {', '.join(ingredients)}.\n"
        f"Generate a {preference} recipe. "
        f"Include a title, ingredients list, step-by-step instructions, and one optional substitution."
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Error generating recipe. Please try again later."
