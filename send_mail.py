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
