from fastapi import FastAPI, UploadFile, File, HTTPException
import os, shutil, uuid
from .ingest import ingest_file

from search import retrieve_and_synthesize  # your search function
from config import UPLOAD_DIR

app = FastAPI(title="RAG Knowledge Base Search Engine")

@app.post("/ingest")
async def ingest(files: list[UploadFile] = File(...)):
    results = []
    for f in files:
        doc_id = str(uuid.uuid4())
        dest_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{f.filename}")
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(dest_path, "wb") as out:
            shutil.copyfileobj(f.file, out)
        res = ingest_file(dest_path, doc_id)
        results.append(res)
    return {"status": "ok", "ingested": results}

@app.post("/query")
async def query(payload: dict):
    q = payload.get("question")
    if not q:
        raise HTTPException(status_code=400, detail="Missing 'question'")
    top_k = int(payload.get("top_k", 5))
    return retrieve_and_synthesize(q, top_k=top_k)

@app.get("/health")
async def health():
    return {"status": "ok"}
