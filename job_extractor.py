import re
from email.header import decode_header
from html import unescape


# ==========================
# Clean Subject
# ==========================

def clean_subject(subject):

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
# Clean HTML
# ==========================

def remove_html(text):

    text = unescape(text)

    text = re.sub(
        r"<script.*?</script>",
        " ",
        text,
        flags=re.S
    )

    text = re.sub(
        r"<style.*?</style>",
        " ",
        text,
        flags=re.S
    )

    text = re.sub(
        r"<[^>]+>",
        "\n",
        text
    )

    text = re.sub(
        r"\n+",
        "\n",
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
        "Infosys",
        "Wipro",
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


    # LinkedIn format:
    # Role
    # Company

    lines = [
        x.strip()
        for x in text.split("\n")
        if x.strip()
    ]


    for i,line in enumerate(lines):

        if "India" in line:

            if i > 0:

                return lines[i-1]


    return "Unknown"




# ==========================
# Extract Job Details
# ==========================

def extract_job_details(subject, body, sender=""):


    subject = clean_subject(subject)

    clean_body = remove_html(body)


    text = subject + "\n" + clean_body


    lower=text.lower()



    # Ignore unwanted mails

    ignore=[

        "security alert",
        "delivery status",
        "delivery incomplete",
        "resume has been viewed",
        "application successful",
        "application status",
        "verify your",
        "survey"

    ]


    for word in ignore:

        if word in lower:

            print("Skipped:",word)

            return None



    # ==========================
    # Role
    # ==========================


    role=subject


    # LinkedIn

    if "linkedin" in sender.lower():

        lines=[

            x.strip()
            for x in clean_body.split("\n")
            if x.strip()

        ]


        for line in lines:

            if (
                "view job" not in line.lower()
                and
                "linkedin" not in line.lower()
                and
                len(line)>5
            ):

                role=line

                break



    role=role.replace(
        "✉️ Job |",
        ""
    )


    role=role.replace(
        "âœ‰ï¸ Job |",
        ""
    )


    job={}


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
        ", ".join(dict.fromkeys(found))
        if found
        else
        "Not Found"
    )



    # Skills


    skills=[]


    skill_list=[

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


    for skill in skill_list:

        if skill.lower() in lower:

            skills.append(skill)



    job["skills"]=skills




    # Apply Link


    urls=re.findall(
        r"https?://[^\s\"<>]+",
        body
    )


    link="Not Found"


    for url in urls:


        url=url.replace(
            "&amp;",
            "&"
        )


        if (
            "linkedin.com/comm/jobs/view"
            in url.lower()
        ):

            link=url.split("&")[0]

            break



        if (
            "remotive.com"
            in url.lower()
            or
            "hirist.tech/j/"
            in url.lower()
        ):

            link=url

            break



    job["apply_link"]=link


    return job