import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index("../faiss-index/candidate_index.faiss")

print("Loading candidate data...")
df = pd.read_csv("../clean_candidates.csv")

job_description = input("Enter Job Description:\n")

print("Generating query embedding...")
query_embedding = model.encode([job_description])

print("Searching candidates...")
distances, indices = index.search(query_embedding, 10)

print("\nTop 10 Candidates:\n")

for rank, idx in enumerate(indices[0], start=1):
    candidate = df.iloc[idx]

    print(f"Rank {rank}")
    print(f"Name: {candidate['Name']}")
    print(f"Title: {candidate['Current_Title']}")
    print(f"Skills: {candidate['Skills']}")
    print(f"Similarity Score: {distances[0][rank-1]:.4f}")
    print("-" * 50)