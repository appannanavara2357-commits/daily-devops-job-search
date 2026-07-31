import json


def generate_report():


    with open(
        "jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        jobs=json.load(file)



    with open(
        "jobs_report.txt",
        "w",
        encoding="utf-8"
    ) as report:


        for job in jobs:


            report.write(
                "\n====================\n"
            )

            report.write(
                "Role: "
                + job["role"]
                + "\n"
            )


            report.write(
                "Company: "
                + job["company"]
                + "\n"
            )


            report.write(
                "Location: "
                + job["location"]
                + "\n"
            )


            report.write(
                "Skills: "
                + str(job["skills"])
                + "\n"
            )


            report.write(
                "Apply Link: "
                + job["apply_link"]
                + "\n"
            )



    print(
        "Report generated successfully"
    )



if __name__=="__main__":

    generate_report()