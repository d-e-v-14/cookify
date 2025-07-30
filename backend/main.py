from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from dotenv import load_dotenv
from yolomodel import detect_ingredients
from llm import generate_recipe  
import logging

load_dotenv()

app = FastAPI()
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

@app.get("/")
def root():
    return {
        "message": "Welcome to the Smart Chef's Assistant API!",
        "upload_endpoint": "/upload/",
        "instructions": "Send a POST request with a file using multipart/form-data to /upload/ to get detected ingredients and a generated recipe."
    }

@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    allergies: str = Form(""),
    suggestions: str = Form("")
):
    save_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        detected = detect_ingredients(save_path)
        ingredients = list(detected.keys())

        if not ingredients:
            return JSONResponse(status_code=400, content={"error": "No ingredients detected."})

        preference = ""
        if allergies:
            preference += f"Exclude these allergens: {allergies}. "
        if suggestions:
            preference += suggestions

        recipe = generate_recipe(ingredients, preference)

        background_tasks.add_task(os.remove, save_path)

        logger = logging.getLogger("uvicorn.error")
        logger.info(f"Detected: {detected}")
        logger.info(f"Recipe: {recipe}")
        logger.info(f"Allergies: {allergies}")
        logger.info(f"Suggestions: {suggestions}")

        return {
            "detected_ingredients": detected,
            "recipe": recipe,
        }

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
