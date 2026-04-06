import csv
from mailer import send_email
from logger_config import setup_logger

# -------- CONFIG --------
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
ATTACHMENT_PATH = "report.pdf"
CSV_FILE = "recipients.csv"

def main():
    setup_logger()

    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                send_email(
                    SENDER_EMAIL,
                    APP_PASSWORD,
                    row["email"],
                    row["name"],
                    ATTACHMENT_PATH
                )

    except FileNotFoundError:
        print(" recipients.csv file not found")

    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()
