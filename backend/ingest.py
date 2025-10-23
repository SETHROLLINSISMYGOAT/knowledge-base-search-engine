import os, pickle
from sentence_transformers import SentenceTransformer
import faiss
from PyPDF2 import PdfReader
from .config import UPLOAD_DIR, FAISS_INDEX_PATH, EMBEDDINGS_PATH

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load existing FAISS index or create new
if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(EMBEDDINGS_PATH, "rb") as f:
        doc_map = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)
    doc_map = {}

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:  # plain text file
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def ingest_file(file_path, doc_id):
    text = extract_text(file_path)
    vector = embedding_model.encode([text])
    index.add(vector)
    doc_map[doc_id] = file_path
    # Save index and mapping
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(doc_map, f)
    return {"doc_id": doc_id, "filename": os.path.basename(file_path)}
