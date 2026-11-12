import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import firestore

app = FastAPI(title="FastAPI + Firestore Microservice")

def get_db():
    return firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT", "project-f838104a-2d52-49a5-808"))

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

@app.get("/")
def read_root():
    return {"status": "online", "database": "Cloud Firestore connected"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/items/{item_id}")
def create_item(item_id: str, item: Item):
    try:
        doc_ref = get_db().collection("items").document(item_id)
        doc_ref.set(item.model_dump())
        return {"id": item_id, **item.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}")
def get_item(item_id: str):
    try:
        doc = get_db().collection("items").document(item_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": doc.id, **doc.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items")
def list_items():
    try:
        docs = get_db().collection("items").stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
