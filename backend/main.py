import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from react_agent import react_loop
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 1. Get the directory of the current script
script_dir = Path(__file__).resolve().parent

# 2. Look for the .env file in the script's directory (or its parent directory)
# If your .env is in the root 'carechoice-ai' folder, and this script is in 'backend/',
# use script_dir.parent / '.env'. If it's in the same folder, use script_dir / '.env'
env_path = script_dir.parent / '.env' 

# 3. Explicitly load the file from that specific path
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Mount frontend folder
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

@app.get("/")
def read_root():
    return FileResponse("../frontend/index.html")

@app.post("/recommend")
def recommend(user_input: dict):
    result = react_loop(user_input, api_key=GEMINI_API_KEY)
    return result
