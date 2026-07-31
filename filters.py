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
    "Cloud Operations Engineer",
    "Cloud Infrastructure Engineer",
    "MLOps Engineer"

]


SKILLS = [

    "AWS",
    "Azure",
    "GCP",

    "Terraform",
    "CloudFormation",

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

    matched_skills = []

    text = text.lower()


    for skill in SKILLS:

        if skill.lower() in text:
            matched_skills.append(skill)


    return matched_skills




def is_matching_role(text):

    text = text.lower()


    for role in ROLES:

        if role.lower() in text:
            return True


    return False




def filter_jobs(jobs):

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


        tags = job.get(
            "tags",
            []
        )


        if isinstance(tags, list):

            tags = " ".join(tags)



        full_text = (

            title
            + " "
            + description
            + " "
            + tags

        )



        role_match = is_matching_role(
            full_text
        )



        skills = find_skills(
            full_text
        )



        # Accept:
        # 1. Exact DevOps role
        # OR
        # 2. Non DevOps title but multiple skills


        if role_match or len(skills) >= 2:


            job["matched_skills"] = skills


            filtered_jobs.append(
                job
            )



    return filtered_jobs