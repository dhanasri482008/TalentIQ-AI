import pandas as pd
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Reading candidate data...")
df = pd.read_csv("../clean_candidates.csv")

# Combine important fields into one text
df["combined_text"] = (
    df["Current_Title"].fillna("") + " " +
    df["Headline"].fillna("") + " " +
    df["Skills"].fillna("") + " " +
    df["Education"].fillna("") + " " +
    df["Projects"].fillna("") + " " +
    df["Job_Titles"].fillna("")
)

print("Generating embeddings...")
embeddings = model.encode(
    df["combined_text"].tolist(),
    show_progress_bar=True
)

print("Embedding Shape:", embeddings.shape)

print("Saving embeddings...")
import numpy as np
np.save("candidate_embeddings.npy", embeddings)

print("Done!")
