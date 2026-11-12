from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import firestore

app = FastAPI(title="FastAPI + Firestore Microservice")
db = firestore.Client()

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
    doc_ref = db.collection("items").document(item_id)
    doc_ref.set(item.model_dump())
    return {"id": item_id, **item.model_dump()}

@app.get("/items/{item_id}")
def get_item(item_id: str):
    doc = db.collection("items").document(item_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": doc.id, **doc.to_dict()}

@app.get("/items")
def list_items():
    docs = db.collection("items").stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]
EO
