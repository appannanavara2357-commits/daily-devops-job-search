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
# Remove HTML
# ==========================

def remove_html(text):

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
# Extract Job Details
# ==========================

def extract_job_details(subject, body, sender=""):


    subject = clean_subject(subject)

    clean_body = remove_html(body)

    text = subject + " " + clean_body

    lower = text.lower()



    # ==========================
    # LinkedIn Filter
    # ==========================

    if "linkedin" in sender.lower():

        if "linkedin.com/comm/jobs/view" not in body.lower():

            print("Skipped LinkedIn alert")

            return None



    # ==========================
    # Ignore Non Job Emails
    # ==========================

    ignore_words = [

        # Delivery

        "delivery status notification",
        "delivery incomplete",
        "mail delivery subsystem",
        "temporary problem while delivering",
        "recipient server did not accept",
        "timed out",


        # Security

        "security alert",
        "new sign-in",
        "verify your",


        # Survey

        "survey",
        "recruiting experience",


        # Application status

        "resume has been viewed",
        "contact viewed",
        "application status",
        "status has been changed",
        "applied-jobs",


        # LinkedIn confirmation

        "job alert has been created",
        "get job alerts for this search",


        # Hirist recommendation

        "10+ jobs matching your profile",
        "jobs recommended for you",
        "matching jobs based on your preferences"

    ]


    for word in ignore_words:

        if word in lower:

            print("Skipped non-job email")

            return None



    # Ignore replies

    if subject.lower().startswith("re:"):

        print("Skipped reply")

        return None



    job = {}



    # ==========================
    # Role
    # ==========================

    role = subject


    if "your job alert for" in role.lower():

        lines = clean_body.split("\n")

        for line in lines:

            line = line.strip()

            if (
                len(line) > 5
                and
                "view job" not in line.lower()
            ):

                role = line

                break



    role = role.replace(
        "âœ‰ï¸ Job |",
        ""
    )


    job["role"] = role.strip()



    # ==========================
    # Company Detection
    # ==========================

    companies = [

        "Amazon",
        "Microsoft",
        "Google",
        "Quantiphi",
        "SysMind",
        "PwC",
        "Deloitte",
        "Infosys",
        "Wipro",
        "Accenture",
        "Philips",
        "Saviynt"

    ]


    company = "Unknown"



    # FIXED COMPANY SEARCH

    for c in companies:

        if c.lower() in clean_body.lower():

            company = c

            break



    job["company"] = company



    # ==========================
    # Location
    # ==========================

    locations = [

        "Bengaluru",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Mumbai",
        "Pune",
        "Noida",
        "Gurgaon"

    ]


    found = []


    for loc in locations:

        if loc.lower() in lower:

            found.append(loc)



    job["location"] = (

        ", ".join(dict.fromkeys(found))

        if found

        else

        "Not Found"

    )



    # ==========================
    # Skills
    # ==========================

    skill_words = [

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


    skills=[]


    for skill in skill_words:

        if skill.lower() in lower:

            skills.append(skill)



    job["skills"] = skills



    # ==========================
    # Extract Apply Link
    # ==========================

    urls = re.findall(
        r'https?://[^\s"<>]+',
        body
    )


    job_link = "Not Found"



    bad_links = [

        "w3.org",
        "xhtml",
        "xmlns",
        "googleapis",
        "fonts.googleapis",
        "unsubscribe",
        "tracking",
        "logs.",
        "survey",
        "accounts.google"

    ]



    for url in urls:


        url = url.replace(
            "&amp;",
            "&"
        )


        url = url.strip(")>,\"'")



        if any(
            bad in url.lower()
            for bad in bad_links
        ):

            continue



        # LinkedIn

        if "linkedin.com/comm/jobs/view" in url.lower():

            job_link = url.split("&")[0]

            break



        # Hirist

        if "hirist.tech%2f" in url.lower():

            decoded = url.split("CL0/")[-1]


            decoded = (

                decoded
                .replace("%2F","/")
                .replace("%3F","?")
                .replace("%3D","=")
                .replace("%26","&")

            )


            if decoded.startswith("https:"):

                job_link = decoded.split("/1/")[0]

                break



        # Normal jobs

        if (
            "/jobs/" in url.lower()
            or
            "/j/" in url.lower()
            or
            "jobid=" in url.lower()
        ):

            job_link=url

            break



    job["apply_link"] = job_link


    return job