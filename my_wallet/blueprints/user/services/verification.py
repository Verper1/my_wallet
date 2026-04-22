import random

from flask import current_app


def generate_email_code() -> str:
    """Generate a 4-digit email verification code."""
    number = random.randint(1, 9999)
    return f"{number:04d}"


def generate_sms_code() -> str:
    """Generate a 4-digit sms verification code."""
    number = random.randint(1, 9999)
    return f"{number:04d}"


def send_verification_email(email: str, code: str) -> None:
    """Send a verification code to the given email."""
    current_app.mailgun.send_email(  # type: ignore[attr-defined]
        **{  # type: ignore[attr-defined]
            "from": current_app.config["FROM_EMAIL"],
            "to": email,
            "subject": "My wallet verification code",
            "html": f"Your email verification code is {code}",
        }
    )


def send_verification_sms(mobile: str, code: str) -> None:
    """Send a verification code to the given mobile number."""
    current_app.twillio_client.messages.create(  # type: ignore[attr-defined]
        body=f"My wallet verification code is {code}",
        from_=current_app.config["TWILLIO_FROM_NUMBER"],
        to=mobile,
    )
