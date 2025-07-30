import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-2.5-pro")

def generate_recipe(ingredients, preference=""):
    prompt = (
        f"You are a smart chef assistant.\n"
        f"Ingredients: {', '.join(ingredients)}.\n"
        f"{'Preferences/Instructions: ' + preference if preference else ''}\n"
        f"Generate a recipe based on these inputs.\n"
        f"Include:\n"
        f"- A title\n"
        f"- A list of ingredients\n"
        f"- Step-by-step cooking instructions\n"
        f"- One optional substitution for flexibility"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Error generating recipe. Please try again later."
