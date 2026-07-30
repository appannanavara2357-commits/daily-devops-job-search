ROLES = [
    "DevOps Engineer",
    "Senior DevOps Engineer",
    "Cloud DevOps Engineer",
    "AWS DevOps Engineer",
    "Azure DevOps Engineer",
    "DevSecOps Engineer",
    "SRE",
    "Platform Engineer",
    "Kubernetes Engineer",
    "Cloud Engineer"
]


SKILLS = [
    "AWS",
    "Azure",
    "Terraform",
    "Kubernetes",
    "Docker",
    "Jenkins",
    "Ansible",
    "Linux",
    "CI/CD",
    "GitHub Actions",
    "Helm",
    "EKS",
    "AKS"
]


def find_skills(text):

    matched_skills = []

    for skill in SKILLS:
        if skill.lower() in text.lower():
            matched_skills.append(skill)

    return matched_skills


def filter_jobs(jobs):

    filtered_jobs = []

    for job in jobs:

        text = (
            job.get("title", "") +
            job.get("description", "")
        )

        skills = find_skills(text)

        if skills:

            job["matched_skills"] = skills
            filtered_jobs.append(job)

    return filtered_jobs