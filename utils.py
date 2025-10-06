import os
from mailersend import emails
import bcrypt

def hash_plain_text(plain_text):
    return bcrypt.hashpw(plain_text.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_plain_text(plain_text, hashed_plain_text):
    return bcrypt.checkpw(plain_text.encode("utf-8"), hashed_plain_text.encode("utf-8"))

def send_email(email, title, content):
    MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')
    MAILERSEND_TEMPLATE_ID = os.getenv('MAILERSEND_TEMPLATE_ID')

    if not all([MAILERSEND_API_KEY, MAILERSEND_TEMPLATE_ID]):
        return False

    mailer = emails.NewEmail(MAILERSEND_API_KEY)
    mail_data ={
        "to": [{"email": email}],
        "subject": title,
        "template_id": MAILERSEND_TEMPLATE_ID,
        "personalization": [
            {
                "email": email,
                "data": {
                    "title": str(title),
                    "content": str(content),
                },
            }
        ]
    }

    return mailer.send(mail_data)