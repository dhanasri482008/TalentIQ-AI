import json
import pandas as pd

input_file = "candidates.jsonl"

clean_candidates = []

with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        candidate = json.loads(line)

        # Profile
        profile = candidate.get("profile", {})

        # Skills (remove duplicates and extra spaces)
        skills = sorted(set(
            skill.get("name", "").strip()
            for skill in candidate.get("skills", [])
            if skill.get("name")
        ))

        # Education
        education = [
            f'{edu.get("degree", "")} in {edu.get("field_of_study", "")}'.strip()
            for edu in candidate.get("education", [])
        ]

        # Experience
        experience = profile.get("years_of_experience", 0)

        # Career History
        companies = [
            job.get("company", "")
            for job in candidate.get("career_history", [])
            if job.get("company")
        ]

        job_titles = [
            job.get("title", "")
            for job in candidate.get("career_history", [])
            if job.get("title")
        ]

        # Projects (if available)
        projects = [
            project.get("name", "")
            for project in candidate.get("projects", [])
            if project.get("name")
        ]

        # Certifications
        certifications = candidate.get("certifications", [])

        # Activity Signals
        signals = candidate.get("redrob_signals", {})

        # Create clean candidate record
        clean_candidate = {
            "Candidate_ID": candidate.get("candidate_id", ""),
            "Name": profile.get("anonymized_name", ""),
            "Current_Title": profile.get("current_title", ""),
            "Headline": profile.get("headline", ""),
            "Location": profile.get("location", ""),
            "Experience_Years": experience,
            "Skills": ", ".join(skills),
            "Education": ", ".join(education),
            "Projects": ", ".join(projects),
            "Companies": ", ".join(companies),
            "Job_Titles": ", ".join(job_titles),
            "Certifications": len(certifications),
            "Github_Score": signals.get("github_activity_score"),
            "Profile_Completeness": signals.get("profile_completeness_score"),
            "Open_To_Work": signals.get("open_to_work_flag"),
            "Notice_Period": signals.get("notice_period_days"),
            "Recruiter_Response_Rate": signals.get("recruiter_response_rate")
        }

        clean_candidates.append(clean_candidate)

# Create DataFrame
df = pd.DataFrame(clean_candidates)

# Save to CSV
df.to_csv("clean_candidates.csv", index=False)

print("✅ Clean dataset created successfully!")
print(f"Total candidates processed: {len(df)}")
print(df.head())