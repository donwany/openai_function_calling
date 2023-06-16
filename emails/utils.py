import json
import os
import smtplib
from email.message import EmailMessage

import openai
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
PORT = int(os.getenv("PORT"))
SMTP = os.getenv("SMTP")

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_email(to: str, subject: str, body: str):
    message = {
        "from": "theodondre@gmail.com",
        "to": to,
        "body": body,
        "subject": subject
    }
    return json.dumps(message)


def email_sender(subject, body):
    """send email"""
    try:
        sender_email = GMAIL_ADDRESS
        sender_password = GMAIL_PASSWORD
        receiver_email = RECEIVER_EMAIL

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        session = smtplib.SMTP(SMTP, PORT)
        session.starttls()
        session.login(sender_email, sender_password)
        session.send_message(msg, sender_email, receiver_email)
        session.quit()
        print("Mail Sent!")
    except Exception as e:
        print(f'Error sending email: {e}')


def draft_email(content: str):
    completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user",
                   "content": content}],
        functions=[
            {
                "name": "send_email",
                "description": "send email to a youtuber",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "email address of receiver, e.g. godataprof@gmail.com",
                        },
                        "subject": {
                            "type": "string",
                            "description": "subject of the email, e.g. Hello! GodataProf"
                        },
                        "body": {
                            "type": "string",
                            "description": "content of the email, e.g. Checking to see what times you upload new youtube videos"
                        },
                    },
                    "required": ["to", "subject", "body"],
                },
            }
        ],
        function_call="auto",
    )

    reply_content = completion.choices[0].message
    funcs = reply_content['function_call']['arguments']
    funcs = json.loads(funcs.replace("\n", ""))

    return funcs

    # {
    # 'to': 'godataprof@gmail.com',
    #  'subject': 'Upload Schedule Inquiry',
    #  'body': "Hello godataprof,  "
    #          "I hope you're doing well."
    #          "I'm a big fan of your content on YouTube, "
    #          "particularly your work with Data Science. "
    #          "If possible, could you kindly let me know when you're planning to upload a new video again?"
    #          "Looking forward to your upcoming content!  Best regards"
    #  }
