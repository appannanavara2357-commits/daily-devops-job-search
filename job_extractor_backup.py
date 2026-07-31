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

        linkedin_job = False


        if "linkedin.com/comm/jobs/view" in body.lower():

            linkedin_job = True



        if not linkedin_job:

            print("Skipped LinkedIn alert")

            return None



    # ==========================
    # Ignore Non Job Emails
    # ==========================


    ignore_words = [


        # Gmail

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


        # Surveys

        "survey",
        "recruiting experience",


        # Application updates

        "resume has been viewed",
        "contact viewed",
        "applied-jobs",
        "application status",
        "status has been changed"


    ]



    for word in ignore_words:


        if word in lower:

            print("Skipped non-job email")

            return None




    # ==========================
    # Ignore Replies
    # ==========================


    if subject.lower().startswith("re:"):

        print("Skipped reply")

        return None




    job={}



    # ==========================
    # Role
    # ==========================


    role = subject


    role = role.replace(
        "✉️ Job |",
        ""
    )


    role = role.replace(
        "=?UTF-8?Q?",
        ""
    )


    job["role"] = role.strip()




    # ==========================
    # Company Detection
    # ==========================


    companies=[


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



    company="Unknown"



    for c in companies:


        if c.lower() in lower:

            company=c

            break




    # Naukri sender company

    if company=="Unknown":


        sender_match=re.search(

            r"<(.+?)>",

            sender

        )


        if sender_match:


            company_name=sender_match.group(1)


            company_name=company_name.split("@")[0]


            if "naukri" not in company_name.lower():

                company=company_name




    job["company"]=company




    # ==========================
    # Location
    # ==========================


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



    job["location"] = (

        ", ".join(dict.fromkeys(found))

        if found

        else

        "Not Found"

    )




    # ==========================
    # Skills
    # ==========================


    skill_words=[


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



    job["skills"]=skills




    # ==========================
    # Extract URLs
    # ==========================


    urls=re.findall(

        r'https?://[^\s"<>]+',

        body

    )



    job_link="Not Found"



    for url in urls:



        url=url.replace(

            "&amp;",

            "&"

        )



        url=url.strip(")>,\"'")



        # Ignore unwanted links

        bad_links=[


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



        if any(

            bad in url.lower()

            for bad in bad_links

        ):

            continue




        # ==========================
        # LinkedIn
        # ==========================


        if "linkedin.com/comm/jobs/view" in url.lower():


            job_link=url.split("&")[0]

            break




        # ==========================
        # Hirist
        # ==========================


        if "hirist.tech%2f" in url.lower():


            decoded=url.split("CL0/")[-1]


            decoded=(

                decoded

                .replace("%2F","/")

                .replace("%3F","?")

                .replace("%3D","=")

                .replace("%26","&")

            )



            if decoded.startswith("https:"):


                job_link=decoded.split("/1/")[0]

                break





        # ==========================
        # Normal Job URL
        # ==========================


        if (

            "/jobs/" in url.lower()

            or

            "/j/" in url.lower()

            or

            "jobid=" in url.lower()

        ):


            job_link=url

            break





    job["apply_link"]=job_link



    return job