import re
from email.header import decode_header
from html import unescape


# ==========================
# Decode Subject
# ==========================

def clean_subject(subject):

    if not subject:
        return ""

    result = ""

    for part, encoding in decode_header(subject):

        if isinstance(part, bytes):

            result += part.decode(
                encoding or "utf-8",
                errors="ignore"
            )

        else:
            result += part

    return result.strip()



# ==========================
# Remove HTML
# ==========================

def remove_html(text):

    if not text:
        return ""

    text = unescape(text)

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()



# ==========================
# Extract Company
# ==========================

def extract_company(text):

    companies = [

        "Amazon",
        "Microsoft",
        "Google",
        "Accenture",
        "Wipro",
        "Infosys",
        "Deloitte",
        "PwC",
        "Quantiphi",
        "SysMind",
        "Saviynt",
        "Omnissa",
        "Wells Fargo",
        "GoKwik",
        "Lemon.io"

    ]


    for company in companies:

        if company.lower() in text.lower():

            return company


    return "Unknown"



# ==========================
# Extract LinkedIn Job
# ==========================

def extract_linkedin(text):

    lines = text.splitlines()

    job={}


    for i,line in enumerate(lines):

        line=line.strip()


        if not line:
            continue


        if "View job:" in line:

            url = line.split("View job:")[-1].strip()

            job["apply_link"]=url


            if i>=3:

                job["role"]=lines[i-3].strip()

                job["company"]=lines[i-2].strip()

                job["location"]=lines[i-1].strip()


            return job



    return None




# ==========================
# Main Extractor
# ==========================


def extract_job_details(subject, body, sender=""):


    subject=clean_subject(subject)

    body_text=remove_html(body)


    text=subject+" "+body_text


    lower=text.lower()



    # Ignore our own emails

    if "daily devops job alert" in lower:

        print("Skipped own alert")

        return None



    # Ignore application emails

    ignore=[

        "security alert",
        "delivery status",
        "application successful",
        "follow up application",
        "set your password",
        "welcome to",
        "recruiting experience",
        "survey",
        "job alert has been created"

    ]


    for word in ignore:

        if word in lower:

            print("Skipped:",word)

            return None




    # LinkedIn

    if "linkedin.com" in lower:


        linkedin_job=extract_linkedin(body_text)


        if linkedin_job:


            linkedin_job["skills"]=extract_skills(text)

            if "location" not in linkedin_job:

                linkedin_job["location"]="Not Found"


            return linkedin_job




    job={}



    # ======================
    # Role
    # ======================


    role=subject


    role=role.replace(
        "✉️ Job |",
        ""
    )


    role=role.replace(
        "âœ‰ï¸ Job |",
        ""
    )


    job["role"]=role.strip()



    # Company

    job["company"]=extract_company(text)



    # Location

    locations=[

        "Bengaluru",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Mumbai",
        "Pune",
        "Noida",
        "Gurgaon"

    ]


    found=[]


    for loc in locations:

        if loc.lower() in lower:

            found.append(loc)



    job["location"]=(
        ", ".join(found)
        if found
        else
        "Not Found"
    )



    job["skills"]=extract_skills(text)



    job["apply_link"]=extract_link(text)



    return job





# ==========================
# Skills
# ==========================


def extract_skills(text):


    skills=[

        "AWS",
        "Azure",
        "GCP",
        "Kubernetes",
        "Docker",
        "Terraform",
        "Jenkins",
        "Ansible",
        "Linux",
        "Python",
        "Java",
        "Git",
        "GitHub",
        "CI/CD"

    ]


    found=[]


    for skill in skills:

        if skill.lower() in text.lower():

            found.append(skill)


    return found




# ==========================
# URL Extraction
# ==========================


def extract_link(text):


    urls=re.findall(
        r'https?://[^\s"<>]+',
        text
    )


    for url in urls:


        if "linkedin.com/comm/jobs/view" in url:

            return url.split("&")[0]


        if "hirist.tech/j/" in url:

            return url


        if "remotive.com" in url:

            return url



    return "Not Found"