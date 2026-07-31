import json
import os
from datetime import datetime

from job_sources.remotive_source import search_jobs
from email_sender import send_email
from filters import filter_jobs


FILE_NAME = "previous_jobs.json"


def load_previous_jobs():
    """
    Load already sent job URLs
    """

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(
            FILE_NAME,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []



def save_jobs(jobs):
    """
    Save job URLs with UTF-8 support
    """

    with open(
        FILE_NAME,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            jobs,
            file,
            indent=4,
            ensure_ascii=False
        )



def create_email_body(jobs):

    today = datetime.now().strftime("%d-%m-%Y")

    email_body = f"""
    <html>
    <body>

    <h2>
    🚀 Daily DevOps Job Alert - {today}
    </h2>

    """

    for job in jobs:

        skills = ", ".join(
            job.get(
                "matched_skills",
                []
            )
        )

        email_body += f"""

        <hr>

        <h3>
        {job.get('title','N/A')}
        </h3>


        <p>

        <b>Company:</b>
        {job.get('company','N/A')}
        <br>


        <b>Location:</b>
        {job.get('location','N/A')}
        <br>


        <b>Skills:</b>
        {skills}
        <br>


        <b>Apply:</b>
        <a href="{job.get('url')}">
        Click Here
        </a>

        </p>

        """

    email_body += """

    </body>
    </html>

    """

    return email_body



def main():

    print("Searching jobs...")

    previous_jobs = load_previous_jobs()


    print(
        f"Previously sent jobs: {len(previous_jobs)}"
    )


    jobs = search_jobs()


    print(
        f"Jobs found: {len(jobs)}"
    )


    jobs = filter_jobs(jobs)


    print(
        f"Jobs after filtering: {len(jobs)}"
    )


    new_jobs = []


    sent_urls = set(previous_jobs)


    for job in jobs:

        url = job.get("url")


        if url and url not in sent_urls:

            new_jobs.append(job)

            sent_urls.add(url)



    if new_jobs:


        print(
            f"New jobs found: {len(new_jobs)}"
        )


        email_body = create_email_body(
            new_jobs
        )


        send_email(
            "Daily DevOps Job Alert",
            email_body
        )


        save_jobs(
            list(sent_urls)
        )


        print(
            "Email sent successfully"
        )


    else:

        print(
            "No new jobs found today."
        )



if __name__ == "__main__":

    main()