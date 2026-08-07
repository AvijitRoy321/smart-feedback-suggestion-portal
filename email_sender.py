import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_otp(receiver_email, otp):

    msg = EmailMessage()

    msg["Subject"] = "Smart Feedback Portal - Email Verification OTP"

    msg["From"] = EMAIL_ADDRESS

    msg["To"] = receiver_email

    msg.set_content(f"""
Hello,

Your OTP for Smart Feedback Portal is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this OTP, please ignore this email.

Thank you,
Smart Feedback Portal
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)