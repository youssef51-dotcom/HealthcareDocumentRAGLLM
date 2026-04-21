import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    vectors = model.encode(texts, convert_to_numpy=True)
    return vectors