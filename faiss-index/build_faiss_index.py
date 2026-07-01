import os
import numpy as np
import faiss

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

embedding_path = os.path.join(
    BASE_DIR,
    "EMBEDDING",
    "candidate_embeddings.npy"
)

print("Loading embeddings...")
embeddings = np.load(embedding_path)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

print("Adding embeddings...")
index.add(embeddings)

index_path = os.path.join(
    BASE_DIR,
    "faiss-index",
    "candidate_index.faiss"
)

print("Saving index...")
faiss.write_index(index, index_path)

print("✅ FAISS index created successfully!")