import faiss, pickle
from embeddings import model

def load_index():
    index = faiss.read_index("data/faiss.index")
    with open("data/chunks.pkl","rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve(query: str, top_k=5):
    q_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(q_emb, top_k)
    return [chunks[i] for i in I[0]]
