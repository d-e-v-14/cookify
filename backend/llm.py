from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GPT")

client = OpenAI(api_key=api_key)

def generate_recipe(ingredients, preference=""):
    prompt = (
        f"Ingredients: {', '.join(ingredients)}.\n"
        f"Generate a {preference} recipe. "
        f"Include title, ingredients,steps,and one substitution."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    recipe = response.choices[0].message.content

