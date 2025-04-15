import os
import time
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define the FastAPI app
app = FastAPI()

# Get the Ollama base URL from environment variables (default to "http://ollama:11434")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

# Function to check if any model is currently loaded
def check_ollama_model():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200 and response.json().get("models"):
            print("Model is available!")
            return True
        else:
            print("No models loaded.")
    except Exception as e:
        print(f"Error checking model: {e}")
    return False

# Function to load a default model if none is loaded
def try_load_default_model(model="llama3"):
    try:
        print(f"Attempting to load default model: {model}")
        response = requests.post(f"{OLLAMA_BASE_URL}/api/load/{model}", timeout=10)
        if response.status_code == 200:
            print(f"Model '{model}' loaded successfully.")
            return True
        else:
            print(f"Failed to load model '{model}': {response.text}")
    except Exception as e:
        print(f"Exception while loading model '{model}': {e}")
    return False

# Wait for Ollama to become available and load a model
def ensure_ollama_ready():
    retries = 5
    while retries > 0:
        if check_ollama_model():
            return True
        print("Model not yet loaded, retrying in 5s...")
        time.sleep(5)
        retries -= 1

    print("No model loaded after retries. Attempting to load default model...")
    return try_load_default_model()

# Attempt to load a model at startup (but don't crash if it fails)
ensure_ollama_ready()

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI server is running 🚀"}

# Pydantic model to define the input structure for generating text
class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3"  # Default model

# Endpoint for generating text based on a prompt
@app.post("/generate")
def generate_text(request: PromptRequest):
    if not check_ollama_model():
        raise HTTPException(status_code=500, detail="No Ollama model is loaded.")

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": request.model,
                "prompt": request.prompt
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return {"response": data.get("response", "")}
    except requests.exceptions.RequestException as e:
        print(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Pydantic model for loading a model
class LoadModelRequest(BaseModel):
    model: str

# Endpoint for loading a model
@app.post("/load")
async def load_model(request: LoadModelRequest):
    ollama_url = f"{OLLAMA_BASE_URL}/api/load/{request.model}"
    try:
        response = requests.post(ollama_url, timeout=10)
        if response.status_code == 200:
            return {"status": "Model loaded successfully"}
        else:
            return {"status": "Failed to load model", "error": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
