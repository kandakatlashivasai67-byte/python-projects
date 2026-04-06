import smtplib
import time
import logging
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MAX_RETRIES = 3

def send_email(sender_email, app_password, receiver_email, name, attachment_path):
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Automated Report Delivery"

    msg.set_content(f"""
Hi {name},

Please find the attached report.

Regards,
Automation Bot
""")

    # Attach file
    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=file_name
    )

    retries = 0
    while retries < MAX_RETRIES:
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)

            logging.info(f"Email sent to {receiver_email}")
            print(f"Email sent to {receiver_email}")
            return

        except Exception as e:
            retries += 1
            logging.error(f"Retry {retries} failed for {receiver_email}: {e}")
            print(f"Retry {retries} for {receiver_email}")
            time.sleep(2)

    logging.error(f"Giving up on {receiver_email}")
