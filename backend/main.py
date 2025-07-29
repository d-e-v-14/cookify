from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from dotenv import load_dotenv
from yolomodel import detect_ingredients
from llm import generate_recipe  # <-- Gemini-powered

load_dotenv()

app = FastAPI()
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    save_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    try:
        # Save image
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detect ingredients
        detected = detect_ingredients(save_path)
        ingredients = list(detected.keys())

        if not ingredients:
            return JSONResponse(status_code=400, content={"error": "No ingredients detected."})

        # Generate recipe using Gemini
        recipe = generate_recipe(ingredients)

        # Clean up image after processing
        background_tasks.add_task(os.remove, save_path)

        return {
            "detected_ingredients": detected,
            "recipe": recipe,
            "image_url": f"/temp/{file.filename}"
        }

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
