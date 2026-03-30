def get_ats_tips(missing_keywords):
    tips = [
        "Use a simple resume format without tables or too many graphics.",
        "Add a clear Skills section.",
        "Use exact job-related keywords naturally.",
        "Keep important skills in Projects, Experience, and Summary sections.",
        "Use standard headings like Education, Skills, Projects, Experience."
    ]

    if missing_keywords:
        tips.append("Try including these important missing keywords: " + ", ".join(missing_keywords[:10]))

    return tips