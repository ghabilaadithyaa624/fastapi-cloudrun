import os
from fastapi import FastAPI

app = FastAPI(title="Cloud Run FastAPI Microservice")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Hello from FastAPI on Google Cloud Run!",
        "project": os.getenv("GOOGLE_CLOUD_PROJECT", "local")
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
