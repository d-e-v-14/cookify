from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from openai import OpenAI
from .yolomodel import detect_ingredients
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GPT")
client = OpenAI(api_key=api_key)


app = FastAPI()
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    save_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        detected = detect_ingredients(save_path)
        ingredients = ", ".join(detected.keys())

        if not ingredients:
            return JSONResponse(status_code=400, content={"error": "No ingredients detected."})

        prompt = f"Create a creative recipe using the following ingredients: {ingredients}. Return ingredients list and step-by-step instructions."

        response = client.chat.completion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        recipe = response["choices"][0]["message"]["content"]

        background_tasks.add_task(os.remove, save_path)

        return {
            "detected_ingredients": detected,
            "recipe": recipe,
            "image_url": f"/temp/{file.filename}"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
