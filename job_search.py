import requests


def search_jobs():
    jobs = []

    url = "https://remotive.com/api/remote-jobs"

    response = requests.get(url)
    data = response.json()

    keywords = [
        "devops",
        "cloud engineer",
        "kubernetes",
        "sre",
        "platform engineer",
        "aws",
        "azure",
        "terraform"
    ]

    remote_keywords = [
        "worldwide",
        "anywhere",
        "remote",
        "asia",
        "india"
    ]

    us_keywords = [
        "usa",
        "us",
        "united states",
        "america"
    ]

    for job in data["jobs"]:

        title = job["title"].lower()
        location = job["candidate_required_location"].lower()

        company = job["company_name"].lower()

        role_match = any(
            keyword in title
            for keyword in keywords
        )

        remote_match = any(
            keyword in location
            for keyword in remote_keywords
        )

        # US company check (basic filter)
        us_company_match = any(
            keyword in company
            for keyword in us_keywords
        )

        if role_match and remote_match:

            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "location": job["candidate_required_location"],
                "url": job["url"]
            })

    return jobs


if __name__ == "__main__":

    results = search_jobs()

    print(f"Found {len(results)} US company remote jobs\n")

    for job in results[:10]:
        print("------------------------")
        print("Title:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("URL:", job["url"])