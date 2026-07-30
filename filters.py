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


def filter_jobs(jobs):

    filtered_jobs = []

    for job in jobs:

        text = (
            job.get("title", "") +
            job.get("description", "")
        ).lower()

        matched = False

        for keyword in ROLES + SKILLS:
            if keyword.lower() in text:
                matched = True
                break

        if matched:
            filtered_jobs.append(job)

    return filtered_jobs