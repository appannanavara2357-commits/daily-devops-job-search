ROLES = [
    "DevOps Engineer",
    "Senior DevOps Engineer",
    "Cloud DevOps Engineer",
    "AWS DevOps Engineer",
    "Azure DevOps Engineer",
    "DevSecOps Engineer",
    "SRE",
    "Site Reliability Engineer",
    "Platform Engineer",
    "Kubernetes Engineer",
    "Cloud Engineer",
    "Infrastructure Engineer",
    "Cloud Operations Engineer"
]


SKILLS = [
    "AWS",
    "Azure",
    "GCP",
    "Terraform",
    "Kubernetes",
    "Docker",
    "Jenkins",
    "GitHub Actions",
    "Azure DevOps",
    "Ansible",
    "Linux",
    "CI/CD",
    "Helm",
    "ArgoCD",
    "EKS",
    "AKS",
    "ECS",
    "ECR",
    "CloudFormation",
    "Prometheus",
    "Grafana",
    "SonarQube",
    "Nexus",
    "Vault",
    "Python",
    "Shell",
    "Git"
]


def find_skills(text):
    """
    Find DevOps skills from job text
    """

    matched_skills = []

    text = text.lower()


    for skill in SKILLS:

        if skill.lower() in text:
            matched_skills.append(skill)


    return matched_skills



def is_matching_role(text):
    """
    Check DevOps related job role
    """

    text = text.lower()


    for role in ROLES:

        if role.lower() in text:
            return True


    return False



def filter_jobs(jobs):
    """
    Filter only relevant DevOps jobs
    """

    filtered_jobs = []


    for job in jobs:


        title = job.get(
            "title",
            ""
        )


        description = job.get(
            "description",
            ""
        )


        company = job.get(
            "company",
            ""
        )


        tags = job.get(
            "tags",
            []
        )


        # Convert tags list into text
        if isinstance(tags, list):
            tags = " ".join(tags)



        full_text = (
            title
            + " "
            + description
            + " "
            + company
            + " "
            + tags
        )



        skills = find_skills(
            full_text
        )


        role_match = is_matching_role(
            full_text
        )



        # Accept DevOps roles
        # even if description is empty

        if role_match:


            job["matched_skills"] = skills


            filtered_jobs.append(job)



    return filtered_jobs