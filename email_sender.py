import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")


def send_otp(receiver_email, otp):

    data = {
        "sender": {
            "name": "Smart Feedback Portal",
            "email": EMAIL_ADDRESS
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "bcc": [
            {
                "email": EMAIL_ADDRESS
            }
        ],
        "subject": f"Smart Feedback Portal - OTP sent to {receiver_email}",
        "htmlContent": f"""
        <html>
        <body>
            <h2>Smart Feedback Portal</h2>

            <p>Hello,</p>

            <p>This OTP was sent to:</p>

            <p><b>{receiver_email}</b></p>

            <p>Your OTP for Smart Feedback Portal is:</p>

            <h1>{otp}</h1>

            <p>This OTP is valid for 5 minutes.</p>

            <p>If you did not request this OTP, please ignore this email.</p>

            <p>Thank you,<br>
            Smart Feedback Portal</p>
        </body>
        </html>
        """
    }

    req = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(data).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status == 201

    except urllib.error.HTTPError as e:
        print("Brevo HTTP Error:", e.code)
        print(e.read().decode())
        return False

    except Exception as e:
        print("Brevo Email Error:", e)
        return False