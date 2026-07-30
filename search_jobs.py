import json
from job_search import search_jobs
from email_sender import send_email


FILE_NAME = "previous_jobs.json"


def load_previous_jobs():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


def save_jobs(jobs):
    with open(FILE_NAME, "w") as file:
        json.dump(jobs, file, indent=4)


previous_jobs = load_previous_jobs()

jobs = search_jobs()

new_jobs = []

for job in jobs:
    if job["url"] not in previous_jobs:
        new_jobs.append(job)
        previous_jobs.append(job["url"])


if new_jobs:

    email_body = """
    <h2>Daily DevOps Job Alert 🚀</h2>
    """

    for job in new_jobs:
        email_body += f"""
        <hr>
        <h3>{job['title']}</h3>
        <p>
        <b>Company:</b> {job['company']}<br>
        <b>Location:</b> {job['location']}<br>
        <b>Apply:</b>
        <a href="{job['url']}">{job['url']}</a>
        </p>
        """

    send_email(
        "Daily DevOps Job Alert",
        email_body
    )

    save_jobs(previous_jobs)

else:
    print("No new jobs found today.")