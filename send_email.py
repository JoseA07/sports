import smtplib
import pandas as pd
from io import BytesIO
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def send_email(config: dict, password: str, df: pd.DataFrame = None):
    try:
        date_str = datetime.now().strftime("%Y_%m_%d")
        today = datetime.now().strftime("%Y-%m-%d")

        msg = MIMEMultipart()
        msg["From"] = config["EMAIL"]
        msg["To"] = config["TO_EMAIL"]
        msg["Subject"] = f"{config['SUBJECT']} - {today}"
        msg.attach(MIMEText(config["MESSAGE"], "plain"))

        if df is not None:
            excel_buffer = BytesIO()  # Create an in-memory buffer
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="matches", index=False)

            excel_buffer.seek(0)  # Reset buffer position

            # Attach Excel file
            filename = f"today_matches_{date_str}.xlsx"
            part = MIMEApplication(excel_buffer.read(), Name=filename)
            part["Content-Disposition"] = f'attachment; filename={filename}'
            msg.attach(part)

        # Connect to Gmail SMTP server
        server = smtplib.SMTP(config["SMTP_SERVER"], config["SMTP_PORT"])
        server.starttls()  # Secure connection
        server.login(config["EMAIL"], password)
        server.sendmail(config["EMAIL"], config["TO_EMAIL"], msg.as_string())
        server.quit()

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
