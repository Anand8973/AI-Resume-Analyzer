import re

COMMON_WORDS = {
    "the", "and", "is", "in", "to", "of", "a", "for", "on", "with",
    "as", "at", "by", "an", "be", "this", "that", "from", "or",
    "are", "was", "were", "it", "you", "your", "will", "can", "have",
    "has", "had", "we", "our", "they", "their", "job", "role", "work"
}

ROLE_SKILLS = {
    "python developer": [
        "python", "flask", "django", "api", "sql", "git", "github", "oop", "debugging"
    ],
    "web developer": [
        "html", "css", "javascript", "react", "node", "api", "mongodb", "git", "responsive"
    ],
    "data analyst": [
        "python", "sql", "excel", "pandas", "numpy", "visualization", "power bi", "statistics"
    ],
    "machine learning engineer": [
        "python", "machine learning", "nlp", "tensorflow", "pytorch", "opencv", "pandas", "numpy"
    ],
    "java developer": [
        "java", "oop", "sql", "spring", "hibernate", "api", "git", "debugging"
    ],
    "full stack developer": [
        "html", "css", "javascript", "react", "node", "python", "sql", "git", "responsive"
    ],
    "backend developer": [
        "python", "java", "node", "sql", "api", "git", "debugging", "oop"
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "angular", "vue", "responsive", "git"
    ],
    "software engineer": [
        "python", "java", "c++", "sql", "git", "oop", "debugging", "api"
    ],
    "data scientist": [
        "python", "machine learning", "nlp", "tensorflow", "pytorch", "pandas", "numpy", "visualization", "statistics"
    ],
    "cloud engineer": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "python", "git", "api"
    ],
    "devops engineer": [
        "docker", "kubernetes", "terraform", "aws", "azure", "gcp", "python", "git", "ci/cd"
    ],
    "mobile developer": [
        "android", "ios", "react native", "flutter", "java", "kotlin", "swift", "git", "api"
    ],
    "data engineer": [
        "python", "sql", "hadoop", "spark", "airflow", "aws", "azure", "gcp", "git", "etl"
    ],
    "cybersecurity analyst": [
        "network security", "penetration testing", "vulnerability assessment", "firewalls",
    ],
    "ui/ux designer": [
        "ui design", "ux design", "wireframing", "prototyping", "figma", "adobe xd", "user research"
    ],
    "UI developer": [
        "html", "css", "javascript", "react", "angular", "vue", "responsive", "git"
    ],
    "QA engineer": [
        "manual testing", "automated testing", "selenium", "cypress", "test cases", "bug tracking", "git"
    ],
    "business analyst": [
        "requirement gathering", "stakeholder communication", "process modeling", "data analysis", "sql", "visualization", "power bi", "statistics"
    ],
    "product manager": [
        "product roadmap", "stakeholder communication", "agile methodologies", "market research", "data analysis", "sql", "visualization", "power bi", "statistics"
    ],
    "data architect": [
        "data modeling", "database design", "sql", "hadoop", "spark", "aws", "azure", "gcp", "git", "etl"
    ],
    "network engineer": [
        "network design", "routing", "switching", "firewalls", "vpn", "network security", "troubleshooting", "git"
    ],
    "system administrator": [
        "linux", "windows server", "networking", "scripting", "aws", "azure", "gcp", "git", "troubleshooting"
    ],
    "technical support specialist": [
        "troubleshooting", "customer service", "technical knowledge", "communication skills", "git"
    ],
    "it support specialist": [
        "troubleshooting", "customer service", "technical knowledge", "communication skills", "git"
    ],
    "help desk technician": [
        "troubleshooting", "customer service", "technical knowledge", "communication skills", "git"
    ],
    "system analyst": [
        "requirement gathering", "stakeholder communication", "process modeling", "data analysis", "sql", "visualization", "power bi", "statistics"
    ],
    "database administrator": [
        "sql", "database design", "performance tuning", "backup and recovery", "hadoop", "spark", "aws", "azure", "gcp", "git", "etl"
    ],
    "it consultant": [
        "technical expertise", "problem-solving", "communication skills", "project management", "git"
    ]
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords(text):
    text = clean_text(text)
    words = text.split()
    keywords = []

    for word in words:
        if word not in COMMON_WORDS and len(word) > 2:
            keywords.append(word)

    return set(keywords)

def check_resume_sections(resume_text):
    text = resume_text.lower()
    return {
        "education": "education" in text,
        "skills": "skills" in text,
        "projects": "project" in text or "projects" in text,
        "experience": "experience" in text,
    }

def detect_multiple_roles(job_description, resume_text):
    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)
    combined_keywords = jd_keywords.union(resume_keywords)

    role_scores = []

    for role, skills in ROLE_SKILLS.items():
        role_skill_set = set(skills)
        matched = combined_keywords.intersection(role_skill_set)

        if len(role_skill_set) == 0:
            score = 0
        else:
            score = int((len(matched) / len(role_skill_set)) * 100)

        role_scores.append({
            "role": role.title(),
            "score": score
        })

    role_scores = sorted(role_scores, key=lambda x: x["score"], reverse=True)
    return role_scores[:3]

def get_role_based_suggestions(best_role, missing_keywords):
    suggestions = []
    role_key = best_role.lower()

    if role_key in ROLE_SKILLS:
        role_skills = ROLE_SKILLS[role_key]
        matched_role_missing = [skill for skill in role_skills if skill in missing_keywords]

        if matched_role_missing:
            suggestions.append(
                f"For a {best_role} role, try adding these relevant skills if you know them: "
                + ", ".join(matched_role_missing[:6])
            )
        else:
            suggestions.append(
                f"Your resume already contains many important skills for a {best_role} role."
            )
    else:
        suggestions.append(
            "Try matching your resume content more closely with the target role's skills and tools."
        )

    return suggestions

def analyze_resume(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    matched_keywords = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords - resume_keywords

    if len(jd_keywords) == 0:
        keyword_score = 0
    else:
        keyword_score = int((len(matched_keywords) / len(jd_keywords)) * 100)

    top_roles = detect_multiple_roles(job_description, resume_text)
    best_role = top_roles[0]["role"] if top_roles else "General"

    important_total = set()
    important_matched = set()

    if best_role.lower() in ROLE_SKILLS:
        important_total = set(ROLE_SKILLS[best_role.lower()])
        important_matched = resume_keywords.intersection(important_total)

    if len(important_total) == 0:
        important_score = 0
    else:
        important_score = int((len(important_matched) / len(important_total)) * 100)

    final_score = int((keyword_score * 0.7) + (important_score * 0.3))

    sections = check_resume_sections(resume_text)
    suggestions = []

    if final_score < 40:
        suggestions.append("Your resume has a low match with the job description. Add more relevant skills, tools, and project keywords.")
    elif final_score < 70:
        suggestions.append("Your resume is moderately matched. Improve it by adding important missing keywords naturally.")
    else:
        suggestions.append("Your resume matches well. Focus on stronger wording and ATS-friendly formatting.")

    if not sections["skills"]:
        suggestions.append("Add a proper Skills section.")
    if not sections["projects"]:
        suggestions.append("Add a Projects section with technologies used.")
    if not sections["experience"]:
        suggestions.append("Add Experience section, or if you are a fresher, add internships, training, or college project work.")
    if missing_keywords:
        suggestions.append("Include relevant missing keywords in Skills, Projects, and Experience sections.")
    if len(matched_keywords) < 5:
        suggestions.append("Your resume should use more job-specific words from the job description.")

    suggestions.extend(get_role_based_suggestions(best_role, missing_keywords))

    return {
        "score": final_score,
        "keyword_score": keyword_score,
        "important_score": important_score,
        "matched_keywords": sorted(list(matched_keywords)),
        "missing_keywords": sorted(list(missing_keywords)),
        "suggestions": suggestions,
        "sections": sections,
        "detected_role": best_role,
        "top_roles": top_roles
    }