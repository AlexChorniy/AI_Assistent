from fastapi import FastAPI, HTTPException
import requests
import time

app = FastAPI()

OLLAMA_URL = "http://ollama:11434"
MODEL_NAME = "llama3"

@app.on_event("startup")
def initialize_model():
    print(f"🔁 Checking if model '{MODEL_NAME}' is loaded...")

    # 1. Pull model if not exists
    tags = requests.get(f"{OLLAMA_URL}/api/tags").json()
    model_names = [model["name"] for model in tags.get("models", [])]

    if not any(MODEL_NAME in name for name in model_names):
        print(f"⬇️ Pulling model '{MODEL_NAME}'...")
        res = requests.post(f"{OLLAMA_URL}/api/pull", json={"name": MODEL_NAME})
        if res.status_code != 200:
            raise RuntimeError(f"Failed to pull model: {res.text}")
        print("✅ Model pulled.")

    # Wait until model is ready (optional, safe for first run)
    time.sleep(2)

@app.post("/generate")
def generate_text(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Model generation failed")
    return {"response": response.json().get("response", "")}
