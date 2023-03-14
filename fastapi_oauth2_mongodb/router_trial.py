import argparse
import asyncio
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

from fastapi_oauth2_mongodb.api_keys import create_api_key
from fastapi_oauth2_mongodb.models import User
from fastapi_oauth2_mongodb.users import create_trial_user

app = FastAPI()
router = APIRouter()

load_dotenv()  # 載入 .env 檔案的環境變數

# read SMTP server and port from environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER')  # replace with your SMTP server
SMTP_PORT = int(os.environ.get('SMTP_PORT', '0'))  # replace with your SMTP port

# read email address and password from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # replace with your email address
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # replace with your email password


class Email(BaseModel):
    email: str


@router.post("/api/trial/v1/trial_email")
async def trial_email(e: Email):
    await create_trial_user(User(email=e.email))
    create_api_key_result = await create_api_key(e.email)
    if SMTP_SERVER is None or SMTP_PORT == 0 or EMAIL_ADDRESS is None or EMAIL_PASSWORD is None:
        raise HTTPException(status_code=500, detail="SMTP server, port, email address, or password is not set.")
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = e.email
        msg['Subject'] = "Welcome to our website!"

        # add your email content here
        html = f'''<html><body><h1>Welcome to our website!</h1><br/>
        Your email account:{create_api_key_result.email}<br/>
        API key:{create_api_key_result.api_key}<br/>
        <p>Thank you for joining us.</p></body></html>'''
        body = MIMEText(html, 'html')
        msg.attach(body)

        # replace the following with your email provider's SMTP settings
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()

        return {"message": "Email sent successfully!"}
    except:
        raise HTTPException(status_code=500, detail="Failed to send email.")


async def send_email(email_address: str):
    """
    Send a welcome email to the specified email address.
    """
    email = Email(email=email_address)
    result = await trial_email(email)
    print(result["message"])


def main():
    parser = argparse.ArgumentParser(description="Send a welcome email to the specified email address.")
    parser.add_argument("email_address", type=str, help="The email address to send the welcome email to.")
    args = parser.parse_args()

    if SMTP_SERVER is None or SMTP_PORT == 0 or EMAIL_ADDRESS is None or EMAIL_PASSWORD is None:
        print("Please set the following environment variables:")
        print("SMTP_SERVER='your_smtp_server'")
        print("SMTP_PORT='587'")
        print("EMAIL_ADDRESS='your_email_address'")
        print("EMAIL_PASSWORD='your_email_password'")
        return

    asyncio.run(send_email(args.email_address))


if __name__ == "__main__":
    main()
