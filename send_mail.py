from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

##############################
def send_verify_email(to_email, user_verification_key):
    try:
        sender_email = "sophieteinvigkjer@gmail.com"
        password = "wrdlqtdinbyuyeue"
        receiver_email = to_email

        message = MIMEMultipart()
        message["From"] = "My company name <YOUR GMAIL HERE>"
        message["To"] = receiver_email
        message["Subject"] = "Please verify your account"

        body = f"""To verify your account, please <a href="http://127.0.0.1/verify/{user_verification_key}">click here</a>"""
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")
        return "email sent"

    except Exception as ex:
        raise Exception("Cannot send email") from ex
