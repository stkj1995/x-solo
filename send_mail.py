from flask import render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import secrets

def generate_verification_key():
    """Generate a 32-character hex verification key"""
    return secrets.token_hex(16)

def send_verify_email(to_email, user_verification_key):
    try:
        sender_email = "sophieteinvigkjer@gmail.com"
        password = "tsmmiisuacbvzppl"  # App Password

        message = MIMEMultipart()
        message["From"] = f"My Company <{sender_email}>"
        message["To"] = to_email
        message["Subject"] = "Please verify your account"

        # Make sure the URL matches your Flask route
        verification_link = f"http://127.0.0.1:5000/verify-account?key={user_verification_key}"
        body = f"""<p>To verify your account, please <a href="{verification_link}">click here</a>.</p>"""
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, message.as_string())

        print("Email sent successfully!")
        return "email sent"

    except Exception as ex:
        print("Error sending email:", ex)
        raise Exception("Cannot send email") from ex
    
####################################
def send_reset_password_email(to_email, reset_token, user_first_name):
    reset_link = f"http://127.0.0.1:5000/reset-password?token={reset_token}"
    body = render_template("_email_forgot_password.html", reset_link=reset_link, user_first_name=user_first_name, user_email=to_email)

    sender_email = "sophieteinvigkjer@gmail.com"
    password = "tsmmiisuacbvzppl"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "Password Reset Request"
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())

####################################
def send_reset_password_email(to_email, reset_token, user_first_name="User"):
    """
    Send a password reset email with a one-time link.
    """
    try:
        sender_email = "sophieteinvigkjer@gmail.com"
        password = "tsmmiisuacbvzppl"  # App Password

        message = MIMEMultipart()
        message["From"] = f"My Company <{sender_email}>"
        message["To"] = to_email
        message["Subject"] = "Reset your password"

        # Make sure the URL matches your Flask reset-password route
        reset_link = f"http://127.0.0.1:5000/reset-password?token={reset_token}"

        # HTML body of the email
        body = f"""
        <p>Hello {user_first_name},</p>
        <p>We received a request to reset your password.</p>
        <p>Click <a href="{reset_link}">here</a> to reset your password. This link will expire in 1 hour.</p>
        <p>If you did not request a password reset, you can ignore this email.</p>
        <p>Thanks,<br>Your Company Team</p>
        """
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, message.as_string())

        print("Reset password email sent successfully!")
        return "email sent"

    except Exception as ex:
        print("Error sending reset email:", ex)
        raise Exception("Cannot send reset email") from ex

