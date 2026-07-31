import os
import base64
import json
from datetime import datetime

from email import message_from_bytes

from job_extractor import extract_job_details

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# -----------------------------
# Gmail Authentication
# -----------------------------

def gmail_service():

    creds = None

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )


    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )


        with open(
            "token.json",
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )


    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service



# -----------------------------
# Remove unwanted emails
# -----------------------------

def is_job_email(subject, sender):

    subject_lower = subject.lower()
    sender_lower = sender.lower()


    ignore_words = [

        "security alert",
        "application successful",
        "follow up application",
        "account notification",
        "google",
        "password",
        "verification"

    ]


    for word in ignore_words:

        if word in subject_lower:

            return False



    allowed_sources = [

        "linkedin",
        "naukri",
        "hirist"

    ]


    for source in allowed_sources:

        if source in sender_lower:

            return True


    return False




# -----------------------------
# Read Gmail
# -----------------------------

def read_emails():


    service = gmail_service()



    results = service.users().messages().list(

        userId="me",
        maxResults=20

    ).execute()



    messages = results.get(
        "messages",
        []
    )



    print(
        "Total emails found:",
        len(messages)
    )



    job_results = []



    for msg in messages:



        email_data = service.users().messages().get(

            userId="me",
            id=msg["id"],
            format="raw"

        ).execute()



        raw_email = base64.urlsafe_b64decode(

            email_data["raw"]

        )



        message = message_from_bytes(
            raw_email
        )



        subject = message["subject"] or ""

        sender = message["from"] or ""



        # Ignore unwanted mails

        if not is_job_email(subject, sender):

            print(
                "Skipped:",
                subject
            )

            continue




        body = ""



        # Extract body

        if message.is_multipart():


            for part in message.walk():


                content_type = part.get_content_type()


                if content_type in [

                    "text/plain",
                    "text/html"

                ]:


                    payload = part.get_payload(
                        decode=True
                    )


                    if payload:


                        body += payload.decode(
                            "utf-8",
                            errors="ignore"
                        )



        else:


            payload = message.get_payload(
                decode=True
            )


            if payload:

                body = payload.decode(
                    "utf-8",
                    errors="ignore"
                )




        print("\n================ JOB EMAIL ================")

        print("SUBJECT:")
        print(subject)


        print("\nFROM:")
        print(sender)


        print("\nBODY SAMPLE:")

        print(
            body[:1000]
        )


        print(
            "============================================"
        )




        job = extract_job_details(

            subject,

            body,

            sender

        )



        if job is None:

            print(
                "No job details extracted"
            )

            continue




        job["date"] = datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )



        job_results.append(
            job
        )





    # Save jobs.json


    with open(

        "jobs.json",

        "w",

        encoding="utf-8"

    ) as file:


        json.dump(

            job_results,

            file,

            indent=4,

            ensure_ascii=False

        )



    print(
        f"Saved {len(job_results)} jobs to jobs.json"
    )





if __name__ == "__main__":

    read_emails()