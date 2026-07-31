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


            title = job.get(
                "role",
                ""
            )


            company = job.get(
                "company",
                "Unknown"
            )


            location = job.get(
                "location",
                "Unknown"
            )


            skills = job.get(
                "skills",
                []
            )


            apply_link = job.get(
                "apply_link",
                ""
            )



            formatted_jobs.append(

                {

                    "title": title,

                    "company": company,

                    "location": location,

                    "url": apply_link,

                    "description":
                        " ".join(skills),

                    "matched_skills":
                        skills

                }

            )


        return formatted_jobs



    except Exception as e:

        print(
            "Error reading Gmail jobs:",
            e
        )

        return []