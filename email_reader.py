import os
import base64
import json
from datetime import datetime

from email import message_from_bytes
from email.header import decode_header

from job_extractor import extract_job_details

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


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
            "w",
            encoding="utf-8"
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



def decode_subject(raw_subject):

    """
    Fix Gmail encoded subjects like:
    =?UTF-8?Q?=E2=9C=89=EF=B8=8F_Job?=
    
    Output:
    ✉️ Job
    """

    subject = ""

    decoded_parts = decode_header(
        raw_subject
    )

    for part, encoding in decoded_parts:

        if isinstance(part, bytes):

            subject += part.decode(
                encoding or "utf-8",
                errors="ignore"
            )

        else:

            subject += part

    return subject



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



        # FIXED UTF-8 SUBJECT

        raw_subject = message["subject"] or ""

        subject = decode_subject(
            raw_subject
        )


        sender = message["from"] or ""


        body = ""


        # Read email body

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



        # Remove unwanted emails

        skip_keywords = [

            "security alert",
            "application successful",
            "follow up application",
            "delivery status notification",
            "account notification",
            "recruiting experience"

        ]


        if any(

            word in subject.lower()

            for word in skip_keywords

        ):

            print(
                "Skipped:",
                subject
            )

            continue



        print(
            "\n================ JOB EMAIL ================"
        )


        print(
            "SUBJECT:"
        )

        print(
            subject
        )


        print(
            "\nFROM:"
        )

        print(
            sender
        )


        print(
            "\nBODY SAMPLE:"
        )

        print(
            body[:1500]
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