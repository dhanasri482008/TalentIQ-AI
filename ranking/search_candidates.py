import os
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer


def search_candidates(job_description):

    print("=" * 70)
    print("AI RECRUITER - CANDIDATE SEARCH")
    print("=" * 70)

    print("\nLoading Sentence Transformer Model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Loading FAISS Index...")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index = faiss.read_index(
       os.path.join(BASE_DIR, "faiss-index", "candidate_index.faiss")
    )
    print("Loading Candidate Dataset...")
    df = pd.read_csv(
       os.path.join(BASE_DIR, "clean_candidates.csv")
    )

    print("\nGenerating Query Embedding...")

    query_embedding = model.encode(
        [job_description]
    ).astype("float32")

    print("Searching Candidates...\n")

    distances, indices = index.search(query_embedding, 10)

    top_candidates = []

    print("=" * 70)
    print("TOP 10 CANDIDATES")
    print("=" * 70)

    for rank, idx in enumerate(indices[0], start=1):

        candidate = df.iloc[idx].to_dict()

        similarity = float(distances[0][rank - 1])

        candidate["Similarity_Score"] = similarity

        top_candidates.append(candidate)

        print(f"\nRank : {rank}")
        print(f"Name : {candidate['Name']}")
        print(f"Current Title : {candidate['Current_Title']}")
        print(f"Skills : {candidate['Skills']}")
        print(f"Similarity Score : {similarity:.4f}")
        print("-" * 70)

    return top_candidates


def get_top_candidates(job_description):
    return search_candidates(job_description)


if __name__ == "__main__":

    print("\nRecruiter Input")
    print("-" * 70)

    print("Paste the complete Job Description.")
    print("Press ENTER twice when finished.\n")

    jd_lines = []

    while True:
        line = input()

        if line.strip() == "":
            break

        jd_lines.append(line)

    job_description = "\n".join(jd_lines)

    top_candidates = search_candidates(job_description)

    print("\nSearch Completed Successfully!")
    print(f"Total Candidates Retrieved : {len(top_candidates)}")