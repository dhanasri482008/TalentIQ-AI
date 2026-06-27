import faiss
import numpy as np

print("Loading embeddings...")

embeddings = np.load("../EMBEDDING/candidate_embeddings.npy")

print("Embeddings Shape:", embeddings.shape)

# Convert to float32 (required by FAISS)
embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

print("Creating FAISS index...")

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Total Candidates Indexed:", index.ntotal)

faiss.write_index(index, "candidate_index.faiss")

print("FAISS Index Saved Successfully!")