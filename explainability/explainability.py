import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import pandas as pd

# Import Top 10 candidates from ranking module
from ranking.search_candidates import get_top_candidates

print("=" * 70)
print("AI RECRUITER - SIGNALS & EXPLAINABILITY")
print("=" * 70)

# ----------------------------------------------------
# Load Top Candidates
# ----------------------------------------------------



# ----------------------------------------------------
# Recruiter Input
# ----------------------------------------------------

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
top_candidates = get_top_candidates(job_description)

print("\nEnter Interview Questions.")
print("Press ENTER on an empty line to finish.\n")

interview_questions = []

while True:

    question = input("Question : ")

    if question.strip() == "":
        break

    interview_questions.append(question)

print("\nRecruiter Input Received Successfully.")

# ----------------------------------------------------
# Skill Database
# ----------------------------------------------------

skill_database = [

    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "React",
    "Node.js",
    "JavaScript",
    "Git",
    "Linux",
    "Flask",
    "Django",
    "Spark",
    "Hadoop",
    "NumPy",
    "Pandas",
    "Scikit-learn"

]

# ----------------------------------------------------
# Extract Required Skills
# ----------------------------------------------------

required_skills = []

for skill in skill_database:

    if skill.lower() in job_description.lower():
        required_skills.append(skill)

print("\nDetected Required Skills")

for skill in required_skills:
    print("✔", skill)

if len(required_skills) == 0:

    print("\nNo valid skills detected.")

    exit()

results = []

print("\n")
print("=" * 70)
print("Analyzing Top Candidates...")
print("=" * 70)
# ----------------------------------------------------
# Analyze Each Candidate
# ----------------------------------------------------

for row in top_candidates:

    candidate_name = row["Name"]
    candidate_title = row["Current_Title"]
    similarity = row["Similarity_Score"]

    candidate_skills = [
        x.strip().lower()
        for x in str(row["Skills"]).split(",")
    ]

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in candidate_skills:
            matched_skills.append(skill)

    if len(required_skills) > 0:
        skill_match = len(matched_skills) / len(required_skills)
    else:
        skill_match = 0

    explanation = []

    explanation.append(
        f"Matched Skills : {len(matched_skills)}/{len(required_skills)}"
    )

    # ----------------------------------------------------
    # Behaviour Signal Analysis
    # ----------------------------------------------------

    github_score = row["Github_Score"]
    profile_score = row["Profile_Completeness"]
    response_score = row["Recruiter_Response_Rate"]
    notice_period = row["Notice_Period"]

    if github_score >= 80:
        explanation.append("Strong GitHub Activity")
    elif github_score >= 60:
        explanation.append("Good GitHub Activity")
    else:
        explanation.append("Low GitHub Activity")

    if profile_score >= 90:
        explanation.append("Highly Complete Profile")
    elif profile_score >= 75:
        explanation.append("Well Maintained Profile")
    else:
        explanation.append("Profile Needs Improvement")

    if str(row["Open_To_Work"]).lower() in ["true", "yes", "1"]:
        explanation.append("Open To Work")

    if response_score >= 80:
        explanation.append("Highly Responsive")
    elif response_score >= 60:
        explanation.append("Moderately Responsive")
    else:
        explanation.append("Low Recruiter Response")

    if notice_period <= 15:
        explanation.append("Immediate Joiner")
    elif notice_period <= 30:
        explanation.append("Can Join Within 30 Days")
    else:
        explanation.append("Long Notice Period")

    # ----------------------------------------------------
    # Confidence Score
    # ----------------------------------------------------

    confidence = (
    similarity * 100 * 0.50 +
    skill_match * 100 * 0.30 +
    github_score * 0.08 +
    profile_score * 0.07 +
    response_score * 0.05
    )

    confidence = round(min(confidence, 100), 2)

    # ----------------------------------------------------
    # Recommendation Category
    # ----------------------------------------------------

    if confidence >= 90:
        category = "Excellent Match"
    elif confidence >= 80:
        category = "Strong Match"
    elif confidence >= 70:
        category = "Good Match"
    elif confidence >= 60:
        category = "Average Match"
    else:
        category = "Low Match"

    # ----------------------------------------------------
    # Store Candidate Result
    # ----------------------------------------------------

    results.append({

        "Candidate": candidate_name,

        "Current_Title": candidate_title,

        "Similarity_Score": similarity,

        "Confidence": confidence,

        "Category": category,

        "Matched Skills": ", ".join(matched_skills),

        "Why This Candidate": " | ".join(explanation),

        "Recruiter Questions": " | ".join(interview_questions)

    })
    # ----------------------------------------------------
# Convert Results to DataFrame
# ----------------------------------------------------

results_df = pd.DataFrame(results)

# Sort by Confidence Score
results_df = results_df.sort_values(
    by=["Confidence", "Similarity_Score"],
    ascending=[False, False]
)

# Top 10 Candidates
top_candidates_df = results_df.head(10)

# ----------------------------------------------------
# Display Results
# ----------------------------------------------------

print("\n")
print("=" * 70)
print("TOP 10 CANDIDATES")
print("=" * 70)

rank = 1

for _, row in top_candidates_df.iterrows():

    print(f"\nRank : {rank}")
    print(f"Candidate : {row['Candidate']}")
    print(f"Current Title : {row['Current_Title']}")
    print(f"Similarity Score : {row['Similarity_Score']:.4f}")
    print(f"Confidence Score : {row['Confidence']} %")
    print(f"Recommendation : {row['Category']}")

    print("\nMatched Skills")

    if row["Matched Skills"] != "":
        print(row["Matched Skills"])
    else:
        print("No matched skills found.")

    print("\nWhy this Candidate?")

    reasons = row["Why This Candidate"].split("|")

    for reason in reasons:
        print("✔", reason.strip())

    print("\nRecruiter's Interview Questions")

    questions = row["Recruiter Questions"].split("|")

    if len(questions) == 1 and questions[0].strip() == "":
        print("No interview questions provided.")
    else:
        for i, question in enumerate(questions, start=1):
            print(f"{i}. {question.strip()}")

    print("-" * 70)

    rank += 1

# ----------------------------------------------------
# Save Results
# ----------------------------------------------------

top_candidates_df.to_csv(
    "candidate_explanations.csv",
    index=False
)

print("\nResults saved successfully!")
print("Output File : candidate_explanations.csv")

print("\nExplainability Module Completed Successfully.")