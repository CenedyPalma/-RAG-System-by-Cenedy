from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

model = SentenceTransformer("sentence-transformers/LaBSE")

def build_vector_store(chunks: list[str], dim=768):
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, "data/faiss.index")
    with open("data/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    return index
