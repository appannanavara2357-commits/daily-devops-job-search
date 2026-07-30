import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECEIVER_EMAIL


def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print("✅ Email sent successfully!")

if __name__ == "__main__":
    send_email(
        "Test Job Alert",
        "<h2>Daily DevOps Job Alert Test</h2><p>Email setup is working.</p>"
    )