import json
import os


JOB_FILE = "jobs.json"


def search_gmail_jobs():

    if not os.path.exists(JOB_FILE):
        return []

    try:

        with open(
            JOB_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            jobs = json.load(file)


        formatted_jobs = []


        for job in jobs:

            formatted_jobs.append({

                "title": job.get(
                    "title",
                    ""
                ),

                "company": job.get(
                    "company",
                    "Unknown"
                ),

                "location": job.get(
                    "location",
                    "Bengaluru"
                ),

                "url": job.get(
                    "url",
                    ""
                ),

                "description": job.get(
                    "description",
                    ""
                )

            })


        return formatted_jobs


    except Exception as e:

        print(
            "Gmail job loading error:",
            e
        )

        return []