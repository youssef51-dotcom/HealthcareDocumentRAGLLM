import faiss
from .embedding import embed_texts, model
import pickle
import numpy as np

def build_faiss_index(chunks):
    texts = [c["text"] for c in chunks["sections"]]

    embeddings = embed_texts(texts)
    dim = embeddings.shape[1]

    # L2 index (simple + reliable)
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings.astype(np.float32))

    return index, embeddings, texts

def search(query, index, chunks, k=5):
    query_vec = model.encode([query], convert_to_numpy=True)

    distances, indices = index.search(query_vec.astype(np.float32), k)

    results = [chunks[i] for i in indices[0]]

    return results

def save_index(index, chunks, path="faiss.index", meta_path="chunks.pkl"):
    faiss.write_index(index, path)

    with open(meta_path, "wb") as f:
        pickle.dump(chunks, f)

def load_index(path="faiss.index", meta_path="chunks.pkl"):
    index = faiss.read_index(path)

    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks